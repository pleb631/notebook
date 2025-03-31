# Web API

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

![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/461b3b2a0c852ecd2081029b2365fdf6.png)

说明:假设页面里有个div，当触发事件时，会经历两个阶段，分别是捕获阶段、冒泡阶段

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

## 本地存储

### localStorage

**作用:** 可以将数据永久存储在本地(用户的电脑), 除非手动删除，否则关闭页面也会存在

**特性：** 可以多窗口（页面）共享（同一浏览器可以共享）、以键值对的形式存储使用

**语法:**

存储数据：`localStorage.setItem(key, value)`
获取数据： `localStorage.getItem(key)`
删除数据：`localStorage.removeItem(key)`

### sessionStorage

**特性：**

生命周期为关闭浏览器窗口,在同一个窗口(页面)下数据可以共享,以键值对的形式存储使用,用法跟 localStorage 基本相同

### 存储复杂数据类型

本地只能存储字符串,无法存储复杂数据类型。

**解决：** 需要将复杂数据类型转换成JSON字符串,在存储到本地

```js
localStorage.setItem('user', JSON.stringify({name: 'name1', age: 18}))
const obj = JSON.parse(localStorage.getItem('user'))
```

