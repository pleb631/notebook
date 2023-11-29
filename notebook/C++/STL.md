[toc]

# 容器

## string

- string是表示字符串的字符串类。
- 该类的接口与常规容器接口基本相同，再添加了一些专门用来操作string的常规操作。
- string在底层实际是：basic_string模板类的别名，typedef basic_string<char, char_traits, alloactor> string。
- 不能操作多字节或者变长字符的序列。

1. 构造函数

| constructor函数名称          | 功能说明                         |
| ---------------------------- | -------------------------------- |
| string()                     | 构造空的string类对象，即空字符串 |
| `string(const char* s)`    | 用C-string来构造string对象       |
| `string(size_t n, char c)` | string类对象中包含n个字符c       |
| `string(const string& s)`  | 拷贝构造函数                     |

2. string类对象的容量操作

| 函数名称           | 功能说明                                             |
| ------------------ | ---------------------------------------------------- |
| size               | 返回字符串字符长度                                   |
| length             | 返回字符串有效字符长度                               |
| capacity           | 返回空间总大小                                       |
| empty              | 判断字符串是否为空串，是返回true，反之返回false      |
| clear              | 清空有效字符                                         |
| reserve            | 为字符串预留空间                                     |
| resize(n,c)        | 将有效字符个数改为n个，多出的空间用字符c填充         |
| substr(i,j)        | 提取第[i,j)的字符，返回值string                      |
| s.substr(pos, len) | 从pos开始len个字符                                   |
| s.substr(i)        | 从i到最后                                            |
| c_str()            | 返回const char* ,可以配合strcpy(ptr, s.c_str());使用 |

3. string类对象的访问及遍历操作

| 函数名称               | 功能说明                                                         |
| ---------------------- | ---------------------------------------------------------------- |
| operator\[\]           | 返回对应位置字符，const string类对象调用                         |
| begin + end            | begin获取一个字符迭代器，end获取最后一个字符下一个位置的迭代器   |
| rbegin + rend          | rbegin获取一个字符迭代器，rend获取最后一个字符下一个位置的迭代器 |
| 范围for(auto s:string) | C++支持的更简洁的for遍历模式                                     |
| operator\""s           | 转换字符数组字面量为 basic_string                                |

4. 非成员函数

| 函数                         | 功能说明                   |
| ---------------------------- | -------------------------- |
| operator+                    | 返回一个相加后的字符串     |
| operator<<                   | 输出运算符重载             |
| operator>>                   | 输入运算符重载             |
| getline(std::cin,stringname) | 输入一行（遇到空格不停止） |

```c++
  //转译字符串 str 中的有符号整数值。
  int       stoi( const std::string& str, std::size_t* pos = 0, int base = 10 );
  long      stol( const std::string& str, std::size_t* pos = 0, int base = 10 );
  long long stoll( const std::string& str, std::size_t* pos = 0, int base = 10 );

  //转译字符串 str 中的无符号整数值
  unsigned long      stoul( const std::string& str, std::size_t* pos = 0, int base = 10 );
  unsigned long long stoull( const std::string& str, std::size_t* pos = 0, int base = 10 );

  //转译 string str 中的浮点值。
  float       stof( const std::string& str, std::size_t* pos = 0 );
  double      stod( const std::string& str, std::size_t* pos = 0 );
  long double stold( const std::string& str, std::size_t* pos = 0 );

  //转换为字符串,T必须是上面格式的其中一种
  template< class T >
  std::string to_string( T value );

```

## 顺序容器

![2023-11-17-10-39-40](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-11-17-10-39-40.png)

| 函数成员         | 函数功能                                                                               | array&lt;T,N&gt; | vector&lt;T&gt; | deque&lt;T&gt; |
| ---------------- | -------------------------------------------------------------------------------------- | ---------------- | --------------- | -------------- |
| begin()          | 返回指向容器中第一个元素的迭代器。                                                     | 是               | 是              | 是             |
| end()            | 返回指向容器最后一个元素所在位置后一个位置的迭代器，通常和 begin() 结合使用。          | 是               | 是              | 是             |
| rbegin()         | 返回指向最后一个元素的迭代器。                                                         | 是               | 是              | 是             |
| rend()           | 返回指向第一个元素所在位置前一个位置的迭代器。                                         | 是               | 是              | 是             |
| cbegin()         | 和&nbsp;begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。      | 是               | 是              | 是             |
| cend()           | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。             | 是               | 是              | 是             |
| crbegin()        | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。          | 是               | 是              | 是             |
| crend()          | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。            | 是               | 是              | 是             |
| assign()         | 用新元素替换原有内容。                                                                 | -                | 是              | 是             |
| operator=()      | 复制同类型容器的元素，或者用初始化列表替换现有内容。                                   | 是               | 是              | 是             |
| size()           | 返回实际元素个数。                                                                     | 是               | 是              | 是             |
| max_size()       | 返回元素个数的最大值。这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。 | 是               | 是              | 是             |
| capacity()       | 返回当前容量。                                                                         | -                | 是              | -              |
| empty()          | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。                        | 是               | 是              | 是             |
| resize()         | 改变实际元素的个数。                                                                   | -                | 是              | 是             |
| shrink _to_fit() | 将内存减少到等于当前元素实际所使用的大小。                                             | -                | 是              | 是             |
| front()          | 返回第一个元素的引用。                                                                 | 是               | 是              | 是             |
| back()           | 返回最后一个元素的引用。                                                               | 是               | 是              | 是             |
| operator[]()     | 使用索引访问元素。                                                                     | 是               | 是              | 是             |
| at()             | 使用经过边界检査的索引访问元素。                                                       | 是               | 是              | 是             |
| push_back()      | 在序列的尾部添加一个元素。                                                             | -                | 是              | 是             |
| insert()         | 在指定的位置插入一个或多个元素。                                                       | -                | 是              | 是             |
| emplace()        | 在指定的位置直接生成一个元素。                                                         | -                | 是              | 是             |
| emplace_back()   | 在序列尾部生成一个元素。                                                               | -                | 是              | 是             |
| pop_back()       | 移出序列尾部的元素。                                                                   | -                | 是              | 是             |
| erase()          | 移出一个元素或一段元素。                                                               | -                | 是              | 是             |
| clear()          | 移出所有的元素，容器大小变为 0。                                                       | -                | 是              | 是             |
| swap()           | 交换两个容器的所有元素。                                                               | 是               | 是              | 是             |
| data()           | 返回指向容器中第一个元素的指针。                                                       | 是               | 是              | -              |

