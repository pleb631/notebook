# 容器

![2023-11-17-10-39-40](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-11-17-10-39-40.png)

| 函数成员         | 函数功能                                                     | array&lt;T,N&gt; | vector&lt;T&gt; | deque&lt;T&gt; |
| ---------------- | ------------------------------------------------------------ | ---------------- | --------------- | -------------- |
| begin()          | 返回指向容器中第一个元素的迭代器。                           | 是               | 是              | 是             |
| end()            | 返回指向容器最后一个元素所在位置后一个位置的迭代器，通常和 begin() 结合使用。 | 是               | 是              | 是             |
| rbegin()         | 返回指向最后一个元素的迭代器。                               | 是               | 是              | 是             |
| rend()           | 返回指向第一个元素所在位置前一个位置的迭代器。               | 是               | 是              | 是             |
| cbegin()         | 和&nbsp;begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是               | 是              | 是             |
| cend()           | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是               | 是              | 是             |
| crbegin()        | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是               | 是              | 是             |
| crend()          | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是               | 是              | 是             |
| assign()         | 用新元素替换原有内容。                                       | -                | 是              | 是             |
| operator=()      | 复制同类型容器的元素，或者用初始化列表替换现有内容。         | 是               | 是              | 是             |
| size()           | 返回实际元素个数。                                           | 是               | 是              | 是             |
| max_size()       | 返回元素个数的最大值。这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。 | 是               | 是              | 是             |
| capacity()       | 返回当前容量。                                               | -                | 是              | -              |
| empty()          | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。 | 是               | 是              | 是             |
| resize()         | 改变实际元素的个数。                                         | -                | 是              | 是             |
| shrink _to_fit() | 将内存减少到等于当前元素实际所使用的大小。                   | -                | 是              | 是             |
| front()          | 返回第一个元素的引用。                                       | 是               | 是              | 是             |
| back()           | 返回最后一个元素的引用。                                     | 是               | 是              | 是             |
| operator[]()     | 使用索引访问元素。                                           | 是               | 是              | 是             |
| at()             | 使用经过边界检査的索引访问元素。                             | 是               | 是              | 是             |
| push_back()      | 在序列的尾部添加一个元素。                                   | -                | 是              | 是             |
| insert()         | 在指定的位置插入一个或多个元素。                             | -                | 是              | 是             |
| emplace()        | 在指定的位置直接生成一个元素。                               | -                | 是              | 是             |
| emplace_back()   | 在序列尾部生成一个元素。                                     | -                | 是              | 是             |
| pop_back()       | 移出序列尾部的元素。                                         | -                | 是              | 是             |
| erase()          | 移出一个元素或一段元素。                                     | -                | 是              | 是             |
| clear()          | 移出所有的元素，容器大小变为 0。                             | -                | 是              | 是             |
| swap()           | 交换两个容器的所有元素。                                     | 是               | 是              | 是             |
| data()           | 返回指向容器中第一个元素的指针。                             | 是               | 是              | -              |

