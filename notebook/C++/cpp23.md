# 1. 基础规则

## 1.1 main函数

入门c++代码如下，main函数是一个程序的入口，每个程序都必须有这么一个函数，并且有且只有一个。

```c++
#include<iostream>
using namespace std;

int main() {

    std::cout << "hello C++" << endl;
    std::cin.get();//pause
    //system("pause"); 不同系统可能用不了

    return 0;
}
```

## 1.2 编译过程

![2023-08-05-15-48-57](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-05-15-48-57.png)

- 预处理
  预编译把一些  #define的宏定义完成文本替换，然后将#include的文件里的内容**复制**到.cpp文件里，如果.h文件里还有.h文件，就递归展开。在预处理这一步，代码注释直接被忽略，不会进入到后续的处理中，所以注释在程序中不会执行。生成文件 `main.i`
- 编译
  编译把我们写的代码转为汇编代码，它的工作是检查词法和语法规则，所以，如果程序没有词法或则语法错误，那么不管逻辑是怎样错误的，都不会报错。编译不是指程序从源文件到二进制程序的全部过程，而是指将经过预处理之后的程序转换成特定汇编代码(assembly code)的过程。生成文件 `main.s`
- 汇编
  汇编过程将上一步的汇编代码(main.s)转换成机器    (machine code)，这一步产生的文件叫做目标文件 `main o`，是二进制格式。生成最终的可执行文件(Executable file)。
- 链接
  链接（Link）其实就是一个“打包”的过程，汇编只会对单个cpp文件进行分开处理，还需要标准库、动态链接库和其他cpp文件等结合起来，生成最终的可执行文件(Executable file)。

## 1.3 基本变量

### 1.3.1变量类型

| 类型          | 含义           | 最小尺寸                       |
| ------------- | -------------- | ------------------------------ |
| `bool`        | 布尔类型       | 8bits                          |
| `char`        | 字符           | 8bits                          |
| `wchar_t`     | 宽字符         | 16bits                         |
| `char16_t`    | Unicode字符    | 16bits                         |
| `char32_t`    | Unicode字符    | 32bits                         |
| `short`       | 短整型         | 16bits                         |
| `int`         | 整型           | 16bits (在32位机器中是32bits)  |
| `long`        | 长整型         | 32bits                         |
| `long long`   | 长整型         | 64bits （是在C++11中新定义的） |
| `float`       | 单精度浮点数   | 4bits，6位有效数字             |
| `double`      | 双精度浮点数   | 8bits,15位有效数字             |
| `long double` | 扩展精度浮点数 | 8bits,15位有效数字             |

### 1.3.2 三种初始化方法

```c++
int a = 2;
int c (222);
int b {1};
// int a1 = 2.1; //不会报错，涉及类型转换
// int b1{2.1}; //会报错，建议用着这种

char character1 {'a'};
char value = 65;
fmt::println("value(int): {}", static_cast<unsigned int>(value));
```

## 1.4 枚举(enum)

枚举类型(enumeration)：是C++中的一种派生数据类型，它是由用户定义的若干枚举常量的集合。
`Enum 枚举类型名 {变量值列表}；`

```c++
enum Weekday{ SUM,MON,TUE,WED,THU,FRSAT };     //定义枚举类型
//SUM = 0;   //SUM是枚举类型，此语句非法
Weekday day1=WED, day2= SAT;
if (day1 > day2)
    cout << day1;
else
    cout << day2;
cin.get();


```

- 枚举元素具有默认值，依次为：0，1，2，3。。。
- 声明时可以另行定义枚举元素的值
- `Enum Weekday {SUM=7,MON=1,TUE,WED,THU,FRI,SAT}`; //后面从TUE依次为23456
- 枚举值可以进行关系运算
- 整数值不能直接赋值给枚举变量，如需将整数值给枚举类型，需要进行强制转换

## 1.5 结构体(struct)

结构体，通俗讲就像是打包封装，把一些变量和函数封装在内部，通过一定方法访问修改内部变量。与class在技术上的区别是struct默认public，class默认private

