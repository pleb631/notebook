# const

constexpr 可以在编译期间定义常量

```c++
constexpr int age{20};
constexpr int age1{age+10};
//此时可以使用static_assert在编译期间做检查
static_assert(age==20)
```

constexpr只能使用字面量或者constexpr的变量进行赋值

如果是常规的变量，则会报错



```c++
// 此时函数可以在编译时使用，也可以在运行时使用
constexpr int add(int a,int b){
    return a+b;
}

 int main()
{
constexpr int value1{22};
    constexpr int value2{33};
    auto result{add(value1,value2)};    // Compile time

    int factor{2}; // Run time variable
    auto result2{add(value1, factor)}; // Run time
	return 0;

  }
```

**consteval**是严格版本的constexpr，如果相关计算不能在编译期间完成，会直接报错，而不是移动到runtime执行

**constinit**的作用在于显式地指定变量的初始化方式为静态初始化,在编译时初始化，但可以修改值

```c++
constinit int  a{8};
a=12;

const constinit int a1{8}; //可以额外指定变量const
```

# for

有两种方法

```c++
//常规
for(i ; i < 10 ; ++i){
		fmt::println( " {}: I love C++", i );
	}
```

```c++
// 迭代器模式
std::vector<int> values{ 1, 2, 3, 4, 5 };
for (auto value : values) {
	fmt::println(" value : {}", value);
}
```

# 随机

依靠标准库直接随机

```c++
std::srand(std::time(nullptr)); // use current time as seed for random generator
int random_value = std::rand();
std::cout << "Random value on [0, " << RAND_MAX << "]: " << random_value << '\n';
```

c++17以上提供一种更好的

```c++
 std::random_device rd;  // Provides seeds with less predictability
 std::mt19937 marsenne{ rd() };  // Initialize our mersenne twister with a random seed
 std::uniform_int_distribution die{ 1, 6 };  // uniform distribution.
auto rando_num {die(marsenne)};
fmt::println("Value: {}", rando_num);
```

# 指针（补充）

**打印指针存储的地址的方法**

对于数组的指针来说，直接打印就可以，但是对于char* 或者char[]，则必须用static_cast做转换，更safe的做法是统一使用fmt::ptr

```c++
const char *a = "hello";
std::cout<<&a<<std::endl; //打印是a的地址而不是a存储的地址 const char**
std::cout << static_cast<const void*>(a) << std::endl;


char c[]{"hello"};
std::cout << static_cast<const void*>(c) << std::endl;

int b[]{1,2,3};
std::cout<<b<<std::endl;

std::cout<<fmt::ptr(a)<<std::endl;
```



**各种指针的用法和含义**



指向常量的指针，不能修改值，

```c++
int a{1};
const int* b{&a} ;
```



不能用变量指针指向常量

```c++
const int a{1};
int* b{&a};  //报错

const int* b1{&a} ;
```



指针本身是常量

```c++
int a{1};
int* const b{&a} ;
```



指针是常量，指向的也是常量

```c++
const int a{1};
const int* const b{&a} ;
```



**指针运算**

如果需要计算两个指针的差值，最好使用`std::ptrdiff_t`类型来存储，如果需要知道array有多大，可以使用`std::size()`

# 动态内存

```c++
int *p(nullptr);
p = new int; //在堆上开辟了一个4字节内存，并用p指向它
*p=22; //解引用
delete p; //释放内存回os
p = nullptr; //重置指针指向
  
```

注意有几种会使程序崩溃的情况

1. 未初始化

```c++
int * p_number;
fmt::println( "p_number: {}", fmt::ptr(p_number));
fmt::println( "*p_number: {}" , *p_number); //CRASH!
```

2. 访问被释放的指针

```c++
int * p_number1 {new int{67}};
fmt::println( "*p_number1(after delete): {}", *p_number1 );
delete p_number1;
fmt::println( "*p_number1(after delete): {}", *p_number1 );//CRASH!
```

3. 多个指针指向同个地址

