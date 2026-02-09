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

查看各个进制的表示

```c++
unsigned short int data {15};

fmt::println("data (dec): {0:d}", data);    // Decimal
fmt::println("data (oct): {0:o}", data);    // Octal
fmt::println("data (hex): {0:x}", data);    // Hexadecimal
fmt::println("data (bin): {:016b}", data);  // Binary (16 digits)
```

 Shift运算符

```c++
unsigned short int value {0xff0u};
value =  static_cast<unsigned short int> (value << 1);
fmt::println("binary value: {:016b}, decimal value: {}", value, value);

value =  static_cast<unsigned short int> (value << 4);
fmt::println("binary value: {:016b}, decimal value: {}", value, value);

value =  static_cast<unsigned short int> (value >> 1);
fmt::println("binary value: {:016b}, decimal value: {}", value, value);
```

逻辑运算

```c++
unsigned int value1 {0x3};  // 0000 0011
unsigned int value2 {0x5};  // 0000 0101
fmt::println("Bitwise and:");
fmt::println("value1 & value2: {:032b}", (value1 & value2));

fmt::println("Bitwise or:");
fmt::println("value1 | value2: {:032b}", (value1 | value2));

fmt::println("Bitwise NOT :");
fmt::println("~value1: {:032b}", ~value1);
fmt::println("~value2: {:032b}", ~value2);

fmt::println("Bitwise xor:");
fmt::println("value1 ^ value2: {:032b}", (value1 ^ value2));
```

当作mask使用。从RGBA提取单通道的值

```c++
unsigned int red_mask{ 0xFF000000 };
unsigned int green_mask{ 0x00FF0000 };
unsigned int blue_mask{ 0x0000FF00 };
unsigned int alpha_mask{ 0x000000FF };
unsigned int color {0xAABCDE00};

fmt::println("Red is: {0:d}", ((my_color & red_mask) >> 24));
fmt::println("Green is: {0:d}", ((my_color & green_mask) >> 16));
fmt::println("Blue is: {0:d}", ((my_color & blue_mask) >> 8));
fmt::println("Alpha is: {0:d}", ((my_color & alpha_mask) >> 0));
```

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

标准库`string`提供了一种更好的字符串容器，并且附带数据转换的接口，这个容器可以使用c_string和字符数组来初始化自己

数据初始化：

```c++
std::string planet{ "Earth. Where the sky is blue" };
std::string prefered_planet{ planet };
std::string result{"planet",1,3}; //切片
std::string result1(4, 'e'); //长度为4填充'e'的字符串
```

字符串赋值

```c++
// 和构造函数类似，但这是赋值过程
string& assign(const char *s)
string& assign(const char *s, int n,int m)
string& assign(const string &s)
string& assign(int n, char c)
```

数据转换：

```c++
std::to_string;
std::stoi;
std::stof;
```

字符串拼接

```c++
//字符串拼接
string a = string("asd")+"asd";

using namespace std::string_literals;
//   `"S` 是来自上一行的命名空间的语法，正式名称叫‘用户自定义字面量（User-Defined Literals, UDL）’
//C++11引入
string b = "asd"s+"asd";

string c = a+"123"+b //可以直接用


std::string str11 {"Hello "};
std::string str12 {str11.append(5,'?')}; // Appends 5 '?' characters
std::string str13{str12.append(str11,2,3)};
```

查找和替换

```c++
string a="hello world";
//int find(const char* s, int pos=0, int n=0)
//从pos开始查看指定字符子串，如果n>0,就存在查找范围。
int f1 = a.find('ll');
int l1 = a.rfinf('o');


//查到字符
//find_first_of
//find_first_not_of
//find_last_of
//find_last_not_of


string& replace(int pos, int n, const string& str); //替换从pos开始n个字符为字符串str
string& replace(int pos, int n,const char* s);  //替换从pos开始的n个字符为字符串s
```

[std::basic_string - cppreference.cn - C++参考手册](https://cppreference.cn/w/cpp/string/basic_string)

```c++
//字符子串
//starts_with
//end_with
//compare
//contains
//substr
//push_back
//pop_back
//erase
//clear
```

如果用这个容器，可以使用全部stl算法

### 1.9.4 string_view

来自c++17，

提供一种只用来看，不能编辑的字符串类型。

特点:不会发生复制，只是用指针指向要看的地址

```c++
const char * c_string1 { "The animals have left the region" };
std::string_view sv10{c_string1};

// 不看前两个字符
sv14.remove_prefix(2);
// 不看最后两个字符
sv14.remove_suffix(2);
```

可以通过提供的接口完成基本的字符串处理,比如

```c++
find;
contains;
starts_with;
find_first_of;
find_last_of;
compare;
```

## 1.10 函数

### 1.10.1 入口函数

通常程序入口是带参数的

```c++
void process_arguments(int argc, char* argv[]){
    fmt::println("number of arguments: {}", argc);

    for(size_t i{0}; i < argc; ++i){
        fmt::println("arg [{}]: {}", i, argv[i]);
    }   
}

int main(int argc, char* argv[]){
    process_arguments(argc, argv);
}
```

这个argv可以继续传递给下一个函数

### 1.10.2 lambda

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

# 2. 进阶基础

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

1. 访问被释放的指针

```c++
int * p_number1 {new int{67}};
fmt::println( "*p_number1(after delete): {}", *p_number1 );
delete p_number1;
fmt::println( "*p_number1(after delete): {}", *p_number1 );//CRASH!
```

1. 多个指针指向同个地址

```c++
int *p_number3 {new int{83}};
int *p_number4 {p_number3};
delete p_number3;
fmt::println( "p_number4(after deleting p_number3) -{} :  {}", fmt::ptr(p_number4) , *p_number4 );//CRASH!
```

1. new失败

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

1. 在释放内存后重置指针

```c++
int *p_number7{ new int{ 82 } };
delete p_number7;
p_number7 = nullptr;// Reset the pointer
```

1. 应该规定一个主指针来管理内存，其他指针必须在主指针可用时才能使用

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

### 2.2.3 高级用法

1. 可以把分配内存和创建对象分开来进行

```c++
#include <new>

struct A {
    A() { std::cout << "A born\n"; }
    ~A() { std::cout << "A dead\n"; }
};
//栈上
char buffer[sizeof(A)]; // 预分配内存
A* p = ::new (buffer) A(); // 在指定内存构造
p->~A(); // 需要显式调用析构函数

/*
void* buffer = operator new(sizeof(A)); //堆上分配
A* p = ::new (buffer) A();
p->~A(); 
operator delete(buffer); //堆上释放
*/ 

```

2. 自定义new、delete

```c++
class A {
public:
    static void* operator new(size_t size) {
        std::cout << "分配 " << size << " 字节\n";
        return ::operator new(size);
    }
    
    static void operator delete(void* p) {
        std::cout << "释放内存\n";
        ::operator delete(p);
    }
};
```



## 2.3 智能指针

手动管理堆上的指针很容易出问题，所以有了能自动管理的智能指针

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
class A {
public:
  weak_ptr<B> b_ptr; // 改为weak_ptr（不增加引用计数）
  ~A() { cout << "A析构" << endl; }
};

class B {
public:
  weak_ptr<A> a_ptr; // 改为weak_ptr
  ~B() { cout << "B析构" << endl; }
};

int main() {
  shared_ptr<A> a = make_shared<A>();
  shared_ptr<B> b = make_shared<B>();
  a->b_ptr = b; // weak_ptr不增加引用计数（b的计数仍为1）
  b->a_ptr = a; // weak_ptr不增加引用计数（a的计数仍为1）

  return 0;
} // a、b析构，引用计数=0 → A、B均析构（无内存泄漏）
```

