[toc]

## 常见问题

### 撤回提交、修改commit

```bash
# 修改最近一次提交
git commit --amend
# 撤回提交，但保存本地修改记录
git reset --soft HEAD^
# 覆盖提交
git push origin  --force
```

### 删除github中的提交历史记录

```bash
# 切换到一个脱离主分支的另外一条全新主分支，不用太在意叫什么，因为后面还会修改分支名称
git checkout --orphan latest_branch
# 暂存所有改动过的文件，内容为当前旧分支的最新版本所有文件
git add -A
# 提交更改
git commit -am "commit message"
# 删除原始主分支
git branch -D main
# 将当前分支重命名为 main
git branch -m main
# 最后，强制更新您的存储库
git push -f origin main

```

### 需要找到本地提交记录

```bash
git reflog
```

### 找回被删除的文件

```bash
# 恢复最新的已删除文件
git checkout HEAD -- 'file_path' # 相对地址

# 恢复过去的已删除文件
# 找到我们需要恢复的文件最后一次存在的提交。记录下该提交的哈希值（commit hash）
git checkout 'commit_hash' -- 'file_path'
```

## 常用操作

```bash
git init
git add 'file'
git commit -m "说明"
git push

git branch newbranch # 新建分支
git checkout newbranch # 切换分支
git remote -v # 查看远程仓库别名
git remote add origin url # 增加远程仓库
git push -u origin main # 推送
git remote rm origin # 删除url
git pull <远程主机名> <远程分支名>:<本地分支名> # 拉取远程并和本地分支合并
git stash  # 将本地暂存在缓存区和提取
git stash pop
```

### 配置git用户名和邮箱

```bash
git config --global user.name        # 查看
git config --global user.name 用户名  # 修改
git config --global user.email       # 查看
git config --global user.email 邮箱   # 修改
```

#### 为本地与GitHub的通信配置ssh

**本地git仓库和GitHub上的远程仓库之间的传输是通过SSH加密的，所以，需要一点设置**：

1. **创建ssh key**：

    ```bash
    ssh-keygen -t rsa -C "youremail@example.com"
    ```

2. **登录你的GitHub帐号，`Settings -> SSH and GPG keys -> new SSH key` ，将id_rsa.pub的内容复制进去**

> 为什么GitHub需要SSH Key呢？因为GitHub需要识别出你推送的提交确实是你推送的，而不是别人冒充的，而Git支持SSH协议，所以，GitHub只要知道了你的公钥，就可以确认只有你自己才能推送

#### 让本地git仓库和远程仓库同步

> 在有了本地git仓库后，还需创建对应的远程仓库

1. **在GitHub上创建远程仓库**（如果已有则省略）
2. **为本地仓库设置远程仓库信息**（如果同时需要为本地仓库添加多个远程仓库（如果github+码云），则可以将`origin`分别换成`github`和`gitee`，推送操作时也要修改`origin`。添加后，远程库的名字就是`origin`，这是Git默认的叫法，也可以改成别的，但是`origin`这个名字一看就知道是远程库）

    ```bash
    git remote add origin https://github.com/用户名/仓库名
    ```

    * **删除本地仓库的远程仓库信息**：`git remote remove origin`
    * **修改远端地址**：`git remote set-url 新地址`
    * **查看远程仓库信息**：`git remote -v`

3. **将本地git仓库push到远程仓库**

    ```bash
    # 由于远程库是空的，我们第一次推送master分支时，加上了-u参数,Git不但会把本地的
    # master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master
    # 分支关联起来，在以后的推送或者拉取时就可以简化命令
    git push [-u] origin 分支名
    ```

### 版本回退

```bash
git reset --hard 版本ID/HEAD形式的版本

git reset --hard HEAD      # 当前版本
git reset --hard HEAD^     # 上一个版本
git reset --hard HEAD^^    # 上上个版本
git reset --hard HEAD~n    # 前n个版本
```

如果回到过去的版本，想要回到原来新的版本：

* 如果终端未关，可以找到新版本的id，通过上述命令回去新版本
* 如果终端已关，`git reflog`查看版本，再通过上述命令回去新版本

## 命令详解

### git add

```bash
git add <文件路径> # 把指定的文件添加到暂存区中

git add -u [<文件路径>] # 添加所有修改、已删除的文件到暂存区中
git add --update [<文件路径>]

git add -A [<文件路径>] # 添加所有修改、已删除、新增的文件到暂存区中，省略 <文件路径> 即为当前目录
git add --all [<文件路径>]
```