```c++
 int *p_number3 {new int{83}};
        int *p_number4 {p_number3};
delete p_number3;
fmt::println( "p_number4(after deleting p_number3) -{} :  {}", fmt::ptr(p_number4) , *p_number4 );//CRASH!
```



4. new失败

```c++
int* data = new int[10000000] //crash,内存不够
```





解决方案如下

1.声明时就进行初始化

```c++
int *p_number5{nullptr};
int *p_number6{new int(87)};

//在使用时进行检查
if(p_number6!= nullptr){
     fmt::println( "p_number6 - {} - {}",                     fmt::ptr(p_number6), *p_number6 );
}else{
      fmt::println( "Invalid address" );
}

```



2. 在释放内存后重置指针

```c++
int *p_number7{ new int{ 82 } };
delete p_number7;
p_number7 = nullptr;// Reset the pointer
```



3. 应该规定一个主指针来管理内存，其他指针必须在主指针可用时才能使用

```c++
int *p_number8{ new int{ 382 } };// Let's say p_number8 is the master pointer
int *p_number9{ p_number8 };
delete p_number8;// Master releases the memory
p_number8 = nullptr;

if (!(p_number8 == nullptr)) {// Only use slave pointers when master pointer is valid
     fmt::println("p_number9 - {} : {}", fmt::ptr(p_number9), *p_number9);
} else {
      fmt::println("WARNING : Trying to use an invalid pointer");
}
```

4.使用catch-except语法或者`std::nothrow`

```c++
try{
     int * data = new int[100000000000000];
     for(size_t i{0} ; i < 10000000 ; ++i){
         int * data = new int[100000000000000];
         // int *data = new (std::nothrow) int[1000000000000000]; //有std::nothrow关键字，如果有异常，则会赋值nullptr，不会程序崩溃
            }
        }catch(std::exception& ex){
            fmt::println("Something went wrong: {}", ex.what());
}


```

# 智能指针

1.unique_ptr

唯一指针，只能有一个指针指向同一内存，使用这个就不用手动delete

```c++
#include <memory>

int* p_int3 = new int(30);
std::unique_ptr<int> up_int4{p_int3}; 

std::unique_ptr<int> up_int5 {new int(50)};
```

在使用了std::unique_ptr后最好不要使用原始指针p_int3了



c++14后有更好的方法，以避免直接使用new

```c++
std::unique_ptr<int> up_int7 = std::make_unique<int>(70);
up_int7.reset() //重置为空指针，内存被释放

```

**注意**：如果初始化两个unique_ptr指向p_int3，程序会崩溃，因为会自动delete两次



如果要转移指针的控制权，可以用std::move,

```c++
int* p_int3 = new int(30);
std::unique_ptr<int> up_int4{p_int3};
std::unique_ptr<int> up_int5{std::move(up_int4)};
```

这种情况下，up_int4会被自动重置为空指针



2. shared_ptr

和unique_ptr不同在于，可以把自身指针信息复制出去。然后进行一个计数，复制一次加1，重置一次减1，use_count()归0的话，内存会被释放

```

std::shared_ptr<int> int_ptr_1{ new int{20} };
std::shared_ptr<int> int_ptr_2 = int_ptr_1;
std::println(stdout, "Use count for int_ptr_1: {}", int_ptr_1.use_count());
std::println(stdout, "Use count for int_ptr_2: {}", int_ptr_2.use_count());

int_ptr_2.reset();
std::println(stdout, "Use count for int_ptr_1: {}", int_ptr_1.use_count());
```



但是仍然不能使用下面方式，会崩溃

```c++
int* p = new int{ 20 };
std::shared_ptr<int> int_ptr_1{ p };
std::shared_ptr<int> int_ptr_2{ p };
```



c++14后可以使用make_shared

```c++
std::shared_ptr<int> int_ptr_1 = std::make_shared<int>(20);

std::shared_ptr<int> int_ptr_2{ nullptr };
int_ptr_2 = int_ptr_1;
int_ptr_2.reset();
```

