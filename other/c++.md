## main函数

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

## 预处理、编译、汇编、链接

![2023-08-05-15-48-57](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-05-15-48-57.png)

- 预处理
  预处理，顾名思义就是编译前的一些准备工作。预编译把一些  #define的宏定义完成文本替换，然后将#include的文件里的内容**复制**到.cpp文件里，如果.h文件里还有.h文件，就递归展开。在预处理这一步，代码注释直接被忽略，不会进入到后续的处理中，所以注释在程序中不会执行。生成文件 `main.i`
- 编译
  编译把我们写的代码转为汇编代码，它的工作是检查词法和语法规则，所以，如果程序没有词法或则语法错误，那么不管逻辑是怎样错误的，都不会报错。编译不是指程序从源文件到二进制程序的全部过程，而是指将经过预处理之后的程序转换成特定汇编代码(assembly code)的过程。生成文件 `main.s`
- 汇编
  汇编过程将上一步的汇编代码(main.s)转换成机器    (machine code)，这一步产生的文件叫做目标文件 `main o`，是二进制格式。生成最终的可执行文件(Executable file)。
- 链接
  链接（Link）其实就是一个“打包”的过程，汇编只会对单个cpp文件进行分开处理，还需要标准库、动态链接库和其他cpp文件等结合起来，生成最终的可执行文件(Executable file)。

## 变量

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
| `float`       | 单精度浮点数   | 6位有效数字                    |
| `double`      | 双精度浮点数   | 10位有效数字                   |
| `long double` | 扩展精度浮点数 | 10位有效数字                   |

## 指针、引用

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

## 结构体(struct)

结构体，通俗讲就像是打包封装，把一些变量和函数封装在内部，通过一定方法访问修改内部变量。与class在技术上的区别是struct默认public，class默认private

```c++
#include <iostream>
using namespace std;
#include <string>
//自定义数据类型，一些类型的集合组成一个类型
//语法 struct 类型名称 { 成员列表 }
struct Student
{
    //成员列表
    string name;
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

## 类(class)

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

### 封装权限

公共权限 public,类内可以访问成员,类外可以访问成员

保护权限 protected,类内可以访问成员,类外不可以访问成员 子类可以访问父类中的保护内容

私有权限 private,类内可以访问权限,类外不可以访问成员 子类不可以访问父类中的私有内容

### 构造函数

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
  int x;
  string y;

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

    /*
    如果你不写，编译器会自动创建一个，但是里面是空语句
    Person()
    {
        
    }
    */
};

int main()
{
    Person x_entiy(2);
    /*=》等价写法
    Person x_entiy=2；//显示法
    Person x_entiy = Person(2) //隐式转换法
    */
    Person y_entiy(1,"asd");
    std::cout << y_entiy.y<<endl;
    std::cout << x_entiy.x<<endl;

    std::cin.get();
    return 0;
}

/*输出
Person 构造函数1的调用
Person 构造函数2的调用
asd
2
*/
```

### 静态成员

① 静态成员就是在成员变量和成员函数前加上关键字static，称为静态成员。

② 静态成员分为：

1. 静态成员变量

- 所有对象共享同一份数据  
- 在编译阶段分配内存  
- 类内声明，类外初始化

2. 静态成员函数  

- 所有对象共享同一个函数  
- 静态成员函数只能访问静态成员变量

3. 调用静态成员函数有两种方法：

- 通过对象调用
- 通过类名调用
