### xargs
xargs可以将stdin中以空格或换行符进行分隔的数据，形成以空格分隔的参数（arguments），传递给其他命令。因为以空格作为分隔符，所以有一些文件名或者其他意义的字符串内含有空格的时候，xargs可能会误判。简单来说，xargs的作用是给其他命令传递参数，是构建单行命令的重要组件之一。
之所以要用到xargs，是因为很多命令不支持使用管道|来传递参数，例如：
```bash
find /sbin -perm +700 | ls -l         # 这个命令是错误,因为标准输入不能作为ls的参数
find /sbin -perm +700 | xargs ls -l   # 这样才是正确的
```
>**命令格式**
`xargs [OPTIONS] [COMMAND]`

|选项|说明|
|------|-------|
-0, --null|#如果输入的stdin含有特殊字符，例如反引号 `、反斜杠 \、空格等字符时，xargs将它还原成一般字符。为默认选项
-a, --arg-file=FILE|#从指定的文件FILE中读取输入内容而不是从标准输入
-d, --delimiter=DEL|#指定xargs处理输入内容时的分隔符，xargs处理输入内容默认是按空格和换行符作为分隔符，输出arguments时按空格分隔
-E EOF_STR|#EOF_STR是end of file string，表示输入的结束
-I REPLACE_STR|#将xargs输出的每一项参数单独赋值给后面的命令，参数需要用指定的替代字符串REPLACE_STR代替。REPLACE_STR可以使用{} $ @ 等符号，其主要作用是当xargs command后有多个参数时，调整参数位置。<br>例如备份以 txt 为后缀的文件：`find . -name "*.txt" | xargs -I {}  cp {} /tmp/{}.bak`
-i, --replace[=REPLACE_STR]|#作用同 -I 选项，参数 REPLACE_STR 是可选的，缺省为 {}。建议使用 -I 选项，因为其符合 POSIX
-L MAX_LINES|#限定最大输入行数。隐含了 -x 选项
-n, --max-args=MAX_ARGS|#表示命令在执行的时候一次使用参数的最大个数
-o, --open-tty|#在执行命令之前，在子进程中重新打开stdin作为/dev/TTY。如果您希望xargs运行交互式应用程序，这是非常有用的
-P, --max-procs=MAX_PROCS|#每次运行最大进程；缺省值为 1。如果MAX_PROCS为 0，xargs将一次运行尽可能多的进程。一般和-n或-L选项一起使用
-p, --interactive|#当每次执行一个argument的时候询问一次用户
--process-slot-var=NAME|#将指定的环境变量设置为每个正在运行的子进程中的唯一值。一旦子进程退出，将重用该值。例如，这可以用于初始负荷分配方案
-r, --no-run-if-empty|#当 xargs 的输入为空的时候则停止xargs，不用再去执行后面的命令了。为默认选项
-s, --max-chars=MAX_CHARS|#命令行的最大字符数，指的是xargs后面那个命令的最大命令行字符数，包括命令、空格和换行符。每个参数单独传入xargs后面的命令
--show-limits|#显示操作系统对命令行长度的限制
-t， --verbose|#先打印命令到标准错误输出，然后再执行
-x, --exit|#配合 -s 使用，当命令行字符数大于 -s 指定的数值时，退出 xargs

**示例**
1. 将 Shell 的特殊字符反引号还原为一般字符
```bash
echo '`0123`4 56789' | xargs -t echo
>echo `0123`4 56789 
>`0123`4 56789
```
如果直接进行如下操作，会报无法找到命令 01234 的错误，因为反引号在 Shell 中会将 01234 作为一个命令来执行，但是 01234 不是一个命令。-t 表示先打印命令，然后再执行。
```bash
echo `01234` 56789
>-bash: 01234: command not found
```
2. 设置 xargs 读入参数时的结束标识，以逗号结束。这里要注意结束标志必须要是单独的字段，即以空格或者换行符分隔的字段。
```bash
echo 01234 , 56789 | xargs -E ","
>01234
```
3. 使用 rm、mv 等命令同时操作多个文件时，有时会报 “argument list too long” 参数列表过长的错误，此时可以使用 xargs 来解决。xargs 将标准输入的字符串分隔后，作为参数传递给后面的命令。例如，给当前目录的所有文件添加后缀名。
```bash
ls | xargs -t -i mv {} {}.bak

# 选择符合条件的文件
ls | grep -E "201701|201702|201703" | xargs -I {} mv {} {}.bak
```
4. 设置命令行的最大字符数。参数默认一个一个单独传入命令中执行。
```bash
echo "01234 56789" | xargs -t -s 11
>echo 01234 
>01234
>echo 56789 
>56789
```
5. 设置标准输入中每次多少行作为命令的参数，默认是将标准输入中所有行的归并到一行一次性传给命令执行。
```bash
echo -e "01234\n56789\n01234" | xargs -t -L 2 echo
>echo 01234 56789 
>01234 56789
>echo 01234 
>01234
```
6. 将文件内容以空格分隔合并为一行输出。
```bash
# 列出文件内容
cat test.txt
a b c d e
f g h i j 
k l m n o

# 多行输入合并为一行输出
cat test.txt | xargs
a b c d e f g h i j k l m n o
```
7. 与ps、grep、awk和kill结合，强制终止指定进程。
```bash
ps -ef | grep spp | awk '{printf "%s ",$2}' | xargs kill -9
```

