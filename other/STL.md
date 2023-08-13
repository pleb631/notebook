[toc]

# 容器

## array

### array介绍

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

### array api

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

## vector

### vector介绍

vector和 array 容器非常类似，都可以看做是对C++普通数组的“升级版”。不同之处在于，array 实现的是静态数组（容量固定的数组），而 vector 实现的是一个动态数组，即可以进行元素的插入和删除，vector 的存储是自动管理的，按需扩张收缩。 vector 通常占用多于静态数组的空间，因为要分配更多内存以管理将来的增长。 vector 所用的方式不在每次插入元素时，而只在额外内存耗尽时重分配

vector 上的常见操作复杂度（效率）如下：

- 随机访问——常数 O(1)
- 在末尾插入或移除元素——均摊常数 O(1)
- 插入或移除元素——与到 vector 结尾的距离成线性 O(n)

### 创建vector容器的几种方式

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

### vector api

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

  //从容器擦除指定位置的元素。
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

# 算法

## algorithm


- 不修改序列的操作

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

    //按顺序应用给定的函数对象 f 到解引用范围 [first, last) 中每个迭代器的结果。
    template< class InputIt, class UnaryFunction >
    UnaryFunction for_each( InputIt first, InputIt last, UnaryFunction f );
    ```