## 2.4 类(class)

与结构体类似,class默认private

范例

```c++
#include <iostream>
using namespace std;

const double PI = 3.14;
class Circle
{
    public:
        int m_r;
        double calculateZC()
        {
            return 2 * PI * m_r;
        }
};   

int main()
{
    Circle c1;
    c1.m_r = 10;
    cout << "圆的周长为：" << c1.calculateZC() << endl;

   std::cin.get();//pause
  
    return 0;
}

```

### 2.4.1封装权限

公共权限 public,类内可以访问成员,类外可以访问成员

保护权限 protected,类内可以访问成员,类外不可以访问成员 子类可以访问父类中的保护内容

私有权限 private,类内可以访问权限,类外不可以访问成员 子类不可以访问父类中的私有内容

### 2.4.2构造函数

构造函数：主要作用在于创建对象时为对象的成员属性赋值，构造函数由编译器自动调用，无须手动调用。
构造函数语法：类名 () {}

1. 构造函数，没有返回值也不写void。
2. 函数名称与类名相同。
3. 构造函数可以有参数，因此可以重载。
4. 程序在调用对象时候会自动调用构造，无须手动调用，而且只会调用一次。

```c++
#include <iostream>
#include <string>

class Person
{

public:  
     // 内部赋值方式
    Person(int x1)
    { 
      x = x1;
      std::cout << "Person 构造函数1的调用" << endl;
    }

    // 初始化列表方式
    Person(int x1,string y1):
      x(x1),
      y(y1)
    { 
      std::cout << "Person 构造函数2的调用" << endl;
    }

    //编译器会自动创建一个，但是里面是空语句
    Person()=default;
    
    /*
     //Not recommended in modern C++
     Pixel(){

     }
     */
    
private:
  int x;
  string y;

};

int main()
{
    Person x_entiy(2);
    /*=》等价写法
    Person x_entiy=2；//隐式转换法
    Person x_entiy = Person(2) //显式法
    */
    Person y_entiy(1,"asd");
    std::cout << y_entiy.y<<endl;
    std::cout << x_entiy.x<<endl;

    std::cin.get();
    return 0;
}

```

### 2.4.3 析构函数

析构函数，没有返回值也不写void,程序在对象销毁前会自动调用析构，无须手动调用，而且只会调用一次。

如果类中有`new`出的堆上的空间，就需要在结束时调用析构函数来释放。如果没有手动管理的，则不需要定义析构函数

```c++
class Person
{
public:
    Person()
    {
        cout << "Person 构造函数的调用" << endl;
    }
    ~Person()
    { 
        delete a;
        cout << "Person 析构函数的调用" << endl;
    }
private:
    a = new int(8);
};
```

**注意**：如果使用的是智能指针管理内存，则不需要使用析构

### 2.4.4 隐式转换和显式转换

explicit：该构造函数是显示的。

implicit：该构造函数是隐式的（默认）

其用处是修饰类构造函数

如果是显示的会被阻止，在编译时无法自动转为对象。

如果是隐式的会被放行。

```c++
#include <iostream>
using namespace std;

class Cat
{
public :
 Cat(int num):n(num){}  // 默认为 implicit
private:
 int n;
};


class Mouse
{
public :
 explicit Mouse(int num):n(num){}
private:
 int n;
};
 
int main()
{
 Cat    t1 = 12; // 编译通过12会自动转为Cat对象赋值到构造函数
 Mouse  t2(13);  // 编译通过，
 Mouse  t3 = 14; // 在编译时，这个地方会报错，因为这个时显示的，因此不能直接转为Test2对象
  
 return 0;
}
```

### 2.4.5 符号重载

1. 运算符重载：对已有的运算符重新进行定义，赋予其另一种功能，以适应不同的数据类型。
2. 对于内置的数据类型的表达式的运算符是不可能改变的。

#### 加号重载

```c++
Person operator+(Person &p1, Person &p2)
{
    Person temp;
    temp.m_A = p1.m_A + p2.m_A;
    temp.m_B = p1.m_B + p2.m_B;
    return temp;
}
```

#### 左移重载

```c++
#include <iostream>

class Person
{
private:
    int m_A;
    int m_B;

public:
    Person(int a, int b) : m_A(a), m_B(b) {}

    friend std::ostream& operator<<(std::ostream &cout, Person &p);
};
// 如果返回类型为void，那么就无法无限追加，也没有办法在后面添加换行符
std::ostream &operator<<(std::ostream &cout, Person &p)
{
    cout << "m_A= " << p.m_A << " m_B=" << p.m_B;
    return cout;
}

int main()
{
    Person p(10,10);

    std::cout << p << " hello world" << std::endl;
    return 0;
}

```

### 2.4.6 拷贝构造函数

c++默认提供一个拷贝构造函数。它的作用是内存复制，将other对象的内存浅层拷贝进这些成员变量。形如以下:

```c++
Entity(const Entity& other)//拷贝构造函数
 {
    memcpy(this,&other,sizeof(other));
 }

// Entity a{};
// Entity b{a};
```

这会带来一个问题，如果有类中有使用指针，或者在堆上开辟内存，那么拷贝后，两个实例共享同一块内存。

且不说普通指针，堆上的空间会被释放两次，程序会直接崩溃（包括智能指针）。加上我们不想数据共享。

所以，在这种情况下，需要手动定义拷贝构造函数，进行深拷贝

下面的例子是拷贝字符串的例子

```c++
#include <iostream>
#include <fmt/format.h>

class String
{

public:
    String(const char *string)
    {
        m_Size = strlen(string);
        m_Buffer = new char[m_Size + 1]; //+1是为了复制'\0'
        memcpy(m_Buffer, string, m_Size + 1);
    }

    String(const String &other)
    {
        m_Size = other.m_Size;
        m_Buffer = new char[m_Size + 1];
        memcpy(m_Buffer, other.m_Buffer, m_Size + 1);
    }

    ~String()
    {
        std::cout << "Destructor called" << std::endl;
        delete[] m_Buffer;
    }

    const char *get()
    {
        return m_Buffer;
    }

private:
    char *m_Buffer;
    unsigned int m_Size;
};

int main()
{
    String string1 = "Cherno";
    String string2 = string1;
    std::cout << fmt::ptr(string2.get()) << std::endl;
    std::cout << fmt::ptr(string1.get()) << std::endl;

    return 0;
}

```

如果我们把上面的拷贝函数注释掉。可以发现打印的两个地址相同，然后程序崩溃了。

### 2.4.7 拷贝赋值函数

与上面的函数不同的是，上面是发生了构造过程，这个则是在构造完想进行赋值

```c++
String string1 = "Cherno";
String string2;
string2 = string1; //区别在这
```

这时候需要定义一个关于`=`的重载函数

```c++
String& &operator=(const String &other)
{
    if (this == &other)
        return *this;

    delete[] m_Buffer; //先释放已有的空间

    m_Size = other.m_Size;
    m_Buffer = new char[m_Size + 1];
    memcpy(m_Buffer, other.m_Buffer, m_Size + 1);

    return *this;
}
```

如果m_Buffer开辟空间失败，结果就是原来的数据损坏，然后该实例则进入半死状态。

而且手动写了这些函数，就必须把析构、拷贝、移动5个函数都写上，非常繁琐

最后就是delete和new必须严格配对。总之这种写法已经落后

### 2.4.8 拷贝函数（智能指针）

上一节是通过new开辟的空间，很繁琐很容易出错。下面用智能指针重构