| 函数成员        | 函数功能                                                                                      | list&lt;T&gt; | forward_list&lt;T&gt; |
| --------------- | --------------------------------------------------------------------------------------------- | ------------- | --------------------- |
| begin()         | 返回指向容器中第一个元素的迭代器。                                                            | 是            | 是                    |
| end()           | 返回指向容器最后一个元素所在位置后一个位置的迭代器。                                          | 是            | 是                    |
| rbegin()        | 返回指向最后一个元素的迭代器。                                                                | 是            | -                     |
| rend()          | 返回指向第一个元素所在位置前一个位置的迭代器。                                                | 是            | -                     |
| cbegin()        | 和 begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。                  | 是            | 是                    |
| before_begin()  | 返回指向第一个元素前一个位置的迭代器。                                                        | -             | 是                    |
| cbefore_begin() | 和 before_begin() 功能相同，只不过在其基础上，增加了 const 属性，即不能用该指针修改元素的值。 | -             | 是                    |
| cend()          | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。                    | 是            | 是                    |
| crbegin()       | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。                 | 是            | -                     |
| crend()         | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。                   | 是            | -                     |
| assign()        | 用新元素替换原有内容。                                                                        | 是            | 是                    |
| operator=()     | 复制同类型容器的元素，或者用初始化列表替换现有内容。                                          | 是            | 是                    |
| size()          | 返回实际元素个数。                                                                            | 是            | -                     |
| max_size()      | 返回元素个数的最大值，这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。        | 是            | 是                    |
| resize()        | 改变实际元素的个数。                                                                          | 是            | 是                    |
| empty()         | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。                               | 是            | 是                    |
| front()         | 返回容器中第一个元素的引用。                                                                  | 是            | 是                    |
| back()          | 返回容器中最后一个元素的引用。                                                                | 是            | -                     |
| push_back()     | 在序列的尾部添加一个元素。                                                                    | 是            | -                     |
| push_front()    | 在序列的起始位置添加一个元素。                                                                | 是            | 是                    |
| emplace()       | 在指定位置直接生成一个元素。                                                                  | 是            | -                     |
| emplace_after() | 在指定位置的后面直接生成一个元素。                                                            | -             | 是                    |
| emplace_back()  | 在序列尾部生成一个元素。                                                                      | 是            | -                     |
| cmplacc_front() | 在序列的起始位生成一个元索。                                                                  | 是            | 是                    |
| insert()        | 在指定的位置插入一个或多个元素。                                                              | 是            | -                     |
| insert_after()  | 在指定位置的后面插入一个或多个元素。                                                          | -             | 是                    |
| pop_back()      | 移除序列尾部的元素。                                                                          | 是            | -                     |
| pop_front()     | 移除序列头部的元素。                                                                          | 是            | 是                    |
| reverse()       | 反转容器中某一段的元素。                                                                      | 是            | 是                    |
| erase()         | 移除指定位置的一个元素或一段元素。                                                            | 是            | -                     |
| erase_after()   | 移除指定位置后面的一个元素或一段元素。                                                        | -             | 是                    |
| remove()        | 移除所有和参数匹配的元素。                                                                    | 是            | 是                    |
| remove_if()     | 移除满足一元函数条件的所有元素。                                                              | 是            | 是                    |
| unique()        | 移除所有连续重复的元素。                                                                      | 是            | 是                    |
| clear()         | 移除所有的元素，容器大小变为 0。                                                              | 是            | 是                    |
| swap()          | 交换两个容器的所有元素。                                                                      | 是            | 是                    |
| sort()          | 对元素进行排序。                                                                              | 是            | 是                    |
| merge()         | 合并两个有序容器。                                                                            | 是            | 是                    |
| splice()        | 移动指定位置前面的所有元素到另一个同类型的 list 中。                                          | 是            | -                     |
| splice_after()  | 移动指定位置后面的所有元素到另一个同类型的 list 中。                                          | -             | 是                    |

### array

#### 介绍

array 容器是 C++ 11 标准中新增的序列容器。它是封装固定大小数组的容器。简单地理解，它就是在 C++ 普通数组的基础上，添加了一些成员函数和全局函数的结构体。在使用上，它比普通数组更安全，且效率并没有因此变差。它不会自动退化成 T* 。它能作为聚合类型聚合初始化。

和其它容器不同，**array 容器的大小是固定的**，无法动态的扩展或收缩，这也就意味着，在使用该容器的过程无法借由增加或移除元素而改变其大小，它只允许访问或者替换存储的元素。

array 容器以类模板的形式定义在 `<array>` 头文件，并位于命名空间 std 中，如下所示：

```c++
namespace std{
    template <typename T, size_t N>  
    class array;
    }
```

因此，在使用该容器之前，代码中需引入 `<array>` 头文件，并默认使用 std 命令空间，如下所示：

```c++
#include <array>
using namespace std;
```

在 array<T,N> 类模板中，T 用于指明容器中的存储的具体数据类型，N 用于指明容器的大小，需要注意的是，这里的 N 必须是常量，不能用变量表示。

