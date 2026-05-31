- [常用命令](#常用命令)
- [CheatSheat](#cheatsheat)
  - [关机/重启/注销](#关机重启注销)
  - [系统信息和性能查看](#系统信息和性能查看)
  - [磁盘和分区](#磁盘和分区)
  - [⽤户和⽤户组](#户和户组)
  - [⽹络和进程管理](#络和进程管理)
  - [常⻅系统服务命令](#常系统服务命令)
  - [⽂件和⽬录操作](#件和录操作)
  - [⽂件查看和处理](#件查看和处理)
  - [打包和解压](#打包和解压)

# 常用命令

du -d 1 -h ./
查看空间占用

- 查找占用GPU资源的PID
fuser -v /dev/nvidia*

- 计算MD5校验码
`md5sum file`

- 清空指定GPU
`nvidia-smi --gpu-reset -i [gpu_id]`
或者`ps -ef | grep "python" | grep -v grep | awk '{print "kill -9 "$2}' | sh`或者

```bash
ps aux | grep python
kill -9 [pid]
```

- 查找文件

```bash
#递归搜索文件内容，如果查找"hello,world!"字符串,可以这样:
    grep -rn "hello,world!" *
 
    # * : 表示当前目录所有文件，也可以是某个文件名
    # -r 是递归查找
    # -n 是显示行号
    # -R 查找所有文件包含子目录
    # -i 忽略大小写
    
#2、搜索文件
    find / -name 'pay.html'
    # /：表示根目录，也可以自己指定搜索的目录。
    # -name：表示搜索文件名称。
    # pay.html：搜索的文件名称。
    
#3、批量替换。
    #替换server.xml文件中的”2020”为”8008”
    sed -i 's/2020/8080/g' ./conf/server.xml
    #批量替换，替换server.xml文件中的”2020”为”8008”，将结果输出到result1.xml
    sed -i 's/2020/8080/g' ./conf/server.xml > result1.xml
```
- 测试读写速度

```bash
time dd if=/dev/zero of=/tmp/test bs=8k count=1000000 #测写
time dd if=/tmp/test of=/dev/null bs=8k #测读

# time 有计时作用，dd 用于复制，从 if 读出，写到 of；
# if=/dev/zero 不产生 IO，因此可以用来测试纯写速度；
# 同理 of=/dev/null 不产生 IO，可以用来测试纯读速度；
# 将/tmp/test 拷贝到/var 则同时测试了读写速度；
# bs 是每次读或写的大小，即一个块的大小，count 是读写块的数量。
```

- 复制打包链接文件

```bash
# 复制符号链接指向的实际文件
cp -rL /tmp/test /var/tmp/test

# 压缩符号链接指向的实际文件
tar  -cvf /var/tmp/test.tar  -h /tmp/test
```

---

# CheatSheat

## 系统信息和性能查看

| 常用命令                    | 作用                               |
| --------------------------- | ---------------------------------- |
| uname -a                    | 查看内核/OS/CPU信息                |
| uname -r                    | 查看内核版本                       |
| uname -m                    | 查看处理器架构                     |
| arch                        | 查看处理器架构                     |
| hostname                    | 查看计算机名                       |
| who                         | 显示当前登录系统的⽤户             |
| who am i                    | 显示登录时的⽤户名                 |
| whoami                      | 显示当前⽤户名                     |
| cat /proc/version           | 查看linux版本信息                  |
| cat /proc/cpuinfo           | 查看CPU信息                        |
| cat /proc/interrupts        | 查看中断                           |
| cat /proc/loadavg           | 查看系统负载                       |
| uptime                      | 查看系统运⾏时间、⽤户数、负载     |
| env                         | 查看系统的环境变量                 |
| lsusb -tv                   | 查看系统USB设备信息                |
| lspci -tv                   | 查看系统PCI设备信息                |
| lsmod                       | 查看已加载的系统模块               |
| grep MemTotal /proc/meminfo | 查看内存总量                       |
| grep MemFree /proc/meminfo  | 查看空闲内存量                     |
| free -m                     | 查看内存⽤量和交换区⽤量           |
| date                        | 显示系统⽇期时间                   |
| cal 2021                    | 显示2021⽇历表                     |
| top                         | 动态显示cpu/内存/进程等情况        |
| vmstat 1 20                 | 每1秒采⼀次系统状态，采20次        |
| iostat                      | 查看io读写/cpu使⽤情况             |
| 查看io读写/cpu使⽤情况      | 查询cpu使⽤情况（1秒⼀次，共10次） |
| sar -d 1 10                 | 查询磁盘性能                       |

## 磁盘和分区

| 常用命令                            | 作用                           |
| ----------------------------------- | ------------------------------ |
| fdisk -l                            | 查看所有磁盘分区               |
| swapon -s                           | 查看所有交换分区               |
| df -h                               | 查看磁盘使⽤情况及挂载点       |
| df -hl                              | 同上                           |
| du -sh /dir                         | 查看指定某个⽬录的⼤⼩         |
| du -sk * \| sort -rn                | 从⾼到低依次显示⽂件和⽬录⼤⼩ |
| mount /dev/hda2 /mnt/hda2           | 挂载hda2盘                     |
| mount -t ntfs /dev/sdc1 /mnt/usbhd1 | 指定⽂件系统类型挂载（如ntfs） |
| mount -o loop xxx.iso /mnt/cdrom    | 挂 载 iso ⽂ 件                |
| umount -v /dev/sda1                 | 通过设备名卸载                 |
| umount -v /mnt/mymnt                | 通过挂载点卸载                 |
| fuser -km /mnt/hda1                 | 强制卸载(慎⽤)                 |

## ⽹络和进程管理

| 常用命令                                                     | 作用                                 |
| ------------------------------------------------------------ | ------------------------------------ |
| ifconfig                                                     | 查看⽹络接⼝属性                     |
| ifconfig eth0                                                | 查看某⽹卡的配置                     |
| route -n                                                     | 查看路由表                           |
| netstat -lntp                                                | 查看所有监听端⼝                     |
| netstat -antp                                                | 查看已经建⽴的TCP连接                |
| netstat -lutp                                                | 查看TCP/UDP的状态信息                |
| ifup eth0                                                    | 启⽤eth0⽹络设备                     |
| ifdown eth0                                                  | 禁⽤eth0⽹络设备                     |
| iptables -L                                                  | 查看iptables规则                     |
| ifconfig eth0 192.168.1.1 netmask 255.255.255.0              | 配置ip地址                           |
| dhclient eth0                                                | 以dhcp模式启⽤eth0                   |
| route add -net 0/0 gw Gateway_IP                             | 配置默认⽹关                         |
| route add -net 192.168.0.0 netmask 255.255.0.0 gw 192.168.1.1 | 配置静态路由到达⽹络'192.168.0.0/16' |
| route del 0/0 gw Gateway_IP                                  | 删除静态路由                         |
| hostname                                                     | 查看主机名                           |
| host [www.baidu.com](http://www.baidu.com)                   | 解析主机名                           |
| nslookup [www.baidu.com](http://www.baidu.com)               | 查询DNS记录，查看域名解析是否正常    |
| ps -ef                                                       | 查看所有进程                         |
| ps -ef \| grep codesheep                                     | 过滤出你需要的进程                   |
| kill -s name                                                 | kill指定名称的进程                   |
| kill -s pid                                                  | kill指定pid的进程                    |
| top                                                          | 实时显示进程状态                     |
| vmstat 1 20                                                  | 每1秒采⼀次系统状态，采20次          |
| iostat                                                       | iostat                               |
| sar -u 1 10                                                  | 查询cpu使⽤情况（1秒⼀次，共10次）   |
| sar -d 1 10                                                  | 查询磁盘性能                         |

## 常⻅系统服务命令

| 常用命令                   | 作用         |
| -------------------------- | ------------ |
| chkconfig --list           | 列出系统服务 |
| service <服务名> status    | 查看某个服务 |
| service <服务名> start     | 启动某个服务 |
| service <服务名> stop      | 终⽌某个服务 |
| service <服务名> restart   | 重启某个服务 |
| systemctl status <服务名>  | 查看某个服务 |
| systemctl start <服务名>   | 启动某个服务 |
| systemctl stop <服务名>    | 终⽌某个服务 |
| systemctl restart <服务名> | 重启某个服务 |
| systemctl enable <服务名>  | 关闭⾃启动   |
| systemctl disable <服务名> | 关闭⾃启动   |

## ⽂件查看和处理

| 常用命令                      | 作用                                    |
| ----------------------------- | --------------------------------------- |
| cat file1                     | 查看⽂件内容                            |
| cat -n file1                  | 查看内容并标示⾏数                      |
| tac file1                     | 从最后⼀⾏开始反看⽂件内容              |
| more file1                    | more file1                              |
| less file1                    | 类似more命令，但允许反向操作            |
| head -2 file1                 | 查看⽂件前两⾏                          |
| tail -2 file1                 | 查看⽂件后两⾏                          |
| tail -f /log/msg              | 实时查看添加到⽂件中的内容              |
| grep codesheep hello.txt      | 在⽂件hello.txt中查找关键词codesheep    |
| grep ^sheep hello.txt         | 在⽂件hello.txt中查找以sheep开头的内容  |
| grep [0-9] hello.txt          | 选择hello.txt⽂件中所有包含数字的⾏     |
| sed 's/s1/s2/g' hello.txt     | 将hello.txt⽂件中的s1替换成s2           |
| sed '/^$/d' hello.txt         | 从hello.txt⽂件中删除所有空⽩⾏         |
| sed '/ *#/d; /^$/d' hello.txt | 从hello.txt⽂件中删除所有注释和空⽩⾏   |
| sed -e '1d' hello.txt         | 从⽂件hello.txt 中排除第⼀⾏            |
| sed -n '/s1/p' hello.txt      | 查看只包含关键词"s1"的⾏                |
| sed -e 's/ *$//' hello.txt    | 删除每⼀⾏最后的空⽩字符                |
| sed -e 's/s1//g' hello.txt    | 从⽂档中只删除词汇s1并保留剩余全部      |
| sed -n '1,5p;5q' hello.txt    | 查看从第⼀⾏到第5⾏内容                 |
| sed -n '5p;5q' hello.txt      | 查看第5⾏                               |
| paste file1 file2             | 合并两个⽂件或两栏的内容                |
| paste -d '+' file1 file2      | 合并两个⽂件或两栏的内容，中间⽤"+"区分 |
| sort file1 file2              | 排序两个⽂件的内容                      |
| comm -1 file1 file2           | ⽐较两个⽂件的内容(去除'file1'所含内容) |
| comm -2 file1 file2           | ⽐较两个⽂件的内容(去除'file2'所含内容  |
| comm -3 file1 file2           | ⽐较两个⽂件的内容(去除两⽂件共有部分)  |

## 打包和解压

| 常用命令                          | 作用                     |
| --------------------------------- | ------------------------ |
| zip xxx.zip file                  | 压缩⾄zip包              |
| zip -r xxx.zip file1 file2 dir1   | 将多个⽂件+⽬录压成zip包 |
| unzip xxx.zip                     | 解压zip包                |
| tar -cvf xxx.tar file             | 创建⾮压缩tar包          |
| tar -cvf xxx.tar file1 file2 dir1 | 将多个⽂件+⽬录打tar包   |
| tar -tf xxx.tar                   | 查看tar包的内容          |
| tar -xvf xxx.tar                  | 解压tar包                |
| tar -xvf xxx.tar -C /dir          | 将tar包解压⾄指定⽬录    |
| tar -cvfj xxx.tar.bz2 dir         | 创建bz2压缩包            |
| tar -jxvf xxx.tar.bz2             | 解压bz2压缩包            |
| tar -cvfz xxx.tar.gz dir          | 创建gzip压缩包           |
| tar -zxvf xxx.tar.gz              | 解压gzip压缩包           |
| bunzip2 xxx.bz2                   | 解压bz2压缩包            |
| bzip2 filename                    | 压缩⽂件                 |
| gunzip xxx.gz                     | 解压gzip压缩包           |
| gzip filename                     | 压缩⽂件                 |
| gzip -9 filename                  | 最⼤程度压缩             |

# vim

## 1.操作

### 3.1.1**删除、复制与粘贴**

1.删除

|      | 说明                                              |
| ---- | ------------------------------------------------- |
| x, X | x 为向后删除一个字符，X 为向前删除一个字符        |
| nx   | 连续向后删除 n 个字符                             |

2.剪切
|      | 说明                                              |
| ---- | ------------------------------------------------- |
| dd   | 剪切当前行，用 p/P 可以粘贴                       |
| ndd  | 剪切光标所在的向下 n 行，用 p/P 可以粘贴          |
| dnG  | 剪切光标所在到第n行的所有数据(可以向前也可以向后) |
| dG   | 剪切光标所在到最后一行的所有数据                  |
| d$   | 剪切游标所在处，到该行的最后一个字符              |
| d0   | 剪切游标所在处，到该行的最前面一个字符            |

3.复制

复制为yy

为了理解方便，命令与dd类似，不再重复列举



4.其他

|        | 说明                                                     |
| ------ | -------------------------------------------------------- |
| p/P    | p 为将已复制的数据在光标下一行贴上，P 则为贴在游标上一行 |
| J      | 将光标所在行与下一行的数据结合成同一行                   |
| u      | 复原前一个动作                                           |
| ctrl+r | 重做上一个动作                                           |

### 3.1.2 光标移动

|                  | 说明                           |
| ---------------- | ------------------------------ |
| G                | 移动到文件最后一行             |
| nG               | 移动到文件第n行                |
| gg               | 移动到文件第一行               |
| n<Enter>         | 向下移动n行                    |
| n<space>         | 向右移动n个字符                |
| H/M/L            | 移动到当前页面顶部、中间、底部 |
| <Home>/<End>/0/$ | 移动到当前行开头/结尾          |

### 3.1.3 搜索替换

|                       | 说明                                               |
| --------------------- | -------------------------------------------------- |
| /word                 | 向光标**下方**查找为 “word” 的字符串               |
| ?word                 | 向光标**上方**查找为 “word” 的字符串               |
| n                     | 继续前一个搜索动作，这个是英文字符“n”              |
| N                     | 反向前一个搜索动作                                 |
| :n1,n2s/word1/word2/g | 在n1行和n2行之间把word1替换成word2，               |
| :1,$s/word1/word2/g   | 从n1行到最后把word1替换成word2，                   |
| :1,$s/word1/word2/g   | 从n1行到最后把word1替换成word2，每次需要给用户确认 |

## 2.vim里配置

新建~/.vimrc,填入以下内容

```txt
" 设置 Vim 内部使用 UTF-8 编码
set encoding=utf-8
" 设置文件读取时的默认编码
set fileencodings=utf-8,gb2312,gbk,latin1
" 设置终端显示编码
set termencoding=utf-8
" 显示行号等信息正常显示中文
set fileformat=unix


set tabstop=4       " 一个 Tab 显示成 4 个空格宽
set shiftwidth=4    " 自动缩进、>>、<< 使用 4 个空格
set expandtab       " 按 Tab 键时插入空格，而不是真 Tab 字符
```

3.其他操作

```python
>>      当前行右缩进
<<      当前行左缩进
4>>     从当前行开始，连续 4 行右缩进
gg=G    全文自动格式化缩进



^      跳到当前行第一个非空字符
w     跳到下一个单词开头
e     跳到当前/下一个单词结尾
b     跳到上一个单词开头
%     按括号匹配跳转



:10,20d 	删除第 10 到 20 行
:10,20t.	复制第 10 到 20 行到当前行下面
:10,20m.    :10,20t.


:%sort		全文排序
:%sort u	全文去重排序



# 分屏
:split   #水平分屏
:vsplit # 垂直分屏
:vsplit file.py  #打开另一个文件

Ctrl-w h # 窗口之间切换
Ctrl-w j
Ctrl-w k
Ctrl-w l

:only #只保留当前窗口
:q # 关闭当前窗口

```



# tmux

打开  `~/.tmux.conf`
输入 `set -g mouse on`
重置 `tmux source-file ~/.tmux.conf`



# xargs

xargs可以将stdin中以空格或换行符进行分隔的数据，形成以空格分隔的参数（arguments），传递给其他命令。因为以空格作为分隔符，所以有一些文件名或者其他意义的字符串内含有空格的时候，xargs可能会误判。简单来说，xargs的作用是给其他命令传递参数，是构建单行命令的重要组件之一。
之所以要用到xargs，是因为很多命令不支持使用管道|来传递参数，例如：

```bash
find /sbin -perm +700 | ls -l         # 这个命令是错误,因为标准输入不能作为ls的参数
find /sbin -perm +700 | xargs ls -l   # 这样才是正确的
```

命令格式

`xargs [OPTIONS] [COMMAND]`

| 选项                        | 说明                                                         |
| --------------------------- | ------------------------------------------------------------ |
| -0, --null                  | #如果输入的stdin含有特殊字符，例如反引号 `、反斜杠 \、空格等字符时，xargs将它还原成一般字符。为默认选项 |
| -a, --arg-file=FILE         | #从指定的文件FILE中读取输入内容而不是从标准输入              |
| -d, --delimiter=DEL         | #指定xargs处理输入内容时的分隔符，xargs处理输入内容默认是按空格和换行符作为分隔符，输出arguments时按空格分隔 |
| -E EOF_STR                  | #EOF_STR是end of file string，表示输入的结束                 |
| -I REPLACE_STR              | #将xargs输出的每一项参数单独赋值给后面的命令，参数需要用指定的替代字符串REPLACE_STR代替。REPLACE_STR可以使用{} $ @ 等符号，其主要作用是当xargs command后有多个参数时，调整参数位置。<br>例如备份以 txt 为后缀的文件：`find . -name "*.txt" | xargs -I {}  cp {} /tmp/{}.bak` |
| -i, --replace[=REPLACE_STR] | #作用同 -I 选项，参数 REPLACE_STR 是可选的，缺省为 {}。建议使用 -I 选项，因为其符合 POSIX |
| -L MAX_LINES                | #限定最大输入行数。隐含了 -x 选项                            |
| -n, --max-args=MAX_ARGS     | #表示命令在执行的时候一次使用参数的最大个数                  |
| -o, --open-tty              | #在执行命令之前，在子进程中重新打开stdin作为/dev/TTY。如果您希望xargs运行交互式应用程序，这是非常有用的 |
| -P, --max-procs=MAX_PROCS   | #每次运行最大进程；缺省值为 1。如果MAX_PROCS为 0，xargs将一次运行尽可能多的进程。一般和-n或-L选项一起使用 |
| -p, --interactive           | #当每次执行一个argument的时候询问一次用户                    |
| --process-slot-var=NAME     | #将指定的环境变量设置为每个正在运行的子进程中的唯一值。一旦子进程退出，将重用该值。例如，这可以用于初始负荷分配方案 |
| -r, --no-run-if-empty       | #当 xargs 的输入为空的时候则停止xargs，不用再去执行后面的命令了。为默认选项 |
| -s, --max-chars=MAX_CHARS   | #命令行的最大字符数，指的是xargs后面那个命令的最大命令行字符数，包括命令、空格和换行符。每个参数单独传入xargs后面的命令 |
| --show-limits               | #显示操作系统对命令行长度的限制                              |
| -t， --verbose              | #先打印命令到标准错误输出，然后再执行                        |
| -x, --exit                  | #配合 -s 使用，当命令行字符数大于 -s 指定的数值时，退出 xargs |

示例

```bash
#将 Shell 的特殊字符反引号还原为一般字符

echo '`0123`4 56789' | xargs -t echo
>echo `0123`4 56789 
>`0123`4 56789
```

如果直接进行如下操作，会报无法找到命令 01234 的错误，因为反引号在 Shell 中会将 01234  作为一个命来执     行，但是 01234 不是一个命令。-t 表示先打印命令，然后再执行。

```bash
echo `01234` 56789
>-bash: 01234: command not found

#设置 xargs 读入参数时的结束标识，以逗号结束。这里要注意结束标志必须要是单独的字段， 即以空格或者换行符分隔的字段。

echo 01234 , 56789 | xargs -E ","
>01234

 
#使用 rm、mv 等命令同时操作多个文件时，有时会报 “argument list too long” 参数列表过长的错误，此时可以使用 xargs 来解决。xargs 将标准输入的字符串分隔后，作为参数传递给后面的命令。例如，给当前目录的所有文件添加后缀名。
ls | xargs -t -i mv {} {}.bak

# 选择符合条件的文件
ls | grep -E "201701|201702|201703" | xargs -I {} mv {} {}.bak


#设置命令行的最大字符数。参数默认一个一个单独传入命令中执行。
echo "01234 56789" | xargs -t -s 11
>echo 01234 
>01234
>echo 56789 
>56789


# 设置标准输入中每次多少行作为命令的参数，默认是将标准输入中所有行的归并到一行一次性传给命令执行。

echo -e "01234\n56789\n01234" | xargs -t -L 2 echo
>echo 01234 56789 
>01234 56789
>echo 01234 
>01234

#将文件内容以空格分隔合并为一行输出。
# 列出文件内容
cat test.txt
a b c d e
f g h i j 
k l m n o

# 多行输入合并为一行输出
cat test.txt | xargs
a b c d e f g h i j k l m n o


#与ps、grep、awk和kill结合，强制终止指定进程。
ps -ef | grep spp | awk '{printf "%s ",$2}' | xargs kill -9

```

# awk

Awk  pattern scanning and processing language，对文本和数据进行处理。
awk 是一种编程语言，用于在linux/unix下对文本和数据进行处理。数据可以来自标准输(stdin)、一个或多个文件，或其它命令的输出。它在命令行中使用，但更多是作为脚本来使用。awk有很多内建的功能，比如数组、函数等，这是它和C语言的相同之处，灵活性是awk最大的优势。

命令格式

`awk [options] 'scripts' var=value filename`
**常用参数**
`awk 'BEGIN{ print "start" } pattern{ commands } END{ print "end" }' filename`
一个awk脚本通常由BEGIN语句+模式匹配+END语句三部分组成,这三部分都是可选项.
工作原理:
第一步执行BEGIN 语句
第二步从文件或标准输入读取一行，然后再执行pattern语句，逐行扫描文件到文件全部被读取
第三步执行END语句
| 选项         | 说明                                   |
| ------------ | -------------------------------------- |
| -F           | 指定分隔符（可以是字符串或正则表达式） |
| -f           | 从脚本文件中读取awk命令                |
| -v var=value | 赋值变量，将外部变量传递给awk          |

示例1

```bash
echo "hello " | awk 'BEGIN{ print "welcome" } END{ print "2017-08-08" }'
welcome
2017-08-08

echo -e "hello" | awk 'BEGIN{ print "welcome" } {print} END{ print "2017-08-08" }'
welcome
hello
2017-08-08
#不加print参数时默认只打印当前的行

echo|awk '{ a="hello"; b="nihao"; c="mingongge"; print a,b,c; }'
hello nihao mingongge
#使用print以逗号分隔时，打印则是以空格分界

echo|awk '{ a="mgg"; b="mingg"; c="mingongge"; print a" is "b" or "c; }'
mgg is mingg or mingongge
#awk的print语句中双引号其实就是个拼接作用
```

变量

外部变量

```bash
>a=100
>b=100
>echo |awk '{print v1*v2 }' v1=$a v2=$b
10000
```

内置变量

```bash
$0   #当前记录
$1~$n #当前记录的第N个字段
FS   #输入字段分隔符（-F相同作用）默认空格
RS   #输入记录分割符，默认换行符
NF   #字段个数就是列 
NR   #记录数，就是行号，默认从1开始
OFS  #输出字段分隔符，默认空格
ORS  #输出记录分割符，默认换行符
```

可以使用各种运算符和正则表达式

示例2

```bash
awk –F : ‘{print $2}’ datafile
#以:分隔打印第二列

awk –F : ‘/^Dan/{print $2}’ datafile
#以:分隔打印以Dan开头行的第二列内容

awk –F : ‘/^[CE]/{print $1}’ datafile 
#打印以C或E开头行的第一列

awk –F : ‘{if(length($1) == 4) print $1}’ datafile 
#打印以:分隔且长度为4字符的第一列内容

awk –F : ‘/[916]/{print $1}’ datafile
#匹配916的行以:分隔打印第一列

awk -F : '/^Vinh/{print "a"$5}' 2.txt
#显示以Dan开头行并在第五列前加上a

awk –F : ‘{print $2”,”$1}’  datafile
#打印第二列第一列并以,分隔

awk -F : '($5 == 68900) {print $1}' 2.txt
#以:分隔打印第五列是68900的行第一列  

awk -F : '{if(length($1) == 11) print $1}' 2.txt
#打印以:分隔且长度为4字符的第一列内容

awk -F : '$1~/Tommy Savage/ {print $5}' 2.txt
awk -F : '($1 == "Tommy Savage") {print $5}' 2.txt
#打印以:分隔且第一列为Tommy Savage的第五列内容

ll |awk 'BEGIN {size=0;} {size=size+$5;} END{print "[end]size is ",size}'
#统计目录个的文件所有的字节数

awk 'BEGIN{size=0;} {size=size+$5;} END{print "[end]size is ",size/1024/1024,"M"}' 
#以M为单位显示目录下的所有字节数

awk 'BEGIN{a=10;a+=10;print a}'
20 
#a+10等价于 a=a+10

echo|awk 'BEGIN{a="100testaaa"}a~/test/{print "ok"}' 
#正则匹配a 是否有test字符，成立打印ok

awk 'BEGIN{a="b";print a=="b"?"ok":"err"}'
ok
awk 'BEGIN{a="b";print a=="c"?"ok":"err"}'
err
#三目运算符?:

awk '/root/{print $0}' passwd 
#匹配所有包含root的行

awk -F: '$5~/root/{print $0}' passwd 
# 以分号作为分隔符，匹配第5个字段是root的行

ifconfig eth0|awk 'BEGIN{FS="[[:space:]:]+"} NR==2{print $4}'
#打印IP地址

awk '{print toupper($0)}' test.txt
#toupper是awk内置函数，将所小写字母转换成大写
```

# grep

文本查找或搜索工具。用于查找内容包含指定的范本样式的文件，如果发现某文件的内容符合所指定的范本样式，预设grep会把含有范本样式的那一列显示出来。若不指定任何文件名称，或是所给予的文件名为 -，则grep会从标准输入设备读取数据。
同样可以配合正则表达式来搜索文本，并将匹配的行打印输出,也可用于过滤与搜索特定字符串，使用十分灵活

常用参数

| 选项  | 说明                                                         |
| ----- | ------------------------------------------------------------ |
| -a    | 不要忽略二进制数据                                           |
| -A    | 除了显示符合范本样式的那一行之外，并显示该行之后的内容       |
| -b    | 在显示符合范本样式的那一行之外，并显示该行之前的内容         |
| -B    | 除了显示符合样式的那一行之外，并显示该行之前的内容           |
| -c    | 计算符合范本样式的列数                                       |
| -C    | 除了显示符合范本样式的那一列之外，并显示该列之前后的内容     |
| -d    | 当指定要查找的是目录而非文件时，必须使用这项参数，否则grep命令将回报信息并停止动作 |
| -e    | 指定字符串作为查找文件内容的范本样式                         |
| -E    | 将范本样式为延伸的普通表示法来使用，意味着使用能使用扩展正则表达式 |
| -f    | 指定范本文件，其内容有一个或多个范本样式，让grep查找符合范本条件的文件内容，格式为每一列的范本样式 |
| -F    | 将范本样式视为固定字符串的列表                               |
| -G    | 将范本样式视为普通的表示法来使用                             |
| -h    | 在显示符合范本样式的那一列之前，不标示该列所属的文件名称     |
| -H    | 在显示符合范本样式的那一列之前，标示该列的文件名称           |
| -i    | 忽略字符大小写的差别                                         |
| -l    | 列出文件内容符合指定的范本样式的文件名称                     |
| -L    | 列出文件内容不符合指定的范本样式的文件名称                   |
| -n    | 在显示符合范本样式的那一列之前，标示出该列的编号             |
| -q    | 不显示任何信息                                               |
| -R/-r | 此参数的效果和指定“-d recurse”参数相同                       |
| -s    | 不显示错误信息                                               |
| -v    | 反转查找                                                     |
| -V    | 显示版本信息                                                 |
| -w    | 只显示全字符合的列                                           |
| -x    | 只显示全列符合的列                                           |
| -y    | 此参数效果跟“-i”相同                                         |
| -o    | 只输出文件中匹配到的部分                                     |

示例

1、在多个文件中查找：

`grep "file" file_1 file_2 file_3`
2、输出除之外的所有行 -v 选项：

`grep -v "file" file_name`
3、标记匹配颜色 --color=auto 选项：

`grep "file" file_name --color=auto`
4、使用正则表达式 -E 选项：

`grep -E "[1-9]+"`

`egrep "[1-9]+"`
5、只输出文件中匹配到的部分 -o 选项：

```bash
>echo this is a test line. | grep -o -E "[a-z]+."
line.

>echo this is a test line. | egrep -o "[a-z]+."
line.
```

6、统计文件或者文本中包含匹配字符串的行数-c 选项：

```bash
>grep -c "text" file_name
2
```

7、输出包含匹配字符串的行数 -n 选项：

```bash
grep "text" -n file_name
#或
cat file_name | grep "text" -n
```

8、多个文件

```bash
grep "text" -n file_1 file_2
```

9、搜索多个文件并查找匹配文本在哪些文件中：
`grep -l "text" file1 file2 file3...`
10、grep递归搜索文件

在多级目录中对文本进行递归搜索：

`grep "text" . -r -n`
11、忽略匹配样式中的字符大小写：

```bash
>echo "hello world" | grep -i "HELLO"
hello
```

12、选项 -e 指定多个匹配样式：

```bash
>echo this is a text line | grep -e "is" -e "line" -o
is
line
```

13、也可以使用 -f 选项来匹配多个样式，在样式文件中逐行写出需要匹配的字符。

```bash
>cat patfile
aaa
bbb

>echo aaa bbb ccc ddd eee | grep -f patfile -o
```

14、在grep搜索结果中包括或者排除指定文件：
只在目录中所有的.php和.html文件中递归搜索字符"main()"
`grep "main()" . -r --include *.{php,html}`
15、在搜索结果中排除所有README文件
`grep "main()" . -r --exclude "README"`
16、在搜索结果中排除filelist文件列表里的文件
`grep "main()" . -r --exclude-from filelist`

# ls

ls(list)，ls命令显示指定目录下的内容，列出指定目录下所含的文件及子目录。此命令与Windows系统中dir命令功能相似。
ls命令的输出信息可以进行彩色加亮显示，以分区不同类型的文件。

选项说明

| 选项 | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| -a   | 显示指定目录下的所有文件以及子目录，包含隐藏文件             |
| -A   | 显示指定目录下的（除“.”和“..”之外）所有文件及子目录          |
| -d   | 显示指定目录的属性信息                                       |
| -l   | 显示指定目录下的文件及子目录详细信息,输出的信息从左到右依次包括文件名，文件类型、权限模式、硬连接数、所有者、组、文件大小和文件的最后修改时间等 |
| -t   | 以时间顺序显示指定目录下的文件及子目录                       |
| -F   | 在列出的文件名称后加一符号；例如可执行档则加 "*", 目录则加 "/" |
| -k   | 以KB（千字节）为单位显示文件大小                             |
| -m   | 用“,”号区隔每个文件和目录的名称                              |
| -s   | 显示文件和目录的大小，以区块为单位                           |
| -L   | 如果遇到性质为符号链接的文件或目录，直接列出该链接所指向的原始文件或目录 |
| -R   | 递归处理，将指定目录下的所有文件及子目录一并处理             |

示例

1. 计算当前目录下的文件数和目录数

```bash
ls -l * |grep "^-" |wc -l
ls -l * |grep  "^d" |wc -l
```

2.在ls中列出文件的绝对路径

```bash
ls |sed "s:^:`pwd`/:"
```

# nohup

nohup 命令用于将进程放后台运行（不挂断）。

语法

nohup Command [ Arg … ] [ & ]

执行test.sh 脚本，并重定向输入到 test.log 文件

```bash
[root@centos7 ~]# nohup /scripts/test.sh > test.log 2>&1 &
```

2>&1 解释:
将标准错误 2 重定向到标准输出 &1 ，标准输出 &1 再被重定向输入到 test.log 文件中。
0 – stdin (standard input，标准输入)
1 – stdout (standard output，标准输出)
2 – stderr (standard error，标准错误输出)

# mount

mount 命令用于挂载设备或文件系统。

命名格式

`mount [option] device|dir`

选项说明

| 选项               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| -a                 | 将 /etc/fstab 中定义的所有档案系统挂上                       |
| -F                 | 这个命令通常和 -a 一起使用，它会为每一个 mount 的动作产生一个行程负责执行在系统需要挂上大量 NFS 档案系统时可以加快挂上的动作 |
| -s -r              | 功能与 -o ro相同                                             |
| -w                 | 功能与 -o rw相同                                             |
| -oasync            | 打开非同步模式                                               |
| -o sync            | 在同步模式下执行                                             |
| -o auto、-o noauto | 打开/关闭自动模式                                            |
| -o ro              | 使用只读模式挂载                                             |
| -o rw              | 使用可读写模式挂载                                           |

# umount

umount 命令用于卸载已经挂载的文件系统。请注意，文件系统在繁忙时无法卸载，例如，当文件系统上有打开的文件，某个进程的工作目录位于其中或正在使用交换文件时。

命名格式

`umount -a [-dflnrv] [-t vfstype] [-O options]`

选项说明

| 选项             | 说明                                               |
| ---------------- | -------------------------------------------------- |
| -a               | 卸载/etc/mtab中记录的所有文件系统                  |
| -n               | 卸载时不要将信息存入/etc/mtab文件中                |
| -r               | 若无法成功卸载，则尝试以只读的方式重新挂入文件系统 |
| -t<文件系统类型> | 卸载指定的文件系统                                 |
| -v               | 显示执行时的详细信息                               |

# top

top 命令用于实时显示系统资源使用情况。它可以显示系统摘要信息，以及内核当前正在管理的进程或线程的列表。

top 命令可以实时动态地查看系统的整体运行情况，是一个非常实用的系统性能和运行信息的监测工具。通过 top 命令所提供的互动式界面，用热键可以管理。

top交互命令

在 top 命令执行过程中会使用到一些交互命令，这些命令都是单字母，如下。
| 选项   | 说明                                              |
| ------ | ------------------------------------------------- |
| h      | 显示帮助信息界面                                  |
| k      | 终止一个进程                                      |
| i      | 忽略闲置和僵死进程，这是一个开关式命令            |
| q      | 退出程序                                          |
| r      | 重新安排一个进程的优先级别                        |
| S      | 切换到累计模式                                    |
| s      | 改变两次刷新之间的延迟时间（单位为s），默认值是5s |
| f或者F | 从当前显示中添加或者删除项目                      |
| o或者O | 改变显示项目的顺序                                |
| l      | 切换显示平均负载和启动时间信息                    |
| m      | 切换显示内存信息                                  |
| t      | 切换显示进程和CPU状态信息                         |
| c      | 切换显示命令名称和完整命令行                      |
| M      | 根据驻留内存大小进行排序                          |
| P      | 根据CPU使用百分比大小进行排序                     |
| T      | 根据时间/累计时间进行排序                         |
| w      | 将当前设置写入~/.toprc文件中                      |

结果说明

```bash
top - 05:59:56  #当前系统时间
up 1 day    #系统已经运行了1天
1 user    #当前登录用户个数 
load average: 0.06, 0.03, 0.05   #系统负载信息

Tasks:  
92 total  #总进程数 
2 running #正在运行的进程数
90 sleeping   #休眠的进程数
0 stopped     #停止的进程数
0 zombie      #冻结的进程数

%Cpu(s):  
0.0 us  #用户空间占用CPU的百分比 
0.3 sy  #内核空间占用CPU的百分比
0.0 ni  #用户进程空间内改变过优先级的进程占用CPU百分比
99.7 id #空闲CPU百分比
0.0 wa  #等待输入输出的CPU时间百分比
0.0 hi  #硬中断占用CPU的百分比 
0.0 si  #软中断占用CPU的百分比
0.0 st  #虚拟机占用百分比 

KiB Mem :   
995684 total  #物理内存的总量
473120 free   #剩余内存的总量
124960 used   #已使用内存的总量
397604 buff/cache  #内核缓存所使用内存的量

KiB Swap:  
2097148 total   #交换分区的总量
2097148 free    #交换分区剩余的总量    
0 used          #交换分区已使用的总量
698120 avail Mem  #可用内存总量

PID  #进程id
USER #进程所有者
PR  #任务的调度优先级，范围0-31，数值越低，优先级越高
NI  #nice值，范围-20到+19，用于调整进程优先级
VIRT #进程所使用的虚拟内存总量（单位 KB）
RES  #任务已使用的未交换物理内存（单位 KB）
SHR  #共享内存大小（单位 KB）
S    #进程状态
      ' D '=不间断的睡眠
      ' R '=运行
      ' S '=睡眠
      ' T '=被跟踪或停止的
      ' Z '=僵尸
%CPU #CPU的使用率
%MEM #内存使用率
TIME+ #CPU时间
COMMAND #进程名称（命令名/命令行），显示用于启动任务的命令行或关联程序的名称。
```

# chmod


1. 三种基本权限
读（Read, r）：允许查看文件内容或列出目录中的文件。
写（Write, w）：允许修改文件内容或在目录中创建 / 删除文件。
执行（Execute, x）：允许运行可执行文件或进入目录（对目录而言，x 权限是使用 cd 命令进入的必要条件）。
2. 三类用户角色
所有者（User, u）：文件或目录的创建者。
所属组（Group, g）：与文件关联的用户组的成员。
其他用户（Others, o）：既不是所有者也不是所属组成员的用户。
所有用户（All, a）：等同于 u + g + o。

3. 权限值映射
每个权限对应一个数字值：

r = 4（二进制 100）
w = 2（二进制 010）
x = 1（二进制 001）
4. 组合权限值
通过加法组合权限：

rwx = 4 + 2 + 1 = 7
rw- = 4 + 2 + 0 = 6
r-x = 4 + 0 + 1 = 5
r-- = 4 + 0 + 0 = 4
--- = 0 + 0 + 0 = 0

```bash
chmod 755 script.sh      # 所有者有 rwx，组和其他用户有 rx
chmod 644 data.txt       # 所有者有 rw，组和其他用户有 r
chmod 700 secret_file    # 仅所有者有 rwx，组和其他用户无权限

```

5.操作符
+：添加权限
-：移除权限
=：设置权限（覆盖原有权限）

```bash
chmod u+x script.sh      # 给所有者添加执行权限
chmod g-w,o-rwx file.txt # 移除组的写权限和其他用户的所有权限
chmod a=rwx directory/   # 所有人拥有所有权限（不推荐）
chmod o=rx file          # 其他用户设置为 rx 权限

```