```c++
#include <iostream>
#include <string>
//自定义数据类型，一些类型的集合组成一个类型
//语法 struct 类型名称 { 成员列表 }
struct Student
{
    //成员列表
    std::string name;
    int age;
    int score;
    char other[20];
    void Log1(){cout <<score;}
};

int main()
{
    Student s1;
    Student s2 = { "李四",19,80 };
    //给s1属性赋值，通过点.访问结构体变量中的属性
    s1.age = 18;
    s1.score = 100;

    cout << "age1：" << s1.age <<endl;
    cout << "score1：" << s2.score <<endl;

    std::cin.get();//pause

    return 0;

}
```

## 1.6 const

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

## 1.7 控制语句

### 1.7.1 for

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

## 1.8 位运算

## 1.9 字符串

### 1.9.1 字符数组

这种方式不常用不建议使用。数组的定义方式是

```c++
char name[10]={'s','t','r','i','n','g','\0'};//需要手动加上'\0'
char a[]="hello world"; 
```

这种情况非常适合使用`cctype`标准库

该库主要是用来判断单个字符是否是数字、字母或其他字符，可以用来判断是否是大小写并转换‘’

比如：

```c++
int isalnum(int c);
int isalpha(int c);
int isblank(int c);
int islower(int c);
int isupper(int c);
int tolower(int c);
int toupper(int c);
```



### 1.9.2 c_string

这种是比较常见，写法是用指针来定义

```c++
const char* message2 {"The sky is blue."};
const char message1 [] {"The sky is blue."};
```

本质是用一个指针来存储字面量的地址,由于是字面量，所以必须使用`const`来申明

此时可以借助`cstring`标准库，该库提供了实用的字符串操作工具,比如：

```c++
char* strcat(char* s1, const char* s2);
int strcmp(const char* s1, const char* s2);
size_t strlen(const char* s);  
char* strchr(char* s, int c); //查找字符的第一次出现
char* strstr(char* s1, const char* s2);  //查找字符子字符串的第一次出现
```



#### 1.9.2.1 字面量(literal)

字面量是指在源代码中直接写出的固定值，字符串字面量通常存储在程序的只读内存区域中



原始字符串字面量`Raw String Literals`是 C++11 引入的一种新的字符串表示方式，它允许你在字符串中直接使用不需要转义的字符（如反斜杠、换行符等），使得处理一些包含特殊字符的字符串更加方便。

原始字符串字面量的语法为：

```c++
R"delimiter(string_contents)delimiter"
```

**`delimiter`**：是可选的标识符，用于确定字符串的开始和结束位置。可以是空字符串，也可以是自定义的字符串，目的是避免与字符串内容中的括号冲突。

**`string_contents`**：表示字符串的内容，可以包含换行符、引号、反斜杠等，而不需要转义。



例子：

```c++
const char* str = R"(This is a raw string literal)";
const char* path = R"(C:\Program Files\MyApp)";  // 路径中无需转义反斜杠
const char* json = R"({
  "name": "John Doe",
  "age": 30,
  "city": "New York"
})";  // JSON 字符串字面量
```



### 1.9.3 std_string

# 2. 基本语法

## 2.1 指针

### 2.1.1介绍

指针是存储内存地址的变量，引用是指针的语法糖，两者会转为同一汇编代码

```c++
//声明
int *p1,*p2;//p1和p2是指向int对象的指针
double *dp1, *dp2;//dp1和dp2是指向double对象的指针
//定义
int a = 1;
int *p = &a;//P中存放变量a的地址，或者说p是指向a的指针
*p = 3;//pi的指向没有改变，但a的值发生了改变
int &p1=a; //创建引用p1,必须赋值
//引用初始化后不能被改变，指针可以改变所指的对象
//不存在指向空值的引用，但是存在指向空值的指针。

//空指针
int *p1 = nullptr;
int *p2 = 0;
int *p3 = NULL;//三种方法等价


```

范例

