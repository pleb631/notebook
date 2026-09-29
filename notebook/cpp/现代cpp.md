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