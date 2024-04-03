<!-- TOC -->
- [python](#python)
  - [opencv](#opencv)
    - [imread,imwrite读写入图片失败](#imreadimwrite读写入图片失败)
    - [lap 安装方法](#lap-安装方法)
    - [Microsoft Visual C++ 14.0 is required](#microsoft-visual-c-140-is-required)
    - [acaconda常用命令](#acaconda常用命令)
    - [Vscode解决 Failed to connect to github.com port 443:connection timed out](#vscode解决-failed-to-connect-to-githubcom-port-443connection-timed-out)
    - [tensorborad:not found](#tensorboradnot-found)


# python

## opencv

### imread,imwrite读写入图片失败

原因1：俩函数不支持中文路径
方案1：用imdecode/imencode替代，见[文档](/notebook/api/cv2.md)
方案2：用PIL包替代

### lap 安装方法

```shell
conda install -c conda-forge lap
```

### Microsoft Visual C++ 14.0 is required

```shell
conda install libpython m2w64-toolchain -c msys2
```

### acaconda常用命令

- pip 永久换镜像源

```shell
pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

- conda 换镜像源

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

```

- 从cmd启动jupyter

```shell
!conda install jupyter notebook
!jupyter notebook
```

- Jupyter Notebook使用指定的conda环境

 ```Jupyter
 !conda install nb_conda
 ```

![2023-03-02-21-22-20](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-03-02-21-22-20.png)

### Vscode解决 Failed to connect to github.com port 443:connection timed out

方案1：先全局代理再取消

```
git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy http://127.0.0.1:1080
git config --global --unset https.https://github.com.proxy
git config --global --unset http.https://github.com.proxy
```

### tensorborad:not found

先找到tensorboard的main.py

```linux
python -m pip show tensorboard
python path/man.py --logdir [args]
```
