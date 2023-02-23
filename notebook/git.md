[TOC]

### git add

- 把指定的文件添加到暂存区中

```shell
git add <文件路径>
```

- 添加所有修改、已删除的文件到暂存区中

```shell
git add -u [<文件路径>]
git add --update [<文件路径>]
```

- 添加所有修改、已删除、新增的文件到暂存区中，省略 <文件路径> 即为当前目录

```shell
git add -A [<文件路径>]
git add --all [<文件路径>]
```

### git branch

- 列出本地的所有分支，当前所在分支以 "*" 标出

```shell
git branch
```

- 列出本地的所有分支并显示最后一次提交，当前所在分支以 "*" 标出

```shell
git branch -v
```

- 创建新分支，新的分支基于上一次提交建立

```shell
git branch <分支名>
```

- 修改分支名称,如果不指定原分支名称则为当前所在分支

```shell
git branch -m [<原分支名称>] <新的分支名称>
```

- 强制修改分支名称

```shell
git branch -M [<原分支名称>] <新的分支名称>
```

- 删除指定的本地分支

```shell
git branch -d <分支名称>
```

- 强制删除指定的本地分支

```shell
git branch -D <分支名称>
```

### git checkout

- 切换到已存在的指定分支

```shell
git checkout <分支名称>
```

- 创建并切换到指定的分支，保留所有的提交记录，等同于 "git branch" 和 "git checkout" 两个命令合并

```shell
git checkout -b <分支名称>
```

- 创建并切换到指定的分支，删除所有的提交记录

```shell
git checkout --orphan <分支名称>
```

- 替换掉本地的改动，新增的文件和已经添加到暂存区的内容不受影响

```shell
git checkout <文件路径>
```

### git clone

- 默认在当前目录下创建和版本库名相同的文件夹并下载版本到该文件夹下

```shell
git clone <远程仓库的网址>
```

- 指定本地仓库的目录

```shell
git clone <远程仓库的网址> <本地目录>
```

- -b 指定要克隆的分支，默认是master分支

```shell
git clone <远程仓库的网址> -b <分支名称> <本地目录>
```

### git commit

- 把暂存区中的文件提交到本地仓库，调用文本编辑器输入该次提交的描述信息

```shell
git commit
```

- 把暂存区中的文件提交到本地仓库中并添加描述信息

```shell
git commit -m "<提交的描述信息>"
```

- 把所有修改、已删除的文件提交到本地仓库中。不包括未被版本库跟踪的文件，等同于先调用了 "git add -u"

```shell
git commit -a -m "<提交的描述信息>"
```

- 修改上次提交的描述信息

```shell
git commit --amend
```

### git fetch

- 将远程仓库所有分支的最新版本全部取回到本地

```shell
git fetch <远程仓库的别名>
```

- 将远程仓库指定分支的最新版本取回到本地

```shell
git fetch <远程主机名> <分支名>
```

### git init

- 初始化本地仓库，在当前目录下生成 .git 文件夹

```shell
git init
```

### git merge

- 把指定的分支合并到当前所在的分支下，并自动进行新的提交

```shell
git merge <分支名称>
```

- 把指定的分支合并到当前所在的分支下，不进行新的提交

```shell
git merge --no-commit <分支名称>
```

### git mv

- 重命名指定的文件或者文件夹

```shell
git mv <源文件/文件夹> <目标文件/文件夹>
```

### git pull

- 从远程仓库获取最新版本并合并到本地。 首先会执行 git fetch，然后执行 git merge，把获取的分支的 HEAD 合并到当前分支。

```shell
git pull
```

### git push

- 把本地仓库的分支推送到远程仓库的指定分支

```shell
git push <远程仓库的别名> <本地分支名>:<远程分支名>
```

- 删除指定的远程仓库的分支

```shell
git push <远程仓库的别名> :<远程分支名>
git push <远程仓库的别名> --delete <远程分支名>
```

### git remote

- 列出已经存在的远程仓库
$ git remote

- 列出远程仓库的详细信息，在别名后面列出URL地址

```shell
git remote -v
git remote --verbose
```

- 添加远程仓库

```shell
git remote add <远程仓库的别名> <远程仓库的URL地址>
```

- 修改远程仓库的别名

```shell
git remote rename <原远程仓库的别名> <新的别名>
```

- 删除指定名称的远程仓库

```shell
git remote remove <远程仓库的别名>
```

- 修改远程仓库的 URL 地址

```shell
git remote set-url <远程仓库的别名> <新的远程仓库URL地址>
```

### git rm

- 移除跟踪指定的文件，并从本地仓库的文件夹中删除

```shell
git rm <文件路径>
```

- 移除跟踪指定的文件，在本地仓库的文件夹中保留该文件

```shell
git rm --cached
```
