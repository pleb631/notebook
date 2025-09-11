# uv

[参考](https://hellowac.github.io/uv-zh-cn/)

## 介绍

uv 是一个非常快速的 Python 依赖安装程序和分解器，使用 Rust 编写，旨在替代 pip 和pip-tools 工作流，速度比他们快 8～10 倍，当前可用于替代 pip, pip-tools, virtualenv，根据路线图，它会向着 “Cargo for Python” 方向前行 —— 一个极其快速、可靠且易于使用的综合项目和包管理器。

Github 地址：[astral-sh/uv](https://github.com/astral-sh/uv)

## 安装uv

它是一个二进制文件，因此支持多种方式安装而不依赖 Rust 和 Python 环境（部分方式如下）

>window
> powershell -ExecutionPolicy ByPass -c "irm <https://astral.sh/uv/install.ps1> | iex"
>
>On macOS and Linux
>
>curl -LsSf <https://astral.sh/uv/install.sh> | sh

## 使用

更新 uv
如果通过独立安装程序安装 uv，可以按需自我更新：
uv self update

Shell 自动补全
要为 uv 命令启用 shell 自动补全，请运行以下命令之一：

```bash

# 确定您的 shell 类型（例如 `echo $SHELL`），然后运行以下之一：
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'uv generate-shell-completion fish | source' >> ~/.config/fish/config.fish
echo 'eval (uv generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv

# window
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

删除

```bash

uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"

# linux
rm ~/.local/bin/uv ~/.local/bin/uvx

# win
$ rm $HOME\.local\bin\uv.exe
$ rm $HOME\.local\bin\uvx.exe
```

## 虚拟环境管理

### 创建 venv 环境

uv init：创建一个新项目。
uv add：向项目添加依赖。
uv remove：从项目中移除依赖。

uv venv myenv: 激活环境

source myenv/bin/activate

uv venv --python 3.12 :指定版本

deactivate

uv async：同步依赖。

### uv python

uv python install：安装 Python 版本。
uv python list：查看可用的 Python 版本。
uv python find：查找已安装的 Python 版本。
uv python pin：为当前项目指定使用的 Python 版本。
uv python uninstall：卸载 Python 版本。

### uv pip

安装卸载依赖
$ uv pip install requests
$ uv pip uninstall requests

更新单个依赖

$ uv pip install --upgrade requests

根据依赖清单安装依赖

$ uv pip install -r requirements.txt
生成 requirements.in 文件
生成 requirements.in 依赖文件，而后根据需要手动精简及调整。

$ uv pip freeze > requirements.in

通过 requirements.in 生成 requirements.txt

$ uv pip compile requirements.in -o requirements.txt

通过 pyproject.toml 生成 requirements.txt

$ uv pip compile pyproject.toml -o requirements.txt
