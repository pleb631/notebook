# docker

## 1.新建容器

```bash
docker run -it --gpus all --net=host --shm-size 16g --privileged=true -v /media:/media -v /home:/home --name ubuntu22_dml1 docker.1ms.run/nvidia/cuda:12.9.2-cudnn-devel-ubuntu22.04 bash

# --restart=unless-stopped
# 进入
docker attach ubuntu22_dml1
```

## 2.配置源

```bash
cat /etc/os-release

#1.
apt-get  update

# 2.备份
cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.bak

# 3. 换源
# 缺少 vim
sed -i.bak -E 's@(archive|security)\.ubuntu\.com@mirrors.tuna.tsinghua.edu.cn@g; s@http:@https:@g' /etc/apt/sources.list

# 重设 DNS 配置
echo -e "nameserver 8.8.8.8\nnameserver 8.8.4.4" | tee /etc/resolv.conf > /dev/null

# 4.更新
apt update

# 5. 报错
# No system certificates available. Try installing ca-certificates.
apt install ca-certificates
update-ca-certificates
apt-get update
```



## 3.配置环境

```bash
apt update
apt install -y openssh-server vim tmux git unzip curl net-tools
service ssh start
passwd root #设置密码
vim /etc/ssh/sshd_config # 改端口
# PermitRootLogin yes
# PasswordAuthentication yes
service ssh restart


# 如果重新创建容器则
ssh-keygen -R [192.168.5.93]:23400

```

## 4.镜像打包

```bash
docker commit ubuntu22_dml1 new_image:v1.0.0
docker save -o new_image.tar new_image:v1.0.0
# 删除镜像
docker rmi -f new_image:v1.0.0
# 加载镜像
docker load -i  new_image.tar
```

## 5.其他配置

```bash
# vim
cat > ~/.vimrc << 'EOF'
set encoding=utf-8
set fileencodings=utf-8,gb2312,gbk,latin1
set termencoding=utf-8
set fileformat=unix

set tabstop=4
set shiftwidth=4
set expandtab
EOF



# tmux
cat > ~/.tmux.conf << 'EOF'
set -g mouse on
EOF

tmux source-file ~/.tmux.conf

# opencv需要
apt install -y libgl1


export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
```



# 管理

1.监听

```bash
netstat -tunlp |grep 35003
```

2.开放端口

```bash
apt-get install firewalld
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload

# 显示所有
firewall-cmd --list-all
# 关闭
firewall-cmd --remove-port=8001/tcp --permanent
```

