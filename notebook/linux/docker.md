# docker

## 1.新建容器

```bash
docker run -it --gpus all --net=host --shm-size 16g --privileged=true -v /media:/media -v /home:/home --name yolo26 docker.1ms.run/nvidia/cuda bash

# 进入
docker attach yolo26 
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
echo -e "Types: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu\nSuites: noble noble-updates noble-backports\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\nTypes: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu\nSuites: noble-security\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg" | tee /etc/apt/sources.list.d/ubuntu.sources > /dev/null

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



```
echo -e "Types: deb\nURIs: https://mirrors.aliyun.com/ubuntu/\nSuites: jammy jammy-updates jammy-backports\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\nTypes: deb\nURIs: https://mirrors.aliyun.com/ubuntu/\nSuites: jammy-security\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\nTypes: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu/\nSuites: jammy jammy-updates jammy-backports\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\n" | tee /etc/apt/sources.list.d/ubuntu.sources > /dev/null
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

# 其他
apt install -y libgl1
```

## 4.镜像打包

```bash
docker commit yolo26 new_image:v1.0.0
docker save -o new_image.tar new_image:v1.0.0
# 删除镜像
docker rmi -f new_image:v1.0.0
# 加载镜像
docker load -i  new_image.tar
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

