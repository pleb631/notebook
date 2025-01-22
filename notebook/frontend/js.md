<!-- TOC -->
- [基础](#基础)
  - [变量](#变量)
    - [命名规范](#命名规范)
    - [let和var的区别](#let和var的区别)
    - [const](#const)
  - [基础数据类型](#基础数据类型)
    - [Number](#number)
    - [string](#string)
      - [字符串拼接](#字符串拼接)
      - [模板字符串](#模板字符串)
    - [boolean](#boolean)
    - [undefined](#undefined)
    - [null](#null)
    - [检测数据类型](#检测数据类型)
    - [类型转换](#类型转换)
      - [隐式转换](#隐式转换)
      - [显式转换](#显式转换)
  - [语句](#语句)
  - [数组](#数组)
    - [操作数组](#操作数组)
  - [函数](#函数)
    - [函数声明](#函数声明)
    - [匿名函数](#匿名函数)
  - [对象](#对象)
    - [声明](#声明)
    - [对象使用](#对象使用)
    - [遍历对象](#遍历对象)
- [Web APIs](#web-apis)
  - [DOM](#dom)
    - [操作DOM](#操作dom)
      - [CSS选择器](#css选择器)
      - [其他方法](#其他方法)
  - [元素属性](#元素属性)
    - [常用属性](#常用属性)
    - [元素样式属性](#元素样式属性)
      - [通过style属性操作CSS](#通过style属性操作css)
      - [用类名(className) 操作CSS](#用类名classname-操作css)
    - [表单元素属性](#表单元素属性)
    - [自定义属性](#自定义属性)
  - [定时器](#定时器)
  - [事件监听](#事件监听)

# 基础

## 变量

### 命名规范

遵守小驼峰命名法，第一个单词首字母小写，后面每个单词首字母大写。例：userName、myFirstName

### let和var的区别

在较旧的JavaScript，使用关键字 var 来声明变量 ，而不是 let。var 现在开发中一般不再使用它，只是我们可能再老版程序中看到它。let 为了解决 var 的一些问题。

var:

- 可以先使用 在声明 (不合理)
- var 声明过的变量可以重复声明(不合理)
- 比如变量提升、全局变量、没有块级作用域等等

**结论：**以后声明变量统一使用 let

### const

const 声明的变量称为“常量”,类似于 let ，但是声明的时候必须赋值（初始化）,变量的值无法被修改。

## 基础数据类型

### Number

js 中的正数、负数、小数等 统一称为 数字类型

```js
let age = 8
let price = 8.8
```

**注意**：JS是弱数据类型，变量属于哪种类型，只有赋值之后我们才能确认
数字可以有很多操作，比如，乘法 \* 、除法 / 、加法 + 、减法 - 等等，所以经常和算术运算符一起。

NaN 代表一个计算错误。它是一个不正确的或者一个未定义的数学操作所得到的结果。

```js
console.log("as"-2) //NAN
console.log("s"-2) //NAN
console.log("s"+2) //"s2"
```

NaN 是粘性的。任何对 NaN 的操作都会返回 NaN

### string

通过单引号('') 、双引号("")或反引号(``) 包裹的数据都叫字符串，单引号和双引号没有本质上的区别，推荐使用单引号。

输出单引号或双引号，可以使用转义符 \\

#### 字符串拼接

Number+string，Number会被隐式转换成string

```js
let age = 25
document.write('我今年' + age + '岁了')
```

#### 模板字符串

使用反引号(``)进行包裹

```js
let uname = prompt('请输入您的姓名:')

let age = prompt('请输入您的年龄:')

document.write(`大家好，我叫${uname}， 我今年贵庚${age}岁了`)
```

### boolean

它有两个固定的值true和false，表示肯定的数据用true，表示否定的数据用false。

### undefined

未定义是比较特殊的类型，只有一个值undefined。

只声明变量，不赋值的情况下，变量的默认值为undefined，一般很少直接为某个变量赋值为undefined。

```js
let num

console.log(num)
```

**使用场景:**开发中经常声明一个变量，等待传送过来的数据。如果我们不知道这个数据是否传递过来，此时我们可以通过检测这个变量是不是undefined，就判断用户是否有数据传递过来。

### null

null 仅仅是一个代表“无”、“空”或“值未知”的特殊值

```js
let obj = null

console.log(obj)
```

null 和 undefined 区别

- undefined 表示没有赋值
- null 表示赋值了，但是内容为空

### 检测数据类型

typeof 运算符可以返回被检测的数据类型。它支持两种语法形式：
返回字符串

1. 作为运算符:  `typeof x`
2. 函数形式： `typeof(x)`

```js
let num = 1
console.log(typeof num) 
let str = "asd"
console.log(typeof(str))

```

### 类型转换

JavaScript是弱数据类型： JavaScript也不知道变量到底属于那种数据类型，只有赋值了才清楚。

坑：使用表单、prompt 获取过来的数据默认是字符串类型的，此时不能直接进行加法运算。

此时需要转换变量的数据类型。

#### 隐式转换

某些运算符被执行时，系统内部自动将数据类型进行转换，这种转换称为隐式转换。

**规则**:

1. - 号两边只要有一个是字符串，都会把另外一个转成字符串

    ```js
    console.log('pink' + 1)
    console.log(2 + 2)  
    console.log(2 + '2')
    ```

2. 除了+以外的算术运算符 比如 \- \* / 等都会把数据转成数字类型

   ```js
   console.log(2 - 2)    
    console.log(2 - '2')  
   ```

3. +号作为正号解析可以转换成数字型

    ```js
    console.log(+'123')  // 转换为数字型 123
    ```

#### 显式转换

转换为数字型

1. `Number(数据)`，如果字符串内容里有非数字，转换失败时结果为NaN，NaN也是number类型的数据
2. `parseInt(数据)` 只保留整数
3. `parseFloat(数据)` 可以保留小数

转换为字符串型

1. `String(数据)`
2. `变量.toString()`

## 语句

for循环

```js
for(变量起始值;循环条件;每次循环后的操作){

}
```

while循环

```js
while(循环条件){
}
```

## 数组

数组：(Array)是一种可以按顺序保存数据的 数据类型

1. 声明：

    ```js
    let arr = new Array(1,2,3,4,5)
    let arr = [1,2,3,4,5]
    ```

2. 访问：
    数组名\[下标\]

    遍历数组

    ```js
    let arr = [1,2,3,4,5]
    for(let i = 0; i < arr.length; i++){
        console.log(arr[i])
    }
    ```

### 操作数组

```js
let arr = [1,2,3,4,5]

//将一个或多个元素添加到数组的末尾，并返回该数组的新长度
arr.push(1,2,3)

//将一个或多个元素添加到数组的开头 ，并返回该数组的新长度
arr.unshift(8,9,0)

//从数组中删除最后一个元素，并返回该元素的值
console.log(arr.pop())

//从数组中删除第一个元素，并返回该元素的值
console.log(arr.shift())

//删除数组中指定的元素，并返回该元素的值
// arr.splice(start, deleteCount)
// 从start开始删除deleteCount个数组元素
console.log(arr.splice(1,2))


//从start开始删除deleteCount个数组元素，并从start处开始添加item
//arr.splice(start, deleteCount, item1, item2, ..., itemN)
console.log(arr.splice(1,2,8,9,0))
```

## 函数

### 函数声明

```js
function 函数名(参数1,参数2,参数3){
}
```

**函数名命名规范**：和变量命名基本一致；尽量小驼峰式命名法；前缀应该为动词。

命名建议:常用动词约定:add,delete,update,get,set,find,search,load,is,has,can

**函数参数**：

1. 实参的个数和形参的个数可以不一致
2. 如果形参过多 会自动填上undefined (了解即可)
3. 如果实参过多 那么多余的实参会被忽略 (函数内部有一个arguments，里面装着所有的实参)

### 匿名函数

就是没有名字的函数

**使用方式（有两种）：**1.函数表达式   2.立即执行函数。

```js
let fn = function(a,b){}

(function(a,b){})()
```

## 对象

是一种 无序的数据集合

### 声明

```js
let obj = {
    uname : 'pink',
    age : 25
    isMarried : false
    sayHello : function(){console.log('hello')}
}

let obj1 = new Object()
```

### 对象使用

查询:

   1. 对象名.属性
   2. 对象[\'属性']

修改： 对象名.属性 = 新值
增加： 对象名.新属性 = 新值
删除： delete 对象名.属性

### 遍历对象

```js
let obj = {
    uname : 'pink',
    age : 25
    isMarried : false
}
for (let k in obj){
    console.log(k,obj[k])
}
```

# Web APIs

## DOM

**DOM 对象**：浏览器根据 html 标签生成的 JS对象

所有的标签属性都可以在这个对象上面找到，修改这个对象的属性会自动映射到标签身上。

**DOM 的核心思想**：把网页内容当做 对象 来处理

**document 对象**:是 DOM 提供的一个 对象 网页所有内容都在document里面。

document 提供的属性和方法都是用来访问和操作网页内容的。例：`document.write()`

### 操作DOM

#### CSS选择器

1. 选择匹配的第一个元素

    语法：

    ```js

    document.querySelector(CSS选择器)
    ```

    **参数:** 包含一个或多个有效的CSS选择器,如类名 .box，id名 #nav
    **返回值：** 返回CSS选择器匹配的 第一个元素 (HTMLElement对象)

    ```html
    <body>

    <div class="box">123</div>

    <div class="box">abc</div>

    <ul class="nav">

    <li>测试1</li>

    <li>测试2</li>

    <li>测试3</li>

    </ul>

    <script>

    const box = document.querySelector('.box')

    console.log(box)

    const li = document.querySelector('ul li:first-child')

    console.log(li)

    </script>

    </body>

    ```

2. 选择匹配的多个元素

    ```js
    document.querySelectorAll(CSS选择器)
    ```

    **返回值：** CSS选择器匹配的NodeList对象集合

    获取的对象集合不可修改，里面的元素可以修改。

    querySelectAll() 得到的是一个 **伪数组** ： 有长度有索引号，但是没有 pop() push() 等数组方法。

    ```js
    const lis = document.querySelectorAll('.nav li')
    for (let i = 0; i < lis.length; i++) {
    console.log(lis[i])
    }
    ```

#### 其他方法

```js
document.getElementById(id)
document.getElementsByClassName(className)
document.getElementsByTagName('div')

//特殊元素
document.images //<img> 标签
document.forms //表单元素
document.links // <a> 标签
```

## 元素属性

### 常用属性

最常见的属性比如： href、title、src 等
**语法：**: `对象.属性 = 值`

### 元素样式属性

#### 通过style属性操作CSS

**语法：** `对象.style.样式属性 = 值`

**注意：**

1. 修改样式通过 style 属性引出
2. 如果属性有 `-` 连接符，需要转换为 小驼峰 命名法
3. 赋值的时候，需要的时候不要忘记加 css单位
4. JS修改style样式操作，产生的是行内样式，CSS权重比较高

#### 用类名(className) 操作CSS

**语法** :`元素.className = css类名`

**注意：**

1. 由于 class 是关键字, 所以使用  className  去代替, className 是使用新值 换 旧值, 如果需要添加一个类，需要保留之前的类名， 直接使用 className 赋值会覆盖以前的类名。
2. 通过 classList 操作类控制CSS,可以解决className 容易覆盖以前的类名的问题，可以通过classList方式追加和删除类名。

```html
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta http-equiv="X-UA-Compatible" content="IE=edge">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Document</title>

<style>

.box {
width: 200px;
height: 200px;
color: #333;
}

.active {
color: red;
background-color: pink;
}
</style>
</head>

<body>
<div class="box active">文字</div>
<script>
const box = document.querySelector('.box')

// 第一种写法
box.className = 'box active'

// 第二种写法
li.classList.add('active')
li.classList.remove('active')

// 第三种写法
// toggle意思是如果有这个类名，就删除，如果没有这个类名，就添加
box.classList.toggle('active')


</script>
</body>
</html>
```

### 表单元素属性

表单很多情况也需要修改属性，比如点击眼睛，可以看到密码，本质是把表单类型转换为文本框。

表单属性中添加就有效果，移除就没有效果，一律使用布尔值表示。如果为true代表添加了该属性， 如果是false 代表移除了该属性。比如： disabled、checked、selected

```html
<body>
  <button>点击</button>
  <script>
    const button = document.querySelector("button");
    button.disabled = true;
  </script>
</body>

```

### 自定义属性

在html5中推出来了专门的data-自定义属性，在标签上一律 以data-开头 ，在DOM对象上一律以 dataset.属性 获取，比如：

```html
<body>
<div data-id="123" data-name="pink">123</div>
<script>
    const div = document.querySelector('div')
    console.log(div.dataset.id)
</script>
```

## 定时器

定时器是 JS 的一个功能，用来在指定的时间后执行代码。
**语法：**

```js
setTimeout(func,间隔时间) //延迟执行
setInterval(func,间隔时间) //循环执行
```

## 事件监听

就是让程序检测是否有事件产生，一旦有事件触发，就立即调用一个函数做出响应，也称为 绑定事件或者注册事件

```js
元素对象.addEventListener('事件类型', func)
```

**事件监听三要素：**

1. 事件源: 事件被触发的对象 。dom元素被事件触发了，要获取dom元素
2. 事件类型: 用什么方式触发，比如鼠标单击 click、鼠标经过 mouseover 等
3. 事件调用的函数: 要做什么事

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      * {
        margin: 0;

        padding: 0;
      }

      h2 {
        text-align: center;
      }

      .box {
        width: 600px;

        margin: 50px auto;

        display: flex;

        font-size: 25px;

        line-height: 40px;
      }

      .qs {
        width: 450px;

        height: 40px;

        color: red;
      }

      .btns {
        text-align: center;
      }

      .btns button {
        width: 120px;

        height: 35px;

        margin: 0 50px;
      }
    </style>
  </head>

  <body>
    <h2>随机点名</h2>

    <div class="box">
      <span>名字是：</span>
      <div class="qs">这里显示姓名</div>
    </div>

    <div class="btns">
      <button class="start">开始</button>
      <button class="end">结束</button>
    </div>

    <script>
      const arr = ["马超", "黄忠", "赵云", "关羽", "张飞"];

      let timerId = 0;
      let random = 0;
      const qs = document.querySelector(".qs");
      const start = document.querySelector(".start");
      let run=false;
      start.addEventListener("click", function () {
        if(run){
          return;
        }
        run = true;
        timerId = setInterval(function () {
          random = parseInt(Math.random() * arr.length);

          qs.innerHTML = arr[random];
        }, 35);

        if (arr.length === 1) {
          start.disabled = end.disabled = true;
        }
      });

      const end = document.querySelector(".end");

      end.addEventListener("click", function () {
        if(!run){
          return;
        }
        clearInterval(timerId);
        arr.splice(random, 1);
        run=false;
        console.log(arr);
      });
    </script>
  </body>
</html>

```
