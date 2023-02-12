[TOC]

[tqdm,argparse]

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

