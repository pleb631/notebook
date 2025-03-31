<!-- TOC -->
- [基础](#基础)
  - [变量](#变量)
    - [命名规范](#命名规范)
    - [let和var的区别](#let和var的区别)
    - [const](#const)
  - [基础数据类型](#基础数据类型)
    - [Number](#number)
    - [String](#string)
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
    - [`new Object`创建对象](#new-object创建对象)
    - [构造函数创建对象(重点)](#构造函数创建对象重点)
      - [实例成员和静态成员](#实例成员和静态成员)
  - [内置构造函数](#内置构造函数)
    - [Object](#object)
    - [Array](#array)
    - [String](#string-1)
    - [Number](#number-1)
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
  - [本地存储](#本地存储)
    - [localStorage](#localstorage)
    - [sessionStorage](#sessionstorage)
    - [存储复杂数据类型](#存储复杂数据类型)
- [进阶语法](#进阶语法)
  - [原型](#原型)
    - [constructor 属性](#constructor-属性)
    - [对象原型](#对象原型)
    - [原型继承](#原型继承)
    - [原型链](#原型链)
  - [异常处理](#异常处理)
    - [throw](#throw)
    - [try/catch](#trycatch)
    - [debugger](#debugger)
  - [深拷贝](#深拷贝)
  - [闭包](#闭包)
  - [箭头函数](#箭头函数)
    - [细节](#细节)
  - [this](#this)
    - [普通函数](#普通函数)
    - [箭头函数](#箭头函数-1)
    - [改变this](#改变this)
      - [call](#call)
      - [apply](#apply)
      - [bind](#bind)
        - [基本写法](#基本写法)
        - [箭头函数的替代方案](#箭头函数的替代方案)
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

### String

通过单引号('') 、双引号("")或反引号(``) 包裹的数据都叫字符串，单引号和双引号没有本质上的区别，推荐使用单引号。

输出单引号或双引号，可以使用转义符 \\

字符串拼接

Number+string，Number会被隐式转换成string

```js
let age = 25
document.write('我今年' + age + '岁了')
```

模板字符串

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

### 获取数据类型typeof

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

// 对象字面量创建对象
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

### `new Object`创建对象

```js
<script>
const obj = new Object({ uname: 'pink' })
console.log(obj)
```

### 构造函数创建对象(重点)

```js
function Pig(uname, age) {
    this.uname = uname
    this.age = age
}
const p = new Pig('佩奇', 6)
console.log(p)
```

说明：

1. 使用 new 关键字调用函数的行为被称为 实例化
2. 实例化构造函数时没有参数时可以省略 ()
3. 构造函数内部无需写return，返回值即为新创建的对象，即自动返回创建的新对象
4. 构造函数内部的 return 返回的值无效，所以不要写return
5. new Object（） new Date（） 也是实例化构造函数

实例化执行过程:

1. 创建新对象
2. 构造函数this指向新对象
3. 执行构造函数代码，修改this，添加新的属性
4. 返回新对象

#### 实例成员和静态成员

实例成员:通过构造函数创建的对象称为实例对象，实例对象中的属性和方法称为实例成员

说明:

1. 实例对象的属性和方法即为实例成员
2. 为构造函数传入参数，动态创建结构相同但值不同的对象
3. 构造函数创建的实例对象彼此独立互不影响 。

静态成员:构造函数的属性和方法被称为静态成员

```js
function Dog(uname, age) {}
Dog.uname = '旺财'
Dog.age = 3
Dog.eat = function () {console.log('吃东西')}
```

说明:

1. 构造函数的属性和方法被称为静态成员
2. 一般公共特征的属性或方法静态成员设置为静态成员
3. 静态成员方法中的 this 指向构造函数本身

## 内置构造函数

### Object

```js
const o = { uname: 'pink', age: 18 }

// 获得对象中所有属性
console.log(Object.keys(o))

//获取对象中所有属性值
console.log(Object.values(o))

// 添加属性
Object.assign(o, { gender: '女' })

```

### Array

```js

const lis = document.querySelectorAll('ul li')
// 假数组转为真数组
const liss = Array.from(lis)


const arr = new Array(1, 2, 3, 4, 5)


// concat
// 拼接
const arr13 = arr.concat([1, 2, 3])

// join
// 将数组元素拼接成字符串
const arr14 = arr.join('-')


// sort
// 排序
const arr9 = arr.sort((a, b) => a - b)

// reverse
// 反转
arr.reverse()

// slice
// 切片
const arr11 = arr.slice(1, 3)


// some
// 检测是否有元素满足条件
const arr7 = arr.some((item) => item > 2)

// every
// 检测是否所有元素满足条件
const arr8 = arr.every((item) => item > 2)



// reduce
// 返回函数累计处理的结果，经常用于求和等
// arr.reduce(function(累计值, 当前元素){}, 起始值)
const re = arr.reduce((prev, item) => prev + item)

// map
// 返回新数组，新数组的元素是处理后的值
const arr2 = arr.map((item) => item * 2)

// filter
// 筛选数组元素
const arr3 = arr.filter((item) => item > 2)


// find
// 返回第一个匹配的元素
const arr5 = arr.find((item) => item > 2)

// findIndex
// 返回第一个匹配的元素索引
const arr6 = arr.findIndex((item) => item > 2)
```

### String

```js
// 获取字符串的长度
let num = string.length; 


// 提取从 start 到 end 之间的字符串（不包含 end）
let newString = string.substring(start, end); 


// 提取从 start 到 end 之间的字符串（可以负数索引）
let newString = string.slice(start, end); 

// 替换字符串中第一次匹配的内容
let newString = string.replace(searchValue, newValue); 


// 替换字符串中所有匹配的内容 (ES2021)
let newString = string.replaceAll(searchValue, newValue);

// 根据分隔符拆分字符串，返回一个数组
let newString = string.split(separator); 

// 检查字符串是否包含指定的子字符串
let result = string.includes(searchValue); 

// 检查字符串是否以指定的子字符串开头
let result = string.startsWith(searchValue); 

// 检查字符串是否以指定的子字符串结尾
let result = string.endsWith(searchValue); 

// 将多个字符串连接成一个新的字符串
let newString = string.concat(otherString); 

// 将字符串转换为大写
let newString = string.toUpperCase(); 

// 将字符串转换为小写
let newString = string.toLowerCase(); 

// 获取指定索引位置的字符
let result = string.charAt(index); 

// 去除字符串两端的空格
let newString = string.trim(); 

// 查找指定子字符串首次出现的位置 (没有找到返回 -1)
let result = string.indexOf(searchValue); 

// 查找指定子字符串最后一次出现的位置 (没有找到返回 -1)
let result = string.lastIndexOf(searchValue); 

// 使用正则表达式匹配字符串 (返回数组)
let result = string.match(regex); 

// 查找符合正则表达式的内容，返回位置（没有找到返回 -1）
let result = string.search(regex); 

// 将字符串重复指定次数
let newString = string.repeat(count); 

```

### Number

```js
const num = 10.923

//保留几位小数
console.log(num.toFixed(1))

```

# 进阶语法

## 原型

构造函数通过原型分配的函数是所有对象所 **共享的**

JavaScript 规定， 每一个构造函数都有一个 prototype 属性 ，指向另一个对象，所以我们也称为原型对象。这个对象可以挂载函数，对象实例化不会多次创建原型上函数， 节约内存 。

可以把那些不变的方法直接定义在 prototype 对象上，这样所有对象的实例都可以共享这些方法。

构造函数和原型对象中的 **this** 都指向 **实例化的对象。**

```js
let that;
function Star(uname) {
  this.uname = uname;
}

Star.prototype.sing = function () {
  that = this;
  console.log("唱歌");
};

const ldh = new Star("刘德华");
ldh.sing();
console.log(that === ldh); // true

```

### constructor 属性

每个原型对象里面都有个constructor 属性（ constructor 构造函数 ）

**作用：** 该属性 指向 该原型对象的 构造函数， 简单理解，就是指向我的爸爸（构造函数）

```js
function Star() {}
Star.prototype = {
  constructor: Star,
  sing: function () {
    console.log("唱歌");
  },
  dance: function () {
    console.log("跳舞");
  },
};
console.log(Star.prototype);
```

### 对象原型

对象都会有一个属性 `__proto__` 指向构造函数的 prototype 原型对象，之所以我们对象可以使用构造函数 prototype 原型对象的属性和方法，就是因为对象有 `__proto__` 原型的存在。`__proto__`是JS非标准属性,用来表明当前实例对象指向哪个原型对象prototype

### 原型继承

继承是面向对象编程的另一个特征，通过继承进一步提升代码封装的程度，JavaScript 中大多是借助原型对象实现继承的特性。

```js
function Person() {
  this.eyes = 2;
  this.head = 1;
}

function Woman() {}
Woman.prototype = Person;
Woman.prototype.constructor = Woman;
```

男人和女人都同时使用了同一个对象，根据引用类型的特点，他们指向同一个对象，修改一个就会都影响,所以需要修改，使用构造函数new 每次都会创建一个新的对象

### 原型链

1. 当访问一个对象的属性（包括方法）时，首先查找这个 对象自身 有没有该属性。
2. 如果没有就查找它的原型（也就是 `__proto__`指向的 prototype 原型对象 ）
3. 如果还没有就查找原型对象的原型（ Object的原型对象 ）
4. 依此类推一直找到 Object 为止（ null ）
5. `__proto__`对象原型的意义就在于为对象成员查找机制提供一个方向，或者说一条路线
6. 可以使用 instanceof 运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上

```js
function Person() {
  this.eyes = 2;
  this.head = 1;
}

function Woman() {}
Woman.prototype = new Person();
Woman.prototype.constructor = Woman;
Woman.prototype.baby = function () {
  console.log("宝贝");
};

function Man() {}
Man.prototype = new Person();
Man.prototype.constructor = Man;

const red = new Woman();
console.log(red.__proto__);

const pink = new Man();
console.log(pink.__proto__);

```

## 异常处理

### throw

```js
function foo() {
  throw new Error("出错了");
}
```

**总结：**  

1. `throw` 抛出异常信息，程序也会终止执行  
2. `throw` 后面跟的是错误提示信息  
3. `Error` 对象配合 `throw` 使用，能够设置更详细的错误信息

### try/catch

```js
try {
  foo();  
}
catch (e) {
  throw new Error('你看看，选择器错误了吧')
}
finally {
alert('弹出对话框')
}
```

### debugger

`debugger` 语句用于在浏览器中设置断点，当执行到这个语句时，浏览器会暂停执行，并进入调试模式。

## 深拷贝

1. 递归函数
2. JSON.parse(JSON.stringify(obj))
3. js库lodash里面cloneDeep

```js
const obj = {
  uname: "pink",
  age: 18,
  hobby: ["乒乓球", "足球"],
  family: {
    baby: "小pink",
  },
};

const o = _.cloneDeep(obj);
```

## 闭包

**概念：**一个函数对周围状态的引用捆绑在一起，内层函数中访问到其外层函数的作用域

**简单理解：** **闭包 =  内层函数 + 外层函数的变量**

**闭包作用：** 封闭数据，提供操作，外部也可以访问函数内部的变量

```js
function count() {
    let i = 0
    function fn() {
        i++
        console.log(`函数被调用了${i}次`)
    }
    return fn
}
const fun = count()
```

## 箭头函数

基本写法

```js
const fn=() => {
}
fn()
```

带一个参数

```js
const fn = x => {}
```

函数体只有一行代码，可以写到一行上，并且无需写 return 直接返回值

```js
const fn = (x,y) => x + y
```

### 细节

1. 箭头函数 没有 arguments 动态参数，但是 有剩余参数 ..args

   ```js
   const getSum = (...arr) => {
       let sum = 0
       for (let i = 0; i < arr.length; i++) {
           sum += arr[i]
       }
       return sum
   }
   const result = getSum(2, 3, 4)
   console.log(result)
   ```

2. 箭头函数不会创建自己的 this ，它只会从自己的作用域链的上一层沿用 this。

  ```js
const obj = {
    uname: '老师',
    sayHi: function () {
        console.log(this)
        let i = 10
        const count = () => {
            console.log(this)
        }
        count()
    }
}
obj.sayHi()
  ```

## this

### 普通函数

普通函数的调用方式决定了 this 的值，即【谁调用 this 的值指向谁】

普通函数没有明确调用者时 this 值为 window，严格模式下没有调用者时 this 的值为 undefined

```js
let obj = {say:function fn() {
  console.log(this)
}}
obj.say() //指向obj

function fn() {
  console.log(this)
}
fn() //指向window
```

### 箭头函数

箭头函数本身中并不存在this

1. 箭头函数会默认帮我们绑定外层 this 的值，所以在箭头函数中 this 的值和外层的 this 是一样的  
2. 箭头函数中的this引用的就是最近作用域中的this  
3. 向外层作用域中，一层一层查找this，直到有this的定义

```js
const person = {
    name: 'Alice',
    age: 30,
    sayHello: function() {
        console.log(this); // 指向 person 对象
        const innerFunction = () => {
            console.log(this); // 由于箭头函数没有自己的 this，继承自外部函数，仍指向 person 对象
        };
        innerFunction();
    }
};

person.sayHello(); //指向person


const person = {
    name: 'Alice',
    age: 30,
    sayHello: () => {
        console.log(this);
    }
}
person.sayHello(); // 指向window
```

### 改变this

#### call

语法:`fun.call(thisArg, arg1, arg2, ...)`
thisArg：在 fun 函数运行时指定的 this 值  
arg1，arg2：传递的其他参数  
返回值就是函数的返回值，因为它就是调用函数

```js
let obj = {say:function fn() {
    console.log(this)
    }}
obj.say() //指向obj
obj.say.call(this) //指向window
```

#### apply

语法:`fun.apply(thisArg, [argsArray])`
thisArg：在fun函数运行时指定的this值
argsArray：传递的值，必须包含在数组里面
返回值就是函数的返回值，因为它就是调用函数  
apply 主要跟数组有关系，比如使用 Math.max() 求数组的最大值

call和apply的区别：

- 都是调用函数，都能改变this指向  
- 参数不一样，apply传递的必须是数组

#### bind

bind() 方法不会调用函数。但是能改变函数内部this 指向  
语法:`fun.bind(thisArg, arg1, arg2, ...)`

##### 基本写法

```js
const obj = {
    age: 18
}
function fn() {
    console.log(this)

}
const fun = fn.bind(obj)
fun()

function fn(x,y) {
    console.log(this)
    console.log(x+y)
}
const fun1 = fn.bind(obj,1)
fun1(2)
```

##### 箭头函数的替代方案

原始写法:

```html
<body>
    <button>发送短信</button>
    <script>
        document.querySelector('button').addEventListener('click', function () {
            this.disabled = true
            window.setTimeout(()=> {
                console.log(this)
                this.disabled = false
            }, 2000)
        })
    </script>
</body>
```

bind 写法

```html
<body>
    <button>发送短信</button>
    <script>
        document.querySelector('button').addEventListener('click', function () {
            this.disabled = true
            window.setTimeout(function () {
                this.disabled = false
            }.bind(this), 2000)
        })
    </script>
</body>

```

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

1. 每个模块内部的:this、exports、modules.exports在初始时，都指向同一个空对象，该空对象就是当前模块导出的数据
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
  return ['北京','上海','深圳','成都','武汉','西安']}

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