```c++
#include <memory>
#include <cstring>
#include <fmt/format.h>

class String {
public:
    String() = default;
    String(const char* str);
    String(const String& other);
    String& operator=(const String& other);
    
    String(String&& other) = delete; //下面章节会补上
    String& operator=(String&& other) = delete;

    const char* get() const { return m_Buffer.get(); }

private:
    size_t m_Size = 0;
    std::unique_ptr<char[]> m_Buffer;
};

String& String::operator=(const String& other)
{
    if (this == &other)
        return *this;

    // 1️⃣ 先分配新内存（异常安全）
    auto newBuffer = std::make_unique<char[]>(other.m_Size + 1);
    std::memcpy(newBuffer.get(), other.m_Buffer.get(), other.m_Size + 1);

    // 2️⃣ 再整体替换
    m_Size = other.m_Size;
    m_Buffer = std::move(newBuffer);

    return *this;
}

String::String(const char* str)
{
    m_Size = std::strlen(str);
    m_Buffer = std::make_unique<char[]>(m_Size + 1);
    std::memcpy(m_Buffer.get(), str, m_Size + 1);
}

 String::String(const String& other)
 {
     m_Size = other.m_Size;
     m_Buffer = std::make_unique<char[]>(m_Size + 1);
     std::memcpy(m_Buffer.get(), other.m_Buffer.get(), m_Size + 1);
 }



int main()
{
    String s1("Hello");
    String s2(s1);
    String s3;

    s3 = s2;
    s1 = s2;
    fmt::println("s1: {}\n", fmt::ptr(s1.get()));
    fmt::println("s2: {}\n", fmt::ptr(s2.get()));
    fmt::println("s3: {}\n", fmt::ptr(s3.get()));
}
```

### 2.4.9 移动构造、移动赋值

这个主要是用来 把“资源的所有权”从一个对象转移到另一个对象，避免深拷贝。

如果只是单纯的转移资源,可以采用默认的函数，智能指针能够自动处理这个事

```c++
class String {
public:
    std::unique_ptr<char[]> m_Buffer;
    size_t m_Size = 0;

    String(String&&) noexcept = default;
    String& operator=(String&&) noexcept = default;
};

```

但如果想精准控制转移后的情况，则可以：

```c++
String::String(String&& other) noexcept
    : m_Size(other.m_Size),
      m_Buffer(std::move(other.m_Buffer))
{
    other.m_Size = 0;
}

String& String::operator=(String&& other) noexcept
{
    if (this != &other) {
        m_Buffer = std::move(other.m_Buffer);
        m_Size = other.m_Size;
        other.m_Size = 0;
    }
    return *this;
}
```

new版本

```c++
String::String(String&& other) noexcept
    : m_Size(other.m_Size),
      m_Buffer(other.m_Buffer)
{
    other.m_Size = 0; // 可以忽略
    other.m_Buffer = nullptr; //必须重置，防止释放资源
}

String& String::operator=(String&& other) noexcept
{
    if (this != &other) {
        delete[] m_Buffer;          // 释放旧资源

        m_Size = other.m_Size;
        m_Buffer = other.m_Buffer;

        other.m_Buffer = nullptr; 
    }
    return *this;
}

/* 更专业的写法
String& String::operator=(String&& other) noexcept
{
    std::swap(m_Size, other.m_Size);
    std::swap(m_Buffer, other.m_Buffer);
    return *this;
}
*/
// 因为传进来的是右值，swap后，右值会被丢弃，所以效果等价
```

实际使用时

```c++
String s1("Hello");
String s2(std::move(s1)); //移动构造
String s3;

s3 = std::move(s2); //移动赋值

```

### 2.4.10 继承

范例:

```c++
#include <iostream>
using namespace std;
class Ball
{
public:
  int diameter;
  void hit()
    {
      std::cout<<"ball has been hited"<<std::endl;
    }
  
  void print()
    {
      std::cout<<"this is a ball"<<std::endl;
    }
};


class Football:public Ball
{
  public:
    int color[3];

}

```

#### 三种继承改变权限

1. 继承的语法：class 子类：继承方式 父类
2. 继承方式一共有三种：

- 公共继承
- 保护继承
- 私有继承

1. 不同的继承方式，父类中的变量被继承后，权限相应的得到了改变，如下图所示。

![2023-08-09-11-18-47](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-09-11-18-47.png)

#### 继承后同名函数的处理

1. 子类对象可以直接访问到子类中同名成员。
2. 子类对象加作用域可以访问到父类同名成员。
3. 当子类与父类拥有同名的成员函数，子类会隐藏父类中所有同名成员函数(有参、无参)，加作用域才可以访问到父类中同名函数。
4. 静态函数下,子类和分类不会共用同一份数据

```c++
//同名成员属性处理方式
void test01()
{
    Son s;
    cout << "Son 下 m_A=" << s.m_A << endl;
    //如果通过子类对象访问到父类中同名成员，需要加作用域
    cout << "Base 下 m_A=" << s.Base::m_A << endl;  

}
```

#### 多继承语法

1. C++运行一个类继承多个类。
2. 语法：`class 子类：继承方式 父类1，继承方式 父类2，.....`
3. 多继承可能会引发父类中有同名成员出现，需要加作用域区分。
4. C++实际开发中不建议用多继承。

#### 菱形继承

菱形继承概念:

1. 两个派生类继承同一个基类
2. 又有某个类同时继承两个派生类
3. 这种继承被称为菱形继承

### 2.4.11 多态、虚函数

静态的多态：函数重载,看起来调用同一个函数却有不同的行为。静态：原理是编译时实现。
动态的多态：一个父类的引用或指针去调用同一个函数，传递不同的对象，会调用不同的函数。动态：原理是运行时实现。

在继承中要构成多态两个条件：

1. 必须通过基类的指针或者引用调用虚函数。
2. 被调用的函数必须是虚函数，且派生类必须对基类的虚函数进行重写。

虚函数：即被virtual修饰的类成员函数称为虚函数。一旦定义了虚函数，该基类的派生类中同名函数也自动成为了虚函数。也就是说在派生类中有一个和基类同名的函数，只要基类加了virtual修饰，派生类不加virtual修饰也是虚函数。虚函数只能是类中的一个成员函数，不能是静态成员或普通函数。

如下面代码中，doSpeak函数入口是基类，但是可以输入派生类，且因为虚函数的覆写，可以产生不同的结果

```c++
#include <iostream>
using namespace std;

class Animal
{
public:
    virtual void speak()
    {
        cout << "动物在说话" << endl;
    }
};

class Cat:public Animal
{
public:
    //重写 函数返回值类型、函数名、参数列表都完全相同才叫重写
    void speak()   override//子类virtual,override可写可不写，也可以写 virtual void speak()
    {
        cout << "小猫在说话" << endl;
    }
};

class Dog:public Animal
{
public:
    virtual void speak() override
    {
        cout << "小狗在说话" << endl;
    }
};


void doSpeak(Animal &animal)  // Animal & animal = cat
{
    animal.speak();
}

int main()
{
    Cat cat;
    doSpeak(cat);

    Dog dog;
    doSpeak(dog);
}

```

#### 纯虚函数和抽象类

1. 在多态中，通常父类中虚函数的实现时毫无意义的，主要都是调用子类重写的内容。因此，可以将虚函数改为纯虚函数。
2. 纯虚函数语法：`virtual 返回值类型 函数名 (参数列表) = 0;`
3. 当类中有了纯虚函数，这个类也称为抽象类。

④ 抽象类特点：