| 函数成员        | 函数功能                                                     | list&lt;T&gt; | forward_list&lt;T&gt; |
| --------------- | ------------------------------------------------------------ | ------------- | --------------------- |
| begin()         | 返回指向容器中第一个元素的迭代器。                           | 是            | 是                    |
| end()           | 返回指向容器最后一个元素所在位置后一个位置的迭代器。         | 是            | 是                    |
| rbegin()        | 返回指向最后一个元素的迭代器。                               | 是            | -                     |
| rend()          | 返回指向第一个元素所在位置前一个位置的迭代器。               | 是            | -                     |
| cbegin()        | 和 begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是            | 是                    |
| before_begin()  | 返回指向第一个元素前一个位置的迭代器。                       | -             | 是                    |
| cbefore_begin() | 和 before_begin() 功能相同，只不过在其基础上，增加了 const 属性，即不能用该指针修改元素的值。 | -             | 是                    |
| cend()          | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是            | 是                    |
| crbegin()       | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是            | -                     |
| crend()         | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 | 是            | -                     |
| assign()        | 用新元素替换原有内容。                                       | 是            | 是                    |
| operator=()     | 复制同类型容器的元素，或者用初始化列表替换现有内容。         | 是            | 是                    |
| size()          | 返回实际元素个数。                                           | 是            | -                     |
| max_size()      | 返回元素个数的最大值，这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。 | 是            | 是                    |
| resize()        | 改变实际元素的个数。                                         | 是            | 是                    |
| empty()         | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。 | 是            | 是                    |
| front()         | 返回容器中第一个元素的引用。                                 | 是            | 是                    |
| back()          | 返回容器中最后一个元素的引用。                               | 是            | -                     |
| push_back()     | 在序列的尾部添加一个元素。                                   | 是            | -                     |
| push_front()    | 在序列的起始位置添加一个元素。                               | 是            | 是                    |
| emplace()       | 在指定位置直接生成一个元素。                                 | 是            | -                     |
| emplace_after() | 在指定位置的后面直接生成一个元素。                           | -             | 是                    |
| emplace_back()  | 在序列尾部生成一个元素。                                     | 是            | -                     |
| cmplacc_front() | 在序列的起始位生成一个元索。                                 | 是            | 是                    |
| insert()        | 在指定的位置插入一个或多个元素。                             | 是            | -                     |
| insert_after()  | 在指定位置的后面插入一个或多个元素。                         | -             | 是                    |
| pop_back()      | 移除序列尾部的元素。                                         | 是            | -                     |
| pop_front()     | 移除序列头部的元素。                                         | 是            | 是                    |
| reverse()       | 反转容器中某一段的元素。                                     | 是            | 是                    |
| erase()         | 移除指定位置的一个元素或一段元素。                           | 是            | -                     |
| erase_after()   | 移除指定位置后面的一个元素或一段元素。                       | -             | 是                    |
| remove()        | 移除所有和参数匹配的元素。                                   | 是            | 是                    |
| remove_if()     | 移除满足一元函数条件的所有元素。                             | 是            | 是                    |
| unique()        | 移除所有连续重复的元素。                                     | 是            | 是                    |
| clear()         | 移除所有的元素，容器大小变为 0。                             | 是            | 是                    |
| swap()          | 交换两个容器的所有元素。                                     | 是            | 是                    |
| sort()          | 对元素进行排序。                                             | 是            | 是                    |
| merge()         | 合并两个有序容器。                                           | 是            | 是                    |
| splice()        | 移动指定位置前面的所有元素到另一个同类型的 list 中。         | 是            | -                     |
| splice_after()  | 移动指定位置后面的所有元素到另一个同类型的 list 中。         | -             | 是                    |

## 1.string

见笔记cpp23

## 2.array

### 2.1介绍

array 容器封装固定大小数组的容器，它就是在 C++ 普通数组的基础上，添加了一些成员函数和全局函数的结构体。在使用上，它比普通数组更安全，且效率并没有因此变差。它不会自动退化成 T* 。

**array 容器的大小是固定的**，它只允许访问或者替换存储的元素。

array 容器以类模板的形式定义在 `<array>` 头文件，并位于命名空间 std 中，如下所示：

```c++
namespace std{
    template <typename T, size_t N>  
    class array;
    }
```

**初始化** ：

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

### 2.2api

### 元素访问

