- [main函数](#main函数)
- [预处理、编译、汇编、链接](#预处理编译汇编链接)
- [变量](#变量)
- [指针、引用](#指针引用)
- [字符串和字面量](#字符串和字面量)
- [枚举(enum)](#枚举enum)
- [结构体(struct)](#结构体struct)
- [类(class)](#类class)
  - [封装权限](#封装权限)
  - [构造函数](#构造函数)
  - [析构函数](#析构函数)
  - [静态成员](#静态成员)
  - [const修饰成员函数、mutable](#const修饰成员函数mutable)
  - [this指针](#this指针)
  - [符号重载](#符号重载)
    - [加号运算符重载](#加号运算符重载)
    - [左移运算符重载](#左移运算符重载)
  - [继承](#继承)
    - [三种继承改变权限](#三种继承改变权限)
    - [继承后同名函数的处理](#继承后同名函数的处理)
    - [多继承语法](#多继承语法)
    - [菱形继承](#菱形继承)
  - [多态、虚函数](#多态虚函数)
    - [纯虚函数和抽象类](#纯虚函数和抽象类)
  - [隐式转换和显式转换](#隐式转换和显式转换)
  - [拷贝赋值函数](#拷贝赋值函数)
- [new](#new)
  - [1.new和operator new](#1new和operator-new)
  - [new (void\*)](#new-void)
- [栈作用域生存期](#栈作用域生存期)
- [箭头运算符](#箭头运算符)
- [重载](#重载)
- [动态数组(std::vector)](#动态数组stdvector)
- [C++中如何处理多返回值](#c中如何处理多返回值)
  - [结构体](#结构体)
  - [数组](#数组)
  - [vector](#vector)
  - [tuple](#tuple)
  - [pair](#pair)
- [模板](#模板)
  - [template \<class ...Args\>](#template-class-args)
- [size\_t,size\_type, typedef和decltype](#size_tsize_type-typedef和decltype)
- [初始化](#初始化)
  - [聚合初始化](#聚合初始化)
    - [语法](#语法)
- [特殊用途语言特性](#特殊用途语言特性)
  - [宏](#宏)
  - [内联（inline）函数](#内联inline函数)
  - [函数指针](#函数指针)
  - [lambda](#lambda)
  - [智能指针](#智能指针)
    - [unique\_ptr](#unique_ptr)
    - [shared\_ptr](#shared_ptr)
    - [weak\_ptr](#weak_ptr)
  - [static\_cast](#static_cast)
    - [用于原C风格的隐式类型转换](#用于原c风格的隐式类型转换)
    - [静态下行转换](#静态下行转换)
    - [左值转换为右值引用](#左值转换为右值引用)
    - [初始化转换](#初始化转换)
    - [转换为void并丢弃](#转换为void并丢弃)
    - [void\*转换到具体类型](#void转换到具体类型)
    - [8.枚举转int（scoped enum to int）](#8枚举转intscoped-enum-to-int)
    - [int转enum以及enum转为其他enum](#int转enum以及enum转为其他enum)
    - [成员指针的上行转换（pointer to member upcast）](#成员指针的上行转换pointer-to-member-upcast)

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

| 类型            | 含义           | 最小尺寸                       |
| --------------- | -------------- | ------------------------------ |
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

## 字符串和字面量

c++的基本写法是 `char *name ="string"`,或者用数组 `char name[10]={'s','t','r','i','n','g','\0'}`
这种语法下，不可以使用 `+`来尝试连接字符串，因为两个地址不可以相加，应使用 `strcat(a,b);`的函数进行连接。

特殊语法

```c++
//进行换行打印
const char* name1 = "asd\n"
        "asd\n";
const char* name2 = R"(asd
        asd)";

```

合适的方法是用string库,`string name="string"`,这里面涉及 `const char *`的隐式转换
此时,可以使用以下语法

```c++

string a = string("asd")+"asd";
string b = "asd"s+"asd";
//string b = "asd"+"asd";//无效语法

```

## 枚举(enum)

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
    Person x_entiy=2；//显式法
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

### 析构函数

析构函数语法：~类名(){}

1. 析构函数，没有返回值也不写void。
2. 函数名称与类名相同，在名称前加上符号。
3. 析构函数不可以有参数，因此不可以发生重载。
4. 程序在对象销毁前会自动调用析构，无须手动调用，而且只会调用一次。

```c++
#include <iostream>
using namespace std;
#include <string>

class Person
{
public:  //无论是构造函数还是析构函数都是在public作用域下
    Person()
    {
        cout << "Person 构造函数的调用" << endl;
    }
    ~Person()
    {
        cout << "Person 析构函数的调用" << endl;
    }
};

//构造和析构都是必须有的实现，如果我们自己不提供，编译器会提供一个空实现
void test()
{
    Person p;  //创建对象的时候，自动调用构造函数
               //这个对象p是一个局部变量，是在栈上的数据，test01执行完，释放这个对象
}

int main()
{
  
    test01();   // 析构释放时机在test01运行完前，test函数运行完后，里面的对象就被释放了,方便观测
    /*
    方式二：     //创建对象的时候，自动调用构造函数
    Person p;   //只有main函数结束完前，对象要释放掉了，才会调用析构函数，不方便观测
    */

    std::cin.get();
    return 0;

}
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

```c++
#include<iostream>
using namespace std;

class Person
{
public:
    static int m_A;
    int m_B;
      static void func()
    {
        m_A = 100; //静态成员函数可以访问静态成员变量，这个数据是共享的，只有一份，所以不需要区分哪个对象的。                        
        //m_B = 200; //静态成员函数不可以访问非静态成员变量，无法区分到底是哪个对象的m_B属性，非静态成员变量属于特定的对象上面
        std::cout << "static void func调用" << std::endl;
    }
};
//类外初始化
int Person::m_A = 100;
int main()
{
    Person p;
    std::cout << p.m_A << endl;

    Person p2;
    p2.m_A = 200;

    //100 ? 200，共享同一份数据，所以p.m_A为200
    std::cout << p.m_A << endl;
      //通过类名进行访问
    std::cout << Person::m_A << endl;
    std::cin.get();
}
/*输出
100
200
200
*/
```

### const修饰成员函数、mutable

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

### this指针

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

### 符号重载

1. 运算符重载：对已有的运算符重新进行定义，赋予其另一种功能，以适应不同的数据类型。
2. 对于内置的数据类型的表达式的运算符是不可能改变的。

#### 加号运算符重载

```c++
Person operator+(Person &p1, Person &p2)
{
    Person temp;
    temp.m_A = p1.m_A + p2.m_A;
    temp.m_B = p1.m_B + p2.m_B;
    return temp;
}
```

#### 左移运算符重载

```c++
#include <iostream>
using namespace std;

//左移运算符
class Person
{   
private:
    int m_A;
    int m_B;
};
//如果返回类型为void，那么就无法无限追加，也没有办法在后面添加换行符
ostream & operator<<(ostream &cout, Person &p)   
{
    cout << "m_A= " << p.m_A << " m_B=" << p.m_B;
    return cout;
}

int main()
{
    Person p(10,10);

    cout << p << " hello world" << endl;
    std::cin.get();
    return 0;
}

```

### 继承

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

3. 不同的继承方式，父类中的变量被继承后，权限相应的得到了改变，如下图所示。

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

### 多态、虚函数

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

//猫类
class Cat:public Animal
{
public:
    //重写 函数返回值类型、函数名、参数列表都完全相同才叫重写
    void speak()   override//子类virtual,override可写可不写，也可以写 virtual void speak()
    {
        cout << "小猫在说话" << endl;
    }
};

//狗类
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

### 隐式转换和显式转换

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

### 拷贝赋值函数

c++默认提供一个拷贝构造函数，拷贝构造函数的函数签名对同样的类对象的常引用const &。它的作用是内存复制，将other对象的内存浅层拷贝进这些成员变量。形如以下:

```c++
Entity(const Entity& other)//拷贝构造函数
 {
    memcpy(this,&other,sizeof(other));
 }

```

如下代码，a和b是两个独立的变量，它们有不同的内存地址，若将b=3则a仍然是2。在Vector2类中是同样的原理，c.x仍然会是2。若要在堆中使用new关键字来进行分配则复制了指针，e和f两个指针本质上有相同的值(内存地址)，但是如果访问这个内存地址并设为某个值，则会同时影响e和f。

```c++
#include<iostream>
struct Vector2
{
 float x, y;
};

int main()
{
 int a = 5;
 int b = a;

 Vector2 c = { 2,3 };
 Vector2 d = c;
 d.x = 5;

 Vector2* e = new Vector2();
 Vector2* f = e;
 f->x = 2;
 std::cout << f->x<<std::endl;
 std::cout << e->x << std::endl;
 std::cin.get();
}
/*输出
2
2
*/
```

使用C++原始特性写一个字符串类，在有new关键字和指针变量，应自己覆写拷贝函数、析构函数进行深拷贝。不然，两个实例中的指针会都指向同一块内寸，之后在调用析构函数时程序就会崩溃。

使用标准的std::cout来打印字符串，需要重载左移字符串。将运算符的重载函数作为这个类的友元，就可以从函数中访问m_Buffer

```c++
#include<iostream>

class String
{
private:
 char* m_Buffer;
 unsigned int m_Size;
public:
 String(const char* string)
 {
  m_Size = strlen(string);
  m_Buffer = new char[m_Size+1];//+1是为了复制'\0'
  memcpy(m_Buffer, string, m_Size+1);
 }

 ~String()
 {
  delete[] m_Buffer;
 }

 friend std::ostream& operator<<(std::ostream& stream, const String& string);//友元
};

std::ostream& operator<<(std::ostream& stream, const String& string)//重载
{
 stream << string.m_Buffer;
 return stream;
}


int main()
{
 String string = "Cherno";
 std::cout << string << std::endl;

 std::cin.get();
}


```

## new

new其实就是告诉计算机开辟一段新的空间，但是和一般的声明不同的是，new开辟的空间在堆上，而一般声明的变量存放在栈上。通常来说，当在局部函数中new出一段新的空间，该段空间在局部函数调用结束后仍然能够使用，可以用来向主函数传递参数。另外需要注意的是，new的使用格式，new出来的是一段空间的首地址。所以一般需要用指针来存放这段地址

下面两段代码在功能上的区别是前者进行了初始化，后者只分配了空间

```c++

Entity* e = new Entity()；
Entity* e = (Entity*)malloc(sizeof(Entity))；
```

### 1.new和operator new

* new：指我们在C++里通常用到的运算符，比如A* a = new A; 对于new来说，有new和::new之分，前者位于std
* operator new()：指对new的重载形式，它是一个函数，并不是运算符。
* 对于operator new来说，分为全局重载和类重载， =全局重载是void* ::operator new(size_t size)= ，在类中重载形式 void* A::operator new(size_t size)。事实上 =系统默认的全局::operator new(size_t size)也只是调用malloc分配内存= ，并且返回一个void*指针。而构造函数的调用(如果需要)是在=new运算符中完成=的；

### new (void*)

new ((void*)ptr) T1(value);

和new(ptr) T1(value);是等价的操作

* 是一种 **定位new运算符** ，它的作用是在**指定的地址**ptr上创建一个 **T1类型的对象** ，并用value作为 **构造函数的参数** 。
* 这种操作可以 **节省内存分配的时间** ，因为它不需要在堆中寻找足够大的空间，而是直接使用已有的空间作为 **缓冲区** 。这样可以 **提高程序的效率** ，并**避免内存碎片**的产生。
* void*是一种 **空指针** ，它没有关联任何数据类型，可以保存任何类型的地址，并可以转换为任何类型的指针。在这里，它的作用是 **强制类型转换** ，把ptr的原始类型转换为void*类型，以便和new运算符匹配

## 栈作用域生存期

 栈可以被认为是一种数据结构，可以在上面堆叠一些东西。每次在c++中进入一个作用域都是在push栈帧，它不一定非得是将数据push进一个栈帧。可以想象把一本书放入书堆上，在此作用域内（这本书内）声明的变量就像是在书里写东西，一旦作用域结束，将这本书从书堆中拿出来，书中栈里创造的所有对象就会消失。

如果我们想在堆上创建一个类，然后想在离开作用域时销毁它。下面代码我们不用new来创建Entity而是用ScopedPtr，一旦我们超出作用域它就会被销毁，因为ScopedPtr类的对象是在栈上分配的。当e被自动删除时，在析构函数中会delete这个被包装的Entity指针。即使用new来做堆分配。

```c++
#include <iostream>
#include <string>

using namespace std;

class Entity
{
public:
    Entity()
    {
        cout << "initial" << endl;

    }
    ~Entity()
    {
        cout << "del" << endl;

    }
};
class ptr
{
private:
    Entity* p;
public:
    ptr(Entity* e) :
        p(e) {}
    ~ptr()
    {
        delete p;
    }

};
int main()
{
    {
        ptr p(new Entity);
    }
    cin.get();
    return 0;
}
```

## 箭头运算符

<<<<<<< HEAD

=======

>>>>>>> 9cc837a255b128768da7d43a0cfa527cd65ddf77
>>>>>>> 可以使用箭头操作符来获取内存中某个成员变量的偏移量。假设有一个Vector3结构体有三个浮点数分量xyz，若想要找出这个变量在内存中的偏移量，例如x偏移量是0，y是4，z是8。
>>>>>>>
>>>>>>
>>>>>
>>>>
>>>
>>

```c++
#include<iostream>
#include<string>

struct Vector3
{
 float x, y, z;

};

int main()
{
 int offse_x = (int)&((Vector3*)0)->x; 
 //int offse_x = (int)&((Vector3*)nullptr)->x;
 int offse_y = (int)&((Vector3*)0)->y; 
 //int offse_y = (int)&((Vector3*)nullptr)->y;
 int offse_z = (int)&((Vector3*)0)->z; 
 //int offse_z = (int)&((Vector3*)nullptr)->z;
 std::cout << offse_x << std::endl;
 std::cout << offse_y << std::endl;
 std::cout << offse_z << std::endl;


 std::cin.get();
}
<<<<<<< HEAD
```

## 重载

待补

## 动态数组(std::vector)

 C++提供给我们一个叫做Vector的类，这个Vector在std命名空间中，它应该被称为ArrayList，本质上是一个动态数组(不是向量)。在创建动态数组时(Vector)，它没有固定大小(可以给一个特定大小来初始化)。创建Vector后每次往里面添加一个元素，Vector的数组大小会增长。当添加的元素超过Vector数组的大小时，它会在内存中创建一个比第一个大的新数组，把所有东西都复制到这里，然后删除旧的那个。

```c++
#include<iostream>
#include<string>
#include<vector>

struct Vertex
{
 float x, y, z;
};

//输出运算符的重载
std::ostream& operator<<(std::ostream& stream, const Vertex& vertex)
{
 stream << vertex.x << "," << vertex.y << "," << vertex.z;

 return stream;
}

int main()
{
 std::vector<Vertex> vertices;
 std::cin.get();
}


```

注意这里并没有存储一堆vertex指针，实际上只是把vertex存储在一条直线(在一段内存)上。如果是vertex对象则它的内存分配将是一条线上的，而动态数组是内存连续的数组，这意味着它在内存中不是碎片，内容都在一条高速缓存线上。那么如何向vector中添加一些东西，只需要输入vertices.push_back();。因为vector是一个完整的类，所以知道它的大小(vertices.size())。

```c++
int main()
{
 std::vector<Vertex> vertices;
 vertices.push_back({ 1,2,3 });
 vertices.push_back({ 4,5,6 });
 
 for (int i = 0; i < vertices.size(); i++)
 {
  std::cout << vertices[i] << std::endl;
 }
    // for (Vertex& v: vertices)
 // {
 //  std::cout << v << std::endl;
//  }

vertices.clear();//清空
 std::cin.get();
}
```

以下代码打印六次"Copied!"

```c++


#include<iostream>
#include<string>
#include<vector>

struct Vertex
{
 float x, y, z;

 Vertex(float x, float y, float z)
  : x(x), y(y), z(z) {}

    Vertex(const Vertex& vertex)//若是写简单的拷贝构造函数可以不需要初始化成员列表
  : x(vertex.x), y(vertex.y), z(vertex.z)
 {
  std::cout << "Copied!" << std::endl;
 }

};

int main()
{
 std::vector<Vertex> vertices;
 vertices.push_back(Vertex(1,2,3));
 vertices.push_back(Vertex(4,5,6));
 vertices.push_back(Vertex(7,8,9));

 std::cin.get();
}


```

首先，这是因为每次 `vertices.push_back(Vertex(1,2,3));`相当于先创建了一个Vertex，然后把这个Vertex复制给vector，正确的方式是使用 `emplace_back`,创建元素后直接移动给vector

```c++

vertices.emplace_back(1,2,3)
```

其次vector每次增加元素后都会开辟新内存，然后把旧内存的内容复制过去，所以这边反复创建了新元素，正确的做法是在添加元素前预先申请足够的空间

```c++
 vertices.reverse(3)//申请了三个空间
```

## C++中如何处理多返回值

本文是ChernoP52视频的学习笔记。
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

## 模板

```c++
template <typename 形参名, typename 形参名...>     //模板头（模板说明）

返回值类型  函数名（参数列表）                   //函数定义

{

        函数体;

}
```

1. template是声明模板的关键字，告诉编译器开始泛型编程。
2. 尖括号<>中的typename是定义形参的关键字，用来说明其后的形参名为类型参数（模板形参。Typename（建议用）可以用class关键字代替，两者没有区别。
3. 模板形参（类属参数）不能为空（俗成约定用一个大写英文字母表示），且在函数定义部分的参数列表中至少出现一次。与函数形参类似，可以用在函数定义的各个位置：返回值、形参列表和函数体。
4. 函数定义部分：与普通函数定义方式相同，只是参数列表中的数据类型要使用尖括号<>中的模板形参名来说明。当然也可以使用一般的类型参数。

```c++
#include<iostream>
#include<string>

template<typename T>//typename也可以写成class

void Print(T value)
{
 std::cout << value << std::endl;
}

int main()
{
 Print(5);//T替换为int
 Print("Hello");
 Print(5.5f);
 std::cin.get();
}

```

这里看上去是显示地指定类型，其实这个类型是**隐式**地从实际参数中得到的。我们还可以调用Print使用尖括号指定类型。

```c++
Print<int>(5);

```

若我们不写任何东西，完全没有使用Print函数那么它就没有真正存在过。这个Print函数只是一个模板，只有当调用时才会被实际创建。

我们也可以不用类型作为模板参数，作用在类上而不是函数上。我们创建一个在栈上的Array类，里面的数组大小是在编译时确定的，不能直接输入一个变量size之类。

```c++
class Array
{
private:
 int m_Array[size];
};

```

因为这是一个栈分配的数组，所以在编译时就需要知道它。显然我们可以使用动态分配栈内存(alloca)或者其他，但我们只想在栈上创建一个普通的C语言风格的数组。因此size值要在编译时就要知道，而模板会在编译期被评估处理。所以正好将类转换成一个模板，但不用typename作为模板参数。我们可以使用int然后将数量命名为N，这里就不用size而是改成N，最后的public函数返回这个数组的大小。

```c++
#include<iostream>
#include<string>

template<int N>

class Array
{
private:
 int m_Array[N];
public:
 int Getsize() const { return N; }
};

int main()
{
 std::cin.get();
}

```

若不是显示地指定int，想让这个类型是可变的。因此希望能够在编译时指定这个数组实际包含的类型，可以添加另一个模板参数，在数字面前添加这个参数。

```c++
#include<iostream>
#include<string>

template<typename T,int N>

class Array
{
private:
 int T[N];
public:
 int Getsize() const { return N; }
};

int main()
{
 Array<int,4> array;
 std::cin.get();
}

```

### template <class ...Args>

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

## size_t,size_type, typedef和decltype

1. typedef
   系统默认的所有基本类型都可以利用 `typedef` 关键字来重新定义类型名

   ```c++
   typedef double my_double;
   //以下两句的效果是一样的
   double a;
   my_double a;

   ```
2. decltype
   decltype的作用是**选择并返回操作数的数据类型**

   ```c++
   int A;
   //以下两句的效果是一样的
   int B;
   decltype(A) B;
   ```
3. size_t 和 size_type

   - size_t and size_type是为了独立于及其设备而定义的类型；比如在这个电脑上int为2字  节，另一台上电脑是4字节，所以经常使用size_t和size_type而不是 `int unsigned`可以    让程序有更好的移植性。
     size_t是一种全局类型，它的定义如下

     ```c++
     typedef unsigned int size_t
     ```
   - size_type属于容器概念,本质上是一样的,但是size_t是在全局命名空间里，size_type在string里（`string::size_type`）或vector命名空间里（`vector::size_type`）,在使用STL中表明容器长度的时候，我们一般用size_type。

## 初始化

### 聚合初始化

聚合初始化是针对数组或者类类型（通常为结构或者联合）的一种列表初始化形式。类类型（常为 struct 或 union）必须符合下面条件：

- 没有私有或者受保护非静态数据成员
- 没有用户声明的构造函数
- 没有用户提供的构造函数（允许显式预置或弃置的构造函数）
- 没有用户提供、继承或 explicit 构造函数（允许显式预置或弃置的构造数）
- 没有用户声明或者继承的构造函数
- 没有虚、私有或受保护 (C++17 起)基类
- 没有虚拟成员函数
- 无默认成员初始化器(C++11 起)(C++14 前)

#### 语法

```c++

T object = {arg1, arg2, ...};
T object {arg1, arg2, ...};
T object (arg1, arg2, ...);//c++ 20起
```

## 特殊用途语言特性

### 宏

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

### 内联（inline）函数

- 普通函数的缺点：调用函数比求解等价表达式要慢得多。
- `inline`函数可以避免函数调用的开销，可以让编译器在编译时**内联地展开**该函数。
- `inline`函数应该在头文件中定义。

### 函数指针

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

### lambda

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

### 智能指针

智能指针是实现分配内存、释放内存这一过程自动化的一种方式。若使用智能指针，当我们调用new时不需要调用delete，甚至不需要调用new。智能指针本质上是一个原始指针的包装，当创建一个智能指针，它会调用new并为其分配内存，基于这个智能指针的内存会在某一时刻自动释放

#### unique_ptr

 unique_ptr是作用域指针，超出作用域时它会被销毁，然后调用delete。我们不能复制一个unique_ptr，因为如果复制一个unique_ptr会有两个指针，两个unique_ptr指向同一个内存块。如果其中一个死了，它会释放那段内存，而另一个unique_ptr指针就会指向被释放的内存。
要访问智能指针，首先要包括memory头文件。如果想要在特定的作用域下(两个大括号)创建一个unique_ptr来分配Entity，可以调用构造函数然后输入new Entity()。

```c++
//std::unique_ptr<Entity> entity=new Entity();报错，因为unique_ptr是显式的
std::unique_ptr<Entity> entity(new Entity());
entity->Print();//想要调用一个函数只需要通过剪头操作符来访问
```

一个更好的方法是把entity赋值给std::make_unique，主要是因为异常安全。如果构造函数抛出异常，使用make_unique(C++14)会保证最终得到的不是没有引用的悬空指针，从而造成内存泄漏。

```c++
std::unique_ptr<Entity> entity = std::make_unique<Entity>();
entity->Print();
```

查看unique_ptr的定义发现拷贝构造函数和拷贝构造操作符实际上被删除了。
![2023-08-10-13-50-00](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-10-13-50-00.png)

#### shared_ptr

shared_ptr是共享指针，它实现的方式实际上取决于编译器和在编译器中使用的标准库。shared_ptr的工作方式是通过引用计数，引用计数基本上是一种方法，可以跟踪我们的指针有多少个引用，一旦引用计数达到0，它就会被删除。在unique_ptr中不直接调用new的原因是因为异常安全，但是在shared_ptr中有所不同。shared_ptr需要分配另一块内存，叫做控制块，用来存储引用计数。如果创建一个new Entity然后将其传递给shared_ptr构造函数，它必须做两次内存分配：先做一次new Entity的分配，然后是shared_ptr的控制内存块的分配。若使用make_unique就可以把它们组合起来。

```c++
std::shared_ptr<Entity> entity = std::make_shared<Entity>();
```

这里有两个作用域，在外面的作用域中有了e0，里面的作用域中有了sharedEntity，然后把e0赋值给sharedEntity。在27行设置断点按F5运行，再按F10发现Entity被创建了。当里面的作用域死亡时，sharedEntity就会死亡，但是e0还存活并且持有对该Entity的引用，所以这里没有调用析构函数。只有当代码进行到更外层的作用域时，引用都消失，Entity才会被删除。
![2023-08-10-13-51-57](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-10-13-51-57.png)

#### weak_ptr

weak_ptr被称为弱指针，可以和shared_ptr一起使用。它只是像声明其他东西一样声明，可以给它赋值为sharedEntity。这里和之前复制sharedEntity所做的一样，但是这里不会增加引用计数。当我们将一个shared_ptr赋值给另外一个shared_ptr时它理会增加引用计数。但是当把一个shared_ptr赋值给一个weak_ptr时不会增加引用计数。如果不想要Entity的所有权，例如在排序一个Entity列表时不关心它们是否有效，只需要存储一个它们的引用就可以了。我们可能会问weak_ptr底层对象是否还存活，但它不会保持底层对象存活，因为它不会增加引用计数。

```c++
std::weak_ptr<Entity> entity;
```

### static_cast

static_cast是可以使用的最简单的类型转换。它是编译时强制转换。它可以在类型之间进行隐式转换(例如int到float，或指针到void*)，它还可以调用显式转换函数(或隐式转换函数)。

#### 用于原C风格的隐式类型转换

例如float转int

```c++
   float a = 1.3;
    int b = static_cast<int>(a);
    cout<<"b="<<b<<endl;
```

#### 静态下行转换

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

#### 左值转换为右值引用

将左值v0的资源转移到右值引用v2, v2为{1, 2, 3}的右值引用

```
 std::vector<int> v0{1, 2, 3};
    std::vector<int> v2 = static_cast<std::vector<int> &&>(v0);
    std::cout << "2) after move, v0.size() = " << v0.size() << '\n';

//3) after move, v0.size() = 0
```

#### 初始化转换

在变量初始化期间就对初始化数据进行类型转换

```
int n = static_cast<int>(3.14);
std::cout << "4) n = " << n << '\n';
std::vector<int> v = static_cast<std::vector<int>>(10);
std::cout << "4) v.size() = " << v.size() << '\n';
//4) n = 3
//4) v.size() = 10
```

```

```

#### 转换为void并丢弃

如果 new type为void类型，static\_cast将会在计算表达式的值之后丢弃这个值，无法使用变量接到这个值。

```c++
static_cast<void>(v2.size());  
int a =  static_cast<void>(v2.size());  //error,void value not ignored as it ought to be
```

#### void\*转换到具体类型

static\_cast可以提取void\*类型中的值

```c++
  void *nv = &n;

  int *ni = static_cast<int *>(nv);

  std::cout << "6) *ni = " << *ni << '\n';

  //6) *ni = 3
```

#### 8.枚举转int（scoped enum to int）

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
   std::cout << "7) " << two << '\n';
```

#### int转enum以及enum转为其他enum

```c++
enum class E
{
    ONE = 1,
    TWO,
    THREE
};
enum EU
{
    ONE = 1,
    TWO,
    THREE
};


   E e2 = static_cast<E>(two);
   [[maybe_unused]] EU eu = static_cast<EU>(e2);
```

#### 成员指针的上行转换（pointer to member upcast）

将D内的成员变量的指针转换为B类型的成员变量指针

```c++
   int D::*pm = &D::m;
   std::cout << "10) " << br.*static_cast<int B::*>(pm) << '\n';
   //10) 42
```