### git branch

```bash
git branch # 列出本地的所有分支，当前所在分支以 "*" 标出
git branch -v # 列出本地的所有分支并显示最后一次提交，当前所在分支以 "*" 标出
git branch <分支名> # 创建新分支，新的分支基于上一次提交建立
git branch -m [<原分支名称>] <新的分支名称> # 修改分支名称,如果不指定原分支名称则为当前所在分支
git branch -M [<原分支名称>] <新的分支名称> # 强制修改分支名称
git branch -d <分支名称> # 删除指定的本地分支

git branch -D <分支名称> # 强制删除指定的本地分支
```

### git checkout

```bash
git checkout <分支名称> # 切换到已存在的指定分支
git checkout -b <分支名称> # 创建并切换到指定的分支，保留所有的提交记录，等同于 "git branch" 和 "git checkout" 两个命令合并
git checkout --orphan <分支名称> # 创建并切换到指定的分支，删除所有的提交记录
git checkout <文件路径> # 替换掉本地的改动，新增的文件和已经添加到暂存区的内容不受影响
```

### git clone

```bash
git clone <远程仓库的网址> # 默认在当前目录下创建和版本库名相同的文件夹并下载版本到该文件夹下
git clone <远程仓库的网址> <本地目录> # 指定本地仓库的目录
git clone <远程仓库的网址> -b <分支名称> <本地目录> # 指定要克隆的分支，默认是master分支
```

### git commit

```bash
git commit # 把暂存区中的文件提交到本地仓库，调用文本编辑器输入该次提交的描述信息
git commit -m "<提交的描述信息>" # 把暂存区中的文件提交到本地仓库中并添加描述信息
git commit -a -m "<提交的描述信息>"  # 把所有修改、已删除的文件提交到本地仓库中。不包括未被版本库跟踪的文件，等同于先调用了 "git add -u"
git commit --amend # 修改上次提交的描述信息
```

### git fetch

```bash
git fetch <远程仓库的别名> # 将远程仓库所有分支的最新版本全部取回到本地

git fetch <远程主机名> <分支名> # 将远程仓库指定分支的最新版本取回到本地
```

### git init

```bash
git init # 初始化本地仓库，在当前目录下生成 .git 文件夹
```

### git merge

```bash
git merge <分支名称> # 把指定的分支合并到当前所在的分支下，并自动进行新的提交
git merge --no-commit <分支名称> # 把指定的分支合并到当前所在的分支下，不进行新的提交
```

### git mv

```bash
git mv <源文件/文件夹> <目标文件/文件夹> # 重命名指定的文件或者文件夹
```

### git pull

```bash
git pull # 从远程仓库获取最新版本并合并到本地。 首先会执行 git fetch，然后执行 git merge，把获取的分支的 HEAD 合并到当前分支。
```

### git push

* 把本地仓库的分支推送到远程仓库的指定分支

```bash
git push <远程仓库的别名> <本地分支名>:<远程分支名> # 把本地仓库的分支推送到远程仓库的指定分支

git push <远程仓库的别名> :<远程分支名> # 删除指定的远程仓库的分支
git push <远程仓库的别名> --delete <远程分支名> 
```

### git remote

```bash
git remote # 列出已经存在的远程仓库
git remote -v # 列出远程仓库的详细信息，在别名后面列出URL地址
git remote add <远程仓库的别名> <远程仓库的URL地址> # 添加远程仓库
git remote rename <原远程仓库的别名> <新的别名> # 修改远程仓库的别名
git remote remove <远程仓库的别名> # 删除指定名称的远程仓库
git remote set-url <远程仓库的别名> <新的远程仓库URL地址> # 修改远程仓库的 URL 地址
```

### git rm

```bash
git rm <文件路径> # 移除跟踪指定的文件，并从本地仓库的文件夹中删除
git rm --cached # 移除跟踪指定的文件，在本地仓库的文件夹中保留该文件
```

### git rebase

```bash
git rebase <branch> # 把当前分支内容合并给其他分支上
git rebase -i <提交记录> # 把该当前节点进行可视化整理并在提交记录下形成新的分支
```

### other

```bash
git reset HEAD^
# 撤销本地仓库的一次提交，并指向上一个节点
git revert \<branch>
# 撤销该分支的修改，并形成新的提交记录
git cherry-pick <提交记录>
# 把其他提交记录复制到当前分支下并形成新的提交记录节点

```
