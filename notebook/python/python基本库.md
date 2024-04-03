<!-- TOC -->
- [OS](#os)
- [shutil](#shutil)
- [glob](#glob)
- [random](#random)
- [多进程和多线程](#多进程和多线程)
- [functools](#functools)
- [time](#time)
- [itertools](#itertools)
- [collection](#collection)
    - [Counter](#counter)
    - [defaultdict](#defaultdict)
    - [namedtuple](#namedtuple)
    - [ChainMap](#chainmap)
- [difflib](#difflib)
- [other](#other)



# OS

| 模块/方法 | 作用 ||
|---|---|---|
| os.getcwd() | 返回当前工作目录 |  |
| os.path.abspath() | 返回绝对路径 |  |
| os.listdir(path) | 列举指定目录中的文件名和目录名 |  |
| os.mkdir(path) | 创建单层目录 |  |
| os.makedirs(path,exist_ok=False) | 递归创建目录 |  |
| os.remove(path) | 删除文件 |  |
| os.rmdir(path) | 删除单层目录 |  |
| os.removedirs() | 递归删除目录 |  |
| os.rename(old,new) | 将老的文件名或目录重新命名为新的文件名或目录 |  |
| os.path.split(path) | 将path分割成目录和文件名二元组返回 |  |
| os.path.dirname(path) | 返回path的目录 |  |
| os.path.basename(path) | 回path最后的文件名 |  |
| os.path.exists(path) | 如果path存在，返回True；如果path不存在，返回False |  |
| os.path.join(path1[, path2[, …]]) | 将多个路径组合后返回 |  |
| os.path.isdir(path) | 是否为目录 |  |
| os.path.isfile(path) | 是否为文件 |  |
| os.path.splitext(path) | 把扩展名和其他字符分开 |  |
| os.path.getsize(path) | 返回path对应文件的大小，以字节为单位<br/>>>>os.path.getsize("D:/PYE/file.txt")<br/>180768 |  |
| os.path.relpath(path1,path2) | 取path2相对path1的相对路径 |  |
| os.getcwd()，os.path.abspath('.')，os.path.abspath(os.curdir) | 获取当前工作路径 | 可以使用`print(__file__)`,`__dir__ = os.path.dirname(os.path.abspath(__file__))`来获取当前py文件的路径,使用sys.argv[0]获取原始执行py文件的路径 |


# shutil

| 模块/方法                     | 作用                 | 备注  |
| ------------------------- | ------------------ | --- |
| shutil.copyfile(src, dst) | 复制文件               |     |
| shutil.copy(src, dst)     | 拷贝文件和权限            |     |
| shutil.rmtree(dir)        | 递归的去删除文件           |     |
| shutil.move(src, dst)     | 移动文件               |     |
| shutil.copytree(src, dst) | 迭代复制文件，如果dst已存在则报错 |     |

# glob

| 模块/方法                                         | 作用        | 备注                                                                                 |
| --------------------------------------------- | --------- | ---------------------------------------------------------------------------------- |
| glob.glob(source,recursive=False)             | 匹配满足条件的文件 | "glob.glob('dir/*') 星号(*)匹配零个或多个字符 ,如果recursive=True,则递归寻找，此时source格式应为"./**/file" |
| glob.glob('dir/file?.txt') 问号(?)匹配任何单个的字符     |           |                                                                                    |
| glob.glob('dir/*[0-9].*') 匹配一个特定的字符，可以使用一个范围" |           |                                                                                    |

# random

| 模块/方法                 | 作用             |
| --------------------- | -------------- |
| random.random()       | 从(0,1)均匀分布随机取数 |
| random.chioce(dict)   | 从列表随机取个元素      |
| random.shuffle(dict)  | 打乱列表顺序         |
| random.sample(dict,n) | 随机采样n个元素       |

# 多进程和多线程

# functools

| 模块/方法           | 作用                                |
| --------------- | --------------------------------- |
| cmp_to_key      | 为sorted()函数自定义比较方法                |
| reduce          | 对列表逐元素数学操作                        |
| partial         | 基于现有函数固定参数生成新的可调用对象               |
| @warps          | 将 被修饰的函数(wrapped) 的一些属性值赋值给 修饰器函数 |
| @total_ordering | 用于自动实现类的比较运算                      |

```python
#cmp_to_key
from functools import cmp_to_key
a = [(9, 4), (2, 10), (4, 3), (3, 6),(9, 2)]
def cmp(x,y):
    if x[0] < y[0]:
        return 1
    elif x[0] > y[0]:
         return -1
    else:
        if x[1] > y[1]:
            return 1
        else:
            return -1
print(sorted(a,key=cmp_to_key(cmp)))
```

```python
# reduce(function, sequence[, initial]) -> value
"""
Apply a function of two arguments cumulatively to the items of a sequence,
from left to right, so as to reduce the sequence to a single value.
For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
of the sequence in the calculation, and serves as a default when the
sequence is empty.
"""
from functools import reduce 
reduce(lambda x,y: x+y, [1, 2, 3]) 
#输出 6 
reduce(lambda x, y: x+y, [1,2,3], 9) 
#输出 15 
reduce(lambda x,y: x+y, [1, 2, 3], 7) 
#输出 13
```

```python
#functools.partial
import functools

def add(a, b):
    print("当前结果值", a+b)

add = functools.partial(add, 1)
add(2)
```

```python

#functools.wraps
from functools import wraps

def wrapper(func):
    @wraps(func)
    def inner_function():
        pass
    return inner_function

@wrapper
def wrapped():
    pass

print(wrapped.__name__)
# wrapped
```

```python
"""
给定一个类，这个类定义了一个或者多个比较排序方法，这个类装饰器将会补充其余的比较方法，减少了自己定义所有比较方法时的工作量。

被修饰的类必须至少定义  __lt__()， __le__()，__gt__()，__ge__() 中的一个，同时，被修饰的类还应该提供 __eq__()方法。
"""
from functools import total_ordering


@total_ordering
class Person:
    # 定义相等的比较函数
    def __eq__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))

    # 定义小于的比较函数
    def __lt__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))


p1 = Person()
p2 = Person()

p1.lastname = "123"
p1.firstname = "000"

p2.lastname = "1231"
p2.firstname = "000"

print(p1 < p2)
print(p1 <= p2)  #
print(p1 == p2)
print(p1 > p2)
print(p1 >= p2)  #

'''
True
True
False
False
False
'''
```

# time

见 [python.ipynb](ipynb/python.ipynb)

# itertools

| 模块/方法                                      | 作用                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------- |
| combinations(iterable,r)                   | 返回的是可迭代对象所有的长度为 r 的子序列                                                |
| permutations(iterable,r=None)              | 返回的是可迭代元素中的一个排列组合                                                     |
| combinations_with_replacement(iterable, r) | 返回一个可与自身重复的元素组合                                                       |
| product(*iterables, repeat=1)              | 返回可迭代对象的笛卡儿积，等价于`((x,y) for x in A for y in B)`                       |
| cycle(iterable)                            | 无限迭代器                                                                 |
| chain(*iterables)                          | 可以把多个可迭代对象组合起来，形成一个更大的迭代器                                             |
| groupby(iterable,key=None)                 | 可以把相邻元素按照 key 函数分组，并返回相应的 key 和 groupby，如果key函数为 None，则只有相同的元素才能放在一组。 |
| accumulate(iterable [,func])               | 可以计算出一个迭代器，这个迭代器是由特定的二元函数的累计结果生成的，如果不指定的话，默认函数为求和函数。                  |
| pairwise(iterable)                         | `pairwise('ABCDEFG') --> AB BC CD DE EF FG`                           |

# collection

### Counter

对列表计数

```python
from collection import Counter
L = ['red', 'blue', 'red', 'green', 'blue', 'blue'] 
Counter(L)
#{'red': 2, 'blue': 3, 'green': 1}
Counter(L).most_common(2)
#{'red': 2, 'blue': 3}
```

### defaultdict

更加易用的dict

```python
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1
sorted(d.items())
#[('i', 4), ('m', 1), ('p', 2), ('s', 4)]
```

### namedtuple

可命名元祖

```python

from collections import namedtuple

Color = namedtuple("Color", "r g b alpha")

a=Color(r=50, g=205, b=50, alpha=0)
b=Color(50, 0, 0, 0)
print(a.r) #打印指定元素

c=b._asdict() #转为dict形式
tuple(b) #转为tuple形式

d=b._replace(b=100) #从已有元组构建出新的元组

print(c._fields) #返回元素名


Color1 = namedtuple("Color", c)#从dict中创建namedtuple
e = Color1(**c)


Account = namedtuple('Account', ['type', 'balance','c'], defaults=[1,0]) #设置默认值
print(Account._field_defaults) #{'balance': 1, 'c': 0}
print(Account('premium')) #Account(type='premium', balance=1, c=0)
```

### ChainMap

适用范围：

- 通过多个字典搜索
- 提供链缺省值
- 经常计算字典子集的性能关键的应用程序

特性：

- 找到一个就不找了：这个列表是按照第一次搜索到最后一次搜索的顺序组织的，搜索查询底层映射，直到一个键被找到。
- 更新原始映射：不同的是，写，更新和删除只操作第一个映射。
- 支持所有常用字典方法。

```python
from collections import ChainMap 
baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
NewMap = ChainMap(adjustments, baseline)

print(NewMap)
#ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})
print(list(ChainMap(adjustments, baseline)))
#['music', 'art', 'opera']
#存在重复元素时，也不会去重

NewMap1=NewMap.new_child(m={'key_new':888}) #把NewMap作为父节点并添加新的字典并创建子节点ChainMap
#ChainMap({'key_new': 888}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

NewMap1.parents #返回父节点

NewMap1['art']='abc' #只会改变第一个字典
#ChainMap({'key_new': 888, 'art': 'abc'}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

print(NewMap1['art']) #'abc'
#按字典顺序、映射顺序依次搜索，搜索第一个key即停止

```

# difflib

比较字符串差异

```python
text1 = "hello"
text2 = "ciallo"
diff = difflib.ndiff(text1, text2)#得到的是如何操作可以由text1变为text2的过程，逐字符比较
print('\n'.join(diff))
similarity = difflib.SequenceMatcher(None, text1, text2).ratio()#计算字符串相似度

with open('file1.txt') as file1, open('file2.txt') as file2:
    diff = difflib.ndiff(file1.readlines(), file2.readlines())
    print('\n'.join(diff))  ##逐行比较文件差异

```

比较列表的差异

```python
import difflib
list1 = ['apple', 'a','banana', 'cherry']
list2 = ['apple', 'b','banana', 'kiwi']
diff = difflib.ndiff(list1, list2)#得到的是如何操作可以由list1变为list2的过程
```

获取两个字符串的相似块

```python
import difflib
text1 = "hello world"
text2 = "there asd hello "
blocks = difflib.SequenceMatcher(None, text1, text2).get_matching_blocks()
#[Match(a=0, b=10, size=6), Match(a=11, b=16, size=0)] 
#可以用blocks[0].a来访问
lcs = difflib.SequenceMatcher(None, text1, text2).find_longest_match(0, len(text1), 0, len(text2))
#返回最大相似块 Match(a=0, b=10, size=6)
```

# other

- print

1. `%`

```python
name = "Alice"
age = 20
print("Hello, %s. You are %d years old." % (name, age))
# Hello, Alice. You are 20 years old.
```

2. `.format`

```python
name = "Bob"
age = 21
print("Hello, {}. You are {} years old.".format(name, age))
# Hello, Bob. You are 21 years old.
print("Hello, {0}. You are {1} years old.".format(name, age))
# Hello, Bob. You are 21 years old.
print("Hello, {name}. You are {age} years old.".format(name=name, age=age))
# Hello, Bob. You are 21 years old.

num = 0.123456
print("%.2f%%" % num) # 输出0.12%
```

3. f-string

[](ipynb\format.ipynb)

```python
name = "Charlie"
age = 22
print(f"Hello, {name}. You are {age} years old.")
# Hello, Charlie. You are 22 years old.

num = 0.123456
print("{:.2f}%".format(num)) # 输出0.12%
print(f"{num:.2f}%") # 输出0.12%
```

- read
read()  ： 一次性读取整个文件内容。推荐使用read(size)方法，size越大运行时间越长  
readline()  ：每次读取一行内容。内存不够时使用，一般不太用  
readlines()   ：一次性读取整个文件内容，并按行返回到list，方便我们遍历