1. 无法实例化对象
2. 子类必须重写抽象类中的纯虚函数，否则也属于抽象类。

```c++
#include <iostream>
using namespace std;

//纯虚函数和抽象类
class Base
{
public:
    virtual void func() = 0;
};

class Son : public Base
{
public:
    virtual void func()
    {
        cout << "func函数调用" << endl;
     }
};

```

#### 虚析构函数

- **核心问题**：当基类指针指向派生类对象时，若基类析构函数非虚函数，销毁对象时只会调用基类析构，派生类析构不会执行，导致**资源泄漏**；

- **核心作用**：确保派生类对象通过基类指针销毁时，先调用派生类析构，再调用基类析构；

- **语法**：在基类析构函数前加`virtual`；

- 示例（对比非虚析构与虚析构）：

  ```
  // 基类
  class Base {
  public:
    // 非虚析构（错误示范）
    ~Base() {
      cout << "Base析构" << endl;
    }
  };
  
  // 派生类（含堆资源）
  class Derived : public Base {
  private:
    int* data;
  public:
    Derived() {
      data = new int(10);
    }
    ~Derived() {
      delete data; // 释放派生类的堆资源
      cout << "Derived析构" << endl;
    }
  };
  
  // 测试：基类指针指向派生类对象
  Base* ptr = new Derived;
  delete ptr; // 仅调用Base析构，Derived析构未执行 → 内存泄漏！
  ```

- **修正（虚析构）**：

  ```
  class Base {
  public:
    virtual ~Base() { // 基类析构设为virtual
      cout << "Base析构" << endl;
    }
  };
  
  Base* ptr = new Derived;
  delete ptr; 
  // 正确执行顺序：Derived析构 → Base析构（无内存泄漏）
  ```

- **面试考点**：虚析构的必要性——只要类可能被继承，且派生类有堆资源，基类析构必须设为`virtual`；抽象类（含纯虚函数）的析构也需设为虚析构（可提供默认实现）。

#### 与重载的区别(重点)

基类为虚函数下，子类重写虚函数，用基类指针调用子类，会使用子类函数

基类不是虚函数下，子类重写函数，用基类指针调用子类，会使用父类函数

```c++
#include <iostream>

class Base {
public:
    void show() { 
        std::cout << "Base class show" << std::endl;
    }
};

class Derived : public Base {
public:
    void show() {  // 这里不是虚函数的重写，只是覆盖
        std::cout << "Derived class show" << std::endl;
    }
};

int main() {
    Base* basePtr = new Derived();  // 基类指针指向派生类对象
    basePtr->show();  // 输出 "Base class show"，而不是 "Derived class show"
    delete basePtr;
    return 0;
}

```

### 2.4.12 const成员函数、mutable

常函数：

1. 成员函数后加const后我们称这个函数为常函数。
2. 常函数内不可以修改成员属性。
3. 成员属性声明时加关键字mutable后，在常函数中依然可以修改，mutable主要用于debug。

常对象：

1. 声明对象前加const称该对象为常对象。
2. 常对象只能调用常函数。

```c++
class TestClass
{
public:
 mutable int count = 0;
 int count1 = 0;
 void print() const
 {
  std::cout << count << std::endl;
  ++count;
  //++count1;//报错
 }

};

```

### 2.4.13 this指针

1. 每一个非静态成员函数只会诞生一份函数实例，也就是说多个同类型的对象会公用一块代码。
2. C++通过提供特殊的对象指针，this指针指向被调用的成员函数所属的对象。
3. this指针是隐含每一个非静态成员函数内的一种指针。
4. this指针不需要定义，直接使用即可。

this指针的用途：

- 当形参和成员变量同名时，可用this指针来区分。
- 在类的非静态成员函数中返回对象本身，可使用return * this。

```c++
#include <iostream>
using namespace std;

class Person
{
public:
    Person(int age)
    {
        this->age = age;  
                          //如果这里是 age = age；那么编译器会将这两个age和上面的形参age当做同一个age，因此age并没有赋值            
    }
  
    //如果用值的方式返回，Person PersonAddAge(Person& p){}，它返回的是本体拷贝的对象p'，而不是本体p                             
    Person& PersonAddAge(Person& p) //要返回本体的时候，要用引用的方式返回
    {
        this->age += p.age;
        return *this;
    }
    int age; 
};

int main()
{

    Person p1(10);
    Person p2(10);

    //链式编程思想
    p2.PersonAddAge(p1).PersonAddAge(p1).PersonAddAge(p1);

    cout << "p2的年龄为：" << p2.age << endl;

    std::cin.get();

    return 0;
}

```

## 2.5 IO

文件IO用于实现“数据持久化”（将数据存储到磁盘文件，或从文件读取数据），C++提供两种方式：**C风格文件IO（`<cstdio>`）** 和 **C++风格文件IO（`<fstream>`）**，推荐使用C++风格（面向对象、类型安全）。

| 模式标志      | 含义                                                         |
| ------------- | ------------------------------------------------------------ |
| `ios::in`     | 读模式（默认用于`ifstream`）                                 |
| `ios::out`    | 写模式（默认用于`ofstream`），若文件存在则清空，不存在则创建 |
| `ios::app`    | 追加模式（写模式的补充），数据写入文件末尾，不覆盖原有内容   |
| `ios::binary` | 二进制模式（默认是文本模式），用于读写二进制文件（如图片、视频） |
| `ios::trunc`  | 截断模式（默认用于`ios::out`），文件存在则清空内容           |
| `ios::ate`    | 打开文件后，文件指针直接指向文件末尾                         |

### 2.5.1 字符流

```c++
#include <vector>
#include <fstream>
#include <filesystem>
#include <fmt/format.h>
#include <vector>

void write_txt(){
    std::filesystem::path file_path("test.txt");
    std::ofstream file(file_path,std::ios::out | std::ios::app);
    std::vector<std::string> content = {"Hello", "World"};
    if (!file.is_open()) {
        fmt::println("Failed to open file for writing: {}", file_path.filename().string());
    }
    for (const auto& line : content) {
        file << line << '\n';
    }

    file.close();
}

void read_txt(){
    std::filesystem::path file_path("test.txt");
    std::ifstream file(file_path,std::ios::in);
    std::vector<std::string> content;
    if (!file.is_open()) {
        fmt::println("Failed to open file for reading: {}", file_path.filename().string());
    }
    std::string line;
    while (std::getline(file, line)) {
        content.push_back(line);
    }
    for (const auto& line : content) {
        fmt::println("{}", line);
    }
}
```

### 2.5.2 字节流

二进制文件存储的是字节序列（人类不可读），适用于存储结构体、图片、视频等数据，读写时需指定`ios::binary`模式，且不会处理换行符。

下面是读写字符的案例

```c++
int main()
{
    std::filesystem::path file_path = "example_binary_file.bin";
    const char *content{"hello world\n123"};

    std::ofstream file(file_path, std::ios::out | std::ios::binary); // Binary mode
    if (!file.is_open())
    {
        fmt::print("Failed to open file for writing: {}\n", file_path.filename().string());
        return 1;
    }

    file.write(content, strlen(content));
    file.close();

    std::ifstream file1(file_path, std::ios::in | std::ios::binary);
    if (!file1.is_open())
    {
        fmt::print("Failed to open file for reading: {}\n", file_path.filename().string());
        return 1;
    }
    std::streamsize size = std::filesystem::file_size(file_path);
    // Get the file size by seeking to the end
    // file.seekg(0, std::ios::end);
    // std::streamsize size = file.tellg();
    // file.seekg(0, std::ios::beg);

    std::vector<char> buffer(size);
    
    if (!file1.read(buffer.data(), size))
    {
        return 1;
    }
    file1.close();
    fmt::println("Content: {}", std::string(buffer.begin(), buffer.end()));
    return 0;
}
```

