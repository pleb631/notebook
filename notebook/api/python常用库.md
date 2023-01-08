[tqdm]
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