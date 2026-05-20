- [multiprocessing](#multiprocessing)
  - [Process](#process)
  - [Pool](#pool)
    - [pool.apply\_async](#poolapply_async)
    - [pool.map\_async](#poolmap_async)
    - [pool.starmap\_async](#poolstarmap_async)
    - [多进程处理文件的demo](#多进程处理文件的demo)
    - [imap 和 imap\_unordered](#imap-和-imap_unordered)
  - [Queue](#queue)
  - [Pipe](#pipe)
  - [ThreadPool](#threadpool)
- [Manager](#manager)
  - [dict、list](#dictlist)
  - [自定义Manager](#自定义manager)
- [threading](#threading)

# 1.**multiprocessing**

## Process

适用于相对独立的任务，比如计时器

```python
import multiprocessing as mp


def func(id):  
    print(f'id {id}\n')

def run__process():  # 这里是主进程
    process = [mp.Process(target=func, args=(1,)),
               mp.Process(target=func, args=(2,)), ]
    [p.start() for p in process]  # 开启了两个进程
    print("start")
    [p.join() for p in process]   # 等待两个进程依次结束
    print("end")

if __name__ =='__main__':
    run__process()
```

## Pool

适用于数据批量处理的任务，需要大量进程干同一件事的情况

### pool.apply_async

**场景**：手动分配数据,子进程函数是无参或1参

```python
import multiprocessing as mp
import time
 
def func(msg):
    print("msg:", msg)
    time.sleep(1)
    print("end")
 
if __name__ == "__main__":
    pool = mp.Pool(processes = 2)
    for i in range(5):
        msg = "hello %d" %(i)
        pool.apply_async(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
 
    print("start")
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("done.")
 
# 输出
# start
# msg: hello 0
# msg: hello 1
# end
# end
# done.


```

### pool.map_async

**场景**：自动分配数据,数据是迭代器，子进程函数是无参或1参

```python
import multiprocessing as mp
import time
 
def func(msg):
    print("msg:", msg)
    time.sleep(2)
    print("end")
 
if __name__ == "__main__":
    pool = mp.Pool(2)
    pool.map_async(func, range(5))
 
    print("start")
    pool.close()
    pool.join()
    print("done.")
 
# 输出：
# start
# msg: 0 
# msg: 1

# end
# end
# msg: 2
# msg: 3
# end
# end

# msg: 4
# end
# done.

```

### pool.starmap_async

**场景**：自动分配数据，数据是迭代器,子进程函数支持多个参数

```python
import multiprocessing as mp
import time
 
def func(msg1, msg2):
    print("msg1:", msg1, "msg2:", msg2)
    time.sleep(2)
    print("end")
 
if __name__ == "__main__":
    pool = mp.Pool(2)
    msgs = [(1, 1), (2, 2)]
    pool.starmap_async(func, msgs)
 
    print("start")
    pool.close()
    pool.join()
    print("done.")
 
# 输出：
# start
# msg1: 1 msg2: 1
# msg1: 2 msg2: 2
# end
# end
# done.
##
```

### 多进程处理文件的demo

```python
import os
import multiprocessing as mp
import tqdm


def process_file(file_path):
    return file_path


def process(args):
    file_list, start, end = args
    result = []
    # 处理单个文件的函数
    for i in tqdm.tqdm(range(end - start)):
        result.append(process_file(file_list[start + i]))
    return result


if __name__ == "__main__":
    # 获取待处理文件列表
    file_list = []
    for root, dirs, files in os.walk(r"D:\project"):
        for file in files:
            file_list.append(os.path.join(root, file))

    num_processes = 2
    each_process_files = len(file_list) // num_processes
    pool = mp.Pool(num_processes)
    asyncResult = []
    for i in range(num_processes):
        start = each_process_files * i
        end = each_process_files * (i + 1) if i<num_processes-1 else len(file_list)
        asyncResult.append(pool.apply_async(process, [(file_list, start, end)]))
      
    pool.close()
    pool.join()
    # 输出处理结果
    for result in asyncResult:
        print(result.get()[0])

```

### imap 和 imap_unordered

> - map将改可迭代的对象转换为列表，并分解为块发送到各个进程中。将该对象分解为块比一次直接执行一个对象要更好。但是需要非常高的内存成本，因为整个列表需要保存在内存中。
> - imap不会将您提供的可迭代对象变为列表，也不会将其分解为块(默认情况下)。它将一次遍历该对象的一个元素，并将它们分别发送到工作进程。这也意味着迭代的性能较慢，因为缺少分块。但是，可以通过传递大于默认值1的chunksize参数来减轻这种情况。
> - 对于imap/imap_unordered,可以在立即开始接收进程的结果，而不必等待所有进程完成工作。 使用map_async，虽然也会立即返回AsyncResult，但是在完成所有对象之前，会阻塞。
> - imap和imap_unordered会立即返回结果。使用imap，结果将在它们准备就绪时从迭代中产生，同时仍保留输入可迭代的顺序。使用imap_unordered，无论输入可迭代的顺序如何，只要它们准备好就会产生结果。

所以，使用imap/imap_unordered替代map_async主要的原因有：所以，使用imap/imap_unordered替代map_async主要的原因有：

1. 可迭代对象足够大，将其转换为列表会导致您耗尽/使用太多内存。
2. 希望能够在完成所有结果之前就先处理结果。

```python
#imap
import multiprocessing as mp
import time
 
def func(msg):
    print("msg: ", msg)
    time.sleep(4-msg)
    return msg
 
if __name__ == "__main__":
    pool = mp.Pool(3)
    results = pool.imap(func, range(3))
    for res in results:
        print("res: ",res)
 
    print("start")
    pool.close()
    pool.join()
 
    print("done.")
 
# 输出
# msg: 0
# msg: 1
# msg: 2
# res: 0
# res: 1
# res: 2
# start
# done.
```

```python
#imap_unordered
import multiprocessing as mp
import time
 
def func(msg):
    print("msg: ", msg)
    time.sleep(4-msg)
    return msg
 
if __name__ == "__main__":
    pool = mp.Pool(3)
    results = pool.imap_unordered(func, range(3))
    for res in results:
        print("res: ", res)
 
    print("start")
    pool.close()
    pool.join()
 
    print("done.")
 
# 输出
# msg: 0
# msg: 1
# msg: 2
# res: 2
# res: 1
# res: 0
# start
# done.
```

## Queue

Queue 类可以方便地实现进程间通信，用于在多个进程之间传递数据。例如，如果需要在一个进程中生成数据，然后将其传递给另一个进程进行处理，可以使用 Queue 类。
需要注意以下几点:

- 如果 Queue 已满，put() 方法会阻塞，直到有空间为止。可以使用 put_nowait() 方法，以避免阻塞。
- 如果 Queue 为空，get() 方法会阻塞，直到有数据为止。可以使用 get_nowait() 方法，以避免阻塞。

```python
import multiprocessing as mp


def producer(queue):
    """producer function"""
    for i in range(10):
        queue.put(i)
    queue.put(None)


def consumer(queue):
    """consumer function"""
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)


if __name__ == "__main__":
    queue = mp.Queue()
    p1 = mp.Process(target=producer, args=(queue,))
    p2 = mp.Process(target=consumer, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

```

## Pipe

Pipe 类可以用于在两个进程之间建立一个管道，用于在两个进程之间传递数据。

```python
import time
import multiprocessing as mp

def func_pipe1(conn, p_id):
    conn.send(f"{p_id}_send1")
    print(f"{p_id} send1\n")

    time.sleep(0.1)
    conn.send(f"{p_id}_send2")
    print(f"{p_id} send2\n")

    time.sleep(0.1)
    rec = conn.recv()
    print(f"{p_id} recv {rec}\n")

    time.sleep(0.1)
    rec = conn.recv()
    print(f"{p_id} recv {rec}\n")


def func_pipe2(conn, p_id):
    conn.send(p_id)
    print(f"{p_id} send\n")
    time.sleep(0.1)
    rec = conn.recv()
    print(f"{p_id} recv {rec}\n")


if __name__ == "__main__":

    conn1, conn2 = mp.Pipe()

    process = [
        mp.Process(target=func_pipe1, args=(conn1, "I1")),
        mp.Process(target=func_pipe2, args=(conn2, "I2")),
        mp.Process(target=func_pipe2, args=(conn2, "I3")),
    ]

    [p.start() for p in process]
    [p.join() for p in process]


```

Pipe还有 duplex参数 和 poll() 方法 需要了解。默认情况下 duplex==True，若不开启双向管道，那么传数据的方向只能 conn1 ← conn2 。conn2.poll()==True 意味着可以马上使用 conn2.recv() 拿到传过来的数据。conn2.poll(n) 会让它等待n秒钟再进行查询

```python
from multiprocessing import Pipe

conn1, conn2 = Pipe(duplex=True)  # 开启双向管道，管道两端都能存取数据。默认开启
# 
conn1.send('A')
print(conn1.poll())  # 会print出 False，因为没有东西等待conn1去接收
print(conn2.poll())  # 会print出 True ，因为conn1 send 了个 'A' 等着conn2 去接收
print(conn2.recv(), conn2.poll(2))  # 会等待2秒钟再开始查询，然后print出 'A False'
```

## ThreadPool（少用）

```python
from multiprocessing.pool import ThreadPool
import time
from tqdm import tqdm
def  func(num):
    time.sleep(0.1)
    if num%3==0:
        return num*10
with ThreadPool(2) as pool:
    results = pool.imap(func=func, iterable=range(10))
    pbar = tqdm(results, total=10,ncols=100)
    for result in pbar:
        pbar.desc = f'{result=}'
    pbar.close()
```

## Manager（不要用）

这个是共享内存的做法，不安全，而且受到锁限制，不会太快

### dict、list

```python
import multiprocessing

test_dict={}
test_dict['test'] ={}

def test(idx, test_dict1):
    
    test_dict1[idx] = idx
    test_dict['test'][idx] = idx # 字典key对应的地址内容不会被修改

if __name__ == '__main__':
    
    mg = multiprocessing.Manager()
    dicMP = mg.dict()  # 多进程，共享字典

    pool = multiprocessing.Pool(4)
    for i in range(10):
        pool.apply_async(test, args=(i, dicMP))

    pool.close()
    pool.join()
    print(dicMP)
    print(test_dict)

```

### 自定义Manager

自定义共享内存，下面的代码可以实现一个共享的set，实际效率很慢

```python
import multiprocessing as mp
from multiprocessing.managers import BaseManager
import random
import tqdm
import time


class shareSet:

    def __init__(self,):
        self.__save=set()

    def addnum(self, x):
        if x not in self.save:
            self.__save.add(x)
            return True
        return False
    
    def getback(self):
        return self.__save 
    

class MyManager(BaseManager):
    pass


MyManager.register('myset', shareSet)


def func(my_set,num):
    i=0
    prog = tqdm.tqdm(total=num)
    while(i<num):
        time.sleep(0.1)
        randint = random.randint(0,30)
        if my_set.addnum(randint):
            i+=1
            prog.update(1)

if __name__ == '__main__':
    with MyManager() as manager:
        
        myset = manager.myset()

        pool = mp.Pool(processes=3)
        for i in range(0, 3):
            pool.apply_async(func, (myset,5))
        pool.close()
        pool.join()

        res = myset.getback()
        print(res)
        print(len(res))


```

# 2.**threading**

截止python3.13，线程受GIL锁限制，对于 CPU 密集型任务来说，没啥用。

线程比较适用于 I/O 密集型的任务，如文件操作或发送网络请求，在此类任务会释放GIL锁

## 简单使用

1.线程同步

```python
import threading
import time

def crawl(link, delay=3):
    print(f"crawl started for {link}")
    time.sleep(delay)  # 阻塞 I/O (模拟网络请求)
    print(f"crawl ended for {link}")

links = [
    "https://python.org",
    "https://docs.python.org",
    "https://peps.python.org",
]

# 针对每个链接启动线程
threads = []
for link in links:
    # 使用 `args` 传入位置参数并使用 `kwargs` 传入关键字参数
    t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
    threads.append(t)

# 启动每个线程
for t in threads:
    t.start()

# 等待所有线程结束
for t in threads:
    t.join()
```

2.线程间通信

```python
import threading
import queue

def worker(q):
    while not q.empty():
        item = q.get()
        print(f"处理项目: {item}")
        q.task_done()

# 创建一个队列并填充数据
q = queue.Queue()
for i in range(10):
    q.put(i)

# 创建线程实例
thread1 = threading.Thread(target=worker, args=(q,))
thread2 = threading.Thread(target=worker, args=(q,))
# 启动线程
thread1.start()
thread2.start()
# 等待队列中的所有项目被处理完毕
q.join()
print("所有项目处理完毕")
```

## `Lock`

1️⃣ `threading.Lock`

1. 作用
   - Lock 是最基本的互斥锁，用来保护共享资源
   - **同一时间只能被一个线程持有**，其他线程必须等待
2. 常用方法
   - `lock.acquire(blocking=True, timeout=-1)`：尝试获取锁
   - `lock.release()`：释放锁
   - `with lock:` 自动 acquire/release
3. 适合场景
   - 多线程访问共享变量、列表、字典等数据结构时，保证数据完整性
   - 只需保证 **同一时刻只有一个线程操作共享资源**
4. 特点
   - 非递归锁：同一个线程不能重复 acquire，否则会死锁
   - 线程之间互斥访问，保证安全，但可能阻塞其他线程

2️⃣ `threading.RLock`（可重入锁）

1. 作用
   - RLock = Recursive Lock，可重入锁
   - **同一线程可以多次 acquire**，每 acquire 一次，必须 release 一次才能完全释放
2. 常用方法
   - 同 Lock，一样支持 `acquire()` / `release()` / `with rlock:`
3. 适合场景
   - 同一线程可能 **嵌套调用需要锁的函数**
   - 避免死锁，例如递归函数访问共享资源，或者函数 A 调用函数 B，都要加锁
4. 特点
   - 线程安全 + 允许同一线程多次获取锁
   - 其他线程仍然被阻塞，直到最后一次 release 完全释放锁



```python
import threading

lock = threading.Lock()

def func1():
    lock.acquire()
    print("第一次 acquire 成功")
    lock.acquire()  # ❌ 死锁
    print("第二次 acquire 成功")
    lock.release()


rlock = threading.RLock()

def func2():
    rlock.acquire()
    print("第一次 acquire 成功")
    rlock.acquire()
    print("第二次 acquire 成功")
    rlock.release()
    rlock.release()
    
threading.Thread(target=func1).start()
threading.Thread(target=func2).start()
```



## `Event`

1. `threading.Event()`用来在 多个线程之间传递信号：
   - `.wait()`：线程阻塞等待事件被触发
   - `.set()`：触发事件，唤醒所有等待的线程
   - `.clear()`：重置事件，回到未触发状态

2. 适合需要多个线程等待某个条件,再执行的场景：

   - 比如：主线程初始化资源，所有工作线程等资源就绪再开始

3. 与锁不同：

   - 锁是互斥的（只能一个线程拿到），
   - Event 是广播型的，触发后 **所有等待的线程都会被唤醒**

```python
import threading
import time

# 创建一个 Event 对象
start_event = threading.Event()

def worker(n):
    print(f"Worker-{n} 等待开始信号...")
    start_event.wait()  # 阻塞，直到 Event 被 set
    print(f"Worker-{n} 收到开始信号，开始工作！")
    time.sleep(1)  # 模拟工作
    print(f"Worker-{n} 工作完成")

# 创建几个线程
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

# 模拟主线程准备工作
print("主线程准备工作...")
time.sleep(2)

# 发送开始信号
print("主线程发送开始信号！")
start_event.set()  # 所有等待的线程立即被唤醒

# 等待所有线程完成
for t in threads:
    t.join()

print("所有线程完成")
```

## `Condition`

1. `threading.Condition()` 用来在多个线程之间进行条件同步：

    - `.wait()`：线程在条件不满足时阻塞等待，同时会 **释放锁**，等待其他线程通知
    - `.notify()`：唤醒 **一个** 正在等待该条件的线程（线程会重新获取锁后继续执行）
    - `.notify_all()`：唤醒 **所有** 正在等待该条件的线程
    - 访问条件时通常配合 `with condition:`，自动获取/释放锁

2. 适合需要线程间协调状态或资源的场景：

    - 生产者-消费者模型：消费者等待缓冲区非空，生产者生产后通知
    - 线程等待某个条件满足再执行：如等待共享资源就绪、等待信号量达到指定值
    - 需要在访问共享状态时进行线程安全判断

3. 与锁或 Event 不同：

    - 锁是互斥的，只能一个线程访问共享资源
    - Event 是广播型信号，触发后所有等待线程立即被唤醒
    - Condition 是 **条件同步 + 锁** 的组合：线程可以在条件不满足时等待，等待时自动释放锁，被唤醒后重新获取锁并检查条件

```python
import threading
import time
import random

buffer = []
buffer_size = 5
condition = threading.Condition()

def producer():
    global buffer
    for i in range(10):
        item = f"item-{i}"
        with condition:  # 获取条件锁
            while len(buffer) >= buffer_size:  # 如果缓冲满，等待
                print("生产者等待，缓冲满了...")
                condition.wait()
            buffer.append(item)
            print(f"生产者生产 {item}")
            condition.notify()  # 通知消费者
        time.sleep(random.uniform(0.1, 0.5))

def consumer():
    global buffer
    for i in range(10):
        with condition:  # 获取条件锁
            while not buffer:  # 如果缓冲空，等待
                print("消费者等待，缓冲为空...")
                condition.wait()
            item = buffer.pop(0)
            print(f"消费者消费 {item}")
            condition.notify()  # 通知生产者
        time.sleep(random.uniform(0.2, 0.6))

# 创建线程
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()

t1.join()
t2.join()

print("所有生产消费完成")
```

## `Barrier`

栅栏类提供一个简单的同步原语，用于应对固定数量的线程需要彼此相互等待的情况。线程调用 `wait()` 方法后将阻塞，直到所有线程都调用了 `wait()` 方法。此时所有线程将被同时释放。

这是一个客户端线程与服务端线程同步的例子：

```python
b = Barrier(2, timeout=5)

def server():
    start_server()
    b.wait()
    while True:
        connection = accept_connection()
        process_server_connection(connection)

def client():
    b.wait()
    while True:
        connection = make_connection()
        process_client_connection(connection)
```



## `Timer`

**基本用法**

- ```
  threading.Timer(interval, function, args=None, kwargs=None)
  ```

  - `interval`：延时秒数
  - `function`：延时执行的函数
  - `args` / `kwargs`：传给函数的参数

- `.start()`：启动计时器线程

- `.cancel()`：在计时器触发前取消

**特点**

- Timer 内部是 **单独的线程**，不会阻塞主线程
- 可以重复创建 Timer 实现周期任务，但 **Timer 本身只触发一次**
- 如果需要循环定时任务，可以用 `threading.Timer` 递归调用自己，或者用 `sched` / `TimerThread` / `asyncio`

```python
import threading
import time

def say_hello(name):
    print(f"{time.strftime('%H:%M:%S')} - Hello, {name}!")

# 创建一个 Timer 对象，3 秒后执行 say_hello
t = threading.Timer(3, say_hello, args=("Alice",))

print(f"{time.strftime('%H:%M:%S')} - Timer 启动")
t.start()  # 启动计时器

# 主线程继续执行其他任务
for i in range(3):
    print(f"{time.strftime('%H:%M:%S')} - 主线程工作 {i}")
    time.sleep(1)

# 可选：如果在计时器触发前想取消
# t.cancel()
```

#  3.**concurrent.futures**

```python
def wait_on_future():
    f = executor.submit(pow, 5, 2)
    print(f.result())

executor = ThreadPoolExecutor(max_workers=1)
future = executor.submit(wait_on_future)
future.result()
```

上面代码会死锁，因为concurrent的`future.result()`和asyncio的future不同，该future在获取结果时会同步阻塞。

## `Future `

`concurrent.futures.Future`,将可调用对象封装为异步执行。`Future`实例由 `Executor.submit()`创建，除非测试或自定义异步环境，不应直接创建

| 方法                       | 作用/说明                                                    |
| -------------------------- | ------------------------------------------------------------ |
| `result(timeout=None)`     | 阻塞等待 Future 完成，返回结果；如果任务抛异常，会重新抛出；可选 `timeout` 指定超时 |
| `done()`                   | 返回布尔值，表示 Future 是否已完成（成功或异常）             |
| `cancel()`                 | 尝试取消 Future，如果任务尚未开始执行则取消成功，返回 `True`；否则返回 `False` |
| `cancelled()`              | 返回布尔值，表示 Future 是否被取消                           |
| `exception(timeout=None)`  | 阻塞等待 Future 完成，返回异常对象；如果任务成功返回 `None`；可选 `timeout` 指定超时 |
| `add_done_callback(fn)`    | 注册回调函数，Future 完成后自动调用 `fn(future)`             |
| `set_result(result)`       | **手动完成 Future 并设置结果**（自定义 Future 时使用）       |
| `set_exception(exception)` | **手动完成 Future 并设置异常**（自定义 Future 时使用）       |

下面是手动创建的案例

```python
from concurrent.futures import Future
import threading
import time

# 自定义函数：异步触发某事件，然后完成 Future
def async_task(fut, delay, result):
    print(f"[{time.strftime('%H:%M:%S')}] 任务开始，等待 {delay} 秒")
    time.sleep(delay)  # 模拟耗时操作
    fut.set_result(result)  # 手动设置 Future 结果
    print(f"[{time.strftime('%H:%M:%S')}] 任务完成，Future 已设置结果")

# 手动创建 Future
# .result() 
fut = Future()

# 用线程模拟异步执行
thread = threading.Thread(target=async_task, args=(fut, 2, "Hello Future"))
thread.start()

# 主线程等待 Future 完成
print(f"[{time.strftime('%H:%M:%S')}] 主线程等待 Future 结果")
# 会阻塞，直到通过 set_result() 或 set_exception() 完成
result = fut.result()
print(f"[{time.strftime('%H:%M:%S')}] Future 返回结果: {result}")

thread.join()
```

## `ThreadPoolExecutor`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 模拟耗时任务
def task(x):
    time.sleep(1)
    return x*x

# 后处理函数（callback）
def on_done(fut):
    try:
        result = fut.result()
        print(f"[Callback] 结果：{result}")
    except Exception as e:
        print(f"[Callback] 异常：{e}")

# 创建线程池
with ThreadPoolExecutor(max_workers=3) as executor:
    # 提交任务并注册回调
    futures = []
    for i in range(5):
        fut = executor.submit(task, i)
        fut.add_done_callback(on_done)  # 异步回调
        futures.append(fut)

    print("主线程可以继续做别的事…")

    # 使用 as_completed 顺序处理最先完成的任务
    for fut in as_completed(futures):
        result = fut.result()  # 阻塞直到该 Future 完成
        print(f"[as_completed] 处理最先完成的任务结果: {result}")
```

## `ProcessPoolExecutor`

```python
from concurrent.futures import ProcessPoolExecutor
import os
import time

# 模拟 CPU 密集型任务
def cpu_task(x):
    print(f"进程 {os.getpid()} 正在处理 {x}")
    total = sum(i*i for i in range(10**6))  # 模拟计算
    return x, total

# --------------------------
# 方法 1：使用 submit 提交单个任务
# --------------------------
with ProcessPoolExecutor(max_workers=3) as executor:
    future1 = executor.submit(cpu_task, 1)
    future2 = executor.submit(cpu_task, 2)
    
    # 阻塞获取结果
    result1 = future1.result()
    result2 = future2.result()
    
    print(f"submit 结果: {result1}, {result2}")

# --------------------------
# 方法 2：使用 map 批量提交任务
# --------------------------
inputs = [3, 4, 5]
with ProcessPoolExecutor(max_workers=3) as executor:
    results = executor.map(cpu_task, inputs)  # map 会按顺序返回结果
    
    for res in results:
        print(f"map 结果: {res}")
```

# 4.asyncio

[asyncio](https://docs.python.org/zh-cn/3/library/asyncio.html)维护一个任务队列，当一个任务执行到 `await`（例如等待网络响应）时，它会被挂起，事件循环立即从队列中找出下一个可以运行（就绪）的任务来执行。当被挂起任务的 I/O 操作完成后，事件循环会收到通知，将该任务状态改回就绪，并在未来某个时刻继续执行它。

由于任务全部在同一个线程中，所以任务之间不会遇到GIL锁切换的情况



## 常用

下面以表格形式列出 `asyncio` 中几个最常用的高级函数：

| 函数                                             | 作用                                            | 关键参数                                                     |
| ------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------ |
| `asyncio.run(coro)`                              | 运行顶层协程，启动事件循环                      | `coro`：顶层协程对象                                         |
| `asyncio.create_task(coro)`                      | 把协程丢给事件循环调度，返回 Task 对象          | `coro`：协程                                                 |
| `asyncio.gather(*tasks)`                         | 并发执行多个协程，等所有完成，返回结果列表      | `*tasks`：多个协程或 Task                                    |
| `asyncio.sleep(seconds)`                         | 异步休眠，不阻塞事件循环                        | `seconds`：休眠时间                                          |
| `asyncio.wait(tasks, return_when=ALL_COMPLETED)` | 并发运行任务，按条件返回 `(done, pending)`      | `tasks`：任务集合；`return_when`：何时返回（全部完成/第一个完成等） |
| `asyncio.to_thread(func, *args)`                 | 把普通阻塞函数丢到线程里跑，返回可 await 的协程 | `func`：同步函数；`*args`：参数                              |

```python
import asyncio
import time

# 普通同步函数
def blocking_task(x):
    print(f"{x} 开始阻塞计算")
    time.sleep(2)
    print(f"{x} 阻塞计算完成")
    return x*10

# 异步函数
async def async_task(x):
    print(f"{x} 异步开始")
    await asyncio.sleep(1)
    print(f"{x} 异步结束")
    return x*2

async def main():
    print("=== asyncio.run ===")

    # create_task: 异步任务，立即排队
    t1 = asyncio.create_task(async_task(1))
    t2 = asyncio.create_task(async_task(2))

    # gather: 等待多个任务完成
    results = await asyncio.gather(t1, t2)
    print("gather 结果:", results)

    # asyncio.to_thread: 把阻塞函数放线程跑
    res = await asyncio.to_thread(blocking_task, 3)
    print("to_thread 结果:", res)

    # wait: 按完成顺序处理
    t3 = asyncio.create_task(async_task(4))
    t4 = asyncio.create_task(async_task(5))
    done, pending = await asyncio.wait([t3, t4], return_when=asyncio.FIRST_COMPLETED)
    for fut in done:
        print("wait 最先完成:", fut.result())

# run 顶层协程
asyncio.run(main())
```

## 同步原语

| 类                                          | 干啥的                                         | 示例                                                     |
| ------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| `asyncio.Lock()`                            | 异步互斥锁，同一时间只允许一个协程访问共享资源 | `python lock = asyncio.Lock() \nasync with lock: ...`    |
| `asyncio.Event()`                           | 事件通知，协程可以等待事件触发                 | `python event = asyncio.Event() \nawait event.wait()`    |
| `asyncio.Queue()`                           | 异步队列，协程安全的 FIFO 队列                 | `python queue = asyncio.Queue() \nawait queue.put(item)` |
| `asyncio.wrap_future(future, *, loop=None)` | 将线程/进程池 Future 转成 asyncio Future       | 可以用 `await` 等待池里的 Future，实现异步调用           |

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# 普通阻塞函数
def blocking_task(x):
    print(f"[线程池] 开始计算 {x}")
    time.sleep(2)  # 模拟耗时
    print(f"[线程池] 计算完成 {x}")
    return x * 10

# 异步协程任务
async def worker(name, lock, event, queue, loop, executor):
    # 等待事件触发
    print(f"{name} 等待事件触发")
    await event.wait()
    print(f"{name} 收到事件信号，开始工作")

    # 异步互斥访问共享资源
    async with lock:
        item = await queue.get()
        print(f"{name} 处理队列 item: {item}")
        await asyncio.sleep(1)  # 模拟异步处理
        print(f"{name} 处理完成: {item}")
        queue.task_done()

    # 异步执行线程池任务，并等待结果
    future = loop.run_in_executor(executor, blocking_task, item)
    result = await asyncio.wrap_future(future)
    print(f"{name} 得到线程池计算结果: {result}")

async def main():
    lock = asyncio.Lock()
    event = asyncio.Event()
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=2)

    # 准备队列
    for i in range(3):
        await queue.put(i)

    # 创建协程 worker
    workers = [
        asyncio.create_task(worker(f"worker-{i}", lock, event, queue, loop, executor))
        for i in range(2)
    ]

    # 模拟主线程准备工作，然后触发事件
    print("[主线程] 准备好，触发事件")
    await asyncio.sleep(1)
    event.set()

    # 等待队列处理完成
    await queue.join()

    # 等待所有 worker 完成
    await asyncio.gather(*workers)
    executor.shutdown(wait=True)
    print("[主线程] 所有任务完成")

# 运行
asyncio.run(main())
```

