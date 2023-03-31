[TOC]
[OS,shutil,glob,multiprocessing,threading,random,other]

# OS

| 模块/方法 | 作用 | 备注 |
|---|---|---|
| os.getcwd() | 返回当前工作目录 |  |
| os.listdir(path) | 列举指定目录中的文件名和目录名 |  |
| os.mkdir(path) | 创建单层目录 |  |
| os.makedirs(path,exist_ok=False) | 递归创建目录 |  |
| os.remove(path) | 删除文件 |  |
| os.rmdir(path) | 删除单层目录 |  |
| os.removedirs() | 递归删除目录 |  |
| os.rename(old,new) | 将老的文件名或目录重新命名为新的文件名或目录 |  |
| os.path.split(path)  | 将path分割成目录和文件名二元组返回 |  |
| os.path.dirname(path) | 返回path的目录 |  |
| os.path.basename(path)  | 回path最后的文件名 |  |
| os.path.exists(path)  | 如果path存在，返回True；如果path不存在，返回False |  |
| os.path.join(path1[, path2[, …]])  | 将多个路径组合后返回 |  |
| os.path.isdir(path) | 是否为目录  |  |
| os.path.isfile(path) | 是否为文件 |  |
| os.path.splitext(path) | 把扩展名和其他字符分开 | |
| os.path.getsize(path)      | 返回path对应文件的大小，以字节为单位<br/>>>>os.path.getsize("D:/PYE/file.txt")<br/>180768 |
|os.getcwd()，os.path.abspath('.')，os.path.abspath(os.curdir)|获取当前文件路径|

# shutil

| 模块/方法 | 作用 | 备注 |
|---|---|---|
| shutil.copyfile(src, dst) | 复制文件 |  |
| shutil.copy(src, dst) | 拷贝文件和权限 |  |
| shutil.rmtree(dir) | 递归的去删除文件 |  |
| shutil.move(src, dst) | 移动文件 |  |

# glob

| 模块/方法 | 作用 | 备注 |
|---|---|---|
| glob.glob(source,recursive=False) | 匹配满足条件的文件 | "glob.glob('dir/*') 星号(*)匹配零个或多个字符 ,如果recursive=True,则递归寻找，此时source格式应为"./**/file"|
| glob.glob('dir/file?.txt') 问号(?)匹配任何单个的字符  |
| glob.glob('dir/*[0-9].*') 匹配一个特定的字符，可以使用一个范围" |

# random

| 模块/方法 | 作用 | 备注 |
|---|---|---|
random.random()|从(0,1)均匀分布随机取数|
random.chioce(dict)|从列表随机取个元素|
random.shuffle(dict)|打乱列表顺序
random.sample(dict,n)|随机采样n个元素

# 多进程和多线程

## multiprocessing

### pool.apply_async

**场景**：输入参数只有1个或0个，手动分配数据

```python
import multiprocessing
import time
 
def func(msg):
    print("msg:", msg)
    time.sleep(1)
    print("end")
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 2)
    for i in range(2):
        msg = "hello %d" %(i)
        pool.apply_async(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
 
    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("Sub-process(es) done.")
 
# 输出
# Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~
# msg: hello 0
# msg: hello 1
# end
# end
# Sub-process(es) done.


```

### pool.map_async

**场景**：输入参数只有1个或0个，自动分配数据

```python
import multiprocessing
import time
 
def func(msg):
    print("msg:", msg)
    time.sleep(2)
    print("end")
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(2)
    pool.map_async(func, range(5))
 
    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()
    print("Sub-process(es) done.")
 
# 输出：
# Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~
# msg: 0
# msg: 1
# end
# end
# Sub-process(es) done.

```

### pool.starmap_async 

**场景**：自动分配数据，支持多个参数

```python
import multiprocessing
import time
 
def func(msg1, msg2):
    print("msg1:", msg1, "msg2:", msg2)
    time.sleep(2)
    print("end")
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(2)
    msgs = [(1, 1), (2, 2)]
    pool.starmap_async(func, msgs)
 
    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()
    print("Sub-process(es) done.")
 
# 输出：
# Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~
# msg1: 1 msg2: 1
# msg1: 2 msg2: 2
# end
# end
# Sub-process(es) done.
##
```

### 多进程通信和处理文件的demo

```python
import os
from multiprocessing import Pool, Manager

def process_file(file_path, result_dict):
    # 处理单个文件的函数
    print(f"Processing file {file_path}")
    # ...

    # 记录处理结果到共享字典中
    result_dict[file_path] = result

if __name__ == '__main__':
    # 获取待处理文件列表
    file_list = []
    for root, dirs, files in os.walk('data/'):
        for file in files:
            if file.endswith('.txt'):
                file_list.append(os.path.join(root, file))

    # 使用进程池并发处理文件，并且利用 Manager 共享数据
    num_processes = os.cpu_count()
    with Manager() as manager:
        result_dict = manager.dict()
        with Pool(num_processes) as pool:
            pool.starmap(process_file, [(file_path, result_dict) for file_path in file_list])

    # 输出处理结果
    for file_path, result in result_dict.items():
        print(f"{file_path}: {result}")

```

## threading

```python
"""
使用锁实现线程同步
"""
import time
import threading

# 创建锁
lock = threading.Lock()

# 全局变量
global_resource = [None] * 5


def change_resource(para, sleep):
    # 请求锁
    lock.acquire()

    # 这段代码如果不加锁，第一个线程运行结束后global_resource中是乱的，输出为：修改全局变量为： ['hello', 'hi', 'hi', 'hello', 'hello']
    # 第二个线程运行结束后，global_resource中还是乱的，输出为：修改全局变量为： ['hello', 'hi', 'hi', 'hi', 'hi']
    global global_resource
    for i in range(len(global_resource)):
        global_resource[i] = para
        time.sleep(sleep)
    print("修改全局变量为：", global_resource)

    # 释放锁
    lock.release()


def main():
    thread_hi = threading.Thread(target=change_resource, args=('hi', 2))
    thread_hello = threading.Thread(target=change_resource, args=('hello', 1))
    thread_hi.start()
    thread_hello.start()


if __name__ == '__main__':
    main()
```

# functools

| 模块/方法 | 作用 | 备注 |
|---|---|---|
cmp_to_key|为sorted()函数自定义比较方法|
reduce|对列表逐元素数学操作|
partial|基于现有函数固定参数生成新的可调用对象|

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

# time

见 [python.ipynb](/notebook/python/ipy/python.ipynb)

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