```c++
#include<iostream>
using namespace std;


int Log(int *num)
{
    std::cout <<*num;
    return 0;
}

int main() {

    int num = 1;
    int* p = #
    int& p1 = num;
    Log(p);
    Log(&num);
    Log(&p1);
    std::cout <<std::endl;
    num=num+1;
    *p=*p+1;
    p1=p1+1;
    std::cout <<num;
    std::cout <<*p;
    std::cout <<p1;
    std::cin.get();//pause

    return 0;
}
//输出结果：
//111
//444
```



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





### 2.1.2 指针的用法和含义



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

## 2.2 动态内存

### 2.2.1 new

一般声明的变量存放在栈上，new则会在堆上开辟空间。new出来的是一段空间的首地址，需要用指针来存放这段地址

```c++
int *p(nullptr);
p = new int; //在堆上开辟了一个4字节内存，并用p指向它
*p=22; //解引用
delete p; //释放内存回os
p = nullptr; //重置指针指向
// 如果初始化失败，会抛出异常
```

### 2.2.2 new使程序崩溃的情况

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

## 2.3 智能指针

手动管理栈上的指针很容易出问题，所以有了能自动管理的智能指针

### 2.3.1.unique_ptr

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



### 2.3.2 shared_ptr

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

### 2.3.3 weak_ptr

weak_ptr被称为弱指针，可以和shared_ptr一起使用。但是它不会增加引用计数。当我们将一个shared_ptr赋值给另外一个shared_ptr时它会增加引用计数。但是当把一个shared_ptr赋值给一个weak_ptr时不会增加引用计数。如果不想要Entity的所有权，例如在排序一个Entity列表时不关心它们是否有效，只需要存储一个它们的引用就可以了。

```c++
std::weak_ptr<Entity> entity;
```

## 2.4 类

# 4.其他

## 4.0标准库

## 4.1随机

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

## 4.2 C++中如何处理多返回值

若有一个函数需要返回两个字符串，有很多不同的方法可以实现。但在C++的默认情况下不能返回两种类型。若一个函数需要返回两个或多个相同类型的变量，则可以返回vector或数组。

### 结构体

  若有个函数叫ParseShader需要返回两个字符串。可以选择的解决方法是：创建一个叫做ShadweProgramSource的结构体，它只包含这两个字符串。若还想返回一个整数或其他不同类型的东西，可以把它添加到结构体中并返回它。

```
struct ShaderProgramSource
{
std::string VertexSource;
std::string FragmentSource;
int a;
}
static ShaderProgramSource ParseShader(const std::string& filepath)
{

}
return {vs,fs};
```

### 数组

  C++也提供了其他不同的处理方式。一种简单的方法就是返回一个数组，我们可以返回一个数组就像返回一个std::string\*指针。这是一个2个元素的数组，我们可以传入VertexSource或者FragmentSource。

```c++
static std::string* ParseShader(const std::string& filepath)
{

}
return new std::string[]{vs,fs};
```

由于使用new导致了堆分配的发生，所以要以下设置。

```c++
std::string* sources=ParseShader(filepath);
```

  还可以返回一个std::array，类型是string，大小是2。

```c++
#include <array>
static std::array<std::string,2> ParseShader(const std::string& filepath)
{

}
return std::array<std::string,2> (vs,fs);
```

  或者

```c++
std::array<std::string,2>results;
results[0]=vs;
results[1]=fs;
return results;
```

### vector

  若返回两种以上则可以使用vector。它和array的区别是array在栈上创建，而vector会把它的底层存储在堆上，所以std::array会更快。

```c++
#include<vector>
static std::vector<std::string> ParseShader(const std::string& filepath)
{

}
std::vector<std::string>results;
results[0]=vs;
results[1]=fs;
return results;
```

### tuple

  vector和array只有在类型相同的情况下才有效。若类型会发生变化有两种方式，一种叫做tuple(元组)的东西，另一个叫做pair。tuple基本上是一个类，它可以包含x个变量但它不关心类型。tuple在functional里面，utitly提供了make\_tuple这样的工具。