### 2.5.3 文件指针操作

文件指针（文件位置指示器）指向当前读写的位置，可通过`seekg()`（读指针）和`seekp()`（写指针）调整位置，配合`tellg()`/`tellp()`获取当前位置。

**核心函数**

| 函数名             | 功能                                                         |
| ------------------ | ------------------------------------------------------------ |
| `seekg(pos, mode)` | 移动读指针到指定位置：pos是偏移量，mode是基准（`ios::beg`：文件开头；`ios::cur`：当前位置；`ios::end`：文件末尾） |
| `seekp(pos, mode)` | 移动写指针（用法同seekg）                                    |
| `tellg()`          | 返回读指针当前位置（字节数，从文件开头算起）                 |
| `tellp()`          | 返回写指针当前位置                                           |

```c++
#include <fstream>
#include <iostream>
using namespace std;

int main() {
  ifstream ifs("test.txt", ios::in | ios::binary);
  if (!ifs.is_open()) return -1;

  // 1. 移动读指针到文件末尾，获取文件大小
  ifs.seekg(0, ios::end);
  int fileSize = ifs.tellg(); // 文件总字节数

  // 2. 移动读指针到文件末尾前10个字节（若文件小于10字节则从开头开始）
  int offset = (fileSize > 10) ? -10 : 0;
  ifs.seekg(offset, ios::end);

  // 3. 读取剩余字节
  char buf[11] = {0}; // 存储10个字符+结束符
  ifs.read(buf, 10);
  cout << "文件最后10个字节：" << buf << endl;

  ifs.close();
  return 0;
}
```

注意事项：

- 文本文件读写时，`string`类型可直接用`<<`/`>>`，但二进制文件不建议存储`string`（动态内存导致结构不固定），推荐用固定长度字符数组；
- 打开文件后必须检查是否成功（`is_open()`），避免因路径错误、权限问题导致后续操作失败；
- 操作完成后手动关闭文件（`close()`），或使用RAII封装（如自定义文件类，析构时自动关闭）；
- 二进制文件的跨平台兼容性：不同平台的字节序（大端/小端）、结构体对齐方式可能不同，需注意兼容性处理。

### 2.5.4 POD序列化

```c++
namespace pod_types
{
    struct PODType
    {
        int id;
        double value;
    };

    // Function to write POD to a binary file (returns bool for success)
    bool write_pod(const std::filesystem::path &filename, const PODType &pod)
    {
        std::ofstream out_file(filename, std::ios::binary);
        if (!out_file)
        {
            return false;
        }
        out_file.write(reinterpret_cast<const char *>(&pod), sizeof(PODType));
        return out_file.good();
    }

    // Function to read POD from a binary file (returns bool for success)
    bool read_pod(const std::filesystem::path &filename, PODType &pod)
    {
        std::ifstream in_file(filename, std::ios::binary);
        if (!in_file)
        {
            return false;
        }
        in_file.read(reinterpret_cast<char *>(&pod), sizeof(PODType));
        return in_file.good();
    }

    // Function to write a vector of PODType objects to a file
    bool write_pod_vector(const std::filesystem::path &file_path,
                          const std::vector<pod_types::PODType> &pod_vector)
    {
        std::ofstream out_file(file_path, std::ios::binary);
        if (!out_file)
        {
            fmt::print("Failed to open file for writing.\n");
            return false;
        }

        for (const auto &pod : pod_vector)
        {
            out_file.write(reinterpret_cast<const char *>(&pod), sizeof(pod_types::PODType));
        }

        if (!out_file.good())
        {
            fmt::print("Failed to write PODType objects to file.\n");
            return false;
        }

        out_file.close();
        return true;
    }

    // Function to read a vector of PODType objects from a file
    bool read_pod_vector(const std::filesystem::path &file_path,
                         std::vector<pod_types::PODType> &pod_vector)
    {
        std::ifstream in_file(file_path, std::ios::binary);
        if (!in_file)
        {
            fmt::print("Failed to open file for reading.\n");
            return false;
        }

        pod_types::PODType read_pod;
        while (in_file.read(reinterpret_cast<char *>(&read_pod), sizeof(pod_types::PODType)))
        {
            pod_vector.push_back(read_pod);
        }

        if (!in_file.eof() && !in_file.good())
        {
            fmt::print("Failed to read PODType objects from file.\n");
            return false;
        }

        in_file.close();
        return true;
    }

} // namespace  pod_types
```

### 2.5.5 非POD序列化

```c++
#include <vector>
#include <fstream>
#include <filesystem>
#include <fmt/format.h>
#include <vector>

namespace non_pod_types
{
    class Person
    {
    public:
        std::string name;
        int age;

        // Serialization function for a single person
        void serialize(std::ofstream &ofs) const
        {
            size_t name_size = name.size();
            ofs.write(reinterpret_cast<const char *>(&name_size), sizeof(name_size));
            ofs.write(name.data(), name_size);
            ofs.write(reinterpret_cast<const char *>(&age), sizeof(age));
        }

        // Deserialization function for a single person
        void deserialize(std::ifstream &ifs)
        {
            size_t name_size;
            ifs.read(reinterpret_cast<char *>(&name_size), sizeof(name_size));

            name.resize(name_size);

            // Read the name and age from the file and store in the object's members: name and age
            ifs.read(name.data(), name_size);
            ifs.read(reinterpret_cast<char *>(&age), sizeof(age));
        }
    };

    // Function to write a vector of person objects to a file
    void write_persons_to_file(const std::vector<Person> &persons, const std::filesystem::path &file_path)
    {
        std::ofstream ofs(file_path, std::ios::binary);
        if (!ofs)
        {
            fmt::println("Failed to open file for writing: {}", file_path.string());
            return;
        }

        size_t vector_size = persons.size();
        ofs.write(reinterpret_cast<const char *>(&vector_size), sizeof(vector_size));

        for (const auto &p : persons)
        {
            p.serialize(ofs);
        }

        fmt::println("Serialized {} person(s) to file: {}", vector_size, file_path.string());
    }

    // Function to read a vector of person objects from a file
    std::vector<Person> read_persons_from_file(const std::filesystem::path &file_path)
    {
        std::ifstream ifs(file_path, std::ios::binary);
        if (!ifs)
        {
            fmt::println("Failed to open file for reading: {}", file_path.string());
            return {};
        }

        size_t vector_size;
        ifs.read(reinterpret_cast<char *>(&vector_size), sizeof(vector_size));

        std::vector<Person> persons(vector_size);
        for (auto &p : persons)
        {
            p.deserialize(ifs);
        }

        fmt::println("Deserialized {} person(s) from file: {}", vector_size, file_path.string());
        return persons;
    }

} // namespace non_pod_types
int main()
{
    non_pod_types::Person p1{"John", 30};
    non_pod_types::Person p2{"Mike", 25};
    // write_to_file
    non_pod_types::write_persons_to_file({p1, p2}, "persons.bin");
    // read_from_file
    auto persons = non_pod_types::read_persons_from_file("persons.bin");
    for (const auto &p : persons)
    {
        fmt::println("Name: {}, Age: {}", p.name, p.age);
    }
}
```

### 2.5.6 类的序列化

其实还是属于非POD的内容，关键在于手动转换。不过这种转换风险太大，最好使用专门的库

