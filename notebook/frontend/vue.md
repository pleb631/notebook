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