```c++
#include<utitly>
#include<functional>
static std::tuple<std::string,std::string,int> ParseShader(const std::string& filepath)//增添int
{

}
return std::make_pair(vs,fs);
std::tuple<std::string,std::string> sources=ParseShader(filepath);
//auto sources=ParseShader("res/shaders/Basic.shader");
```

  从tuple里获取数据需要使用std::get，

```c++
std::string vs=std::get<0>(sources);
```

### pair

  在这个例子中有两个返回值，所以可以返回一个std::pair。它与tuple的区别是返回值是2个字符串，也可以使用std::get或者sources.first，sources.second。

```c++
static std::pair<std::string,std::string> ParseShader(const std::string& filepath)
{

}
```

由于并不能知道第一个变量和第二个变量是什么，所以还是建议使用[struct结构体]

## 4.3 lambda函数

lambda的本质是一个普通函数，但不像普通函数一样做声明。它是我们的代码在过程中生成的，用完即弃的函数。

```c++
#include<iostream>
#include<vector>


void ForEach(const std::vector<int>& values, void(*func)(int))
{
 for (int value : values)
  func(value);
}

int main()
{
 std::vector<int> values = { 1,5,4,2,3 };

 ForEach(values, [](int value) {std::cout << " Value:" << value << std::endl;});

 std::cin.get();
}


```

> 这里的[]叫做捕获方式，lambda可以把上下文变量以值或引用的方式捕获，在body中直接使用。int value是我们的参数，后面就和PrintValue函数体一样了。
> [] 什么也不捕获;
> [=] 按值的方式捕获所有变量 ;
> [&] 按引用的方式捕获所有变量;
> [=, &a] 除了变量a之外，按值的方式捕获所有局部变量，变量a  使用引用的方式来捕获。这里可以按引用捕获多个，例如 [=, &  a, &b,&c]。这里注意，如果前面加了=，后面加的具体的参数必  须以引用的方式来捕获，否则会报错;
> [&, a] 除了变量a之外，按引用的方式捕获所有局部变量，变量  a使用值的方式来捕获。这里后面的参数也可以多个，例如 [&,   a, b, c]。这里注意，如果前面加了&，后面加的具体的参数必  须以值的方式来捕获;
> [a, &b] 以值的方式捕获a，引用的方式捕获b，也可以捕获多个;
> [this] 在成员函数中，也可以直接捕获this指针，其实在成员  函数中，[=]和[&]也会捕获this指针。

```c++
int x = 1; int y = 2;
auto plus = [=] (int a, int b) -> int { return x + y + a + b; };
int c = plus(1, 2);
//把x，y按值捕获
```

可以把lambda赋值给一个auto类型变量，然后将lambda变量传入函数。

```c++
int main()
{
 std::vector<int> values = { 1,5,4,2,3 };
 
 auto lambda = [](int value) {std::cout << " Value:" << value << std::endl;};

 ForEach(values, lambda);
 
 std::cin.get();
}

```

当我们试图传入某些变量时，不管是通过值还是引用来捕获变量，这里的ForEach都会出错，因为我们正在使用原始函数指针。若转变成std::function，返回void，有一个int参数叫做func就可以了。
![2023-08-13-15-02-43](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-13-15-02-43.png)
我们有一个可选的修饰符mutable，它允许函数体修改通过拷贝传递捕获的参数。若我们在lambda中给a赋值会报错，需要写上mutable。
![2023-08-13-15-04-11](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-13-15-04-11.png)

还可以写一个lambda接受vector的整数元素，遍历这个vector找到比3大的整数，然后返回它的迭代器，也就是满足条件的第一个元素。

```c++
#include<iostream>
#include<vector>
#include<algorithm>

int main()
{
 std::vector<int> values = { 1,5,4,2,3 };

 auto it = std::find_if(values.begin(), values.end(), [](int value) {return value > 3;});

 std::cout << *it << std::endl;
 
 std::cin.get();
}
```

### 
