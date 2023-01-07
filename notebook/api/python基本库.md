[TOC]
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


# multiprocessing
## Pool

pool.apply_async 用多线程执行函数
```python
import multiprocessing
import time111111
 
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
pool.map_async 可以自动把数据分配给多个线程，缺点是不好支持多个输入参数
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
pool.starmap_async 在支持自动分配线程的同时也可以支持多个输入参数
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

```
# other

## print
| 模块/方法 | 作用 | 备注 |
|---|---|---|
|制表符 \t|用来为字符串与字符串之间产生间距||
|"{},{}".format(object1,object)|格式化输出||
|#-*- coding: UTF-8 -*-|放在文件开头来解决中文乱码问题||
| print(*object,sep=' ',end='\n',file=sys.stdout,flush=False)|objects -> 可以为一个或多个对象，输出多个对象时，需要用逗号分隔 <br>sep -> 用来间隔多个对象，默认值是一个空格 <br>end -> 用来设定结尾方式，默认值是换行符 \n ，也可以换成其他字符串 <br>file -> 要写入的文件对象||

## read
read()  ： 一次性读取整个文件内容。推荐使用read(size)方法，size越大运行时间越长  
readline()  ：每次读取一行内容。内存不够时使用，一般不太用  
readlines()   ：一次性读取整个文件内容，并按行返回到list，方便我们遍历