- 访问
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
T* data();

  ```

- 容量

  ```c++
  //检查容器是否无元素，即是否 begin() == end()
  constexpr bool empty();
  
  //返回容器中的元素数，即 std::distance(begin(), end())
  constexpr size_type size();
  
  //返回根据系统或库实现限制的容器可保有的元素最大数量，即对于最大容器的 std::distance(begin(), end())
  constexpr size_type max_size();
  ```

- 操作

  ```c++
  void fill( const T& value );
  
  void swap( array& other );
  ```
  
- 非成员函数

  ```c++
  std::get(std::array)
  std::swap(std::array)
  to_array
  ```

## 3.vector

### 3.1vector介绍

 vector 是一个动态数组，即可以进行元素的插入和删除，vector 的存储是自动管理的，按需扩张收缩。 vector 通常占用多于静态数组的空间，因为要分配更多内存以管理将来的增长。 vector 所用的方式不在每次插入元素时，而只在额外内存耗尽时重分配

vector 上的常见操作复杂度（效率）如下：

- 随机访问——常数 O(1)
- 在末尾插入或移除元素——均摊常数 O(1)
- 插入或移除元素——与到 vector 结尾的距离成线性 O(n)

### 3.2创建vector容器的几种方式

创建 vector 容器的方式有很多，大致可分为以下几种。

1. 常规：

   ```c++
   std::vector<double> values;
   //扩容
   values.reserve(20);
   
   //赋值构造
   std::vector<int> primes {2, 3, 5, 7, 11, 13, 17, 19};
   
   //只定义容量
   std::vector<double> values1(20);
   
   //定义容量并都赋值1.0
   std::vector<double> values2(20, 1.0);4
   
       
   //拷贝构造
   std::vector<char> value3(value2);
   ```

   2.切片

   ```c++
   int array[]={1,2,3};
   std::vector<int>values(array,array+2);
   //values 将保存{1,2}
   std::vector<int> value1{1,2,3,4,5};
   std::vector<int> value2(std::begin(value1),std::begin(value1)+3);
   //value2保存{1,2,3}
   ```

### 3.3api

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

- 容量

  ```c++
  //检查容器是否无元素，即是否 begin() == end()
  bool empty();
  
  //返回容器中的元素数，即 std::distance(begin(), end())
  size_type size();
  
  //返回根据系统或库实现限制的容器可保有的元素最大数量
  size_type max_size();
  
  //增加 vector 的容量到大于或等于new_cap的值。若 new_cap 大于当前的 capacity() ，则分配新存储，否则该方法不做任何事。reserve() 不更改 vector 的 size。
  void reserve(size_type new_cap );
  
  //返回空间容量。
  size_type capacity()
  
  //移除未使用的容量。减少 capacity() 到 size()
  void shrink_to_fit();
  ```
  
- 修改

  ```c++
  //从容器擦除所有元素。  
  void clear();
  
  //将内容与 other 的交换。不在单个元素上调用任何移动、复制或交换操作。
  void swap(vector& other );
  
  //
  //insert
  // 在 pos 前插入 value
  iterator insert(const_iterator pos, const T& value );
  
  iterator insert(const_iterator pos, T&& value );
  
  //在 pos 前插入 value 的 count 个副本
  iterator insert( const_iterator pos, size_type count, const T& value );
  
  //在 pos 前插入来自范围 [first, last) 的元素。
  iterator insert(const_iterator pos, InputIt first, InputIt last );
  
  //在 pos 前插入来自 initializer_list ilist 的元素。
  iterator insert(const_iterator pos, std::initializer_list<T> ilist );
  
  //直接于 pos 前插入元素到容器中。
  iterator emplace(const_iterator pos, Args&&... args );
  
  //从容器擦除指定位置的元素。函数擦除的最后一个元素后跟的元素
  iterator erase(const_iterator pos );
  
  //移除范围 [first; last) 中的元素。左闭右开
  iterator erase(const_iterator first, const_iterator last );
  
  //初始化新元素为 value 的副本。
  void push_back(const T& value );
  
  // 移动 value 进新元素。
  void push_back(T&& value );
  
  //添加新元素到容器尾
  template< class... Args >
  void emplace_back(Args&&... args );
  
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

## 4.deque

### 4.1介绍

**deque** 是一种双端队列，允许在两端高效地插入和删除元素。它的底层实现基于分段连续空间，动态分配内存，避免了像 *vector* 那样因容量不足而重新分配整个空间的开销。

deque 的核心由以下部分组成：

1. **map 中控器**：*map* 是一块小的连续空间，每个元素是指针，指向一段较大的缓冲区。缓冲区是 deque 的实际存储空间。
2. **缓冲区**：每个缓冲区存储固定数量的元素，缓冲区之间通过 *map* 链接起来。
3. **迭代器**：迭代器通过 *cur*、*first*、*last* 和 *node* 等指针维护对缓冲区的访问，支持随机访问和高效的插入、删除操作。

```c++
template <class T, class Alloc = alloc, size_t BufSize = 0>
class deque {
protected:
   typedef T** map_pointer; // map 是指针的指针
   map_pointer map; // 指向 map 的指针
   size_t map_size; // map 的大小
   iterator start; // 指向第一个缓冲区的第一个元素
   iterator finish; // 指向最后一个缓冲区的最后一个元素
};
```

deque有以下特点：

- 在其首尾可以快速插入及删除，并且不会非法化指向其余元素的指针或引用。
- 随机访问需要二次指针解引用，所以略慢于vector
- 扩张 deque 不会涉及复制既存元素
- 内存开销较大，至少要维护一个map大小的空间