```c++
#include <vector>
#include <fstream>
#include <filesystem>
#include <fmt/format.h>
#include <vector>

namespace class_with_non_pod_types
{

    // Position struct definition
    struct Position
    {
        unsigned int x{0};
        unsigned int y{0};

        Position() = default;
        Position(unsigned int x, unsigned int y) : x(x), y(y) {}
    };

    // Pixel class definition
    class Pixel
    {

    public:
        Pixel() = default;
        Pixel(uint32_t color, unsigned int x, unsigned int y)
            : m_color(color), m_pos(x, y) {}

        uint32_t get_color() const { return m_color; }
        const Position &get_position() const { return m_pos; }

        void set_color(uint32_t color) { m_color = color; }
        void set_position(unsigned int x, unsigned int y)
        {
            m_pos.x = x;
            m_pos.y = y;
        }

        void serialize(std::ofstream &out) const
        {
            out.write(reinterpret_cast<const char *>(&m_color), sizeof(m_color));
            out.write(reinterpret_cast<const char *>(&m_pos.x), sizeof(m_pos.x));
            out.write(reinterpret_cast<const char *>(&m_pos.y), sizeof(m_pos.y));
        }

        void deserialize(std::ifstream &in)
        {
            in.read(reinterpret_cast<char *>(&m_color), sizeof(m_color));
            in.read(reinterpret_cast<char *>(&m_pos.x), sizeof(m_pos.x));
            in.read(reinterpret_cast<char *>(&m_pos.y), sizeof(m_pos.y));
        }

    private:
        uint32_t m_color{0xFF000000};
        Position m_pos; // Now directly embedded, no heap allocation
    };

    void save_pixels(const std::vector<Pixel> &pixels, const std::filesystem::path &filepath)
    {
        std::ofstream out(filepath, std::ios::binary);
        if (!out)
        {
            fmt::println("Error opening file for writing: {}", filepath.string());
            return;
        }
        for (const auto &pixel : pixels)
        {
            pixel.serialize(out);
        }
    }

    std::vector<Pixel> load_pixels(const std::filesystem::path &filepath)
    {
        std::vector<Pixel> pixels;
        std::ifstream in(filepath, std::ios::binary);
        if (!in)
        {
            fmt::println("Error opening file for reading: {}", filepath.string());
            return pixels;
        }
        while (true)
        {
            Pixel temp;
            temp.deserialize(in);
            if (in.eof())
                break;
            pixels.push_back(temp);
        }
        return pixels;
    }

} // namespace class_with_non_pod_types

int main()
{
    using namespace class_with_non_pod_types;
    std::vector<Pixel> pixels = {Pixel(0xFF000000, 0, 0), Pixel(0xFF0000FF, 1, 1)};
    save_pixels(pixels, "pixels.bin");
    auto loaded_pixels = load_pixels("pixels.bin");
    fmt::println("Loaded {} pixels", loaded_pixels.size());
    return 0;
}
```

# 3.现代cpp

## 3.1 template

### 3.1.1 函数模板

- **核心作用**：定义“通用函数”，支持多种数据类型，避免重复编写同逻辑不同类型的函数（如`int`求和、`double`求和）；

- **语法**：`template <typename T>` 或 `template <class T>`（`typename`和`class`等价）；

- 示例：通用求和函数

  ```
  // 函数模板：T是模板参数（类型占位符）
  template <typename T>
  T add(T a, T b) {
    return a + b;
  }
  
  int main() {
    // 方式1：编译器自动推导类型
    int sum1 = add(1, 2); // T=int → 返回3
    double sum2 = add(1.5, 2.5); // T=double → 返回4.0
  
    // 方式2：显式指定类型
    int sum3 = add<int>(3, 4); // 显式指定T=int
    return 0;
  }
  ```

- **模板实例化**：编译器遇到`add(1,2)`时，会自动生成`int add(int a, int b)`的具体实现（实例化），模板本身不会生成代码。

### 3.1.2 类模板

- **核心作用**：定义“通用类”，类的成员变量/函数可以是模板类型；

- **语法**：`template <typename T>` 声明模板，类名后可加模板参数；

- 示例：通用栈类（支持任意类型元素）

  ```
  template <typename T, int Size = 100> // 模板参数+默认值
  class Stack {
  private:
    T data[Size]; // 模板类型数组
    int top;
  public:
    Stack() : top(-1) {}
  
    void push(const T& val) {
      if (top < Size - 1) data[++top] = val;
    }
  
    T pop() {
      if (top >= 0) return data[top--];
      throw runtime_error("栈空");
    }
  
    bool isEmpty() const {
      return top == -1;
    }
  };
  
  // 使用
  int main() {
    // 栈1：int类型，默认大小100
    Stack<int> intStack;
    intStack.push(10);
    intStack.push(20);
    cout << intStack.pop() << endl; // 20
  
    // 栈2：double类型，大小50
    Stack<double, 50> doubleStack;
    doubleStack.push(3.14);
    cout << doubleStack.pop() << endl; // 3.14
  
    return 0;
  }
  ```

- **注意**：类模板的成员函数若在类外定义，需重新声明模板参数：

  ```
  template <typename T, int Size>
  void Stack<T, Size>::push(const T& val) {
    // 类外实现...
  }
  ```

### 3.1.3`...Args`

是一个类型模板形参包，它可以接受任意个数和类型的模板实参。它的语法是在模板形参的类型前加上省略号(…)，表示这个形参是一个可变的参数包，它可以匹配任意个数和类型的模板实参。例如，下面的函数模板就使用了类型模板形参包：

```c++
template <class ...Args>
void print(Args... args) {
  // 这里的args...是一个可变参数包，它可以接受任意个数和类型的函数实参
  // 这里的sizeof...(args)是一个运算符，它可以计算可变参数包中的参数个数
  cout << "The number of arguments is: " << sizeof...(args) << endl;
}
print(); // 输出 The number of arguments is: 0
print(1); // 输出 The number of arguments is: 1
print(1, 2.0, "hello"); // 输出 The number of arguments is: 3


```

## 3.2元编程

### 3.2.1 类型解析

`type_traits`

该库提供了类型判断的api，比如

```c++
is_void
is_integral
is_enum
is_floating_point
is_array
is_function
is_class
is_pointer
is_lvalue_reference
is_rvalue_reference
is_member_object_pointer
is_member_function_pointer
```

除此之外，还有类型属性

```c++
is_pod
is_abstract
is_unsigned
is_final
```

目前我看到比较常见的。

```c++
//判断是否同一类型
template< class T, class U >
struct is_same;
constexpr bool is_same_v = is_same<T, U>::value;

//demo
bool same = std::is_same<int, int>::value; // true
bool notSame = std::is_same<int, float>::value; // false
bool same = std::is_same_v<int, int>; // true
bool notSame = std::is_same_v<int, float>; // false
```

```c++
//判断函数结果类型
template< class F, class... ArgTypes >
class invoke_result;

template< class F, class... ArgTypes >
using invoke_result_t = typename invoke_result<F, ArgTypes...>::type;


//demo
#include <type_traits>
#include <functional>
int main() {
   std::function<int(int, double)> func = [](int a, double b) { return a + b; };
   using RetType = std::invoke_result_t<decltype(func), int, double>;
   static_assert(std::is_same_v<RetType, int>, "返回类型应为 int");
}
```



## 3.3 RAII

即Resource Acquisition Is Initialization

- 核心思想：“资源获取即初始化”——将资源（堆内存、文件句柄、锁等）的生命周期与对象的生命周期绑定：

  - 对象创建时（构造函数）获取资源；
  - 对象销毁时（析构函数）自动释放资源；