### cat
cat命令用来连接文件内容并打印输出到标准设备上，所以，它常常被用来查看显示文件的内容，或者将几个文件连接起来显示，或者从标准输入读取内容并显示，它常与重定向符号配合使用。
**cat命令三大功能**
1、显示一个文件的全部内容，cat file_name
2、创建一个文件，cat > file_name
3、合并文件，将几个文件合并到一个文件，cat file1 file2 > file
|选项|说明|
|------|-------|
-b, --number-nonblank     |对非空输出行编号
-E, --show-ends           |在每行结束处显示 $
-n, --number              |对输出的所有行编号,由1开始对所有输出的行数编号
-s, --squeeze-blank       |有连续两行以上的空白行，就代换为一行的空白行 
-T, --show-tabs          |将跳格字符显示为 ^I
示例
1. 键盘录入内容到文件，回车是保存，退出Ctrl+z
```bash
[root@localhost ~]# cat > mingongge.txt
111111111111111
2233445566778899
0126459fdfdfdkffffkfkfkfkfdkfdkdfkk
^Z
[4]+  Stopped                 cat > mingongge.tx
```
2. 合并文件
```bash
[root@localhost ~]# cat mingongge.tar.gz_?? > mingongge.tar.gz   
#可以用cat命令将多个压缩包合并成一个
```
3. 追加文字内容
```bash
cat mingongge.txt >> mingongge.doc  #将mingongge.txt内容添加到mingongge.doc内容后
```
4. 插入多行内容
```bash
[root@localhost ~]# cat >> mingongge.doc <<EOF
> 111111111111
> 222222222222
> aa+aabb-bbcc
> EOF
#将你所要输入的内容插入到文件中，输入EOF即为结束插入，EOF也可以使用其它字符替代。
```
### wc
wc 命令用来统计文件中的行数、单词数或字节数，然后将结果输出在终端上。我们可以使用 wc 命令来计算文件的Byte数、字数或是列数
**语法格式**
```bash
wc [选项] [文件]
wc [OPTION] [FILE]
```
**选项说明**
|选项|说明|
|------|-------|
-c |统计字节数
-l |统计行数
-m |统计字符数
-w |统计字数
-L |显示最长行的长度

### ls
ls(list)，ls命令显示指定目录下的内容，列出指定目录下所含的文件及子目录。此命令与Windows系统中dir命令功能相似。
ls命令的输出信息可以进行彩色加亮显示，以分区不同类型的文件。
**选项说明**
|选项|说明|
|------|-------|
-a |显示指定目录下的所有文件以及子目录，包含隐藏文件
-A |显示指定目录下的（除“.”和“..”之外）所有文件及子目录
-d |显示指定目录的属性信息
-l |显示指定目录下的文件及子目录详细信息,输出的信息从左到右依次包括文件名，文件类型、权限模式、硬连接数、所有者、组、文件大小和文件的最后修改时间等
-t |以时间顺序显示指定目录下的文件及子目录
-F|在列出的文件名称后加一符号；例如可执行档则加 "*", 目录则加 "/"
-k|以KB（千字节）为单位显示文件大小
-m|用“,”号区隔每个文件和目录的名称
-s|显示文件和目录的大小，以区块为单位
-L|如果遇到性质为符号链接的文件或目录，直接列出该链接所指向的原始文件或目录
-R|递归处理，将指定目录下的所有文件及子目录一并处理
**示例**
1. 计算当前目录下的文件数和目录数
```bash
ls -l * |grep "^-" |wc -l
ls -l * |grep  "^d" |wc -l
```
2.在ls中列出文件的绝对路径
```bash
ls |sed "s:^:`pwd`/:"
```