与 std::vector 相反， deque 的元素不是相接存储的：典型实现用单独分配的固定大小数组的序列，外加额外的登记，这表示下标访问必须进行二次指针解引用，与之相比 vector 的下标访问只进行一次。

常见操作的复杂度（效率）如下：

- 随机访问——常数 O(1)
- 在结尾或起始插入或移除元素——常数 O(1)
- 插入或移除元素——线性 O(n)

### 4.2 api

构造、赋值

```c++
deque<T> deqT; //默认构造形式
deque(beg, end);//构造函数将[区间中的元素拷贝给本身。
deque(n, elem); //构造函数将n个elem拷贝给本身。
deque(const deque &deq);   //拷贝构造函数

deque& operator=(const deque &deq);//重载等号操作符
assign(beg, end);//将区间中的数据拷贝赋值给本身。
assign(n, elem);//将n个elem拷贝赋值给本身。
```

```c++
deque.empty();
deque.size();
deque.resize(num);
deque.resize(num, elem);
```

数据访问

```c++
at(int idx);
operator[];
front(); 
back();
```

插入删除

```c++
push_back(elem);
push_front(elem);
pop_back();
pop_front();

insert(pos,elem);
insert(pos,n,elem);
insert(pos,beg,end);
clear();
erase(beg,end);
erase(pos);
```

stack、queue的底层就是deque

### 4.3 queue

Queue是一种**先进先出**(First In First Out,FIFO)的数据结构

```c++
push(elem);//往队尾添加元素
pop();//从队头移除第一个元素
back();
front();
```

### 4.4 stack

stack是一种**先进后出**(First In Last Out,FILO)的数据结构，它只有一个出口

```c++
push(elem);//向栈顶添加元素
pop();//从栈顶移除第一个元素
top();//返回栈顶元素
```

## 5.list

std::list 提供了双向链表的功能。

- 支持常数时间从容器任何位置插入和移除元素的容器。
- 不支持快速随机访问。
- 添加、移除和移动元素不会非法化迭代器或引用。迭代器仅在对应元素被删除时非法化。

## 6. set/multiset

- 所有元素都会在插入时自动被排序
- 属于**关联式容器**，底层结构是用**二叉树**实现。

**set和multiset区别**：

- set不允许容器中有重复的元素
- multiset允许容器中有重复的元素

```c++
template<
    class Key,
    class Compare = std::less<Key>,
> class set;
//用比较函数 比较 (Compare) 进行排序。搜索、移除和插入拥有对数复杂度。 
```

### 6.1api

- 构造函数

  ```c++
  set();
  set(const Compare& comp);
  set(InputIt first, InputIt last, const Compare& comp = Compare());
  set(std::initializer_list<value_type> init, const Compare& comp = Compare(),);
  
  set& operator=(const set &st);
  ```
  
- 修改

  ```c++
  //插入 value
  std::pair<iterator,bool> insert( value_type&& value );
  
  //若范围中的多个元素拥有比较等价的关键，则插入哪个元素是未定义行为
  void insert( InputIt first, InputIt last );
  
  void insert( std::initializer_list<value_type> ilist );
  
  iterator insert( iterator hint, const value_type& value );
  
  template< class... Args >
  std::pair<iterator,bool> emplace( Args&&... args );
  
  iterator emplace_hint( const_iterator hint, Args&&... args );
  
  
  void swap( set& other );
  
- 查找

  ```c++
  
  //返回拥有关键比较等价于指定参数的元素数，因为此容器不允许重复故为 1 或 0。
  template< class K >
  size_type count( const K& x ) const;
  
  template< class K >
  iterator find( const K& x );
  
  //返回容器中所有拥有给定关键的元素范围。范围以二个迭代器定义，一个指向首个不小于 key 的元素，另一个指向首个大于 key 的元素。首个迭代器可以换用 lower_bound() 获得，而第二迭代器可换用 upper_bound() 获得
  //比较关键与 key
  template< class K >
  std::pair<iterator,iterator> equal_range( const K& x );
  
  //返回指向首个不小于 key 的元素的迭代器。
  template< class K >
  iterator lower_bound(const K& x);
  
  
  //返回指向首个大于 key 的元素的迭代器。
  template< class K >
  iterator upper_bound( const K& x );

### 6.2示例

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
    bool operator()(song& left,song&  right)  //重载（）运算符
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

