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
