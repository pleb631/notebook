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
    - [事件监听对比](#事件监听对比)
    - [解绑事件](#解绑事件)
    - [鼠标经过事件的区别](#鼠标经过事件的区别)
  - [事件对象](#事件对象)
    - [常见属性](#常见属性)
  - [环境对象](#环境对象)
  - [回调函数](#回调函数)
  - [事件流](#事件流)
    - [阻止冒泡](#阻止冒泡)
  - [事件委托](#事件委托)
  - [其他事件](#其他事件)
    - [页面加载事件](#页面加载事件)
  - [日期对象](#日期对象)
  - [DOM节点](#dom节点)
    - [查找节点](#查找节点)
    - [创建节点](#创建节点)
    - [删除节点](#删除节点)
  - [BOM](#bom)
- [模块化](#模块化)
  - [commonjs](#commonjs)
    - [导出](#导出)
    - [导入](#导入)
    - [扩展](#扩展)
    - [浏览器端运行](#浏览器端运行)
  - [ES6 模块化](#es6-模块化)
    - [初步使用](#初步使用)
    - [Node中运行ES6模块](#node中运行es6模块)
    - [ES6导出](#es6导出)
    - [ES6导入](#es6导入)
      - [mjs 和es6 语法区别](#mjs-和es6-语法区别)

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
let time1 = setTimeout(func,间隔时间) //延迟执行
let time2 = setInterval(func,间隔时间) //循环执行

// 清除定时函数
clearInterval(time2)
clearTimeout(timer1)
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

### 事件监听对比

事件源.on事件 = function(){}
事件源.addEventListener(事件,事件处理函数)

on方式会被覆盖， addEventListener 方式可绑定多次，拥有事件更多特性。

### 解绑事件

on事件方式，直接使用null覆盖偶就可以实现事件的解绑
事件源.removeEventListener(事件,事件处理函数)

**注意**：匿名函数无法被解绑

### 鼠标经过事件的区别

1. `mouseover` 和 `mouseout` 会有冒泡效果
2. `mouseenter 和 mouseleave` 没有冒泡效果

## 事件对象

语法：

```js
事件源.addEventListener(事件,function(event){})
```

### 常见属性

type：获取当前的事件类型
clientX/clientY：获取光标相对于浏览器可见窗口左上角的位置
offsetX/offsetY：获取光标相对于当前DOM元素左上角的位置
key：用户按下的键盘键的值，现在不提倡使用keyCode

## 环境对象

指的是函数内部特殊的变量`this`， 它代表着当前函数运行时所处的环境

## 回调函数

当一个函数当做参数来传递给另外一个函数的时候，这个函数就是 回调函数

## 事件流

指的是事件完整执行过程中的流动路径

![](https://i-blog.csdnimg.cn/blog_migrate/461b3b2a0c852ecd2081029b2365fdf6.png)

说明：假设页面里有个div，当触发事件时，会经历两个阶段，分别是捕获阶段、冒泡阶段

简单来说：捕获阶段是从父到子，冒泡阶段是从子到父

实际工作都是使用事件冒泡为主。

addEventListener第三个参数传入 true 代表是 捕获阶段 触发,若传入 false 代表 冒泡阶段 触发，默认就是false

### 阻止冒泡

因为默认有冒泡模式的存在，所以容易导致事件影响到父级元素,若想把事件就限制在当前元素内，就需要阻止事件冒泡
**语法**:e.stopPropagation()

**注意**:此方法可以阻断事件流动传播，不光在冒泡阶段有效，捕获阶段也有效

我们某些情况下需要阻止**默认行为**的发生，比如 阻止 链接的跳转，表单域跳转

**语法**: e.preventDefault()

## 事件委托

事件委托是利用事件流的特征解决一些开发需求的知识技巧。
**场景：** 当页面中有很多个按钮，当点击按钮时，需要执行一些操作，但是每个按钮都要注册事件，这样会增加代码量，并且代码冗余，如果使用事件委托，只需要注册一次事件，当触发事件时，会冒泡到父级元素，从而触发父级元素的事件。

**实现**: `e.target.tagName` 可以获得真正触发事件的元素

如：`ul.addEventListener('click' , function(){})` 执行父级点击事件

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tab栏切换</title>
    <style>
      .tab {
        width: 590px;
        height: 100px;
        margin: 20px;
        border: 1px solid #e4e4e4;
      }
      .tab-nav {
        width: 100%;
        height: 60px;
        line-height: 60px;
        display: flex;
        justify-content: space-between;
      }
      .tab-nav h3 {
        font-size: 24px;
        font-weight: normal;
        margin-left: 20px;
      }
      .tab-nav ul {
        list-style: none;
        display: flex;
        justify-content: flex-end;
      }
      .tab-nav ul li {
        margin: 0 20px;
        font-size: 14px;
      }
      .tab-nav ul li a {
        text-decoration: none;
        border-bottom: 2px solid transparent;
        color: #333;
      }
      .tab-nav ul li a.active {
        border-color: #e1251b;
        color: #e1251b;
      }
    </style>
  </head>
  <body>
    <div class="tab">
      <div class="tab-nav">
        <h3>每日特价</h3>
        <ul>
          <li><a class="active" href="javascript:;" data-id="0">精选</a></li>
          <li><a href="javascript:;" data-id="1">美食</a></li>
          <li><a href="javascript:;" data-id="2">百货</a></li>
          <li><a href="javascript:;" data-id="3">个护</a></li>
          <li><a href="javascript:;" data-id="4">预告</a></li>
        </ul>
      </div>
    </div>

    <script>
      const ul = document.querySelector(".tab-nav ul");

      const items = document.querySelectorAll(".tab-content .item");

      ul.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
          document.querySelector(".tab-nav .active").classList.remove("active");
          e.target.classList.add("active");
          const i = +e.target.dataset.id;
        }
      });
    </script>
  </body>
</html>
```

## 其他事件

### 页面加载事件

## 日期对象

```javascript
// 获得当前时间
const date = new Date()

// 获取指定时间
const date = new Date('2023-5-25')

// 获取时间戳
//第一种方法
console.log(date.getTime())

////第二种方法
console.log(+new Date())

////第三种方法
console.log(Date.now())
```

## DOM节点

DOM树里每一个内容都称之为节点，

1. 元素节点：所有的标签 比如 body、 div，html 是根节点
2. 属性节点：所有的属性 比如 href
3. 文本节点：所有的文本

### 查找节点

`子元素.parentNode`, 返回最近一级的父节点 找不到返回为 null
`子元素.childNodes`, 获得所有子节点、包括文本节点（空格、换行）、注释节点等
`子元素.children`,仅获得所有元素节点，返回的还是一个 伪数组
`nextElementSibling` ,下一个兄弟节点
`previousElementSibling`, 上一个兄弟节点

### 创建节点

**创建**元素节点方法：

```js
document.createElement('标签名')
```

**追加**节点:要想在界面看到，还得插入到某个父元素中
`父元素.appendChild(要插入的元素)`,插入到父元素的最后一个子元素的后面：
`父元素.insertBefore(要插入的元素,在哪个元素前面)` ,插入到父元素中某个子元素的前面

**克隆**节点:元素.cloneNode(布尔值)
布尔值为true，则克隆时会包含后代节点一起克隆。若为false(默认)，则克隆时不包含后代节点。

### 删除节点

要删除元素必须通过父元素删除。

**语法：** `父元素.removeChlid(子元素)`， 如不存在父子关系则删除不成功

## BOM
BOM(Browser Object Model ) 是浏览器对象模型。
所有通过var定义在全局作用域中的变量、函数都会变成window对象的属性和方法,window对象下的属性和方法调用的时候可以省略window,像document、alert()、console.log()这些都是window的属性,基本BOM属性和方法都是window的
# 模块化

## commonjs

### 导出

- exports.name = value

  ```js
  // school.js
  const name = 'name1'
  const slogan = '让天下没有难学的技术！'
  
  function getTel (){
    return '010-56253825'
  }
  
  function getCities(){
    return ['北京','上海','深圳','成都','武汉','西安']
  }
  
  // 通过给exports对象添加属性的方式，来导出数据（注意：此处没有导出getCities）
  exports.name = name
  exports.getTel = getTel
  ```

  ```js
  // 导入
  const student = require('./student')
  console.log(student.getTel())
  ```

- module.exports = value

  ```js
  module.exports = {
    name: name,
    getTel: getTel
  }

  ```

注意:

1. 每个模块内部的：this、exports、modules.exports在初始时，都指向同一个空对象，该空对象就是当前模块导出的数据
2. 无论如何修改导出对象，最终导出的都是module.exports的值。
3.exports是对module.exports的初始引用，仅为了方便给导出象添加属性，所以不能使用 exports = value的形式导出数据，但是可以使用module.exports = xxxx导出数据

### 导入

```js
// 直接引入模块
const school = require('./school')
 
// 引入同时解构出要用的数据
const { name, slogan, getTel } = require('./school')
 
// 引入同时解构+重命名
const {name:stuName,motto,getTel:stuTel} = require('./student')
```

### 扩展

一个 JS 模块在执行时，是被包裹在一个内置函数中执行的，所以每个模块都有自己的作用域，我们可以通过如下方式验证这一说法：

```js
console.log(arguments)
console.log(arguments.callee.toString())
```

内置函数的大致形式如下：

```js
function (exports, require, module, __filename, __dirname){
  /*********************/
}
```

### 浏览器端运行

Node.js 默认是支持 CommonJS 规范的，但浏览器端不支持，所以需要经过编译，步骤如下：

1. 全局安装 browserify ：npm i browserify -g
2. 编译

    ```bash
    browserify index.js -o build.js
    ```

3. 页面中引入使用

   ```js
   <script type="text/javascript" src="./build.js"></script>
   ```

## ES6 模块化

### 初步使用

```js
//  school.js
// 导出name
export let name = {str:'name'}
// 导出slogan
export const slogan = '让天下没有难学的技术！'
 
// 导出name
export function getTel (){
  return '010-56253825'
}
 
function getCities(){
  return ['北京','上海','深圳','成都','武汉','西安']

```

```html
// 引入
<script type="module" src="./index.js"></script>
```

### Node中运行ES6模块

Node.js中运行ES6模块代码有两种方式：

1. 将JavaScript文件后缀从.js 改为.mjs，Node 则会自动识别 ES6 模块。
2. 在package.json中设置type属性值为module

### ES6导出

ES6 模块化提供 3 种导出方式：①分别导出、②统一导出、③默认导出

分别导出

```js

// 导出name
export let name = {str:'name'}
// 导出slogan
export const slogan = '让天下没有难学的技术！'
 
// 导出getTel
export function getTel (){
  return '010-56253825'
}
```

统一导出

```js
const name = {str:'name'}
const slogan = '让天下没有难学的技术！'
 
function getTel (){
  return '010-56253825'
}
 
function getCities(){
  return ['北京','上海','深圳','成都','武汉','西安']
}
 
// 统一导出了：name,slogan,getTel
export {name,slogan,getTel}
```

默认导出

```js
const name = '张三'
const motto = '走自己的路，让别人五路可走！'
 
function getTel (){
  return '13877889900'
}
 
function getHobby(){
  return ['抽烟','喝酒','烫头']
}
 
//默认导出：name,motto,getTel
export default {name,motto,getTel}
```

### ES6导入

导入全部
可以将模块中的所有导出内容整合到一个对象中

```js
import * as school from './school.js'

```

命名导入(对应导出方式：分别导出、统一导出)

```js
import {name,slogan,getTel} from './school'
import {name as stuName,motto,getTel as stuTel} from './student'
```

默认导入(对应导出方式：默认导出)

```js
import student from './student.js' //默认导出的名字可以修改，不是必须为student
```

命名导入 与 默认导入混合

默认导入的内容必须放在前方

```js
import getTel,{name,slogan} from './school.js'
```

动态导入

允许在运行时按需加载模块，返回值是一个 Promise

```js
const school = await import('./school.js');
```

#### mjs 和es6 语法区别

1. mjs导出的变量的值传递，es6导出的变量的是引用传递
