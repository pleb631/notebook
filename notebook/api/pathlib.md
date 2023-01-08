# pathlib
## Path
[官方文档](https://pathlib.readthedocs.io/en/pep428/)
```python
from pathlib import Path
Path('path')
#WindowsPath('path')
```
| 模块/方法                         | 作用                          | 备注        |
| --------------------------------- | ----------------------------- | ----------- |
|Path.cwd()|返回文件当前所在目录|
|Path.home()|返回电脑用户的目录|#WindowsPath('C:/Users/admin')
|Path(Path.home(), "Desktop")|#拼接地址|WindowsPath('C:/Users/admin/Desktop')
|Path(INPUT).name|返回文件名+文件后缀|
|Path(INPUT).stem|返回文件名|
|Path(INPUT).suffix|返回文件后缀
|Path(INPUT).suffixes|返回文件后缀列表|
|Path(INPUT).root|返回根目录
|Path(INPUT).parts||
|Path(INPUT).anchor||
|Path(INPUT).parent|返回父级目录|
|Path(INPUT).exists()|判断 Path 路径是否存在|
|Path(INPUT).is_dir()|判断 Path 是否是一个文件夹
Path(INPUT).is_file()|判断 Path 是否是一个文件
Path(INPUT).mkdir()|创建文件夹；
Path(INPUT).rmdir()|删除文件夹，文件夹必须为空
Path(INPUT).unlink()|删除文件
Path(INPUT).iterdir()|查找文件夹下的所有文件，返回的是一个生成器类型
Path(INPUT).glob(pattern)|查找文件夹下所有与 pattern 匹配的文件，返回的是一个生成器类型；
Path(INPUT).rglob(pattern)|查找文件夹下所有子文件夹中与 pattern 匹配的文件，返回的是一个生成器
Paht(INPUT).rename('INPUT1')|剪切UNPUT文件至INPUT1
Paht(INPUT).with_name('INPUT1')|改变路径中文件名
Paht(INPUT).with_suffix('INPUT1')|改变路径中文件名后缀
Path(INPUT).match('pattern')|测试路径是否符合pattern