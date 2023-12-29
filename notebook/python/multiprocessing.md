# multiprocessing

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

### 线程池

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