- **核心价值**：无需手动管理资源，从根源上避免内存泄漏、资源泄漏；

- 典型应用：

  - 智能指针（`unique_ptr`/`shared_ptr`）：封装堆内存，析构时自动`delete`；
  - 锁管理（`lock_guard`）：构造时加锁，析构时自动解锁；

- 示例（RAII封装文件句柄）：

  ```
  class FileGuard {
  private:
    FILE* file; // 资源：文件句柄
  public:
    // 构造时获取资源（打开文件）
    FileGuard(const char* path, const char* mode) {
      file = fopen(path, mode);
      if (!file) throw runtime_error("文件打开失败");
    }
  
    // 析构时释放资源（关闭文件）
    ~FileGuard() {
      if (file) fclose(file);
    }
  
    // 提供访问接口
    FILE* getFile() const { return file; }
  };
  
  // 使用：无需手动关闭文件
  void readFile() {
    FileGuard fg("test.txt", "r"); // 打开文件（获取资源）
    fread(..., fg.getFile()); // 操作文件
  } // fg销毁，析构函数自动关闭文件（释放资源）
  ```

## 3.4 Rule of Five

  C++11后扩展自“三大法则”（Rule of Three），核心规则：

> 若类中显式定义了以下任意一个成员，必须显式定义其余四个，否则可能导致资源管理错误：
>
> 1. 析构函数（`~类名()`）；
> 2. 拷贝构造函数（`类名(const 类名&)`）；
> 3. 拷贝赋值运算符（`operator=(const 类名&)`）；
> 4. 移动构造函数（`类名(类名&&)`）；
> 5. 移动赋值运算符（`operator=(类名&&)`）；

- **核心原因**：显式定义析构函数通常意味着类管理了资源（堆内存等），默认的拷贝/移动语义是“浅拷贝”，会导致资源重复释放或内存泄漏；

- 简化方案：

  - 若不需要拷贝/移动：显式删除（`= delete`）拷贝/移动相关函数；
  - 若需要：手动实现深拷贝/移动语义；

- 示例（删除拷贝，保留移动）：

  ```
  class String {
  public:
    // 拷贝构造和拷贝赋值删除（禁止拷贝）
    String(const String&) = delete;
    String& operator=(const String&) = delete;
  
    // 移动构造和移动赋值实现（允许移动）
    String(String&&) noexcept;
    String& operator=(String&&) noexcept;
  
    // 析构函数
    ~String();
  };
  ```

## 3.5 虚函数表vtable

- **核心概念**：vtable是编译器为含有虚函数的类生成的静态数组，存储该类所有虚函数的地址；

- **核心机制**：

  1. 每个对象包含一个`vptr`（虚表指针，通常在对象内存的最前面），指向所属类的vtable；
  2. 基类有vtable，派生类若重写虚函数，会替换vtable中对应函数的地址；若新增虚函数，会追加到vtable末尾；
  3. 调用虚函数时，通过`vptr`找到vtable，再通过函数索引找到实际函数地址（动态绑定，运行时确定调用哪个版本）；

- **内存结构示例**（`Animal`基类，`Dog`派生类）：

  ```
  Animal类vtable：
  [0] → Animal::makeSound()
  [1] → Animal::~Animal()
  
  Dog类vtable（重写makeSound）：
  [0] → Dog::makeSound()（替换基类函数）
  [1] → Animal::~Animal()（继承基类虚析构）
  ```

- **重点**：

  - 含有虚函数的类，对象大小会增加（多一个vptr的大小，32位系统4字节，64位8字节）；
  - 虚函数调用比普通函数慢（多一次vptr查找和间接跳转）；
  - 构造函数不能是虚函数（对象未完全创建时，vptr未初始化）；
  - 析构函数可以是虚函数（且推荐设为虚函数）。

# 4.其他

## 4.0标准库

常用的c库的c++头文件

```bash
cstring # 详情见 #1.9.2
cctype # 详情见 #1.9.1
cmath # 数学
cstddef # size_t,ptrdiff_t,byte
ctime #
cstdio # 文件读写
cfloat # 宏定义的浮点数的大小
climits # 宏定义了整数的大小
cstdlib # 比较杂的工具

# c++11
cstdint # 提供了按位定义int的类型，比如int32_t

```

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

## 4.4 static_cast

static_cast是可以使用的最简单的类型转换。它是编译时强制转换。它可以在类型之间进行隐式转换(例如int到float，或指针到void*)，它还可以调用显式转换函数(或隐式转换函数)。

1. 用于原C风格的隐式类型转换

例如float转int

```c++
float a = 1.3;
int b = static_cast<int>(a);
cout<<"b="<<b<<endl;
```

1. 静态下行转换

不执行类型安全检查。

将父类的引用转换为子类的引用

```c++
struct B
{
    int m = 42;
    const char *hello() const
    {
        return "Hello world, this is B!\n";
    }
};

struct D : B
{
    const char *hello() const
    {
        return "Hello world, this is D!\n";
    }
};


D d;
B &br = d; // upcast via implicit conversion
std::cout << "1) " << br.hello();
D &another_d = static_cast<D &>(br); // downcast
std::cout << "1) " << another_d.hello();

//1) Hello world, this is B!
//1) Hello world, this is D!
```

1. 左值转换为右值引用

将左值v0的资源转移到右值引用v2, v2为{1, 2, 3}的右值引用

```
std::vector<int> v0{1, 2, 3};
std::vector<int> v2 = static_cast<std::vector<int>&&>(v0);
std::cout << "2) after move, v0.size() = " << v0.size() << '\n';

//3) after move, v0.size() = 0
```

1. 初始化转换

在变量初始化期间就对初始化数据进行类型转换

```
int n = static_cast<int>(3.14);
std::cout << "4) n = " << n << '\n';
std::vector<int> v = static_cast<std::vector<int>>(10);
std::cout << "4) v.size() = " << v.size() << '\n';
//4) n = 3
//4) v.size() = 10
```

1. 转换为void并丢弃

如果 new type为void类型，static\_cast将会在计算表达式的值之后丢弃这个值，无法使用变量接到这个值。

```c++
static_cast<void>(v2.size());  
int a =  static_cast<void>(v2.size());  //error,void value not ignored as it ought to be
```

void\*转换到具体类型

static\_cast可以提取void\*类型中的值

```c++
  void *nv = &n;

  int *ni = static_cast<int *>(nv);

  std::cout << "6) *ni = " << *ni << '\n';

  //6) *ni = 3
```

1. 枚举转int（scoped enum to int）

将枚举代表的值转换为int

```c++
enum class E
{
    ONE = 1,
    TWO,
    THREE
};

   E e = E::TWO;
   int two = static_cast<int>(e);
 E e2 = static_cast<E>(two);
   std::cout << "7) " << two << '\n';
```

## 4.5宏

宏提供了一种机制，能够使你在编译期替换代码中的符号或者语句。当你的代码中存在大量相似的、重复的代码时，使用宏可以极大的减少代码量，便于书写。

```c++
#include<iostream>

//发生在编译器的预处理阶段
#define WAIT std::cin.get() //注意无需分号

int main()
{
 WAIT;
}

```

宏还可以发送参数

```c++
#include<iostream>

#define LOG(x) std::cout << x << std::endl

int main()
{
 LOG("Hello");
 std::cin.get();
}

```

在实际工作中，常常在release版本中去掉所有的日志代码，但是在debug版本中保留。我们可以通过宏做到这一点。首先要修改项目属性。
![2023-08-12-17-33-11](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-12-17-33-11.png)
![2023-08-12-17-33-25](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-12-17-33-25.png)