## 8.map/unordered_map

### 8.1介绍

- map中所有元素都是pair

- unordered_map是一个将key和value关联起来的容器，它可以高效的根据单个key值查找对应的value。
- key值应该是唯一的，key和value的数据类型可以不相同。
- unordered_map存储元素时是没有顺序的，只是根据key的哈希值，将元素存在指定位置，所以根据key查找单个value时非常高效，平均可以在常数时间内完成。
- unordered_map查询单个key的时候效率比map高，但是要查询某一范围内的key值时比map效率低。
- 可以使用[]操作符来访问key值对应的value值。

### 8.2api

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
  
  unordered_map& operator=( const unordered_map& other );
  unordered_map& operator=( unordered_map&& other );
  
  //以 initializer_list ilist 所标识者替换内容。
  //    std::unordered_map<int, int> nums1 {{3, 1}, {4, 1}, {5, 9}}            
  unordered_map& operator=( std::initializer_list<value_type> ilist );
  ```
  
- 增删

  ```c++
  #include <utility>
  #include <map>
  
  std::map<int, int> m;
  //第一种插入方式
  m.insert(std::pair<int, int>(1, 10));
  //第二种插入方式
  m.insert(std::make_pair(2, 20));
  //第三种插入方式
  m.insert(map<int, int>::value_type(3, 30));
  //第四种插入方式
  m[4] = 40;
  
  for (std::map<int, int>::iterator it = m.begin(); it != m.end(); it++){
    cout << "key = " << it->first << " value = " << it->second << endl;
  }
  
  m.erase(m.begin());
  m.erase(3);
  
  m.erase(m.begin(),m.end());
  m.clear();
  ```

- 查

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
  empty
  size
  swap
  count//要么1要么0，无意义
  emplace    //move
  ```

### 8.3 map容器排序

map容器默认排序规则为 按照key值进行 从小到大排序，利用仿函数，可以改变排序规则

```c++
#include <map>

class MyCompare {
public:
 bool operator()(int v1, int v2) {
  return v1 > v2;
 }
};

int main() 
{
 //默认从小到大排序
 //利用仿函数实现从大到小排序
 map<int, int, MyCompare> m;

 m.insert(make_pair(1, 10));
 m.insert(make_pair(2, 20));
 m.insert(make_pair(3, 30));
 m.insert(make_pair(4, 40));
 m.insert(make_pair(5, 50));

 for (map<int, int, MyCompare>::iterator it = m.begin(); it != m.end(); it++) {
  cout << "key:" << it->first << " value:" << it->second << endl;
 }
    return 0;
}
```

# 算法

## 1.非修改序列操作

### for循环

用函数f 顺序使用到范围内所有元素

api有两种，但用法都一样

```c++
// 类似于带`operator()`运算符重载的对象
UnaryFunc for_each( InputIt first, InputIt last, UnaryFunc f );
//普通函数、匿名函数
void for_each(ForwardIt first, ForwardIt last, UnaryFunc f );
```

### 统计

1. 检查谓词是否对范围中所有、任一或无元素为 true

```c++
// 对范围中所有元素返回 true 则为 true 。范围为空则返回 true。
bool all_of( InputIt first, InputIt last, UnaryPred p );

//对范围中至少有1个元素是true则返回true。
bool any_of( InputIt first, InputIt last,     UnaryPred p );

//对范围中都是false元素返回 true 。范围为空则返回true。
bool none_of( InputIt first, InputIt last, UnaryPred p );

```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/QQ_1770351730600.png)

1. 统计数量

   ```c++
   //返回范围 [first, last) 中满足特定条件的元素数量。
   difference_type count( InputIt first, InputIt last, const T& value );
   difference_type count_if( InputIt first, InputIt last, UnaryPred p );
   ```

### 搜索元素/序列

1. 查找元素

```c++
//也支持ForwardIt
//搜索等于value的元素。
InputIt find( InputIt first, InputIt last, const T& value);

//搜索函数p返回true的元素。
InputIt find_if( InputIt first, InputIt last, UnaryPred p );

//搜索函数q返回false的元素。
InputIt find_if_not( InputIt first, InputIt last,UnaryPred q );


```

1. 搜索元素是否存在于给定集合中

