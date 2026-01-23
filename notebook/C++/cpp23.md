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

