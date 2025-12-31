## 数据仓库、代码仓库分开存放

1. 数据仓库设置

```bash
# 切换到数据目录
cd <数据根目录>
# 创建git仓库
git init
# 初始化dvc
dvc init
# 配置缓存权限
dvc config cache.shared group
# 配置缓存方式，可选reflink,symlink,hardlink,copy
dvc config cache.type symlink
# 配置dvc自动git add
dvc config core.autostage true
# 配置缓存目录路径，不放在当前路径里，放在一个全局的路径下，因为代码也要访问
dvc cache dir <缓存路径>
# 添加数据到dvc（这一步会复制数据到缓存目录）
dvc add <数据子目录，train、val等>
git commit
# 推送数据到远程
dvc remote add -d origin <远程地址，ssh://user@host:port/path>
dvc remote add -d origin ssh://user@10.20.0.61/mnt/monitor/dvc/datasets/xxx
dvc push
# 推送git到远程
git remote add origin <远程地址>
git push origin main
```

2. 代码仓库设置

```bash
# 切换到代码目录
cd <代码根目录>
# 创建git仓库
git init
# 初始化dvc
dvc init
# 配置缓存方式，可选reflink,symlink,hardlink,copy
dvc config cache.type copy
# 配置dvc自动git add
dvc config core.autostage true
# 创建存放数据的目录
mkdir data
# 配置允许文件协议，用于把数据仓库添加到子模块
git config --global protocol.file.allow always
# 添加数据作为子模块
git submodule add <数据根目录> data/<数据名>
# 切换到数据目录
cd data/<数据名>
# 检出数据
dvc checkout
# 添加训练结果、评估结果、环境等到dvc
dvc add <需要添加的目录路径>
git commit
# 推送数据到远程
dvc remote add -d origin <远程地址，ssh://user@host:port/path>
dvc push
# 推送git到远程
git remote add origin <远程地址>
git push origin main
```

## 从dvc中删除文件

```bash
# 不在跟踪指定路径
dvc remove <路径>.dvc
# 远程回收
dvc gc -r <远程名称> --workspace
```


