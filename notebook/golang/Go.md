- [1.基础](#1基础)
  - [1.1 基础数据类型](#11-基础数据类型)
    - [整型](#整型)
    - [浮点数](#浮点数)
    - [string](#string)
    - [byte和rune](#byte和rune)
    - [bool](#bool)
    - [const](#const)
    - [iota 常量生成器](#iota-常量生成器)
  - [1.2 逻辑语句](#12-逻辑语句)
    - [if](#if)
    - [for](#for)
    - [switch](#switch)
    - [goto](#goto)
  - [1.3 函数](#13-函数)
    - [变长参数](#变长参数)
    - [defer](#defer)
    - [闭包](#闭包)
      - [将函数作为返回值](#将函数作为返回值)
      - [使用闭包调试](#使用闭包调试)
    - [错误处理](#错误处理)
  - [1.4 复合数据类型](#14-复合数据类型)
    - [数组](#数组)
    - [slice](#slice)
      - [声明](#声明)
      - [内置方法](#内置方法)
    - [map](#map)
  - [1.5 结构体](#15-结构体)
    - [匿名字段和内嵌结构体](#匿名字段和内嵌结构体)
    - [命名冲突](#命名冲突)
    - [方法](#方法)
  - [1.6 interface](#16-interface)
    - [接口嵌套接口](#接口嵌套接口)
    - [类型断言：如何检测和转换接口变量的类型](#类型断言如何检测和转换接口变量的类型)
    - [获取type](#获取type)
    - [测试变量是否实现了接口函数](#测试变量是否实现了接口函数)
    - [接口上的方法集](#接口上的方法集)
    - [空接口](#空接口)
      - [构建通用类型或包含不同类型变量的数组](#构建通用类型或包含不同类型变量的数组)
      - [复制数据切片至空接口切片](#复制数据切片至空接口切片)
    - [通用类型的节点数据结构](#通用类型的节点数据结构)
  - [1.7 并发](#17-并发)
    - [go func](#go-func)
    - [chan struct](#chan-struct)
      - [select](#select)

# 1.基础

## 1.1 基础数据类型

声明变量的一般形式是使用 var 关键字：

```go
var name type
var hp int = 100
var hp1 = 100
hp2 := 100 //简化写法
```

其中，var 是声明变量的关键字，name 是变量名，type 是变量的类型。

简化写法不能提供数据类型，只能用在函数内部

Go语言的基本类型有：

- bool
- string
- int、int8、int16、int32、int64
- uint、uint8、uint16、uint32、uint64、uintptr
- byte // uint8 的别名
- rune // int32 的别名 代表一个 Unicode 码
- float32、float64
- complex64、complex128
当一个变量被声明之后，系统自动赋予它该类型的零值：int 为 0，float 为 0.0，bool 为 false，string 为空字符串，指针为 nil 等

### 整型

Go语言同时提供了有符号和无符号类型的整数运算。有int8、int16、int32和int64四种有符号整数类型，分别对应8、16、32、64bit大小的有符号整数，与此对应的是uint8、uint16、uint32和uint64四种无符号整数类型。

int和uint，一般为32或64bit，这跟硬件平台相关

rune类型是和int32等价的类型，通常用于表示一个Unicode字符。这两个名称可以互换使用。同样byte也是uint8类型的等价类型，byte类型一般用于强调数值是一个原始的数据而不是一个小的整数。

### 浮点数

这些浮点数类型的取值范围可以从很微小到很巨大。浮点数取值范围的极限值可以在 math 包中找到：
常量 math.MaxFloat32 表示 float32 能取到的最大数值，大约是 3.4e38；
常量 math.MaxFloat64 表示 float64 能取到的最大数值，大约是 1.8e308；
float32 和 float64 能表示的最小值分别为 1.4e-45 和 4.9e-324。

一个 float32 类型的浮点数可以提供大约 6 个十进制数的精度，而 float64 则可以提供约 15 个十进制数的精度，通常应该**优先使用 float64 类型**。

```go
var f float32 = 16777216 // 1 << 24
fmt.Println(f == f+1)    // "true"!
```

### string

可以使用双引号`""`来定义字符串。字符串的值是不可变的：一个字符串包含的字节序列永远不会被改变

字符串的内容（纯字节）可以通过标准索引法来获取，在方括号`[]`内写入索引，索引从 0 开始计数：

- 字符串 str 的第 1 个字节：`str[0]`
- 第 i 个字节：`str[i - 1]`
- 最后 1 个字节：`str[len(str)-1]`

**注意**：获取字符串中某个字节的地址属于非法行为，例如 &str[i]。

**字符串拼**:两个字符串 s1 和 s2 可以通过 s := s1 + s2 拼接在一起。将 s2 追加到 s1 尾部并生成一个新的字符串 s。

### byte和rune

字符串中的每一个元素叫做“字符”，在遍历或者单个获取字符串元素时可以获得字符。

Go语言的字符有以下两种：

- 一种是 uint8 类型，或者叫 byte 型，代表了 ASCII 码的一个字符。
- 另一种是 rune 类型，代表一个 UTF-8 字符，当需要处理中文、日文或者其他复合字符时，则需要用到 rune 类型。rune 类型等价于 int32 类型。

byte 类型是 uint8 的别名，对于只占用 1 个字节的传统 ASCII 编码的字符来说，完全没有问题，例如 var ch byte = 'A'，字符使用单引号括起来。

在 ASCII 码表中，A 的值是 65，使用 16 进制表示则为 41，所以下面的写法是等效的：

```go
var ch byte = 65 或 var ch byte = '\x41'      //（\x 总是紧跟着长度为 2 的 16 进制数）
```

### bool

```go
var aVar = 10
aVar == 5  // false
aVar == 10 // true
aVar != 5  // true
aVar != 10 // false
```

布尔值并不会隐式转换为数字值 0 或 1，反之亦然，必须使用 if 语句显式的进行转换

```go
i := 0
if b {
    i = 1
}
```

### const

你可以省略类型说明符 [type]，因为编译器可以根据变量的值来推断其类型。
显式类型定义： const b string = "abc"
隐式类型定义： const b = "abc"

常量的值必须是能够在编译时就能够确定的，可以在其赋值表达式中涉及计算过程，但是所有用于计算的值必须在编译期间就能获得。

- 正确的做法：const c1 = 2/3
- 错误的做法：const c2 = getNumber() // 引发构建错误: getNumber() 用做值

如果是批量声明的常量，除了第一个外其它的常量右边的初始化表达式都可以省略，如果省略初始化表达式则表示使用前面常量的初始化表达式，对应的常量类型也是一样的。例如

```go
const (
    a = 1
    b
    c = 2
    d
)
fmt.Println(a, b, c, d) // "1 1 2 2"
```

### iota 常量生成器

常量声明可以使用iota常量生成器初始化，它用于生成一组以相似规则初始化的常量，但是不用每行都写一遍初始化表达式。在一个const声明语句中，在第一个声明的常量所在的行，iota将会被置为0，然后在每一个有常量声明的行加一。

```go
type Weekday int

const (
    Sunday Weekday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
)
```

还可以加上一些表达式

```go
const (
 _   = 1 << (10 * iota)
 KiB // 1024
 MiB // 1048576
 GiB // 1073741824
 TiB // 1099511627776             (exceeds 1 << 32)
 PiB // 1125899906842624
 EiB // 1152921504606846976
 ZiB // 1180591620717411303424    (exceeds 1 << 64)
 YiB // 1208925819614629174706176
)
```

## 1.2 逻辑语句

### if

```go

if condition {
    // do something
} else {
    // do something
}
```

关键字 if 和 else 之后的左大括号{必须和关键字在同一行，如果你使用了 else if 结构，则前段代码块的右大括号}必须和 else if 关键字在同一行，这两条规则都是被编译器强制规定的。

if 还有一种特殊的写法，可以在 if 表达式之前添加一个执行语句，再根据变量值进行判断

```go
if err := Connect(); err != nil {
    fmt.Println(err)
    return
}
```

### for

```go
sum := 0
for i := 0; i < 10; i++ {
    sum += i
}
```

简易版(类似c++的while)：

```go
sum := 0
for {
    sum++
    if sum > 100 {
        break
    }
}
```

for 支持 continue 和 break 来控制循环，但是它提供了一个更高级的 break，可以选择中断哪一个循环，如下例：

```go
for j := 0; j < 5; j++ {
    for i := 0; i < 10; i++ {
        if i > 5 {
            break JLoop
        }
        fmt.Println(i)
    }
}
JLoop:
// ...
```

break 语句终止的是 JLoop 标签处的外层循环

### switch

```go
var a = "hello"
switch a {
case "hello":
    fmt.Println(1)
case "world":
    fmt.Println(2)
default:
    fmt.Println(0)
}
```

匹配项后面不需要加`break`

case 后面可以带多个表达式，

```go
case 5,10,15
```

switch 后面不写表达式，Go 会当成 switch true，就会变成条件匹配（能写判断语句），和if一样

```go
switch {
case x > 0:
    fmt.Println("Positive")
case x < 0:
    fmt.Println("Negative")
default:
    fmt.Println("Zero")
}
```

switch 默认只匹配一个分支，但是可以增加`fallthrough`继续执行下一个case,不做语句判断

```go
switch grade:=90 {
    case grade >90:
        fmt.Println('1')
        fallthrough
    case grade >70:
        fmt.Println('2')
        fallthrough
    case grade >60:
        fmt.Println('3')
    case grade >50:
        fmt.Println('4')
}
```

### goto

goto 语句可以让程序切换到某个被 Label 标记的地方继续执行。

```go
    i := 0
Start:
    fmt.Println(i)
    if i > 5 {
        goto End
    } else {
        i += 1
        goto Start
    }
End:

```

## 1.3 函数

```go
func f2(a int, b byte) (int, bool){

}
```

前一个括号里是输入和类型，后一个括号内是输出类型

### 变长参数

如果函数的最后一个参数是采用 ...type 的形式，那么这个函数就可以处理一个变长的参数，这个长度可以为 0，这样的函数称为变参函数。

```go
// func myFunc(a, b, arg ...int) {}
func Greeting(prefix string, who ...string)
Greeting("hello:", "Joe", "Anna", "Eileen")

```

如果参数被存储在一个 slice 类型的变量 slice 中，则可以通过 slice... 的形式来传递参数，调用变参函数。

```go
package main

import "fmt"

func main() {
 x := min(1, 3, 2, 0)
 fmt.Printf("The minimum is: %d\n", x)
 slice := []int{7,9,3,5,1}
 x = min(slice...)
 fmt.Printf("The minimum in the slice is: %d", x)
}

func min(s ...int) int {
 if len(s)==0 {
  return 0
 }
 min := s[0]
 for _, v := range s {
  if v < min {
   min = v
  }
 }
 return min
}
```

如果变长参数的类型并不是都相同？使用多 个参数来进行传递并不是很明智的选择，有 2 种方案可以解决这个问题：

1. 使用struct：

    定义一个结构类型，假设它叫 Options，用以存储所有可能的参数：

    ```go
    type Options struct {
     par1 type1,
     par2 type2,
     ...
    }
    ```

    函数 F1() 可以使用正常的参数 a 和 b，以及一个没有任何初始化的 Options 结构： F1(a, b,   Options {})。如果需要对选项进行初始化，则可以使用 F1(a, b, Options {par1:val1,    par2:val2})。

2. 使用interface：

    如果一个变长参数的类型没有被指定，则可以使用默认的空接口 interface{}，这样就可以接受任何类型的参数。该方案不仅可以用于长度未知的参数，还可以用于任何不确定类型的 参数。一般而言可以使用一个 for-range 循环以及 switch 结构对每个参数的类型进行判断：

    ```go
    func typecheck(..,..,values … interface{}) {
     for _, value := range values {
      switch v := value.(type) {
       case int: …
       case float: …
       case string: …
       case bool: …
       default: …
      }
     }
    }
    ```

### defer

允许我们延迟到函数返回之前（或任意位置执行 return 语句之后）一刻才执行某个语句或函数

```go
package main
import "fmt"

func main() {
 function1()
}

func function1() {
 fmt.Printf("In function1 at the top\n")
 defer function2()
 fmt.Printf("In function1 at the bottom!\n")
}

func function2() {
 fmt.Printf("Function2: Deferred until the end of the calling function!")
}
/*
In Function1 at the top
In Function1 at the bottom!
Function2: Deferred until the end of the calling function!
*/
```

当有多个 defer 行为被注册时，它们会以逆序执行（类似栈，即后进先出）：

```go
func f() {
 for i := 0; i < 5; i++ {
  defer fmt.Printf("%d ", i)
 }
}
// 4 3 2 1 0
```

defer可以用在关闭文件流 、解锁加锁资源、打印最终报告

使用 defer 语句来记录函数的参数与返回值

```go
package main

import (
 "io"
 "log"
)

func func1(s string) (n int, err error) {
 defer func() {
  log.Printf("func1(%q) = %d, %v", s, n, err)
 }()
 return 7, io.EOF
}

func main() {
 func1("Go")
}
//Output: 2011/10/04 10:46:11 func1("Go") = 7, EOF
```

### 闭包

当我们不希望给函数起名字的时候，可以使用匿名函数。这样的一个函数不能够独立存在（编译器会返回错误：non-declaration statement outside function body），但可以被赋值于某个变量，即保存函数的地址到变量中：`fplus := func(x, y int) int { return x + y }`，然后通过变量名对函数进行调用：`fplus(3,4)`

```go
package main

import "fmt"

func main() {
 f()
}
func f() {
 for i := 0; i < 4; i++ {
  g := func(i int) { fmt.Printf("%d ", i) }
  g(i)
  fmt.Printf(" - g is of type %T and has value %v\n", g, g)
 }
}
```

特殊案例

```go
package main

import "fmt"

func f() (ret int) {
 defer func() {
  ret++
 }()
 return 1
}
func main() {
 fmt.Println(f())
}
// 2
```

#### 将函数作为返回值

```go
package main

import "fmt"

func main() {
 // make an Add2 function, give it a name p2, and call it:
 p2 := Add2()
 fmt.Printf("Call Add2 for 3 gives: %v\n", p2(3))
 // make a special Adder function, a gets value 2:
 TwoAdder := Adder(2)
 fmt.Printf("The result is: %v\n", TwoAdder(3))
}

func Add2() func(b int) int {
 return func(b int) int {
  return b + 2
 }
}

func Adder(a int) func(b int) int {
 return func(b int) int {
  return a + b
 }
}
```

为字符串增加指定后缀

```go
func MakeAddSuffix(suffix string) func(string) string {
 return func(name string) string {
  if !strings.HasSuffix(name, suffix) {
   return name + suffix
  }
  return name
 }
}
```

#### 使用闭包调试

在分析和调试复杂的程序时，无数个函数在不同的代码文件中相互调用，如果这时候能够准确地知道哪个文件中的具体哪个函数正在执行，对于调试是十分有帮助的。您可以使用 runtime 或 log 包中的特殊函数来实现这样的功能。包 runtime 中的函数 Caller() 提供了相应的信息，因此可以在需要的时候实现一个 where() 闭包函数来打印函数执行的位置

```go
where := func() {
 _, file, line, _ := runtime.Caller(1)
 log.Printf("%s:%d", file, line)
}
where()
// some code
where()
// some more code
where()
```

### 错误处理

默认情况下，如果运行发生错误，程序就会停止运行，所以需要捕获异常，并让程序继续运行

```go
func test(){
    defer func(){
        err:= recover() //内置函数，用来捕获异常
        if err != nil {
            fmt.Println(err)
        }
        
    }()

    num1 := 10
    num := 0
    res := num1/num
}
```

## 1.4 复合数据类型

### 数组

数组的声明语法如下：

```go
var intarray [10]int

q := [...]int{1, 2, 3}
// "..."表示数组的长度是根据初始化值的个数来计算
```

上面是直接提供顺序初始化值序列，但是也可以指定一个索引和对应值列表的方式初始化

```go
type Currency int

const (
    USD Currency = iota // 美元
    EUR                 // 欧元
    GBP                 // 英镑
    RMB                 // 人民币
)

symbol := [...]string{USD: "$", EUR: "€", GBP: "￡", RMB: "￥"}

fmt.Println(RMB, symbol[RMB]) // "3 ￥"
```

在这种形式的数组字面值形式中，初始化索引的顺序是无关紧要的，而且没用到的索引可以省略，和前面提到的规则一样，未指定初始值的元素将用零值初始化。例如，

```go
r := [...]int{99: -1}
```

定义了一个含有100个元素的数组r，最后一个元素被初始化为-1，其它元素都是用0初始化。

遍历数组的方法如下

```go
//
var team [3]string
team[0] = "hammer"
team[1] = "soldier"
team[2] = "mum"
for k, v := range team {
    fmt.Println(k, v)
}
```

### slice

slice是一种引用类型，其结构类似

```go
type IntSlice struct {
    ptr      *int
    len, cap int
}
```

#### 声明

切片（slice）是对数组的一个连续片段的引用，所以切片是一个引用类型,（类似于 C/C++ 中的数组类型，或者 Python 中的 list 类型）

1. 从数组或切片生成新的切片

    切片默认指向一段连续内存区域，可以是数组，也可以是切片本身。

    从连续内存区域生成切片是常见的操作，格式如下：

    ```go
    //slice [开始位置 : 结束位置]
    var a  = [3]int{1, 2, 3}
    fmt.Println(a, a[1:2]) //[1 2 3]  [2]
    fmt.Println(a[1:], a[:2]) // [2,3] [1,2]
    fmt.Println(a[:]) // [1,2,3]
    ```

2. 直接声明

    与数组的声明的区别在于指定长度。
    如果不初始化

    ```go
    // var name []Type
    var strList []string
    var numList []int
    var numListEmpty = []int{} //初始化
    fmt.Println(numList == nil) // true
    fmt.Println(numListEmpty == nil) // false
    ```

    切片是动态结构，只能与 nil 判定相等，不能互相判定相等。声明新的切片后，可以使用 append() 函数向切片中添加元素。

3. make

    ```go
    //make( []Type, size, cap )
    //Type 是指切片的元素类型，size 指的是为这个类型分配多少个元素，cap 为预分配的元素数量，这个值设定后不影响 size，只是能提前分配空间，降低多次分配空间造成的性能问题
    a := make([]int, 2)
    b := make([]int, 2, 10)
    ```

#### 内置方法

1. append

    ```go
    var a []int
    a = append(a, 1) // 追加1个元素
    a = append(a, 1, 2, 3) // 追加多个元素, 手写解包方式
    a = append(a, []int{1,2,3}...) // 追加一个切片, 切片需要解包
    ```

    在使用 append() 函数为切片动态添加元素时，如果空间不足以容纳足够多的元素，切片就会进行“扩容”，此时新切片的长度会发生改变。

    切片在扩容时，容量的扩展规律是按容量的 2 倍数进行扩充，例如 1、2、4、8、16……

    ```go
    var numbers []int
    for i := 0; i < 10; i++ {
        numbers = append(numbers, i)
        fmt.Printf("len: %d  cap: %d pointer: %p\n", len(numbers), cap(numbers), numbers)
    }
    ```

    也可以在头部增加元素,

    ```go
    var a = []int{1,2,3}
    a = append([]int{0}, a...) // 在开头添加1个元素
    a = append([]int{-3,-2,-1}, a...) // 在开头添加1个切片
    ```

    在切片开头添加元素一般都会导致内存的重新分配，而且会导致已有元素全部被复制 1 次，因此，从切片的开头添加元素的性能要比从尾部追加元素的性能差很多。

    因为 append 函数返回新切片的特性，所以切片也支持链式操作，我们可以将多个 append 操作组合起来，实现在切片中间插入元素：

    ```go
    var a []int
    a = append(a[:i], append([]int{x}, a[i:]...)...) // 在第i个位置插入x
    a = append(a[:i], append([]int{1,2,3}, a[i:]...)...) // 在第i个位置插入切片```
    ```

2. copy

    可以将一个数组切片复制到另一个数组切片中，如果加入的两个数组切片不一样大，就会按照其中较小的那个数组切片的元素个数进行复制。

    ```go
    slice1 := []int{1, 2, 3, 4, 5}
    slice2 := []int{5, 4, 3}
    copy(slice2, slice1) // 只会复制slice1的前3个元素到slice2中
    copy(slice1, slice2) // 只会复制slice2的3个元素到slice1的前3个位置
    ```

3. for循环

   ```go
   import "fmt"

    // nonempty returns a slice holding only the non-empty strings.
    // The underlying array is modified during the call.
    func nonempty(strings []string) []string {
        i := 0
        for _, s := range strings {
            if s != "" {
                strings[i] = s
                i++
            }
        }
        return strings[:i]
    }
   ```

### map

map 是**引用**类型，一种元素对（pair）的无序集合，pair 对应一个 key（索引）和一个 value（值），所以这个结构也称为关联数组或字典，这是一种能够快速寻找值的理想结构，给定 key，就可以迅速找到对应的 value。

```go
var mapname map[keytype]valuetype
// - mapname 为 map 的变量名。
// - keytype 为键类型。
// - valuetype 是键对应的值类型。
//[keytype] 和 valuetype 之间允许有空格。
```

在声明的时候不需要知道 map 的长度，因为 map 是可以动态增长的，未初始化的 map 的值是 nil，使用函数 len() 可以获取 map 中 pair 的数目。

和数组不同，map 可以根据新增的 key-value 动态的伸缩，因此它不存在固定长度或者最大限制，但是也可以选择标明 map 的初始容量 capacity，格式如下：

```go
make(map[keytype]valuetype, cap)
```

既然一个 key 只能对应一个 value，而 value 又是一个原始类型，那么如果一个 key 要对应多个值怎么办？通过将 value 定义为 []int 类型或者其他类型的切片，就可以解决

```go
mp1 := make(map[int][]int)
mp2 := make(map[int]*[]int)
```

直接初始化

```go
m := map[int]int{
    0:0,
    1:1,                                  // 最后的逗号是必须的
}
n := map[string]S{
    "a":S{0,1},
    "b":{2,3},                            // 类型名称可省略
}
```

增查删改

```go
m[0] = 3                              // 修改m中key为0的值为3
m[4] = 8                              // 添加到m中key为4值为8

a := n["a"]                           // 获取n中key为"a"的值
b, ok := n["c"]                       // 取值, 并通过ok(bool)判断key对应的元素是否存在.

delete(n, "a")                        // 使用内置函数delete删除key为"a"对应的元素.
```

清空 map 的唯一办法就是重新 make 一个新的 map

遍历

```go
for k,v :=range m{
    
}
```

## 1.5 结构体

结构体定义的一般方式如下

```go
type identifier struct {
    field1 type1
    field2 type2
    ...
}
```

有4种初始化方法

```go
var p T
var p1 = T{}
var p2 *T = new(T) //结构体指针
var p3 *T = &T{}
```

然后像下面这样给它的字段赋值：

```go
var s T
s.a = 5
s.b = 8

//结构体指针的标准方式是`(*s).a = 5`
//但go做了简化，可以直接写`s.a = 5` ,由编译器进行转化



// 或者在声明时就赋值
var p4 = T{5,8}  //要注意顺序
var p5 = T{field1:5,field2:8} 
```

数组可以看作是一种结构体类型，不过它使用下标而不是具名的字段。

**使用 `new()`**

使用 `new()` 函数给一个新的结构体变量分配内存，它返回指向已分配内存的指针：`var t *T = new(T)`，如果需要可以把这条语句放在不同的行。

```go
var t *T
t = new(T)
```

写这条语句的惯用方法是：`t := new(T)`，变量 `t` 是一个指向 `T` 的指针，此时结构体字段的值是它们所属类型的零值。

```go
package main
import "fmt"

type struct1 struct {
    i1  int
    f1  float32
    str string
}

func main() {
    ms := new(struct1)
    ms.i1 = 10
    ms.f1 = 15.5
    ms.str= "Chris"
    fmt.Println(ms) // &{10 15.5 Chris}
}
```

使用 `fmt.Println()` 打印一个结构体的默认输出可以很好的显示它的内容，类似使用 `%v` 选项。

初始化一个结构体实例（一个结构体字面量：struct-literal）的更简短和惯用的方式如下：

```go
    ms := &struct1{10, 15.5, "Chris"}
    // 此时 ms 的类型是 *struct1

    ms1 = struct1{i1:10, f1:15.5, str:"Chris"}
    var ms2 struct1
    ms2 = struct1{10, 15.5, "Chris"}
```

混合字面量语法 (composite literal syntax) `&struct1{a, b, c}` 是一种简写，底层仍然会调用 `new()`，这里值的顺序必须按照字段顺序来写。在下面的例子中能看到可以通过在值的前面放上字段名来初始化字段的方式。表达式 `new(Type)` 和 `&Type{}` 是等价的。

### 匿名字段和内嵌结构体

结构体可以包含一个或多个 **匿名（或内嵌）字段**，即这些字段没有显式的名字，只有字段的类型是必须的，此时类型就是字段的名字。匿名字段本身可以是一个结构体类型，即 **结构体可以包含内嵌结构体**。

```go
package main

import "fmt"

type innerS struct {
 in1 int
 in2 int
}

type outerS struct {
 b    int
 c    float32
 int  // anonymous field
 innerS //anonymous field
}

func main() {
 outer := new(outerS)
 outer.b = 6
 outer.c = 7.5
 outer.int = 60
 outer.in1 = 5
 outer.in2 = 10

// 使用结构体字面量
outer2 := outerS{6, 7.5, 60, innerS{5, 10}}
}
```

### 命名冲突

当两个字段拥有相同的名字（可能是继承来的名字）时该怎么办呢？

1. 外层名字会覆盖内层名字（但是两者的内存空间都保留），这提供了一种重载字段或方法的方式；
2. 如果相同的名字在同一级别出现了两次，如果这个名字被程序使用了，将会引发一个错误（不使用没关系）。没有办法来解决这种问题引起的二义性，必须由程序员自己修正。

```go
type A struct {a int}
type B struct {a, b int}

type C struct {A; B}
var c C
//只能用c.A.a 和 c.B.a来调用
```

### 方法

方法值是将一个方法绑定到特定接收器对象上并得到一个函数值。通过这个函数值，你可以在不需要指定接收器的情况下调用该方法。

```go
type Point struct{ X, Y float64 }

func (p Point) Distance(q Point) float64 {
// calculate distance between p and q
}

p := Point{1, 2}
q := Point{4, 6}
distanceFromP := p.Distance // method value
distance := distanceFromP(q) // Call the method using method value
```

有两种参数传输方式

1. 按值传递，调用函数时会复制该对象与传递函数形参，在函数内部修改该对象需要通过return来返回（否则将只相当于函数内部的临时变量）
2. 按指针传递，调用函数时将传递对象指针，然后传递函数形参，在函数内部的修改就是对指针指向的内存的修改。

```go
import "fmt"

type Number struct {
sum int
}

func (n Number) Add(i int) Number {
n.sum += i
//res = n
return n
}

func (np *Number) AddbyPtr(i int) {
np.sum += i
}

func Test() {
a := Number{1}
b := Number{1}
a.Add(1)
fmt.Printf("a: %d\n", a.sum)
b.AddbyPtr(1)
fmt.Printf("b: %d\n", b.sum)

fmt.Println()

c := a
c.Add(1)
fmt.Printf("a: %d\n", a.sum)
fmt.Printf("c: %d\n", c.sum)

e := a.Add(1)
fmt.Printf("e: %d\n", e.sum)

fmt.Println()

d := b
d.AddbyPtr(1)
fmt.Printf("b: %d\n", b.sum)
fmt.Printf("d: %d\n", d.sum)
}

/*
运行结果：
a: 1
b: 2

a: 1
c: 1
e: 2

b: 2
d: 3
*/
```

## 1.6 interface

接口定义了一组方法（方法集），但是这些方法不包含（实现）代码：它们没有被实现（它们是抽象的）。接口里也不能包含变量。

通过如下格式定义接口：

```go
type Namer interface {
    Method1(param_list) return_type
    Method2(param_list) return_type
    ...
}
```

上面的 `Namer` 是一个 **接口类型**。

```go
package main

import "fmt"

type Shaper interface {
 Area() float32
}

type Square struct {
 side float32
}

func (sq *Square) Area() float32 {
 return sq.side * sq.side
}

func main() {
 sq1 := new(Square)
 sq1.side = 5

 var areaIntf Shaper
 areaIntf = sq1
 // shorter,without separate declaration:
 // areaIntf := Shaper(sq1)
 // or even:
 // areaIntf := sq1
 fmt.Printf("The square has area: %f\n", areaIntf.Area())
}

```

多态：

```go
package main

import "fmt"

type Shaper interface {
 Area() float32
}

type Square struct {
 side float32
}

func (sq *Square) Area() float32 {
 return sq.side * sq.side
}

type Rectangle struct {
 length, width float32
}

func (r Rectangle) Area() float32 {
 return r.length * r.width
}

func main() {

 r := Rectangle{5, 3} // Area() of Rectangle needs a value
 q := &Square{5}      // Area() of Square needs a pointer
 // shapes := []Shaper{Shaper(r), Shaper(q)}
 // or shorter
 shapes := []Shaper{r, q}
 fmt.Println("Looping through shapes for area ...")
 for n, _ := range shapes {
  fmt.Println("Shape details: ", shapes[n])
  fmt.Println("Area of this shape is: ", shapes[n].Area())
 }
}
```

### 接口嵌套接口

```go
type ReadWrite interface {
    Read(b Buffer) bool
    Write(b Buffer) bool
}

type Lock interface {
    Lock()
    Unlock()
}

type File interface {
    ReadWrite
    Lock
    Close()
}
```

### 类型断言：如何检测和转换接口变量的类型

如果转换合法，`v` 是 `varI` 转换到类型 `T` 的值，`ok` 会是 `true`；否则 `v` 是类型 `T` 的零值，`ok` 是 `false`，也没有运行时错误发生。

```go
if v, ok := varI.(T); ok {  // checked type assertion
    Process(v)
    return
}
// varI is not of type T

```

```go
package main

import (
 "fmt"
 "math"
)

type Square struct {
 side float32
}

type Circle struct {
 radius float32
}

type Shaper interface {
 Area() float32
}

func main() {
 var areaIntf Shaper
 sq1 := new(Square)
 sq1.side = 5

 areaIntf = sq1
 // Is Square the type of areaIntf?
 if t, ok := areaIntf.(*Square); ok {
  fmt.Printf("The type of areaIntf is: %T\n", t)
 }
 if u, ok := areaIntf.(*Circle); ok {
  fmt.Printf("The type of areaIntf is: %T\n", u)
 } else {
  fmt.Println("areaIntf does not contain a variable of type Circle")
 }
}

func (sq *Square) Area() float32 {
 return sq.side * sq.side
}

func (ci *Circle) Area() float32 {
 return ci.radius * ci.radius * math.Pi
}
```

### 获取type

```go
switch t := areaIntf.(type) {
case *Square:
 fmt.Printf("Type Square %T with value %v\n", t, t)
case *Circle:
 fmt.Printf("Type Circle %T with value %v\n", t, t)
case nil:
 fmt.Printf("nil value: nothing to check?\n")
default:
 fmt.Printf("Unexpected type %T\n", t)
}
```

### 测试变量是否实现了接口函数

```go
type Stringer interface {
    String() string
}

if sv, ok := v.(Stringer); ok {
    fmt.Printf("v implements String(): %s\n", sv.String()) // note: sv, not v
}

```

### 接口上的方法集

作用于变量上的方法实际上是不区分变量到底是指针还是值的。当碰到接口类型值时，这会变得有点复杂，原因是接口变量中存储的具体值是不可寻址的

```go
package main

import (
 "fmt"
)

type List []int

func (l List) Len() int {
 return len(l)
}

func (l *List) Append(val int) {
 *l = append(*l, val)
}

type Appender interface {
 Append(int)
}

func CountInto(a Appender, start, end int) {
 for i := start; i <= end; i++ {
  a.Append(i)
 }
}

type Lener interface {
 Len() int
}

func LongEnough(l Lener) bool {
 return l.Len()*10 > 42
}

func main() {
 // A bare value
 var lst List
 // compiler error:
 // cannot use lst (type List) as type Appender in argument to CountInto:
 //       List does not implement Appender (Append method has pointer receiver)
 // CountInto(lst, 1, 10)
 if LongEnough(lst) { // VALID: Identical receiver type
  fmt.Printf("- lst is long enough\n")
 }

 // A pointer value
 plst := new(List)
 CountInto(plst, 1, 10) // VALID: Identical receiver type
 if LongEnough(plst) {
  // VALID: a *List can be dereferenced for the receiver
  fmt.Printf("- plst is long enough\n")
 }
}
```

**讨论**

在 `lst` 上调用 `CountInto` 时会导致一个编译器错误，因为 `CountInto` 需要一个 `Appender`，而它的方法 `Append` 只定义在指针上。 在 `lst` 上调用 `LongEnough` 是可以的，因为 `Len` 定义在值上。

在 `plst` 上调用 `CountInto` 是可以的，因为 `CountInto` 需要一个 `Appender`，并且它的方法 `Append` 定义在指针上。 在 `plst` 上调用 `LongEnough` 也是可以的，因为指针会被自动解引用。

**总结**

在接口上调用方法时，必须有和方法定义时相同的接收者类型或者是可以根据具体类型 `P` 直接辨识的：

- 指针方法可以通过指针调用
- 值方法可以通过值调用
- 接收者是值的方法可以通过指针调用，因为指针会首先被解引用
- 接收者是指针的方法不可以通过值调用，因为存储在接口中的值没有地址

将一个值赋值给一个接口时，编译器会确保所有可能的接口方法都可以在此值上被调用，因此不正确的赋值在编译期就会失败。

Go 语言规范定义了接口方法集的调用规则：

- 类型 `*T` 的可调用方法集包含接受者为 `*T` 或 `T` 的所有方法集
- 类型 `T` 的可调用方法集包含接受者为 `T` 的所有方法
- 类型 `T` 的可调用方法集**不**包含接受者为 `*T` 的方法

### 空接口

**空接口或者最小接口** 不包含任何方法，它对实现不做任何要求：

空接口类型的变量赋任何类型的值。

```go
type Any interface {}

var val Any
val = 5
val = str
pers1 := new(Person)
pers1.name = "Rob Pike"
pers1.age = 55
val = pers1

switch t := val.(type) {
case int:
    ...
case string:
    ...
}
```

每个 `interface {}` 变量在内存中占据两个字长：一个用来存储它包含的类型，另一个用来存储它包含的数据或者指向数据的指针

#### 构建通用类型或包含不同类型变量的数组

```go
type Element interface{}
type Vector struct {
 a []Element
}

func main() {
 var  m Vector
 m.a = append(m.a, 1)
 m.a = append(m.a, 1.1)
 m.a = append(m.a, "hello")
 for i, v := range m.a {
     fmt.Printf("m.a[%d] = %v (%T)\n", i, v, v)
 }

}

```

#### 复制数据切片至空接口切片

假设你有一个 `myType` 类型的数据切片，你想将切片中的数据复制到一个空接口切片中，类似：

```go
var dataSlice []myType = FuncReturnSlice()
var interfaceSlice []interface{} = dataSlice
```

可惜不能这么做，编译时会出错：`cannot use dataSlice (type []myType) as type []interface { } in assignment`。

原因是它们俩在内存中的布局是不一样的,接口切片是被特殊实现的，在底层类似于下面结构，由类型和指针组成的数据对

```go
type iface struct {
    tab  *itab     // 指向类型信息和方法表
    data unsafe.Pointer // 指向实际值的内存
}
```

必须使用 `for-range` 语句来一个一个显式地赋值：

```go
var dataSlice []myType = FuncReturnSlice()
var interfaceSlice []interface{} = make([]interface{}, len(dataSlice))
for i, d := range dataSlice {
    interfaceSlice[i] = d
}
```

### 通用类型的节点数据结构

```go
// node_structures.go
package main

import "fmt"

type Node struct {
 le   *Node
 data interface{}
 ri   *Node
}

func NewNode(left, right *Node) *Node {
 return &Node{left, nil, right}
}

func (n *Node) SetData(data interface{}) {
 n.data = data
}

func main() {
 root := NewNode(nil, nil)
 root.SetData("root node")
 // make child (leaf) nodes:
 a := NewNode(nil, nil)
 a.SetData("left node")
 b := NewNode(nil, nil)
 b.SetData("right node")
 root.le = a
 root.ri = b
 fmt.Printf("%v\n", root) // Output: &{0x125275f0 root node 0x125275e0}
}
```

## 1.7 并发

### go func

go func() 是 Go 语言中的一个常用的语法结构，用于启动一个新的 goroutine。 go func 创建的 goroutine 是非阻塞。主程序会继续执行而不会等待 goroutine 的完成，如果主程序执行结束则全部 goroutine 也会被终止。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("Start")

    fmt.Println("greet start")
    go greet()
    fmt.Println("greet end")

    time.Sleep(2 * time.Second)
    fmt.Println("Main function ends")
}

func greet() {
    // 在新的 goroutine 中执行的函数
    time.Sleep(1 * time.Second)
    fmt.Println("Hello from goroutine")
}

```

### chan struct

chan struct{}是一个通道（channel），它用于在Go语言中进行并发通信。与其他类型的通道相比，chan struct{}是一种特殊的通道，因为它不存储任何实际的数据，而是仅仅用于在goroutines之间进行同步。

通常情况下，我们可以使用空结构struct{}来创建一个零大小的结构，这样就不会占用任何额外的内存空间。因此，chan struct{}通道不会存储任何实际的数据，它的主要作用是作为一个信号量来进行同步

常见的用途包括：

- 同步多个goroutine的启动和结束：可以使用chan struct{}来等待一组goroutines完成它们的工作，以确保在主goroutine继续执行之前所有的goroutines都已经完成。
- 触发事件：可以使用chan struct{}来触发某些事件的发生。例如，当某个特定的条件满足时，可以向chan struct{}发送一个值，通知其他goroutines该事件已经发生。
- 控制并发访问：可以使用chan struct{}来控制对共享资源的并发访问。例如，可以使用一个chan struct{}作为信号量，限制同时访问某个资源的goroutine数量。

```go
package main

import (
 "fmt"
 "time"
)

func main() {
 stopCh := make(chan struct{})
 go func() {
  fmt.Println("func1")
  time.Sleep(time.Duration(2) * time.Second) //协程1休眠2s stopCh 阻塞其他携程
  //从一个被close的channel中接收数据不会被阻塞，而是立即返回，接收完已发送的数据后会返回元素类型的零值(zero value)
  stopCh <- struct{}{}
  stopCh <- struct{}{}
  stopCh <- struct{}{}
  stopCh <- struct{}{}
  stopCh <- struct{}{}
  stopCh <- struct{}{}
  //close(stopCh) //close之后，其他协程结束阻塞，相当于通知其他协程开启任务 如果没有close或者nil channel中写入 stopCh <- struct{}{}则死锁
 }()
 go func() {
  //从一个nil channel中接收数据会一直被block,除非nil channel被close或者往nil channel中写入 stopCh <- struct{}{}
  x, ok := <-stopCh
  fmt.Println("func2", x, ok)
 }()
 go func() {
  x, ok := <-stopCh
  fmt.Println("func3", x, ok)
 }()
 go func() {
  x, ok := <-stopCh //使用一个额外的返回参数ok来检查channel是否关闭。false表示channel关闭
  fmt.Println("func4", x, ok)
 }()

 time.Sleep(time.Duration(4) * time.Second) //主线程休眠4s 等待其他协程完成任务
 x, ok := <-stopCh
 fmt.Println("main", x, ok)
}

```

在异步通信时，上面func2，func3，func4会阻塞，直到func1发送数据。或者使用close(stopCh) 关闭channel，这样结束阻塞，继续执行任务。

```go
stopCh := make(chan struct{})
close(stopCh)
x, ok := <-stopCh
fmt.Print(x,ok)
// {} false
```

如果是`make(chan int)`,在关闭channel，会直接返回(0),如果是`make(chan string)` ,会直接返回("")

```go

package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    ch := make(chan struct{})

    // 启动一组goroutines
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Goroutine %d started\n", id)
            // 模拟goroutine执行一些任务
            // 在这里可以添加实际的业务逻辑
        }(i)
    }

    // 等待所有goroutines完成
    go func() {
        wg.Wait()
        // 所有goroutines完成后，向通道发送一个值
        ch <- struct{}{}
    }()

    // 等待通道接收到值
    <-ch
    fmt.Println("All goroutines completed")
}

```

#### select

select 语句用于处理一个或多个 channel 操作。它类似于 switch 语句，但是每个 case 表达式必须是一个 channel 操作

```go
select {
case <-ch1:
    // 如果 ch1 可读，则执行此处的代码
case ch2 <- value:
    // 如果 ch2 可写，则执行此处的代码
default:
    // 如果没有任何 case 可以执行，则执行 default 分支
}

```
