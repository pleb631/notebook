[TOC]

[tqdm,argparse,pprint,pickledb，pathlib]

## tqdm

tqdm是 Python 进度条库，可以在 Python长循环中添加一个进度提示信息。用户只需要封装任意的迭代器，是一个快速、扩展性强的进度条工具库

- 手动更新

```python
import time
from tqdm import tqdm

with tqdm(total=200) as pbar:
    pbar.set_description('Processing:')
    # total表示总的项目, 循环的次数20*10(每次更新数目) = 200(total)
    for i in range(20):
        # 进行动作, 这里是过0.1s
        time.sleep(0.1)
        # 进行进度更新, 这里设置10个
        pbar.update(10)
Processing:: 100%|██████████| 200/200 [00:02<00:00, 91.94it/s]
```

- 自动更新

```python
import time
from tqdm import *

for i in tqdm(range(100)):
    time.sleep(0.01)
100%|██████████| 100/100 [00:01<00:00, 64.60it/s]
```

## argparse

基本框架

```python
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('--name', default='Great'，type=str，help='')
    parser.add_argument('--output', action='store_true')
    parser.add_argument("--pattern","-p", type=str, required=True,default="plane",choices=['plane', 'line'])
    args = parser.parse_args()
    
    def print_args(args):
        args = args.__dict__
        for k, v in args.items():
            print("{}: {}".format(k, v))

    return args


if __name__ == '__main__':
    args = get_parser()
    name = args.name
    print('Hello {}'.format(name))
```

其他参数

dest

`parser.add_argument('-num',dest='n',action='store_const', const=10)`

在代码运行的过程中，`num`会被`n`进行复写，只能通过`args.n`来调用`num`·的数据

nargs

`parser.add_argument('--ls', nargs=2, type=int)`

此案例中`ls`需要输入两个值，输多或少都会报错。

|值|  含义|
|--|--|
N  | 参数的绝对个数（例如：3）
'?' |  0或1个参数
'*' |  0或所有参数
'+' |  所有，并且至少一个参数

## pprint

可以按照目标格式按行输出内容，易于debug
pprint.pprint(content)


## pickledb

一般命令
```python
import pickledb

db = pickledb.load('testdb.db',True)
db.set('strtest','a')
print(db.get('strtest')) # 输出结果为 a

db.append('strtest','b')
print(db.get('strtest')) # 输出结果为 ab

db.rem('strtest') #删除
print(db.get('strtest')) #输出False

print(db.getall()) #输出所有key

print(db.exists('3')) #判断key是否存在
db.deldb() #删除所有内容
```
list
```python

#-*- coding:utf-8 -*-
import pickledb
import pickle

db=pickledb.load('example.db',False) # 加载数据库，如果没有会自动创建

list_=db.lcreate('database') # 创建list

data={1:1,2:2,3:3}

db.ladd('database',data) # 将data 添加到list
print db.lgetall('database') # 获取list中的所有内容 [{1: 1, 2: 2, 3: 3}]
db.lextend('database',data) # 用序列扩展列表
print db.lgetall('database') # [{1: 1, 2: 2, 3: 3}, 1, 2, 3]
print db.lget('database',0) # 在列表中返回一个值 {1: 1, 2: 2, 3: 3}
# db.lrem('database') # 删除一个列表及其所有值
db.lpop('database',-1) # 从列表中删除一个值
print db.lgetall('database') # [{1: 1, 2: 2, 3: 3}, 1, 2]
print(db.llen('database')) # 返回列表的长度 3
db.lappend('database',0,data) # 在列表中添加更多值
print db.lgetall('database') # ['{1: 1, 2: 2, 3: 3}{1: 1, 2: 2, 3: 3}', 1, 2]
print db.getall() # ['database']
```

dict

```python
#-*- coding:utf-8 -*-
import pickledb
import pickle

db=pickledb.load('example.db',False) # 加载数据库，如果没有会自动创建
dict_=db.dcreate('database') # 创建dict
db.dadd('database',(1,2)) # 将一个键值对添加到字典中，“pair”是一个元组
db.dadd('database',(2,3))
print db.dgetall('database') # 从字典中返回所有键值对 {1: 2, 2: 3}
print db.dget('database',1) # 2 在字典中返回一个key的值
print db.dkeys('database') # 在字典中返回一个key的值 [1,2]
print db.dvals('database') # 返回一个字典的所有value [2,3]
print db.dexists('database',2) # 确定key是否存在 存在返回1,不存在报错
# db.drem('database') # 删除一个字典和所有的对
db.dpop('database',1) # 删除一个字典中的一个key
print db.dgetall('database') # {2: 3}
print db.getall() # ['database']
db.deldb() # 从数据库中删除所有内容

db.dump() # 将数据库从内存保存到文件
```

## pathlib

[官方文档](https://pathlib.readthedocs.io/en/pep428/)

```python
from pathlib import Path
Path('path')
#WindowsPath('path')
```

| 模块/方法                         | 作用                          | 备注        |
| --------------------------------- | ----------------------------- | ----------- |
|Path.cwd()|返回工作路径|
|Path.home()|返回电脑用户的目录|#WindowsPath('C:/Users/admin')
|Path(Path.home(), "Desktop")|#拼接地址|WindowsPath('C:/Users/admin/Desktop')
|Path(INPUT).name|返回文件名+文件后缀|
|Path(INPUT).stem|返回文件名|
|Path(INPUT).relative_to('path')|去掉路径前缀|
|Path(INPUT).suffix|返回文件后缀|
|Path(INPUT).suffixes|返回文件后缀列表|
|Path(INPUT).root|返回根目录|
Path.replace()|文件重命名或移动|
Path.joinpath('path')
|Path(INPUT).parts|拆分路径，类似os.path.split('\\')|
|Path(INPUT).anchor||
|Path(INPUT).parent|返回父级目录|
|Path(INPUT).exists()|判断 Path 路径是否存在|
|Path(INPUT).is_dir()|判断 Path 是否是一个文件夹
Path(INPUT).is_file()|判断 Path 是否是一个文件
Path(INPUT).mkdir(exist_ok=True,parents=True)|创建文件夹；
Path(INPUT).rmdir()|删除文件夹，文件夹必须为空
Path(INPUT).unlink()|删除文件
Path(INPUT).iterdir()|查找文件夹下的所有文件，返回的是一个生成器类型
Path(INPUT).glob(pattern)|查找文件夹下所有与 pattern 匹配的文件，返回的是一个生成器类型；
Path(INPUT).rglob(pattern)|查找文件夹下所有子文件夹中与 pattern 匹配的文件，返回的是一个生成器
Path(INPUT).rename('INPUT1')|剪切UNPUT文件至INPUT1
Path(INPUT).with_name('INPUT1')|改变路径中文件名
Path(INPUT).with_suffix('INPUT1')|改变路径中文件名后缀
Path(INPUT).match('pattern')|测试路径是否符合pattern
Path(INPUT).relative_to('path')|取相对路径