```c++
#include<iostream>

#if 1//可以置0把下面代码禁用掉


#if PR_DEBUG == 1
#define LOG(x) std::cout << x << std::endl
#elif defined(PR_RELEASE)  //defined是检测函数，检测预定义是否存在
#define LOG(x)
#endif

#endif


int main()
{
 LOG("Hello");
 std::cin.get();
}

```

还可以使用反斜杠来写多行的宏，因为宏必须在同一行。

```c++
#include<iostream>

#define MAIN int main() \
{\
   std::cin.get();\
}

MAIN

```

## 4.6内联（inline）函数

- 普通函数的缺点：调用函数比求解等价表达式要慢得多。
- `inline`函数可以避免函数调用的开销，可以让编译器在编译时**内联地展开**该函数。
- `inline`函数应该在头文件中定义。

## 4.6函数指针

如果在程序中定义了一个函数，那么在编译时系统就会为这个函数代码分配一段存储空间，这段存储空间的首地址称为这个函数的地址。而且函数名表示的就是这个地址。既然是地址我们就可以定义一个指针变量来存放，这个指针变量就叫作函数指针变量，简称函数指针。

函数指针的类型是

```c++
T (*) (T1 x,);
```

函数指针的定义方式为：

> 函数返回值类型 (* 指针变量名) (函数参数列表);

“函数返回值类型”表示该指针变量可以指向具有什么返回值类型的函数；“函数参数列表”表示该指针变量可以指向具有什么参数列表的函数。这个参数列表中只需要写函数的参数类型即可。

示例：

```c++
int Func(int x);   /*声明一个函数*/

//
int (*p) (int x);  /*定义一个函数指针*/
p = Func;          /*将Func函数的首地址赋给指针变量p*/

//typedef
typedef int (*pfuna)(int);
pfuna p=Func;

//using 
using pfuna = float(*)(int, float);
pfuna  p=Func

//auto
auto fa = Func;
```

我们所做的是将function作为一个变量名进行调用，将函数参数化

```c++
#include<iostream>
#include<vector>

void PrintValue(int value)
{
 std::cout << " Value:" << value << std::endl;
}

void ForEach(const std::vector<int>& values, void(*func)(int))
{
 for (int value : values)
  func(value);
}

int main()
{
 std::vector<int> values = { 1,5,4,2,3 };

 ForEach(values, PrintValue);//vector中的每个元素都执行PrintValue
 
 std::cin.get();
}

```

## 4.7 异常

C++标准库提供了异常基类`exception`（定义在`<exception>`头文件中），自定义异常类建议继承`exception`，并重写`what()`方法（返回异常描述），便于统一处理。

####

```
#include <iostream>
#include <exception>
#include <string>
using namespace std;

// 自定义异常类：继承exception
class DivideException : public exception {
private:
  string msg;
public:
  // 构造函数：传入异常描述
  DivideException(const string& message) : msg(message) {}

  // 重写what()方法（必须是const noexcept）
  const char* what() const noexcept override {
    return msg.c_str(); // 返回C风格字符串
  }
};

int divide(int a, int b) {
  if (b == 0) {
    throw DivideException("除数不能为零！"); // 抛出自定义异常
  }
  if (b < 0) {
    throw runtime_error("除数不能为负数！"); // 抛出标准库异常
  }
  return a / b;
}

int main() {
  try {
    divide(10, -2);
  } catch (const DivideException& e) { // 捕获自定义异常
    cout << "自定义异常：" << e.what() << endl;
  } catch (const exception& e) { // 捕获所有继承自exception的异常
    cout << "标准库异常：" << e.what() << endl; // 输出：除数不能为负数！
  }
  return 0;
}
```

## 4.8`new` 与 `malloc`

`new/delete`是C++的运算符，`malloc/free`是C语言的函数，两者都用于堆内存分配，但`new/delete`更符合C++的面向对象特性：

| 对比维度     | `new/delete`                                                 | `malloc/free`                                            |
| ------------ | ------------------------------------------------------------ | -------------------------------------------------------- |
| 本质         | C++运算符                                                    | C语言标准库函数                                          |
| 类型安全     | 分配时指定类型，返回对应类型指针（无需强制转换）             | 返回`void*`，需手动强制转换为目标类型                    |
| 构造/析构    | `new`自动调用构造函数，`delete`自动调用析构函数              | 仅分配/释放内存，不调用构造/析构（无法用于自定义类对象） |
| 内存分配失败 | 抛出`bad_alloc`异常（C++11后）                               | 返回`NULL`指针                                           |
| 数组分配     | `new[]`分配数组，`delete[]`释放（必须匹配）                  | `malloc(n * sizeof(类型))`，需手动计算字节数             |
| 自定义分配器 | 支持重载`operator new`/`operator delete`，自定义内存分配逻辑 | 不支持，只能使用系统默认分配逻辑                         |

**示例对比**

```
// 1. 基础类型分配
int* p1 = new int(10); // new：分配+初始化，返回int*
int* p2 = (int*)malloc(sizeof(int)); // malloc：仅分配，返回void*需转换
*p2 = 10; // 手动初始化

delete p1; // 释放+调用析构（基础类型无析构，仅释放内存）
free(p2); // 仅释放内存

// 2. 数组分配
int* arr1 = new int[5]; // new[]：分配5个int的数组
int* arr2 = (int*)malloc(5 * sizeof(int)); // malloc：计算字节数

delete[] arr1; // 必须用delete[]，否则仅释放第一个元素（内存泄漏）
free(arr2);

// 3. 自定义类对象分配
class Person {
public:
  Person() { cout << "构造函数" << endl; }
  ~Person() { cout << "析构函数" << endl; }
};

Person* p3 = new Person; // new：分配内存+调用构造 → 输出"构造函数"
delete p3; // delete：调用析构+释放内存 → 输出"析构函数"

Person* p4 = (Person*)malloc(sizeof(Person)); // malloc：仅分配内存，不调用构造
free(p4); // 仅释放内存，不调用析构 → 资源泄漏（若类有堆资源）
```

## 4.9 `decltype`

- **核心作用**：获取表达式的类型（无需初始化变量），与`auto`互补（`auto`推导变量类型，`decltype`推导表达式类型）；

- 核心规则：

  - 若表达式是变量或函数调用，`decltype`直接返回其类型；
  - 若表达式是带括号的变量（如`decltype((x))`），返回引用类型；
  - 推导时保留`const`和引用属性。

**示例**

```
#include <vector>
using namespace std;

int add(int a, int b) { return a + b; }

int main() {
  int x = 10;
  const int y = 20;
  int& z = x;

  // 推导变量类型
  decltype(x) a = 5; // a为int
  decltype(y) b = 15; // b为const int
  decltype(z) c = x; // c为int&（引用）

  // 推导表达式类型
  decltype(x + y) d = 25; // x+y为int → d为int
  decltype(add(1,2)) e = 30; // add返回int → e为int

  // 带括号的变量（返回引用）
  decltype((x)) f = x; // f为int&（注意双层括号）
  f = 100;
  cout << x << endl; // x变为100

  // 结合模板使用（推导容器元素类型）
  vector<int> vec = {1,2,3};
  decltype(vec[0]) g = vec[0]; // g为int&（vector的[]返回引用）

  return 0;
}
```

**核心用途:**

- 模板中推导返回值类型（C++11前需用`typename`和`::type`，C++11后可结合`decltype`）；
- 定义与表达式类型一致的变量（避免类型冗余）；
- 配合`auto`实现泛型编程。