```c++
//在范围 [first, last) 中搜索范围 [s_first, s_last) 中的任何元素。
//用 operator== 比较元素。
InputIt find_first_of( InputIt first, InputIt last,ForwardIt s_first, ForwardIt s_last );

//用二元函数p比较
InputIt find_first_of( InputIt first, InputIt last,ForwardIt s_first, ForwardIt s_last, BinaryPred p );
```

1. 查找子序列出现的位置

```c++
//查找首先出现的位置
//用 operator== 比较元素。
ForwardIt1 search( ForwardIt1 first, ForwardIt1 last,ForwardIt2 s_first, ForwardIt2 s_last );

//用给定的二元谓词 p 比较。
ForwardIt1 search( ForwardIt1 first, ForwardIt1 last,ForwardIt2 s_first, ForwardIt2 s_last, BinaryPred p );

// 查找最后出现的位置
//用 operator== 比较元素。
ForwardIt1 find_end( ForwardIt1 first, ForwardIt1 last,ForwardIt2 s_first, ForwardIt2 s_last );

//用二元函数p比较元素。
ForwardIt1 find_end( ForwardIt1 first, ForwardIt1 last,ForwardIt2 s_first, ForwardIt2 s_last, BinaryPred p );
```

1. 搜索n个连续相等的元素序列

```c++
//在范围 [first, last) 中搜索二个相继的相等元素。
//用 operator== 比较元素。
ForwardIt adjacent_find( ForwardIt first, ForwardIt last );

//用给定的二元函数 p 比较元素。
ForwardIt adjacent_find( ForwardIt first, ForwardIt last, BinaryPred p );

//搜索n个连续相同的元素的子序列
ForwardIt search_n( ForwardIt first, ForwardIt last, Size count, const T& value );

ForwardIt search_n( ForwardIt first, ForwardIt last, Size count, const T& value, BinaryPred p );
```

1. 查找两个序列第一次不匹配的位置

```c++
//两个序列可以不等长
std::pair<InputIt1, InputIt2> mismatch( InputIt1 first1, InputIt1 last1, InputIt2 first2 );
std::pair<InputIt1, InputIt2> mismatch( InputIt1 first1, InputIt1 last1, InputIt2 first2, BinaryPred p );
```

1. 检查两个序列是否相同

```c++
bool equal( InputIt1 first1, InputIt1 last1, InputIt2 first2 );
bool equal( InputIt1 first1, InputIt1 last1, InputIt2 first2, BinaryPred p );
```

## 2.修改序列操作

### 复制

将某一范围的元素复制到一个新的位置

```c++
  
//复制范围中的元素到始于d_first的空间。
  
OutputIt copy( InputIt first, InputIt last, OutputIt d_first );
OutputIt copy_n( InputIt first, Size count, OutputIt result );
OutputIt copy_if( InputIt first, InputIt last, OutputIt d_first, UnaryPred pred );
  
// 逆序复制元素（首先复制末元素），但保持其相对顺序
BidirIt2 copy_backward(BidirIt1 first, BidirIt1 last, BidirIt2 d_last );
  
//移动
OutputIt move(InputIt first, InputIt last, OutputIt d_first );
BidirIt2 move_backward( BidirIt1 first, BidirIt1 last, BidirIt2 d_last );
```

### 交换

交换两个对象的值

```c++
void swap( T& a, T& b );
  
//交换 a 与 b 数组
void swap( T2 (&a)[N], T2 (&b)[N]);
  
// 在范围 [first1, last1) 和始于 first2 的另一范围间交换元素。
auto swap_ranges( I1 first1, S1 last1, I2 first2, S2 last2 );
  
//交换两个迭代器指向的元素
void iter_swap( ForwardIt1 a, ForwardIt2 b );
```

### 转换

1. 转换

  ```c++
  //给范围元素应用函数并存储结果于始于d_first的另一范围。
  // 应用一元函数 unary_op。
  OutputIt transform( InputIt first1, InputIt last1, OutputIt d_first,UnaryOperation unary_op );
  
  //应用二元函数 binary_op 到来自二个范围的元素对：一个以 [first1, last1) 定义，而另一个始于 first2 。
  OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2, OutputIt d_first, BinaryOperation binary_op );
  ```

1. 替换元素。