array 容器**遵循[聚合初始化](c++.md#初始化#聚合初始化)的规则初始化** ：

```c++
std::array<double, 10> values;
std::array<double, 10> values {};
std::array<double, 10> values {0.5,1.0,1.5,,2.0};
```

array 容器不会做默认初始化操作，所以不初始化时，各个元素的值是不确定的。

可以看到，如果初始化了前 4 个元素，剩余的元素都会被初始化为 0.0。下图说明了这一点。

![2023-08-11-16-42-42](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-08-11-16-42-42.png)

在 `<array>` 头文件中还重载了 get() 全局函数，该重载函数的功能是访问容器中指定的元素，并返回该元素的引用。

> 正是由于 array 容器中包含了 at() 这样的成员函数，使得操作元素时比普通数组更安全。

例如代码演示了一部分成员函数的用法和功能：

```c++
#include <iostream>
#include <array>
using namespace std;

int main(){    
    std::array<int, 4> values{};        
    for (int i = 0; i < values.size(); i++)
     {        
        values.at(i) = i;    
     }        
     cout << get<3>(values) << endl;
     if (!values.empty()) 
     {        
        for (auto val = values.begin(); val < values.end(); val++) 
        {            
            cout << *val << " ";        
        }    
    }
}
```

注意，代码中的 auto 关键字，可以使编译器自动判定变量的类型。运行这段代码，输出结果为：

3
0 1 2 3

#### api

| 隐式定义的成员函数   |                                                                                |
| -------------------- | ------------------------------------------------------------------------------ |
| (构造函数)(隐式声明) | 遵循聚合初始化的规则初始化 array （注意默认初始化可以导致非类的 T 的不确定值） |
| (析构函数)(隐式声明) | 销毁 array 的每个元素                                                          |
| operator=(隐式声明)  | 以来自另一 array 的每个元素重写 array 的对应元素                               |
| (公开成员函数)       |                                                                                |

- 元素访问

  ```c++

  // 类模板 array
  template<class T, size_t N> struct array;

  //std::array<int,6> data = { 1, 2, 4, 5, 5, 6 };
  //元素访问
  reference at( size_type pos );
  data.at(1);

  //访问指定的元素，同时进行越界检查
  reference operator[]( size_type pos );
  data[1];

  //访问第一个元素
  reference front();

  //访问最后一个元素
  reference back();

  //返回指向内存中数组第一个元素的指针
  T* data() noexcept;

  ```

- 迭代器

  ```c++
  //返回返回指向起始的迭代器
  iterator begin() noexcept;
  const_iterator begin() const noexcept;
  const_iterator cbegin() const noexcept;

  //返回指向 array 末元素后一元素的迭代器。
  //此元素表现为占位符；试图访问它导致未定义行为。
  iterator end() noexcept;
  const_iterator end() const noexcept;
  const_iterator cend() const noexcept;

  //返回指向逆向 array 首元素的逆向迭代器。它对应非逆向 array 的末元素。若 array 为空，则返回的迭代器等于 rend() 。
  reverse_iterator rbegin() noexcept;
  const_reverse_iterator rbegin() const noexcept;
  const_reverse_iterator crbegin() const noexcept;

  //返回指向逆向 array 末元素后一元素的逆向迭代器。它对应非逆向 array 首元素的前一元素。此元素表现为占位符，试图访问它导致未定义行为。
  reverse_iterator rend() noexcept;
  const_reverse_iterator rend() const noexcept;
  const_reverse_iterator rend() const noexcept;
  ```

- 容量

  ```c++
  //检查容器是否无元素，即是否 begin() == end()
  constexpr bool empty() const noexcept;

  //返回容器中的元素数，即 std::distance(begin(), end())
  constexpr size_type size() const noexcept;

  //返回根据系统或库实现限制的容器可保有的元素最大数量，即对于最大容器的 std::distance(begin(), end())
  constexpr size_type max_size() const noexcept;
  ```

- 操作

  ```c++

  //将定值 value 赋给容器中的所有元素。
  void fill( const T& value );

  //将容器内容与 other 的内容交换。不导致迭代器和引用关联到别的容器。
  void swap( array& other ) noexcept(/* see below */);
  ```

- 非成员函数

  ```c++
  std::get(std::array)
  std::swap(std::array)
  to_array
  ```

### vector

#### vector介绍

vector和 array 容器非常类似，都可以看做是对C++普通数组的“升级版”。不同之处在于，array 实现的是静态数组（容量固定的数组），而 vector 实现的是一个动态数组，即可以进行元素的插入和删除，vector 的存储是自动管理的，按需扩张收缩。 vector 通常占用多于静态数组的空间，因为要分配更多内存以管理将来的增长。 vector 所用的方式不在每次插入元素时，而只在额外内存耗尽时重分配

vector 上的常见操作复杂度（效率）如下：

- 随机访问——常数 O(1)
- 在末尾插入或移除元素——均摊常数 O(1)
- 插入或移除元素——与到 vector 结尾的距离成线性 O(n)

#### 创建vector容器的几种方式

创建 vector 容器的方式有很多，大致可分为以下几种。

1. 如下代码展示了如何创建存储 double 类型元素的一个 vector 容器：

   ```c++
   std::vector<double> values;
   ```

   注意，这是一个空的 vector 容器，因为容器中没有元素，所以没有为其分配空间。当添加第一个元素（比如使用 push\_back () 函数）时，vector 会自动分配内存。

   在创建好空容器的基础上，还可以像下面这样通过调用 reserve    () 成员函数来增加容器的容量：

   ```c++
   values.reserve(20);
   ```

   这样就设置了容器的内存分配，即至少可以容纳 20 个元素。注意，如果 vector 的容量在执行此语句之前，已经大于或等于  20 个元素，那么这条语句什么也不做；另外，调用 reserve()  不会影响已存储的元素，也不会生成任何元素，即 values 容器 内此时仍然没有任何元素。

   > 还需注意的是，如果调用 reserve() 来增加容器容量，之前创   建好的任何迭代器（例如开始迭代器和结束迭代器）都可能会失效，这是因为，为了增加容器的容量，vector\<T> 容器的元素可   能已经被复制或移到了新的内存地址。所以后续再使用这些迭代器 时，最好重新生成一下。
   >
2. 除了创建空 vector 容器外，还可以在创建的同时指定初始值以及元素个数，比如：

   ```c++
   std::vector<int> primes {2, 3, 5, 7, 11, 13, 17, 19};
   ```

   这样就创建了一个含有 8 个素数的 vector 容器。
3. 在创建 vector 容器时，也可以指定元素个数：

   ```c++
   std::vector<double> values(20);
   ```

   如此，values 容器开始时就有 20 个元素，它们的默认初始值都为 0。

   > 注意，圆括号 () 和大括号 {} 是有区别的，前者（例如    (20) ）表示元素的个数，而后者（例如 {20} ） 则表示     vector 容器中只有一个元素 20。
   >

   如果不想用 0 作为默认值，也可以指定一个其它值，例如：

   ```c++
   std::vector<double> values(20, 1.0);
   ```

   第二个参数指定了所有元素的初始值，因此这 20 个元素的值都是 1.0。值得一提的是，圆括号 () 中的 2 个参数，既可以是常量，也可以用变量来表示，例如：

   ```c++
   int num=20;double value =1.0;
   std::vector<double>    values(num, value);
   ```

4. 通过存储元素类型相同的其它 vector 容器，也可以创建新 的 vector 容器，例如：

   ```c++
   std::vector<char> value1(5, 'c');   
   std::vector<char> value2(value1);
   ```

   由此，value2 容器中也具有 5 个字符 'c'。在此基础上，如果不想复制其它容器中所有的元素，可以用一对指针或者迭代器来指定初始值的范围，例如：

   ```c++
   int array[]={1,2,3};
   std::vector<int>values(array,array+2);
   //values 将保存{1,2}
   std::vector<int> value1{1,2,3,4,5};std::vector<int> value2(std::begin(value1),std::begin(value1)+3);
   //value2保存{1,2,3}
   ```

#### api

- 构造函数、复制函数

  ```c++
  template<class T, class Allocator = allocator<T>> class vector;

  // 默认构造函数。构造拥有默认构造的分配器的空容器。
  vector()
  //构造拥有给定分配器 alloc 的空容器
  explicit vector( const Allocator& alloc );

  //构造拥有 count 个有值 value 的元素的容器。
  vector(size_type count,const T& value,const Allocator& alloc = Allocator());

  //构造拥有个 count 默认插入的 T 实例的容器。不进行复制。
  explicit vector( size_type count, const Allocator& alloc = Allocator() );

  //
  //构造拥有范围 [first, last) 内容的容器。
  template<class InputIt>
  vector(InputIt first, InputIt last,
      const Allocator& alloc = Allocator() );
  //

  //复制构造函数。构造拥有 other 内容的容器
  vector( const vector& other);

  //构造拥有 other 内容的容器，以 alloc 为分配器。
  vector( const vector& other, const Allocator& alloc );

  // 移动构造函数。用移动语义构造拥有 other 内容的容器。分配器通过属于 other 的分配器移动构造获得。移动后，保证 other 为 empty() 。
  vector( vector&& other );

  //  有分配器扩展的移动构造函数。以 alloc 为新容器的分配器，从 other 移动内容；若 alloc != other.get_allocator() ，则它导致逐元素移动。（该情况下，移动后不保证 other 为空）
  vector( vector&& other, const Allocator& alloc );

  //构造拥有 initializer_list init 内容的容器。
  vector( std::initializer_list<T> init,const Allocator& alloc = Allocator() );
  ```

- assign

  ```c++
  //分配
  //以 count 份 value 的副本替换内容。
  void assign( size_type count, const T& value );

  //以范围 [first, last) 中元素的副本替换内容。若任一参数是指向 *this 中的迭代器则行为未定义。
  template< class InputIt >
  void assign( InputIt first, InputIt last );
  //

  //以来自 initializer_list ilist 的元素替换内容。
  void assign( std::initializer_list<T> ilist );

  ```

- operator=

  ```c++
  // 复制赋值运算符。以 other 的副本替换内容
  vector& operator=( const vector& other );

  //移动赋值运算符
  vector& operator=( vector&& other );

  //以 initializer_list ilist 所标识者替换内容。
  vector& operator=( std::initializer_list<T> ilist );

  ```

- 元素访问

  ```c++

  // std::vector<int> data = { 1, 2, 4, 5, 5, 6 };
  //元素访问
  reference at( size_type pos );
  //data.at(1);

  //访问指定的元素，同时进行越界检查
  reference operator[]( size_type pos );
  //data[1];

  //访问第一个元素
  reference front();

  //访问最后一个元素
  reference back();

  //返回指向内存中数组第一个元素的指针
  T* data() noexcept;

  ```

- 迭代器

  ```c++
  //返回返回指向起始的迭代器
  iterator begin() noexcept;
  const_iterator begin() const noexcept;
  const_iterator cbegin() const noexcept;

  //返回指向 array 末元素后一元素的迭代器。
  //此元素表现为占位符；试图访问它导致未定义行为。
  iterator end() noexcept;
  const_iterator end() const noexcept;
  const_iterator cend() const noexcept;

  //返回指向逆向 array 首元素的逆向迭代器。它对应非逆向 array 的末元素。若 array 为空，则返回的迭代器等于 rend() 。
  reverse_iterator rbegin() noexcept;
  const_reverse_iterator rbegin() const noexcept;
  const_reverse_iterator crbegin() const noexcept;

  //返回指向逆向 array 末元素后一元素的逆向迭代器。它对应非逆向 array 首元素的前一元素。此元素表现为占位符，试图访问它导致未定义行为。
  reverse_iterator rend() noexcept;
  const_reverse_iterator rend() const noexcept;
  const_reverse_iterator rend() const noexcept;

  ```

- 容量

  ```c++
  //检查容器是否无元素，即是否 begin() == end()
  constexpr bool empty() const noexcept;

  //返回容器中的元素数，即 std::distance(begin(), end())
  constexpr size_type size() const noexcept;

  //返回根据系统或库实现限制的容器可保有的元素最大数量，即对于最大容器的 std::distance(begin(), end())
  constexpr size_type max_size() const noexcept;

  //增加 vector 的容量到大于或等于new_cap的值。若 new_cap 大于当前的 capacity() ，则分配新存储，否则该方法不做任何事。reserve() 不更改 vector 的 size。若发生重分配，则所有迭代器，包含尾后迭代器，和所有到元素的引用都被非法化
  void reserve( size_type new_cap );

  //返回容器当前已为之分配空间的元素数。
  size_type capacity() const noexcept;

  //请求移除未使用的容量。它是减少 capacity() 到 size()非强制性请求,若发生重分配，则所有迭代器，包含尾后迭代器，和所有到元素的引用都被非法化
  void shrink_to_fit();
  ```

- 修改

  ```c++
  //从容器擦除所有元素。此调用后 size() 返回零。非法化任何指代所含元素的引用、指针或迭代器。任何尾后迭代器亦被非法化。  
  void clear() noexcept;

  //将内容与 other 的交换。不在单个元素上调用任何移动、复制或交换操作。
  void swap( vector& other );

  //
  //insert
  // 在 pos 前插入 value
  iterator insert( const_iterator pos, const T& value );

  iterator insert( const_iterator pos, T&& value );

  //在 pos 前插入 value 的 count 个副本
  iterator insert( const_iterator pos, size_type count, const T& value );

  //在 pos 前插入来自范围 [first, last) 的元素。
  template< class InputIt >
  iterator insert( const_iterator pos, InputIt first, InputIt last );

  //在 pos 前插入来自 initializer_list ilist 的元素。
  iterator insert( const_iterator pos, std::initializer_list<T> ilist );
  //
  //

  //直接于 pos 前插入元素到容器中。
  iterator emplace( const_iterator pos, Args&&... args );

  //从容器擦除指定位置的元素。函数擦除的最后一个元素后跟的元素
  iterator erase( const_iterator pos );

  //移除范围 [first; last) 中的元素。左闭右开
  iterator erase( const_iterator first, const_iterator last );

  //初始化新元素为 value 的副本。
  void push_back( const T& value );

  // 移动 value 进新元素。
  void push_back( T&& value );

  //添加新元素到容器尾
  template< class... Args >
  void emplace_back( Args&&... args );

  //移除容器的末元素。
  void pop_back();

  //重设容器大小以容纳 count 个元素。
  //若当前大小大于 count ，则减小容器为其首 count 个元素。若当前大小小于 count ，
  //1. 则后附额外的默认插入的元素
  void resize( size_type count );
  //2.则后附额外的 value 的副本
  void resize( size_type count, T value = T() );

  //
  void swap( vector& other );

  ```

### deque

std::deque （ double-ended queue ，双端队列）是有下标顺序容器，它允许在其首尾两段快速插入及删除。另外，在 deque 任一端插入或删除不会非法化指向其余元素的指针或引用。

与 std::vector 相反， deque 的元素不是相接存储的：典型实现用单独分配的固定大小数组的序列，外加额外的登记，这表示下标访问必须进行二次指针解引用，与之相比 vector 的下标访问只进行一次。

deque 的存储按需自动扩展及收缩。扩张 deque 比扩张 std::vector 更优，因为它不涉及到复制既存元素到新内存位置。另一方面， deque 典型地拥有较大的最小内存开销；只保有一个元素的 deque 必须分配其整个内部数组（例如 64 位 libstdc++ 上为对象大小 8 倍； 64 位 libc++ 上为对象大小 16 倍或 4096 字节的较大者）。

deque 上常见操作的复杂度（效率）如下：

随机访问——常数 O(1)
在结尾或起始插入或移除元素——常数 O(1)
插入或移除元素——线性 O(n)

### list

std::list 是支持常数时间从容器任何位置插入和移除元素的容器。不支持快速随机访问。它通常实现为双向链表。与 std::forward_list 相比，此容器提供双向迭代但在空间上效率稍低。

在 list 内或在数个 list 间添加、移除和移动元素不会非法化迭代器或引用。迭代器仅在对应元素被删除时非法化。

### forward_list

std::forward_list 是支持从容器中的任何位置快速插入和移除元素的容器。不支持快速随机访问。它实现为单链表，且实质上与其在 C 中实现相比无任何开销。与 std::list 相比，此容器在不需要双向迭代时提供更有效地利用空间的存储。

在链表内或跨数个链表添加、移除和移动元素，不会非法化当前指代链表中其他元素的迭代器。然而，在从链表移除元素（通过 erase_after ）时，指代对应元素的迭代器或引用会被非法化。

### std::set

```c++
template<
    class Key,
    class Compare = std::less<Key>,
    class Allocator = std::allocator<Key>
> class set;
std::set 是关联容器，含有 Key 类型对象的已排序集。用比较函数 比较 (Compare) 进行排序。搜索、移除和插入拥有对数复杂度。 set 通常以红黑树实现。

在每个标准库使用比较 (Compare) 概念的场所，用等价关系确定唯一性。不精确地说，若二个对象 a 与 b 相互间既不比较大于亦不比较小于： !comp(a, b) && !comp(b, a) ，则认为它们等价。
```

#### api

- 构造函数
  ```c++
  //默认构造函数
  set();
  explicit set( const Compare& comp,
              const Allocator& alloc = Allocator() );
  explicit set( const Allocator& alloc );
  
  //范围构造函数。构造拥有范围 [first, last) 内容的容器。若范围中的多个元素拥有比较等价的关键，则插入哪个元素是未指定的
  template< class InputIt >
  set( InputIt first, InputIt last,
     const Compare& comp = Compare(),
     const Allocator& alloc = Allocator() );
  
  // 复制构造
  set( const set& other );
  set( const set& other, const Allocator& alloc );

  //移动构造
  set( set&& other );
  set( set&& other, const Allocator& alloc );

  //initializer_list 构造函数。构造拥有 initializer_list init 内容的容器。若范围中的多个元素拥有比较等价的关键，则插入哪个元素是未指定的
  set( std::initializer_list<value_type> init,
     const Compare& comp = Compare(),
     const Allocator& alloc = Allocator() );
     ```
- 修改

  ```c++
  //插入 value
  std::pair<iterator,bool> insert( value_type&& value );

  //插入来自范围 [first, last) 的元素。 若范围中的多个元素拥有比较等价的关键，则插入哪个元素是未指定的
  template< class InputIt >
  void insert( InputIt first, InputIt last );

  //插入来自 initializer_list ilist 的元素
  void insert( std::initializer_list<value_type> ilist );


  //插入 value 到尽可能接近，正好前于(C++11 起) hint 的位置。
  iterator insert( iterator hint, const value_type& value );


  //若容器中无拥有该关键的元素，则插入以给定的 args 原位构造的新元素到容器。细心地使用 emplace 允许在构造新元素的同时避免不必要的复制或移动操作。 准确地以与提供给 emplace 者相同的参数，通过 std::forward<Args>(args)... 转发调用新元素的构造函数。 即使容器中已有拥有该关键的元素，也可能构造元素，该情况下新构造的元素将被立即销毁。
  template< class... Args >
  std::pair<iterator,bool> emplace( Args&&... args );

  
  //插入新元素到容器中尽可能接近于恰在 hint 前的位置。原位构造元素，即不进行复制或移动操作。以提供给函数的参数准确相同者，以 std::forward<Args>(args)... 转发调用元素的构造函数。没有迭代器或引用被非法化。
  template <class... Args>
  iterator emplace_hint( const_iterator hint, Args&&... args );


  //将内容与 other 的交换
  void swap( set& other );
  ```


- 查找

  ```c++
  //返回拥有关键比较等价于指定参数的元素数，因为此容器不允许重复故为 1 或 0。
  size_type count( const Key& key ) const;

  template< class K >
  size_type count( const K& x ) const;

  //寻找键等于 key 的的元素。
  iterator find( const Key& key );
  // 寻找键比较等价于值 x 的元素
  template< class K > iterator find( const K& x );

  //返回容器中所有拥有给定关键的元素范围。范围以二个迭代器定义，一个指向首个不小于 key 的元素，另一个指向首个大于 key 的元素。首个迭代器可以换用 lower_bound() 获得，而第二迭代器可换用 upper_bound() 获得
  //比较关键与 key
  std::pair<iterator,iterator> equal_range( const Key& key );
  // 比较关键与值 x 
  template< class K >
  std::pair<iterator,iterator> equal_range( const K& x );


  //返回指向首个不小于 key 的元素的迭代器。
  iterator lower_bound( const Key& key );
  //返回指向首个比较不小于值 x 的元素的迭代器
  template< class K >
  iterator lower_bound(const K& x);


  //返回指向首个大于 key 的元素的迭代器。
  iterator upper_bound( const Key& key );
  //返回指向首个比较大于值 x 的元素的迭代器
  template< class K >
  iterator upper_bound( const K& x );
  ```

#### 示例

自定义比较函数的set

```c++
#include <iostream>
#include <set>
using namespace std;
struct song
{
    int m_id;
    int m_hot;
    song(int id,int hot)
    {

        this->m_id = id;
        this->m_hot = hot;
    }
    /*
    bool operator<(const struct song & right)const   //重载<运算符
    {
        if(this->m_id == right.m_id)     //根据id去重
            return false;
        else
        {
            if(this->m_hot != right.m_hot)
            {
                return this->m_hot > right.m_hot;      //降序
            }
            else
            {
                return this->m_id > right.m_id;
            }
        }
    }
    */
};
struct comp
{
    bool operator()(struct song left,struct song  right)  //重载（）运算符
    {

        if(left.m_id == right.m_id)     //根据id去重
            return false;
        else
        {
            if(left.m_hot != right.m_hot)
            {
                return left.m_hot > right.m_hot;      //降序
            }
            else
            {
                return left.m_id > right.m_id;
            }

        }
    }

};
void main()
{
    std::set<song,comp> mySet;      //
    //std::set<song> mySet; //重载函数写在struct里面时
    song s1(10,100);
    song s2(20,200);
    song s3(20,300);
    song s4(30,200);
    mySet.insert(s1);    //插入s1
    mySet.insert(s2);    //插入s2
    mySet.insert(s3);    //s3和s2的id相同，不插入
    mySet.insert(s4);    //插入s4
    for(auto it:mySet)
    {
        std::cout<<"id:"<<it.m_id<<",hot:"<<it.m_hot<<std::endl;
    }
    std::cout<<"end"<<std::endl;
};

```

### unordered_map

#### 介绍

- unordered_map是一个将key和value关联起来的容器，它可以高效的根据单个key值查找对应的value。
- key值应该是唯一的，key和value的数据类型可以不相同。
- unordered_map存储元素时是没有顺序的，只是根据key的哈希值，将元素存在指定位置，所以根据key查找单个value时非常高效，平均可以在常数时间内完成。
- unordered_map查询单个key的时候效率比map高，但是要查询某一范围内的key值时比map效率低。
- 可以使用[]操作符来访问key值对应的value值。

#### api

- 构造函数

  ```c++
  #include <unordered_map>
  #include <vector>
  #include <bitset>
  #include <string>
  #include <utility>

  struct Key {
      std::string first;
      std::string second;
  };

  struct KeyHash {
   std::size_t operator()(const Key& k) const
   {
       return std::hash<std::string>()(k.first) ^
              (std::hash<std::string>()(k.second) << 1);
   }
  };

  struct KeyEqual {
   bool operator()(const Key& lhs, const Key& rhs) const
   {
      return lhs.first == rhs.first && lhs.second == rhs.second;
   }
  };

  struct Foo {
      Foo(int val_) : val(val_) {}
      int val;
      bool operator==(const Foo &rhs) const { return val == rhs.val; }
  };

  namespace std {
      template<> struct hash<Foo> {
          std::size_t operator()(const Foo &f) const {
              return std::hash<int>{}(f.val);
          }  
      };
  }

  int main()
  {
      // 默认构造函数：空 unordered_map
      std::unordered_map<std::string, std::string> m1;

      // 列表构造函数
      std::unordered_map<int, std::string> m2 =
      {
          {1, "foo"},
          {3, "bar"},
          {2, "baz"},
      };

      // 复制构造函数
      std::unordered_map<int, std::string> m3 = m2;

      // 移动构造函数
      std::unordered_map<int, std::string> m4 = std::move(m2);

      // 范围构造函数
      std::vector<std::pair<std::bitset<8>, int>> v = { {0x12, 1}, {0x01,-1} };
      std::unordered_map<std::bitset<8>, double> m5(v.begin(), v.end());

      // 带定制 Key 类型的构造函数的选项 1
      // 定义 KeyHash 与 KeyEqual 结构体并在模板中使用它们
      std::unordered_map<Key, std::string, KeyHash, KeyEqual> m6 = {
              { {"John", "Doe"}, "example"},
              { {"Mary", "Sue"}, "another"}
      };

      // 带定制 Key 类型的构造函数的选项 2
      // 为 class/struct 定义 const == 运算符并于 std 命名空间特化 std::hash 结构体
      std::unordered_map<Foo, std::string> m7 = {
          { Foo(1), "One"}, { 2, "Two"}, { 3, "Three"}
      };

      // 选项 3 ：用 lambdas
      // 注意必须将初始桶数传递给构造函数
      struct Goo {int val; };
      auto hash = [](const Goo &g){ return std::hash<int>{}(g.val); };
      auto comp = [](const Goo &l, const Goo &r){ return l.val == r.val; };
      std::unordered_map<Goo, double, decltype(hash), decltype(comp)> m8(10, hash, comp);
  }
  ```

- operator=

  ```c++
  //复制赋值运算符
  unordered_map& operator=( const unordered_map& other );

  //移动赋值运算符
  unordered_map& operator=( unordered_map&& other );

  //以 initializer_list ilist 所标识者替换内容。
  //    std::unordered_map<int, int> nums1 {{3, 1}, {4, 1}, {5, 9}}            
  unordered_map& operator=( std::initializer_list<value_type> ilist );
  ```

- 特殊

  ```c++
  //返回到拥有等于 key 的关键的元素被映射值的引用
  T& at( const Key& key );

  //寻找键等于 key 的的元素,若找不到这种元素，则返回尾后
  iterator find( const Key& key );

  //返回到映射到等于 key 的键的值的引用，若这种键不存在则进行插入。
  T& operator[]( const Key& key );

  ```

- other

  ```c++
  begin
  cbegin
  end
  cend
  empty
  size
  max_size //基本是内存大小，无意义
  clear
  swap
  count//要么1要么0，无意义
  emplace    //move
  insert    //插入元素
  ```

# 算法

## algorithm

- 不修改序列的操作

  检查谓词是否对范围中所有、任一或无元素为 true

  ```c++
  // 若一元谓词对范围中所有元素返回 true 则为 true ，否则为 false 。若范围为  空则返回 true 。
  template< class InputIt, class UnaryPredicate >
  bool all_of( InputIt first, InputIt last, UnaryPredicate p );

  //检查一元谓词 p 是否对范围 [first, last) 中至少一个元素返回 true 。
  template< class InputIt, class UnaryPredicate >
  bool any_of( InputIt first, InputIt last,     UnaryPredicate p );

  //检查一元谓词 p 是否不对范围 [first, last) 中任何元素返回 true 。
  template< class InputIt, class UnaryPredicate >
  bool none_of( InputIt first, InputIt last, UnaryPredicate p );

  ```

  应用函数到范围中的元素

  ```c++

  //按顺序应用给定的函数对象 f 到解引用范围 [first, last) 中每个迭代器的结果。
  //f<=> void fun(const Type &a);
  template< class InputIt, class UnaryFunction >
  UnaryFunction for_each( InputIt first, InputIt last, UnaryFunction f );
  ```

  返回满足指定判别标准的元素数

  ```c++
  //返回范围 [first, last) 中满足特定判别标准的元素数。
  //计数等于 value 的元素。
  template< class InputIt, class T >
  typename iterator_traits<InputIt>::difference_type
      count( InputIt first, InputIt last, const T &value );

  //计数谓词 p 对其返回 true 的元素。
  template< class InputIt, class UnaryPredicate >
  typename iterator_traits<InputIt>::difference_type
      count_if( InputIt first, InputIt last, UnaryPredicate p );
  ```

  寻找两个范围出现不同的首个位置

  ```c++
  //返回来自二个范围：一个以 [first1, last1) 定义而另一个以 [first2,last2) 定义，的首个匹配对
  // 用 operator== 比较元素
  template< class InputIt1, class InputIt2 >
  std::pair<InputIt1,InputIt2> mismatch( InputIt1 first1, InputIt1 last1,
            InputIt2 first2 );
  //用给定的二元谓词 p 比较元素
  template< class InputIt1, class InputIt2, class BinaryPredicate >
  std::pair<InputIt1,InputIt2> mismatch( InputIt1 first1, InputIt1 last1,
            InputIt2 first2, BinaryPredicate p );
  ```

  寻找首个满足特定判别标准的元素

  ```c++

  //find 搜索等于 value 的元素。
  template< class InputIt, class T >
  InputIt find( InputIt first, InputIt last, const T& value );

  //find_if 搜索谓词 p 对其返回 true 的元素。
  template< class InputIt, class UnaryPredicate >
  InputIt find_if( InputIt first, InputIt last, UnaryPredicate p );

  //find_if_not 搜索谓词 q 对其返回 false 的元素。
  template< class InputIt, class UnaryPredicate >
  InputIt find_if_not( InputIt first, InputIt last,UnaryPredicate q );
  ```

  在特定范围中寻找最后出现的元素序列

  ```c++
  //在范围 [first, last) 中搜索序列 [s_first, s_last) 的最后一次出现。
  //用 operator== 比较元素。
  template< class ForwardIt1, class ForwardIt2 >
  ForwardIt1 find_end( ForwardIt1 first, ForwardIt1 last,
                   ForwardIt2 s_first, ForwardIt2 s_last );

  //用给定的二元谓词 p 比较元素。
  template< class ForwardIt1, class ForwardIt2, class BinaryPredicate >
  ForwardIt1 find_end( ForwardIt1 first, ForwardIt1 last,
                   ForwardIt2 s_first, ForwardIt2 s_last, BinaryPredicate p );
  ```

  搜索元素集合中的任意元素

  ```c++
  //在范围 [first, last) 中搜索范围 [s_first, s_last) 中的任何元素。
  //用 operator== 比较元素。
  template< class InputIt, class ForwardIt >
  InputIt find_first_of( InputIt first, InputIt last,
                     ForwardIt s_first, ForwardIt s_last );

  //用给定的二元谓词 p 比较元素用给定的二元谓词 p 比较元素
  template< class InputIt, class ForwardIt, class BinaryPredicate >
  InputIt find_first_of( InputIt first, InputIt last,
                     ForwardIt s_first, ForwardIt s_last, BinaryPredicate p );
  ```

  查找首对相邻的相同（或满足给定谓词的）元素

  ```c++
  //在范围 [first, last) 中搜索二个相继的相等元素。
  //用 operator== 比较元素。
  template< class ForwardIt >
  ForwardIt adjacent_find( ForwardIt first, ForwardIt last );

  //用给定的二元谓词 p 比较元素。
  template< class ForwardIt, class BinaryPredicate>
  ForwardIt adjacent_find( ForwardIt first, ForwardIt last, BinaryPredicate p );
  ```

  搜索一个元素范围

  ```c++
  //搜索范围 [first, last - (s_last - s_first)) 中元素子序列 [s_first, s_last) 的首次出现。
  // 元素用 operator== 比较。
  template< class ForwardIt1, class ForwardIt2 >
  ForwardIt1 search( ForwardIt1 first, ForwardIt1 last,
                 ForwardIt2 s_first, ForwardIt2 s_last );

  //元素用给定的二元谓词 p 比较。
  template< class ForwardIt1, class ForwardIt2, class BinaryPredicate >
  ForwardIt1 search( ForwardIt1 first, ForwardIt1 last,
                 ForwardIt2 s_first, ForwardIt2 s_last, BinaryPredicate p );
  ```

  在范围中搜索一定量的某个元素的连续副本

  ```c++
  //在范围 [first, last) 中搜索 count 个等同元素的序列，每个都等于给定的值 value 。
  //用 operator== 比较元素。
  template< class ForwardIt, class Size, class T >
  ForwardIt search_n( ForwardIt first, ForwardIt last, Size count, const T& value );

  //用给定的二元谓词 p 比较元素。
  template< class ForwardIt, class Size, class T, class BinaryPredicate >
  ForwardIt search_n( ForwardIt first, ForwardIt last, Size count, const T& value,
                   BinaryPredicate p );
  ```

- 修改序列的操作

  将某一范围的元素复制到一个新的位置

  ```c++
  //复制 [first, last) 所定义的范围中的元素到始于 d_first 的另一范围。
  // 复制范围 [first, last) 中的所有元素，从首元素开始逐次到末元素
  template< class InputIt, class OutputIt >
  OutputIt copy( InputIt first, InputIt last, OutputIt d_first );

  //仅复制谓词 pred 对其返回 true 的元素。保持被复制元素的相对顺序。
  template< class InputIt, class OutputIt, class UnaryPredicate >
  OutputIt copy_if( InputIt first, InputIt last,
                OutputIt d_first, UnaryPredicate pred );
  ```

  将一定数目的元素复制到一个新的位置

  ```c++
  //若 count>0 ，则准确复制来自始于 first 的范围的 count 个值到始于 result 的范围
  template< class InputIt, class Size, class OutputIt >
  OutputIt copy_n( InputIt first, Size count, OutputIt result );
  ```

  按从后往前的顺序复制一个范围内的元素

  ```c++
  //复制来自 [first, last) 所定义范围的元素，到终于 d_last 的范围。以逆序复制元素（首先复制末元素），但保持其相对顺序。
  template< class BidirIt1, class BidirIt2 >
  BidirIt2 copy_backward( BidirIt1 first, BidirIt1 last, BidirIt2 d_last );
  ```

  将某一范围的元素移动到一个新的位置

  ```c++
  //移动范围 [first, last) 中的元素到始于 d_first 的另一范围，从首元素开始逐次到末元素。此操作后被移动范围中的元素将仍然含有适合类型的合法值，但不必与移动前的值相同。
  template< class InputIt, class OutputIt >
  OutputIt move( InputIt first, InputIt last, OutputIt d_first );


  //移动来自范围 [first, last) 的元素到终于 d_last 的另一范围。以逆序移动元素（首先复制末元素），但保持其相对顺序。
  template< class BidirIt1, class BidirIt2 >
  BidirIt2 move_backward( BidirIt1 first, BidirIt1 last, BidirIt2 d_last );
  ```

  将一个给定值复制赋值给一个范围内的每个元素

  ```c++
  //赋值给定的 value 给 [first, last) 中的元素。
  template< class ForwardIt, class T >
  void fill( ForwardIt first, ForwardIt last, const T& value );

  // 若 count > 0 ，则赋值给定的 value 给始于 的范围的首 count 个元素。否则不做任何事。
  template< class OutputIt, class Size, class T >
  OutputIt fill_n( OutputIt first, Size count, const T& value );
  ```

  ```c++
  //std::transform 应用给定的函数到范围并存储结果于始于 d_first 的另一范围。
  // 应用一元函数 unary_op 到 [first1, last1) 所定义的范围。
  template< class InputIt, class OutputIt, class UnaryOperation >
  OutputIt transform( InputIt first1, InputIt last1, OutputIt d_first,
                  UnaryOperation unary_op );
  //应用二元函数 binary_op 到来自二个范围的元素对：一个以 [first1, last1) 定义，而另一个始于 first2 。
  template< class InputIt1, class InputIt2, class OutputIt, class BinaryOperation >
  OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                  OutputIt d_first, BinaryOperation binary_op );
  ```

  将相继的函数调用结果赋值给一个范围中的每个元素

  ```c++
  //给定函数对象 g 所生成的值赋值范围 [first, last) 中的每个元素。
  //  std::generate(v.begin(), v.end(), [n = 0] () mutable { return n++; });
  template< class ForwardIt, class Generator >
  void generate( ForwardIt first, ForwardIt last, Generator g );


  //若 count>0 ，则赋值给定函数对象 g 所生成的值给始于 first 的范围的首 count 个元素。否则不做任何事
  template< class OutputIt, class Size, class Generator >
  OutputIt generate_n( OutputIt first, Size count, Generator g );
  ```

  复制一个范围的元素，忽略满足特定判别标准的元素

  ```c++
  //从范围 [first, last) 移除所有满足特定判别标准的元素，并返回范围新结尾的尾后迭代器。
  //移除所有等于 value 的元素，用 operator== 比较它们。
  template< class ForwardIt, class T >
  ForwardIt remove( ForwardIt first, ForwardIt last, const T& value );

  //移除所有 p 对于它返回 true 的元素。
  template< class ForwardIt, class UnaryPredicate >
  ForwardIt remove_if( ForwardIt first, ForwardIt last, UnaryPredicate p );


  //通过以满足不移除的元素出现在范围起始的方式，迁移（以移动赋值的方式）范围中的元素进行移除。保持剩余元素的相对顺序，且不更改容器的物理大小。指向范围的新逻辑结尾和物理结尾之间元素的迭代器仍然可解引用，但元素自身拥有未指定值（因为可移动赋值 (MoveAssignable) 的后条件）。调用 remove 典型地后随调用容器的 erase 方法，它擦除未指定值并减小容器的物理大小，以匹配其新的逻辑大小。
  ```

  替换所有谓词 p 对其返回 true 的元素。

  ```c++
  //以 new_value 替换范围 [first, last) 中所有满足特定判别标准的元素。
  //替换所有等于 old_value 的元素。
  template< class ForwardIt, class T >
  void replace( ForwardIt first, ForwardIt last,
            const T& old_value, const T& new_value );

  //替换所有谓词 p 对其返回 true 的元素。
  template< class ForwardIt, class UnaryPredicate, class T >
  void replace_if( ForwardIt first, ForwardIt last,
                   UnaryPredicate p, const T& new_value );
  ```

  复制一个范围内的元素，并将满足特定判别标准的元素替换为另一个值

  ```c++
  //复制来自范围 [first, last) 的元素到始于 d_first 的范围，并以 new_value 替换所有满足特定判别标准的元素。源与目标范围不能重叠。
  //替换所有等于 old_value 的元素。
  template< class InputIt, class OutputIt, class T >
  OutputIt replace_copy( InputIt first, InputIt last, OutputIt d_first,
                     const T& old_value, const T& new_value );


  //替换所有谓词 p 对其满足 true 的元素。
  template< class InputIt, class OutputIt, class UnaryPredicate, class T >
  OutputIt replace_copy_if( InputIt first, InputIt last, OutputIt d_first,
                        UnaryPredicate p, const T& new_value );
  ```

  交换两个对象的值

  ```c++
  //交换 a 与 b 
  //定义于头文件 <algorithm>(C++11 前)
  //定义于头文件 <utility>(C++11 起)
  //定义于头文件 <string_view>(C++17 起)
  template< class T >
  void swap( T& a, T& b ) noexcept();

  //交换 a 与 b 数组
  template< class T2, std::size_t N >
  void swap( T2 (&a)[N], T2 (&b)[N]) noexcept();

  // 在范围 [first1, last1) 和始于 first2 的另一范围间交换元素。
  template< class ForwardIt1, class ForwardIt2 >
  ForwardIt2 swap_ranges( ForwardIt1 first1, ForwardIt1 last1,
                      ForwardIt2 first2 );

  ```

  逆转范围中的元素顺序

  ```c++
  //反转 [first, last) 范围中的元素顺序
  template< class BidirIt >
  void reverse( BidirIt first, BidirIt last );

  //复制来自范围 [first, last) 的元素到始于 d_first 的新范围，使得新范围中元素以逆序排列。
  template< class BidirIt, class OutputIt >
  OutputIt reverse_copy( BidirIt first, BidirIt last, OutputIt d_first );
  ```

  旋转范围中的元素顺序

  ```c++
  //具体而言， std::rotate 交换范围 [first, last) 中的元素，方式满足元素 n_first 成为新范围的首个元素，而 n_first - 1 成为最后元素。此函数的前提条件是 [first, n_first) 和 [n_first, last) 为合法范围。
  //进行元素范围上的左旋转。
  template< class ForwardIt >
  ForwardIt rotate( ForwardIt first, ForwardIt n_first, ForwardIt last );

  //从范围 [first, last) 复制元素到始于 d_first 的另一范围，使得 n_first 成为新范围的首元素，而 n_first - 1 成为末元素。
  template< class ForwardIt, class OutputIt >
  OutputIt rotate_copy( ForwardIt first, ForwardIt n_first,
                    ForwardIt last, OutputIt d_first );
  ```

  随机数生成器为函数对象 r

  ```c++
  //重排序给定范围 [first, last) 中的元素，使得这些元素的每个排列拥有相等的出现概率。
  //随机数生成器是实现定义的，但经常使用函数 std::rand 
  template< class RandomIt >
  void random_shuffle( RandomIt first, RandomIt last );
  //随机数生成器为函数对象 r
  template< class RandomIt, class RandomFunc >
  void random_shuffle( RandomIt first, RandomIt last, RandomFunc&& r );
  // 随机数生成器为函数对象 g 
  template< class RandomIt, class URBG >
  void shuffle( RandomIt first, RandomIt last, URBG&& g );
  ```

  移除范围内的连续重复元素

  ```C++
  //从来自范围 [first, last) 的相继等价元素组消除首元素外的元素，并返回范围的新逻辑结尾的尾后迭代器。
  //通过用覆写要被擦除的元素的方式迁移范围中的元素进行移除。保持剩余元素的相对顺序，且不更改容器的物理大小。指向范围的新逻辑结尾和物理结尾之间元素的迭代器仍然可解引用，但元素自身拥有未指定值。调用 unique 典型地后随调用容器的 erase 方法，它擦除未指定值并减小容器的物理大小，以匹配其新的逻辑大小。

  // 用 operator== 比较元素
  template< class ForwardIt >
  ForwardIt unique( ForwardIt first, ForwardIt last );

  // 用 operator== 比较元素
  template< class ForwardIt, class BinaryPredicate >
  ForwardIt unique( ForwardIt first, ForwardIt last, BinaryPredicate p );

  //
  template< class InputIt, class OutputIt >
  OutputIt unique_copy( InputIt first, InputIt last,
                    OutputIt d_first );

  //
  template< class InputIt, class OutputIt, class BinaryPredicate >
  OutputIt unique_copy( InputIt first, InputIt last,
                    OutputIt d_first, BinaryPredicate p );
  ```
