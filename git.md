#简单操作
- 初始化
```
git init
```
- 增加文件
```
git add 'file'
```
- 增加说明
```
git commit -m "说明"
```
- 上传文件
```
git push
```

*********
#更多操作
- 新建一个分支
```
git branch newbranch  
```
-切换另一个分支
```
git checkout newbranch
```
- 查看远程仓库别名
```
git remote -v 
```
- 增加远程仓库
```
git remote add origin url
```
- 推送
```
git push -u origin main
```
- 删除url
```
git remote rm origin
```
- 拉取远程并和本地分支合并
```
git pull <远程主机名> <远程分支名>:<本地分支名>
```
- 将本地暂存在缓存区和提取
```
git stash 
git stash pop
```

-----------------------------------------
# 第二次笔记
- git rebase \<branch>
把当前分支内容合并给其他分支上
- git merge \<branch>
把其他分支合并给当前分支

- git checkout \<branch>^
把head切换到指定分支的父节点

- git checkout HEAD^
  git checkout HEAD~\<n>
把head向父节点移动1/n次

- git branch -f \<branch> <提交记录>
将当前分支强制指向某个提交记录

- git reset HEAD^
撤销本地仓库的一次提交，并指向上一个节点
- git revert \<branch>
撤销该分支的修改，并形成新的提交记录 

- git cherry-pick <提交记录>
把其他提交记录复制到当前分支下并形成新的提交记录节点

- git rebase -i <提交记录>
把该当前节点进行可视化整理并在提交记录下形成新的分支

- git commit --amend 
修改当前提交记录

- git tag \<name> <提交记录>
为某个提交记录增加标识

- git pull=fetch+merge
  git pull --rebase =fetch+rebase
`