```c++
//以 new_value 替换范围中所有满足特定判别标准的元素。
//替换所有等于 old_value 的元素。
void replace( ForwardIt first, ForwardIt last, const T& old_value, const T& new_value );

//替换所有谓词 p 对其返回 true 的元素。
void replace_if( ForwardIt first, ForwardIt last, UnaryPred p, const T& new_value );
```

1. 复制一个范围内的元素，并将满足特定判别标准的元素替换为另一个值

```c++
//复制范围的元素到始于 d_first 的范围，并以 new_value 替换所有满足特定判别标准的元素。
//替换所有等于 old_value 的元素。
OutputIt replace_copy( InputIt first, InputIt last, OutputIt d_first, const T& old_value, const T& new_value );

//替换所有函数 p 对其满足 true 的元素。
OutputIt replace_copy_if( InputIt first, InputIt last, OutputIt d_first,UnaryPred p, const T& new_value );
```

### 生成

1.填充固定值

```c++
// 将给定值复制赋给一个范围中的每个元素
void fill(ForwardIt first, ForwardIt last, const T& value );
ForwardIt fill_n( ForwardIt first, Size count, const T& value )
```

1. 使用函数生成的结果赋值

  ```c++
//给定函数对象 g 所生成的值赋值范围中的每个元素。
//std::generate(v.begin(), v.end(), [n = 0] () mutable { return n++; });
  template< class ForwardIt, class Generator >
void generate( ForwardIt first, ForwardIt last, Generator g );

OutputIt generate_n( OutputIt first, Size count, Generator g );
  ```

### 移除

 移除所有满足条件的元素

  ```c++
//移除所有满足条件的元素，并返回范围新结尾的尾后迭代器。
ForwardIt remove( ForwardIt first, ForwardIt last, const T& value );

ForwardIt remove_if( ForwardIt first, ForwardIt last, UnaryPred p );

//将范围元素复制到另外一个区间，并忽略满足条件的元素
OutputIt remove_copy( InputIt first, InputIt last,
                      OutputIt d_first, const T& value )
OutputIt remove_copy_if( InputIt first, InputIt last,
                         OutputIt d_first, UnaryPred p );
  ```

 移除每个连续的元素组中除第一个元素外的所有元素

  ```C++
ForwardIt unique( ForwardIt first, ForwardIt last );

ForwardIt unique( ForwardIt first, ForwardIt last, BinaryPred p );


OutputIt unique_copy( InputIt first, InputIt last,
                    OutputIt d_first );

OutputIt unique_copy( InputIt first, InputIt last,
                    OutputIt d_first, BinaryPred p );
  ```

### 改变顺序  

1. 逆转范围中的元素顺序

  ```c++
void reverse( BidirIt first, BidirIt last );

OutputIt reverse_copy( BidirIt first, BidirIt last, OutputIt d_first );
  ```

1. 旋转范围中的元素顺序

  ```c++
//进行元素范围上的左旋转。
ForwardIt rotate( ForwardIt first, ForwardIt n_first, ForwardIt last);

OutputIt rotate_copy( ForwardIt first, ForwardIt n_first,ForwardIt last, OutputIt d_first);

// 指定旋转n个位置
ForwardIt shift_left(ForwardIt first, ForwardIt last,
                       ifference_type n );
ForwardIt shift_right(ForwardIt first, ForwardIt last,
                       ifference_type n );
  ```

1. 随机排序

  ```c++
  void random_shuffle(RandomIt first, RandomIt last);
  
  //随机数生成器为函数对象 r
  template< class RandomIt, class RandomFunc >
  void random_shuffle( RandomIt first, RandomIt last, RandomFunc&& r );
  
  // 随机数生成器为函数对象 g 
  template< class RandomIt, class URBG >
  void shuffle( RandomIt first, RandomIt last, URBG&& g );
  ```

1. 采样

从序列 中（不重复地）随机选择 n 个元素，并将这些选定的元素写入输出迭代器 out。随机数使用随机数生成器 g 生成。

```c++
template< class PopulationIt, class SampleIt, class Distance, class URBG >
SampleIterator sample( PopulationIt first, PopulationIt last, SampleIt out, Distance n, URBG&& g );
```

```c++
std::string in {"ABCDEFGHIJK"}, out;
std::sample(in.begin(), in.end(), std::back_inserter(out), 4,std::mt19937{std::random_device{}()});
std::cout << "Four random letters out of " << in << " : " << out << '\n';
```
