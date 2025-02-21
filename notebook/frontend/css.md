<!-- TOC -->

- [css](#css)
  - [语法](#语法)
  - [选择器](#选择器)
  - [伪类选择器](#伪类选择器)
    - [动态伪类](#动态伪类)
    - [结构伪类](#结构伪类)
    - [否定伪类](#否定伪类)
    - [UI伪类](#ui伪类)
    - [表单伪类](#表单伪类)
    - [目标伪类](#目标伪类)
    - [语言伪类](#语言伪类)
    - [伪元素](#伪元素)
  - [常用属性](#常用属性)
    - [字体](#字体)
    - [文本](#文本)
      - [文本颜色](#文本颜色)
      - [文本间距](#文本间距)
      - [文本修饰](#文本修饰)
      - [文本对齐](#文本对齐)
      - [行间距](#行间距)
    - [列表相关](#列表相关)
    - [表格](#表格)
    - [背景](#背景)
    - [鼠标](#鼠标)
  - [长度距离](#长度距离)
  - [标签显示模式（display）](#标签显示模式display)
    - [块级元素(block)](#块级元素block)
    - [行内元素(inline)](#行内元素inline)
    - [行内块元素(inline-block)](#行内块元素inline-block)
  - [盒子模型](#盒子模型)
    - [盒子边框](#盒子边框)
    - [内边距](#内边距)
    - [外边距](#外边距)
    - [水平居中](#水平居中)
  - [浮动](#浮动)
  - [定位](#定位)
    - [定位模式 (position)](#定位模式-position)
    - [相对单位](#相对单位)
    - [绝对定位](#绝对定位)
    - [固定定位](#固定定位)
    - [z-index](#z-index)
- [css3](#css3)
  - [私有前缀](#私有前缀)
  - [css3新增语法](#css3新增语法)
    - [长度单位](#长度单位)
    - [盒模型](#盒模型)
    - [背景属性](#背景属性)
    - [边框属性](#边框属性)
    - [文本属性](#文本属性)
    - [渐变](#渐变)
    - [2D变换](#2d变换)
    - [3D变换](#3d变换)
    - [过渡](#过渡)
    - [动画](#动画)
      - [动画的基本使用](#动画的基本使用)
      - [动画的其他属性](#动画的其他属性)
      - [动画复合属性](#动画复合属性)
    - [多列布局](#多列布局)
    - [伸缩盒子](#伸缩盒子)
      - [属性](#属性)
      - [flex-direction](#flex-direction)
      - [flex-wrap](#flex-wrap)
      - [flex-flow](#flex-flow)
      - [justify-content](#justify-content)
      - [align-items](#align-items)
      - [align-content](#align-content)
      - [order](#order)
      - [flex-grow](#flex-grow)
      - [flex-shrink](#flex-shrink)
      - [flex-basis](#flex-basis)
      - [flex](#flex)
      - [align-self](#align-self)
    - [响应式布局](#响应式布局)
    - [媒体查询](#媒体查询)

# css

## 语法

```css
p {
  color: red;
  text-align: center;
}
```

- p 是 CSS 中的选择器（它指向要设置样式的 HTML 元素：\<p>）。
- color 是属性，red 是属性值
- text-align 是属性，center 是属性值

## 选择器

- id 选择器

```css
#para1 {
  text-align: center;
  color: red;
}
```

这条CSS 规则将应用于 id="para1" 的 HTML 元素

- 类选择器

```css
.center {
  text-align: center;
  color: red;
}
```

类选择器选择有特定 class 属性的 HTML 元素。
如需选择拥有特定 class 的元素，请写一个句点（.）字符，后面跟类名

```css
p.center {
  text-align: center;
  color: red;
}
```

该例子中，只有具有 class="center" 的 `<p>`元素会居中对齐

`<p class="center large">这个段落引用两个类。</p>`

- 通用选择器
  会应用于所有元素上

```css
* {
  text-align: center;
  color: blue;
}
```

- 并集选择器
h1,h2,p都会应用这个样式

```css
h1, h2, p {
  text-align: center;
  color: red;
}
```

- 交集选择器
选择具有 class="intro" 的所有 `<p>` 元素

```css
p.intro {
  text-align: center;
  color: red;
}
```

- 后代选择器
选择所有 `<h1>` 元素内的 `<p>` 元素

```css
h1 p {
  color: gray;
  font-size: 20px;
}
```

- 子元素选择器
选择所有 `<h1>` 元素的所有直接子 `<p>` 元素

```css
h1 > p {
  color: gray;
  font-size: 20px;
}
```

- 兄弟选择器

```css
/* 选择所有紧接在 `<h1>` 元素后的 `<p>` 元素 */
h1 + p {
  color: gray;
}
/* 选择所有 `<h1>` 元素后的 `<p>` 元素 */
h1~p {
  color: red;
}
```

- 属性选择器

```css
/*选择所有具有 title 属性的元素*/
[title] {
  color: red;
}

/*选择所有具有 title="W3School" 属性的元素*/
[title=W3School] {
  border: 5px solid blue;
}

/*选择所有具有 title 属性且值以 "W3S" 开头的元素*/
[title^="W3S"] {
  color: red;
}

/*选择所有具有 title 属性且值以 "W3S" 结尾的元素*/
[title$="W3S"] {
  color: red;
}

/*选择所有具有 title 属性且值包含 "W3S" 的元素*/
[title*="W3S"] {
  color: red;
}
```

## 伪类选择器

### 动态伪类

```css
/* 选择所有未访问的链接 */
a:link {
  color: #FF0000;
}

/* 选择所有访问过的链接 */
a:visited {
  color: #00FF00;
}

/* 选择鼠标指针浮动在其上的链接 */
a:hover {
  color: #FF00FF;
}

/* 选择被激活的链接 */
a:active {
  color: #0000FF;
}

/*获取焦点*/
input:focus {
  background-color: yellow;
}
```

### 结构伪类

```css
/* 选择所有 <p> 元素中的第一个且是 <i> 的元素 */
p i:first-child {
  color: red;
}

/* 选择所有 <p> 元素中的最后一个 且是<i> 元素 */
p i:last-child {
  color: red;
}

/* 选择所有 <p> 元素是它父类的最后一个且是<i> 元素 */
p :last-child {
  color: red;
}


/* 选择所有 <p> 元素中的第1个且是<i> 的子元素 */
p > i:first-child {
  color: red;
}


/* 选择所有 <p> 元素中的第2个且是<i> 子元素*/
p > i:nth-child(2) {
  color: red;
}

/* 选择所有 <p> 元素中的偶数的且是<i> 子元素*/
p > i:nth-child(2n) {
  color: red;
}

/* 选择所有 <p> 元素中的前5个且是<i> 子元素,格式an+b*/
p > i:nth-child(-n+5) {
  color: red;
}


/* 选择所有<p>元素中子元素中同类型元素的第一个*/
p > i:nth-of-type(1) {
  color: red;
}

/* 选择所有<p>元素中子元素中同类型元素的第一个*/
p > i:first-of-type {
  color: red;
}
/*选择没有兄弟元素的<p>*/
p:only-child{ 
  color: red;
  }

/*选择没有同类型兄弟元素的<p>*/
p:only-of-type {
  color: red;
}

/*选择所有空元素*/
div:empty {
  width: 100px;
  height: 100px;
  background-color: yellow;
}
```

### 否定伪类

```css
/* 选择所有不包含 class="intro" 的 <p> 元素 */
p:not(.intro) {
  color: red;
}
```

### UI伪类

```css
/* 选择所有勾选的复选框 */
input:checked {
  width: 100px;
  height: 100px;
}

input:enabled {
  width: 100px;
  height: 100px;
}

input:disabled {
  width: 100px;
  height: 100px;
}
```

### 表单伪类

```css
/* 选择没有值的输入字段 */
input:invalid {
  background-color: yellow;
}

/* 选择已选中的输入字段 */
input:valid {
}
```

### 目标伪类

```css
/* 选择当前活动的链接 */
a:target {
  background-color: yellow;
}
```

### 语言伪类

```css
/* 选择所有 lang 属性值以 "en" 开头的元素 */
q:lang(en) {
  background-color: yellow;
}
```

### 伪元素

```css
/* 选择每个 <p> 元素的首字母 */
p::first-letter {
}

/* 选择每个 <p> 元素的首行 */
p::first-line{

}

/* 在p元素之前插入内容 */
p::before {
  content: "Hello, ";
} 
```

## 常用属性

### 字体

```css
/* 设置字体大小 */
.at{font-size: 40px;}

/* 字体族 */
.at{font-family:"宋体"}
/* 备选值:"微软雅黑"、"楷体"、"华文彩云"等 */


/* 字体样式 */
.at{font-style: italic;} /* 斜体 */
.at{font-style: normal;} /* 默认 */


/* 字体粗细 */
.at{font-weight: bold;}
/* 备选值: "lighter"、"normal"、"bold"、"bolder"、"600px" */

/* 复合属性 */
.at{
  font: italic bold 40px/1.5 "微软雅黑";
}
```

### 文本

#### 文本颜色

```css

.at{color: red;}

.at1 {color: rgb(255, 0, 0);}

.at2 {color: hsl(0, 100%, 50%);}

.at3 {color: #00f;}
```

#### 文本间距

```css
/* 字母间距 */
.at1{letter-spacing: 20px;}

 /* 单词间距 */
.at2 {word-spacing: 20px;}
```

#### 文本修饰

```css
/* 上划的绿色虚线 */
.at1 {
  text-decoration:overline dotted green;
}

/* 下划的红色波浪线 */
.at2 {
    text-decoration: underline wavy red;
}

/* 删除线 */
.at3 {
    text-decoration: line-through;
}

/* 没有线 */
.at4 {
    text-decoration: none;
}
```

#### 文本对齐

```css
/* 缩进 */
div { text-indent: 120px;}


/* 水平对齐 */
.at1 {text-align: left;}
/* right left center */

/* 垂直对齐 */
.at2 {text-align: top;}
/* middle top bottom */
```

#### 行间距

```css
/* 第一种写法，值为像素 */
/* line-height: 40px; */

/* 第二种写法，值为normal */
/* line-height: normal; */

/* 第三种写法，值为数值 —— 用的比较多 */
/* line-height: 1.5; */

/* 第四种写法，值为百分比 */
/* line-height: 150%; */
```

### 列表相关

```css
/* 列表符号 */
/* list-style-type: decimal; */
/* 备用选项：circie,disc,square,decimal */

/* 列表符号的位置 */
/* list-style-position: outside; */
/* 备用选项：inside,outside; */

/* 自定义列表符号 */
/* list-style-image: url("../images/video.gif"); */

/* 复合属性 */
/* list-style: decimal url("../images/video.gif") inside; */
```

### 表格

```css
table {
    border:2px green solid;
    width:500px;
    /* 控制表格的列宽 */
    table-layout: fixed; 
    /*auto会换行，fixed不会换行 */


    /* 控制单元格间距（生效的前提是：不能合并边框） */
    border-spacing: 10px;

    /* 合并相邻的单元格的边框 */
    border-collapse: collapse;
    /* collapse边框合并 separate不合并 */

    /* 隐藏没有内容的单元格（生效的前提是：不能合并边框） */
    empty-cells: hide;

    /* 设置表格标题的位置 */
    caption-side: top;
}
td,th {
    border:2px orange solid;
}
```

### 背景

```css
body {
    background-color: gray;
}
div {
    width: 400px;
    height: 400px;
    border:5px black solid;
    font-size: 20px;
    /* 设置背景颜色，默认值是transparent */
    background-color: skyblue;
    /* 设置背景图片 */
    background-image: url(../images/悟空.jpg);
    /* 设置背景图片的重复方式 */
    background-repeat: no-repeat;
    /* 控制背景图片的位置——第一种写法：用关键词 */
    background-position: center;
    /* 控制背景图片的位置——第二种写法：用具体的像素值 */
    background-position: 100px 200px;
    /* 复合属性 */
    background: url(../images/悟空.jpg) no-repeat 100px 200px;
    
}
```

### 鼠标

设置或检索在对象上移动的鼠标指针采用何种系统预定义的光标形状。

| 属性值          | 描述       |
| --------------- | ---------- |
| **default**     | 小白  默认 |
| **pointer**     | 小手       |
| **move**        | 移动       |
| **text**        | 文本       |
| **not-allowed** | 禁止       |

鼠标放我身上查看效果哦：

```html
<ul>
  <li style="cursor:default">我是小白</li>
  <li style="cursor:pointer">我是小手</li>
  <li style="cursor:move">我是移动</li>
  <li style="cursor:text">我是文本</li>
  <li style="cursor:not-allowed">我是文本</li>
</ul>
```

## 长度距离

「px」：绝对单位，页面按精确像素展示
「em」：相对单位，基准点为当前节点或父节点字体的大小，如果自身定义了`font-size`按自身来计算，整个页面内`1em`不是一个固定的值
「rem」：相对单位，可理解为`root em`, 相对根节点`html`的字体大小来计算
「%」：参考父元素设置的百分比

## 标签显示模式（display）

### 块级元素(block)

例：

```html
常见的块元素有
<h1>~<h6>、<p>、<div>、<ul>、<ol>、<li>等，
其中<div>标签是最典型的块元素。
```

块级元素的特点

1. 自己独占一行
2. 高度，宽度、外边距以及内边距都可以控制。
3. 宽度默认是容器（父级宽度）的100%
4. 是一个容器及盒子，里面可以放行内或者块级元素。

注意：

> 只有 文字才 能组成段落  因此 p  里面不能放块级元素，特别是 p 不能放div
>
> 同理还有这些标签h1,h2,h3,h4,h5,h6,dt，他们都是文字类块级标签，里面不能放其他块级元素。

### 行内元素(inline)

例：

```html
常见的行内元素有
<a>、<strong>、<b>、<em>、<i>、<s>、<ins>、<u>、<span>等，
其中<span>标签最典型的行内元素。有的地方也成内联元素
```

行内元素的特点：

1. 相邻行内元素在一行上，一行可以显示多个。
2. 高、宽直接设置是无效的。
3. 默认宽度就是它本身内容的宽度。
4. 行内元素只能容纳文本或则其他行内元素。

注意：

> 链接里面不能再放链接。
>
> 特殊情况a里面可以放块级元素，但是给a转换一下块级模式最安全。

### 行内块元素(inline-block)

例：

```css
在行内元素中有几个特殊的标签
<img />、<input />、<td>，
可以对它们设置宽高和对齐属性，有些资料可能会称它们为行内块元素。
```

行内块元素的特点：

1. 和相邻行内元素（行内块）在一行上,但是之间会有空白缝隙。一行可以显示多个
2. 默认宽度就是它本身内容的宽度。
3. 高度，行高、外边距以及内边距都可以控制。

## 盒子模型

盒子模型：本质是一个盒子，用来装内容

组成：边框，外边距，内边距和内容

content：内容
padding：内边距（内容与盒子之间的距离）
border：边框
margin：外边距（盒子之间距离）

![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/v2-7e1c9f496a41859bb34614e2db24fc1d_r.jpg)

### 盒子边框

盒子边框会使实际盒子变大，定义一个200X200像素的盒子后加了一个10px像素的边框，最后会显示一个220X220像素的盒子
`border`：边框粗细、边框样式、边框颜色

属性：

- `border-width`：边框粗细，单位px
- `border-style`：边框样式（常用的：solid实线边框，dashed虚线边框，dotted点线边框）
  ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/v2-d77bbe230169b3a6de839219a83b28e8_1440w.jpg)
- `border-color`：边框颜色

可以简写:
`border：1px solid red;`

也可以给边框的某个边单独设置样式：

如`border-top`:给上边框单独指定样式。

### 内边距

控制内容在盒子内部的位置，通过内边距实现`padding`

用法与border类似

### 外边距

控制元素之间的距离，通过外边距实现`margin`

注意

1. 当蓝色的块向下margin20，紫色的块向上margin10，最后这两个块之间的距离还是20
2. 嵌套块第一个子元素margin失效，有三个方法解决
   - 可以为父元素定义上边框
   - 可以为父元素定义上内边距
   - 可以为父元素加上 （常用，因为这种不会影响盒子大小）`overflow:hidden`

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .father {
            width: 600px;
            height: 600px;
            background-color: aqua;
            margin-top: 50px;
            border-top: 1px solid transparent;
            padding-top: 1px;
        }

        /*或者：overflow:hidden; */
        .son {
            width: 300px;
            height: 300px;
            background-color: blue;
            margin-top: 150px;
        }
    </style>
</head>

<body>
    <div class="father">
        <div class="son"></div>
    </div>
</body>

</html>
```

### 水平居中

1. 块级元素

    如果**块级**元素始终在页面的**水平居中**位置，需要满足两个条件：

    1. 块级元素的**宽度**必须设置  
    2. 块级元素的**左右margin**设置为：`auto`  

    ```css
    display: block; 
    width: fit-content; 
    margin: 0  auto;
    ````

2. 行内元素

    ```css

    /*作用在父元素上*/

    text-align: center;

    ```

## 浮动

## 定位

### 定位模式 (position)

在 CSS 中，通过 `top`、`bottom`、`left` 和 `right` 属性定义元素的边偏移

在 CSS 中，通过 `position` 属性定义元素的**定位模式**，语法如下：

定位模式是有不同分类的，在不同情况下，我们用到不同的定位模式。

| **值** | **语义** |
|---|---|
| `static` | 静态定位 |
| `relative` | 相对定位 |
| `absolute` | 绝对定位 |
| `fixed` | 固定定位 |

### 相对单位

相对定位是元素相对于它原来在标准流中的位置来说的。

相对定位的特点：

> 相对于 自己原来在标准流中位置来移动的
> 原来**在标准流的区域继续占有**，后面的盒子仍然以标准流的方式对待它。

### 绝对定位

绝对定位是元素以带有定位的父级元素来移动位置

1. 完全脱标 —— 完全不占位置；
2. 父元素没有定位，则以浏览器为准定位
3. 父元素要有定位，将元素依据最近的已经定位（绝对、固定或相对定位）的父元素（祖先）进行定位。

### 固定定位

固定定位是绝对定位的一种特殊形式：

1. 完全脱标 —— 完全不占位置；
2. 只认浏览器的可视窗口 —— `浏览器可视窗口 + 边偏移属性` 来设置元素的位置
   > 跟父元素没有任何关系；单独使用的
   > 不随滚动条滚动。

注意:绝对定位/固定定位的盒子不能通过设置 `margin: auto` 设置水平居中
可以使用下面的配置进行设置

1. `left: 50%;`：让盒子的左侧移动到父级元素的水平中心位置；
2. `margin-left: -100px;`：让盒子向左移动自身宽度的一半

### z-index

在使用**定位**布局时，可能会**出现盒子重叠的情况**。

加了定位的盒子，默认**后来者居上**， 后面的盒子会压住前面的盒子。

应用 `z-index` 层叠等级属性可以**调整盒子的堆叠顺序**。如下图所示：

`z-index` 的特性如下：

1. 属性值：正整数、负整数或 0，默认值是 0，数值越大，盒子越靠上；
2. 如果属性值相同，则按照书写顺序，后来居上；
3. 数字后面不能加单位。

注意:`z-index` 只能应用于相对定位、绝对定位和固定定位的元素，其他标准流、浮动和静态定位无效。

# css3

## 私有前缀

W3C 标准所提出的某个 CSS 特性，在被浏览器正式支持之前，浏览器厂商会根据浏览器的内核，使用私有前缀来测试该 CSS 特性，在浏览器正式支持该 CSS 特性后，就不需要私有前缀了。

比如

```css
-webkit-border-radius: 20px;
-moz-border-radius: 20px;
-ms-border-radius: 20px;
-o-border-radius: 20px;
border-radius: 20px;
```

查看兼容性的网站[https://caniuse.com/](https://caniuse.com/)

常见浏览器私有前缀:

- Chrome 浏览器： -webkit-
- Safari 浏览器： -webkit-
- Firefox 浏览器： -moz-
- Edge 浏览器： -webkit-
- 旧 Opera 浏览器： -o-
- 旧 IE 浏览器： -ms-

## css3新增语法

### 长度单位

1. rem 根元素字体大小的倍数，只与根元素字体大小有关。
2. vw 视口宽度的百分之多少 10vw 就是视口宽度的 10% 。
3. vh 视口高度的百分之多少 10vh 就是视口高度的 10% 。
4. vmax 视口宽高中大的那个的百分之多少。（了解即可）
5. vmin 视口宽高中小的那个的百分之多少。（了解即可）

### 盒模型

1. box-sizing 怪异盒模型
    使用 box-sizing 属性可以设置盒模型的两种类型

    | 可选值       | 含义                                                    |
    |--------------|---------------------------------------------------------|
    | content-box  | width 和 height 设置的是盒子内容区的大小。（默认值）    |
    | border-box   | width 和 height 设置的是盒子总大小。（怪异盒模型）      |

2. resize 调整盒子大小
    使用 resize 属性可以控制是否允许用户调节元素尺寸

    | 值           | 含义                                               |
    |--------------|----------------------------------------------------|
    | none         | 不允许用户调整元素大小。 (默认)                    |
    | both         | 用户可以调节元素的宽度和高度。                      |
    | horizontal   | 用户可以调节元素的宽度。                            |
    | vertical     | 用户可以调节元素的高度。                            |

3. box-shadow 盒子阴影

    | 值          | 含义                                          |
    |-------------|-----------------------------------------------|
    | h-shadow    | 水平阴影的位置，必须填写，可以为负值           |
    | v-shadow    | 垂直阴影的位置，必须填写，可以为负值           |
    | blur        | 可选，模糊距离                                |
    | spread      | 可选，阴影的外延值                            |
    | color       | 可选，阴影的颜色                              |
    | inset       | 可选，将外部阴影改为内部阴影                  |

    默认值

    - `box-shadow: none` 表示没有阴影。

    示例

    ```css
    box-shadow: h-shadow v-shadow blur spread color inset;
    /* 写两个值，含义：水平位置、垂直位置 */
    box-shadow: 10px 10px;

    /* 写三个值，含义：水平位置、垂直位置、颜色 */
    box-shadow: 10px 10px red;
    /* 写三个值，含义：水平位置、垂直位置、模糊值 */
    box-shadow: 10px 10px 10px;
    /* 写四个值，含义：水平位置、垂直位置、模糊值、颜色 */
    box-shadow: 10px 10px 10px red;
    /* 写五个值，含义：水平位置、垂直位置、模糊值、外延值、颜色 */
    box-shadow: 10px 10px 10px 10px blue;
    /* 写六个值，含义：水平位置、垂直位置、模糊值、外延值、颜色、内阴影 */
    box-shadow: 10px 10px 20px 3px blue inset;
    ```

4. opacity 不透明度

    opacity 属性能为整个元素添加透明效果， 值是 0 到 1 之间的小数， 0 是完全透明， 1 表示完
    全不透明。
    >opacity 与 rgba 的区别？
    >opacity 是一个属性，设置的是整个元素（包括元素里的内容）的不透明度。
    >rgba 是颜色的设置方式，用于设置颜色，它的透明度，仅仅是调整颜色的透明度。

### 背景属性

1. background-origin
    作用：设置背景图的原点。
    语法
    1. padding-box:从 padding 区域开始显示背景图像。—— 默认值
    2. border-box: 从 border 区域开始显示背景图像。
    3. content-box: 从 content 区域开始显示背景图像

2. background-clip
    作用：设置背景图的向外裁剪的区域。
    语法
    1. border-box: 从 border 区域开始向外裁剪背景。 —— 默认值
    2. padding-box: 从 padding 区域开始向外裁剪背景。
    3. content-box: 从 content 区域开始向外裁剪背景。
    4. text:背景图只呈现在文字上

3. background-size
    作用：设置背景图的尺寸。
    语法：
    1. 用长度值指定背景图片大小，不允许负值。`background-size: 300px 200px`
    2. 用百分比指定背景图片大小，不允许负值。`background-size: 100% 100%`
    3. auto: 背景图片的真实大小。 —— 默认值
    4. contain: 将背景图片等比缩放，使背景图片的宽或高，与容器的宽或高相等，再将完整
    背景图片包含在容器内，但要注意：可能会造成容器里部分区域没有背景图片。`background-size: contain;`
    5. cover:将背景图片等比缩放，直到完全覆盖容器，图片会尽可能全的显示在元素上，但要
    注意：背景图片有可能显示不完整。—— 相对比较好的选择。`background-size: cover;`

4. backgorund 复合属性
    语法：`background: color url repeat position / size origin clip`
    注意：
    1. origin 和 clip 的值如果一样，如果只写一个值，则 origin 和 clip 都设置；如
    果设置了两个值，前面的是 origin ，后面的 clip 。
    2. size 的值必须写在 position 值的后面，并且用 / 分开。

5. 多背景图
    CSS3 允许元素设置多个背景图片

    ```css
    /* 添加多个背景图 */
    background: url(../images/bg-lt.png) no-repeat,
    url(../images/bg-rt.png) no-repeat right top,
    url(../images/bg-lb.png) no-repeat left bottom,
    url(../images/bg-rb.png) no-repeat right bottom;

    ```

### 边框属性

在 CSS3 中，使用 border-radius 属性可以将盒子变为圆角。
同时设置四个角的圆角：`border-radius:10px`

1. 一个值是正圆半径，
2. 两个值分别是椭圆的 x 半径、 y 半径

分开四个角：
border-top-left-radius
border-top-right-radius
border-bottom-right-radius
border-bottom-left-radius

综合写法

`border-raidus: 左上角x 右上角x 右下角x 左下角x / 左上y 右上y 右下y 左下y`

边框外轮廓
outline-width:外轮廓的宽度。
outline-color:外轮廓的颜色。
outline-style:外轮廓的风格。

none: 无轮廓
dotted: 点状轮廓
dashed: 虚线轮廓
solid: 实线轮廓
double: 双线轮廓

outline-offset 设置外轮廓与边框的距离，正负值都可以设置。
>注意： outline-offset 不是 outline 的子属性，是一个独立的属性。
outline 复合属性
`outline:50px solid blue;`

### 文本属性

1. 文本阴影text-shadow
    语法：`text-shadow: h-shadow v-shadow blur color;`

    | 值          | 描述                                      |
    |-------------|-------------------------------------------|
    | h-shadow    | 必需写，水平阴影的位置。允许负值。         |
    | v-shadow    | 必需写，垂直阴影的位置。允许负值。         |
    | blur        | 可选，模糊的距离。                        |
    | color       | 可选，阴影的颜色                          |

    默认值： text-shadow:none 表示没有阴影

2. 文本换行white-space

    | 值       | 含义                                                                          |
    | -------- | ----------------------------------------------------------------------------- |
    | normal   | 文本超出边界自动换行，文本中的换行被浏览器识别为一个空格。（默认值）          |
    | pre      | 原样输出，与 pre 标签的效果相同。                                             |
    | pre-wrap | 在 pre 效果的基础上，超出元素边界自动换行。                                   |
    | pre-line | 在 pre 效果的基础上，超出元素边界自动换行，且只识别文本中的换行，空格会忽略。 |
    | nowrap   | 强制不换行                                                                    |

3. 文本溢出text-overflow

    | 值          | 含义                                                      |
    |-------------|-----------------------------------------------------------|
    | clip        | 当内联内容溢出时，将溢出部分裁切掉。（默认值）            |
    | ellipsis    | 当内联内容溢出块容器时，将溢出部分替换为 ...               |

    注意：要使得 text-overflow 属性生效，块容器必须显式定义 overflow 为非 visible
    值， white-space 为 nowrap 值。

4. 文本修饰
    CSS3 升级了 text-decoration 属性，让其变成了复合属性。
    `text-decoration: text-decoration-line || text-decoration-style || text-decoration-color`

    - text-decoration-line 设置文本装饰线的位置

      - none ： 指定文字无装饰 （默认值）
      - underline ： 指定文字的装饰是下划线
      - overline ： 指定文字的装饰是上划线
      - line-through ： 指定文字的装饰是贯穿线
    - text-decoration-style 文本装饰线条的形状
      - solid ： 实线 （默认）
      - double ： 双线
      - dotted ： 点状线条
      - dashed ： 虚线
      - wavy ： 波浪线
    - text-decoration-color 文本装饰线条的颜色

5. 文本描边
    注意：文字描边功能仅 webkit 内核浏览器支持。

    - -webkit-text-stroke-width ：设置文字描边的宽度，写长度值。
    - -webkit-text-stroke-color ：设置文字描边的颜色，写颜色值。
    - -webkit-text-stroke ：复合属性，设置文字描边宽度和颜色

### 渐变

1. 线性渐变
    语法
    `background-image: linear-gradient(red,yellow,green);`

    ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/linear-css.png)

    关键词指定方向

    ```css
    background-image: linear-gradient(to top,red,yellow,green);
    background-image: linear-gradient(to right top,red,yellow,green);
    ```

    角度设置方向

    ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1739871045752.png)

    ```css
    background-image: linear-gradient(30deg,red,yellow,green);
    ```

    调整开始渐变的位置
    ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1739871099249.png)

    ```css
    background-image: linear-gradient(red 50px,yellow 100px ,green 150px);
    ```

2. 径向渐变
    多个颜色之间的渐变， 默认从圆心四散

    ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1739871133642.png)

    ```css
    background-image: radial-gradient(red,yellow,green)
    ```

    关键词调整圆心位置

    ```css
    background-image: radial-gradient(at right top,red,yellow,green)
    ```

    使用像素值调整渐变圆的圆心位置

    ```css
    background-image: radial-gradient(at 100px 50px,red,yellow,green)
    ```

    调整渐变形状为正圆

    ```css
    background-image: radial-gradient(circle,red,yellow,green)
    ```

    调整圆的的半径
    ![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1739871172342.png)

    ```css
    background-image: radial-gradient(100px,red,yellow,green);
    background-image: radial-gradient(50px 100px,red,yellow,green);
    ```

    调整渐变的位置

    ```css
    background-image: radial-gradient(red 50px,yellow 100px,green 150px)
    ```

3. 重复渐变
    无论线性渐变，还是径向渐变，在没有发生渐变的位置，继续进行渐变，就为重复渐变。
    使用 repeating-linear-gradient 进行重复线性渐变，具体参数同 linear-gradient
    使用 repeating-radial-gradient 进行重复径向渐变，具体参数同 radial-gradient

### 2D变换

二维坐标系如下图所示
![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1739871278657.png)

1. 2D位移
    语法：`transform: translateX(30px) translateY(40px);`

    | 值        | 含义                                                                 |
    |-----------|----------------------------------------------------------------------|
    | translateX | 设置水平方向位移，需指定长度值；若指定的是百分比，是参考自身宽度的百分比。 |
    | translateY | 设置垂直方向位移，需指定长度值；若指定的是百分比，是参考自身高度的百分比。 |
    | translate  | 一个值代表水平方向，两个值代表：水平和垂直方向。                      |

    注意点：

      1. 位移与相对定位很相似，都不脱离文档流，不会影响到其它元素。
      2. 与相对定位的区别：相对定位的百分比值，参考的是其父元素；定位的百分比值，参考的是
      其自身。
      3. 浏览器针对位移有优化，与定位相比，浏览器处理位移的效率更高。
      4. 位移对行内元素无效。
      5. 位移配合定位，可实现元素水平垂直居中

2. 2D缩放
    让元素放大或缩小

    | 值        | 含义                                                                 |
    |-----------|----------------------------------------------------------------------|
    | scaleX    | 设置水平方向的缩放比例，值为一个数字，1表示不缩放，大于1放大，小于1缩小。 |
    | scaleY    | 设置垂直方向的缩放比例，值为一个数字，1表示不缩放，大于1放大，小于1缩小。 |
    | scale     | 同时设置水平方向、垂直方向的缩放比例，一个值代表同时设置水平和垂直缩放；两个值分别代表：水平缩放、垂直缩放。 |

    注意点：

    1. scale 的值，是支持写负数的，但几乎不用，因为容易让人产生误解。
    2. 借助缩放，可实现小于 12px 的文字

3. 2D旋转
    让元素在二维平面内，顺时针旋转或逆时针旋转
    语法：`rotate(20deg)`
    rotate 设置旋转角度，需指定一个角度值( deg )，正值顺时针，负值逆时针

4. 变换原点

    元素变换时，默认的原点是元素的中心，使用 transform-origin 可以设置变换的原点。
    修改变换原点对位移没有影响， 对旋转和缩放会产生影响。
    如果提供两个值，第一个用于横坐标，第二个用于纵坐标。
    如果只提供一个，若是像素值，表示横坐标，纵坐标取 50% ；若是关键词，则另一个坐标取 50%

    1. transform-origin: 50% 50% ， 变换原点在元素的中心位置，百分比是相对于自
    身。—— 默认值
    2. transform-origin: left top ，变换原点在元素的左上角 。
    3. transform-origin: 50px 50px ， 变换原点距离元素左上角 50px 50px 的位置。
    4. transform-origin: 0 ，只写一个值的时候，第二个值默认为 50% 。

### 3D变换

1. 开启3D空间
    重要原则：元素进行 3D 变换的首要操作：父元素必须开启 3D 空间！
    使用 transform-style 开启 3D 空间，可选值如下：
    flat ： 让子元素位于此元素的二维平面内（ 2D 空间）—— 默认值
    preserve-3d ： 让子元素位于此元素的三维空间内（ 3D 空间）

2. 设置景深
    何为景深？—— 指定观察者与 z=0 平面的距离，能让发生 3D 变换的元素，产生透视效果，看来更加立
    体。
    使用 perspective 设置景深，可选值如下：

    - none ： 不指定透视 ——（默认值）
    - 长度值 ： 指定观察者距离 z=0 平面的距离，不允许负值。

    注意： perspective 设置给发生 3D 变换元素的父元素

3. 透视点位置
    所谓透视点位置，就是观察者位置；默认的透视点在元素的中心。
    使用 perspective-origin 设置观察者位置（透视点的位置），例如：
    >/*相对坐标轴往右偏移400px， 往下偏移300px（相当于人蹲下300像素，然后向右移动400像素看元素）*/
    > perspective-origin: 400px 300px;
    注意：通常情况下，我们不需要调整透视点位置

4. 3D位移

    3D 位移是在 2D 位移的基础上，可以让元素沿 z 轴位移

    | 值          | 含义                                                                 |
    |-------------|----------------------------------------------------------------------|
    | translateZ  | 设置 z 轴位移，需指定长度值，正值向屏幕外，负值向屏幕里，且不能写百分比。 |
    | translate3d | 第1个参数对应 x 轴，第2个参数对应 y 轴，第3个参数对应 z 轴，且均不能省略。 |

5. 3D 旋转

    3D 旋转是在 2D 旋转的基础上，可以让元素沿 x 轴和 y 轴旋转

    | 值        | 含义                                                                 |
    |-----------|----------------------------------------------------------------------|
    | rotateX   | 设置 x 轴旋转角度，需指定一个角度值(deg)，面对 x 轴正方向：正值顺时针，负值逆时针。 |
    | rotateY   | 设置 y 轴旋转角度，需指定一个角度值(deg)，面对 y 轴正方向：正值顺时针，负值逆时针。 |
    | rotate3d  | 前 3 个参数分别表示坐标轴：x, y, z，第 4 个参数表示旋转的角度，参数不允许省略。例如：transform: rotate3d(1,1,1,30deg)，意思是：x、y、z 分别旋转 30 度。 |

6. 3D 缩放
    3D 缩放是在 2D 缩放的基础上，可以让元素沿 z 轴缩放

    | 值          | 含义                                                                 |
    |-------------|----------------------------------------------------------------------|
    | scaleZ      | 设置 z 轴方向的缩放比例，值为一个数字，1表示不缩放，大于1放大，小于1缩小。 |
    | scale3d     | 第1个参数对应 x 轴，第2个参数对应 y 轴，第3个参数对应 z 轴，参数不允许省略。 |

7. 背部可见性

    使用 backface-visibility 指定元素背面，在面向用户时是否可见，常用值如下：
    - visible ： 指定元素背面可见，允许显示正面的镜像。—— 默认值
    - hidden ： 指定元素背面不可见
    注意： backface-visibility 需要加在发生 3D 变换元素的自身上

### 过渡

过渡可以在不使用 Flash 动画，不使用 JavaScript 的情况下，让元素从一种样式，平滑过渡为另一
种样式。

1. transition-property
    作用：定义哪个属性需要过渡，只有在该属性中定义的属性（比如宽、高、颜色等）才会以有过渡
    效果。
    常用值：

    - none ：不过渡任何属性。
    - all ：过渡所有能过渡的属性。
    - 具体某个属性名 ，例如： width 、 heigth ，若有多个以逗号分隔。

    不是所有的属性都能过渡，值为数字，或者值能转为数字的属性，都支持过渡，否则不支持
    过渡。
    常见的支持过渡的属性有：颜色、长度值、百分比、 z-index 、 opacity 、 2D 变换属
    性、 3D 变换属性、阴影。

2. transition-duration
    作用：设置过渡的持续时间，即：一个状态过渡到另外一个状态耗时多久。
    常用值：

    - 0 ：没有任何过渡时间 —— 默认值。
    - s 或 ms ：秒或毫秒。
    - 列表 ：如果想让所有属性都持续一个时间，那就写一个值。如果想让每个属性持续不同的时间那就写一个时间的列表。

3. transition-delay
    作用：指定开始过渡的延迟时间，单位： s 或 ms

4. transition-timing-function
    作用：设置过渡的类型
    常用值：

    - ease ： 平滑过渡 —— 默认值
    - linear ： 线性过渡
    - ease-in ： 慢 → 快
    - ease-out ： 快 → 慢
    - ease-in-out ： 慢 → 快 → 慢
    - step-start ： 等同于 steps(1, start)
    - step-end ： 等同于 steps(1, end)
    - steps( integer,?) ： 接受两个参数的步进函数。第一个参数必须为正整数，指定函数的步数。第二个参数取值可以是 start 或 end ，指定每一步的值发生变化的时间点。第二个参数默认值为 end 。
    - cubic-bezie ( number, number, number, number)： 特定的贝塞尔曲线类型。
  在线制作贝赛尔曲线： [https://cubic-bezier.com](https://cubic-bezier.com)

5. 复合属性
transition 复合属性
如果设置了一个时间，表示 duration ；如果设置了两个时间，第一是 duration ，第二个是
delay ；其他值没有顺序要求。

```css
transition:1s 1s linear al
```

### 动画

#### 动画的基本使用

1. 定义关键帧
   - 简单方式

    ```css
    /*写法一*/
    @keyframes 动画名 {
    from {
    /*property1:value1*/
    /*property2:value2*/
    }
    to {
    /*property1:value1*/
    }
    }
    ```

   - 复杂方式

    ```css
    @keyframes 动画名 {
        0% {
        /*property1:value1*/
        }
        40% {
        /*property1:value1*/
        }
        80% {
        /*property1:value1*/
        }
        100% {
        /*property1:value1*/
        }
        }
        ```

2. 应用动画

- animation-name ：给元素指定具体的动画（具体的关键帧）
- animation-duration ：设置动画所需时间
- animation-delay ：设置动画延迟

```css
.box {
/* 指定动画 */
animation-name: testKey;
/* 设置动画所需时间 */
animation-duration: 5s;
/* 设置动画延迟 */
animation-delay: 0.5s;
}
```

#### 动画的其他属性

1. animation-timing-function ，设置动画的类型，常用值如下

   - ease ： 平滑过渡 —— 默认值
   - linear ： 线性过渡
   - ease-in ： 慢 → 快
   - ease-out ： 快 → 慢
   - ease-in-out ： 慢 → 快 → 慢
   - step-start ： 等同于 steps(1, start)
   - step-end ： 等同于 steps(1, end)
   - steps( integer,?) ： 接受两个参数的步进函数。第一个参数必须为正整数，指定函数的步数。第二个参数取值可以是 start 或 end ，指定每一步的值发生变化的时间点。第二个参数默认值为 end 。
   - cubic-bezie ( number, number, number, number)： 特定的贝塞尔曲线类型。

2. animation-iteration-count ，指定动画的播放次数
   - number ：动画循环次数
   - infinite ： 无限循环

3. animation-direction ，指定动画方向

   - normal ： 正常方向 (默认)
   - reverse ： 反方向运行
   - alternate ： 动画先正常运行再反方向运行，并持续交替运行  
   - alternate-reverse ： 动画先反运行再正方向运行，并持续交替运行

4. animation-fill-mode ，设置动画之外的状态
   - forwards ： 设置对象状态为动画结束时的状态
   - backwards ： 设置对象状态为动画开始时的状态

5. animation-play-state ，设置动画的播放状态
   - running ： 运动 (默认)
   - paused ： 暂停

#### 动画复合属性

只设置一个时间表示 duration ，设置两个时间分别是： duration 和 delay ，其他属性没有数量和
顺序要求。

```css
.inner {
animation: atguigu 3s 0.5s linear 2 alternate-reverse forwards;
}
```

备注： animation-play-state 一般单独使用。

### 多列布局

作用：专门用于实现类似于报纸的布局
常用属性如下：

- column-count ：指定列数，值是数字。
- column-width ：指定列宽，值是长度。
- columns ：同时指定列宽和列数，复合属性；值没有数量和顺序要求。
- column-gap ：设置列边距，值是长度。
- column-rule-style ：设置列与列之间边框的风格，值与 border-style 一致。
- column-rule-width ：设置列与列之间边框的宽度，值是长度。
- column-rule-color ：设置列与列之间边框的颜色。
- coumn-rule ：设置列边框，复合属性。
- column-span 指定是否跨列；值: none 、 all

### 伸缩盒子

`Flexible Box` 简称 `flex`，意为”弹性布局”，可以简便、完整、响应式地实现各种页面布局

采用Flex布局的元素，称为`flex`容器`container`

它的所有子元素自动成为容器成员，称为`flex`项目`item`

容器中默认存在两条轴，主轴和交叉轴，呈90度关系。项目默认沿主轴排列，通过`flex-direction`来决定主轴的方向

每根轴都有起点和终点，这对于元素的对齐非常重要

#### 属性

关于`flex`常用的属性，我们可以划分为容器属性和容器成员属性

容器属性有：

- flex-direction
- flex-wrap
- flex-flow
- justify-content
- align-items
- align-content

#### flex-direction

决定主轴的方向(即项目的排列方向)

```css
.container {   
    flex-direction: row | row-reverse | column | column-reverse;  
} 
```

属性对应如下：

- row（默认值）：主轴为水平方向，起点在左端
- row-reverse：主轴为水平方向，起点在右端
- column：主轴为垂直方向，起点在上沿。
- column-reverse：主轴为垂直方向，起点在下沿

#### flex-wrap

弹性元素永远沿主轴排列，那么如果主轴排不下，通过`flex-wrap`决定容器内项目是否可换行

```css
.container {  
    flex-wrap: nowrap | wrap | wrap-reverse;
}  
```

属性对应如下：

- nowrap（默认值）：不换行
- wrap：换行，第一行在容器最上面
- wrap-reverse：反向换行，第一行在容器最下面

默认情况是不换行，但这里也不会任由元素直接溢出容器，会涉及到元素的弹性伸缩

#### flex-flow

是`flex-direction`属性和`flex-wrap`属性的简写形式，默认值为`row nowrap`

```css
.box {
  flex-flow: <flex-direction> || <flex-wrap>;
}
```

#### justify-content

定义了项目在主轴上的对齐方式

```css
.box {
    justify-content: flex-start | flex-end | center | space-between | space-around;
}
```

属性对应如下：

- flex-start（默认值）：左对齐
- flex-end：右对齐
- center：居中
- space-between：两端对齐，项目之间的间隔都相等
- space-around：两个项目两侧间隔相等

#### align-items

定义项目在交叉轴上如何对齐

```css
.box {
  align-items: flex-start | flex-end | center | baseline | stretch;
}
```

属性对应如下：

- flex-start：交叉轴的起点对齐
- flex-end：交叉轴的终点对齐
- center：交叉轴的中点对齐
- baseline: 项目的第一行文字的基线对齐
- stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度

#### align-content

定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用

```css
.box {
    align-content: flex-start | flex-end | center | space-between | space-around | stretch;
}
```

属性对应如吓：

- flex-start：与交叉轴的起点对齐
- flex-end：与交叉轴的终点对齐
- center：与交叉轴的中点对齐
- space-between：与交叉轴两端对齐，轴线之间的间隔平均分布
- space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍
- stretch（默认值）：轴线占满整个交叉轴

容器成员属性如下：

- `order`
- `flex-grow`
- `flex-shrink`
- `flex-basis`
- `flex`
- `align-self`

#### order

定义项目的排列顺序。数值越小，排列越靠前，默认为0

```css
.item {
    order: <integer>;
}
```

#### flex-grow

上面讲到当容器设为`flex-wrap: nowrap;`不换行的时候，容器宽度有不够分的情况，弹性元素会根据`flex-grow`来决定

定义项目的放大比例（容器宽度>元素总宽度时如何伸展）

默认为`0`，即如果存在剩余空间，也不放大

```css
.item {
    flex-grow: <number>;
}
```

规则：

1. 若所有伸缩项目的 flex-grow 值都为 1 ，则：它们将等分剩余空间（如果有空间的话）。
2. 若三个伸缩项目的 flex-grow 值分别为： 1 、 2 、 3 ，则：分别瓜分到： 1/6 、 2/6 、
3/6 的空间

#### flex-shrink

定义了项目的缩小比例（容器宽度<元素总宽度时如何收缩），默认为1，即如果空间不足，该项目将缩小

```css
.item {
    flex-shrink: <number>; /* default 1 */
}
```

如果所有项目的`flex-shrink`属性都为1，当空间不足时，都将等比例缩小

如果一个项目的`flex-shrink`属性为0，其他项目都为1，则空间不足时，前者不缩小

>例如：
>三个收缩项目，宽度分别为： 200px 、 300px 、 200px ，它们的 flex-shrink 值分别
>为： 1 、 2 、 3
>若想刚好容纳下三个项目，需要总宽度为 700px ，但目前容器只有 400px ，还差 300px
>所以每个人都要收缩一下才可以放下，具体收缩的值，这样计算：
>
>1. 计算分母： (200×1) + (300×2) + (200×3) = 1400
>2. 计算比例：
> 项目一： (200×1) / 1400 = 比例值1
> 项目二： (300×2) / 1400 = 比例值2
> 项目三： (200×3) / 1400 = 比例值3
>3. 计算最终收缩大小：
> 项目一需要收缩： 比例值1 × 300
> 项目二需要收缩： 比例值2 × 300
> 项目三需要收缩： 比例值3 × 300

#### flex-basis

设置的是元素在主轴上的初始尺寸，所谓的初始尺寸就是元素在`flex-grow`和`flex-shrink`生效前的尺寸

浏览器根据这个属性，计算主轴是否有多余空间，默认值为`auto`，即项目的本来大小，如设置了`width`则元素尺寸由`width/height`决定（主轴方向），没有设置则由内容决定

```css
.item {
   flex-basis: <length> | auto; /* default auto */
}
```

当设置为0的是，会根据内容撑开

它可以设为跟`width`或`height`属性一样的值（比如350px），则项目将占据固定空间

#### flex

`flex`属性是`flex-grow`, `flex-shrink` 和 `flex-basis`的简写，默认值为`0 1 auto`，也是比较难懂的一个复合属性

```css
.item {
  flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```

一些属性有：

- flex: 1 = flex: 1 1 0%
- flex: 2 = flex: 2 1 0%
- flex: auto = flex: 1 1 auto
- flex: none = flex: 0 0 auto，常用于固定尺寸不伸缩

`flex:1` 和 `flex:auto` 的区别，可以归结于`flex-basis:0`和`flex-basis:auto`的区别

当设置为0时（绝对弹性元素），此时相当于告诉`flex-grow`和`flex-shrink`在伸缩的时候不需要考虑我的尺寸

当设置为`auto`时（相对弹性元素），此时则需要在伸缩时将元素尺寸纳入考虑

注意：建议优先使用这个属性，而不是单独写三个分离的属性，因为浏览器会推算相关值

#### align-self

允许单个项目有与其他项目不一样的对齐方式，可覆盖`align-items`属性

默认值为`auto`，表示继承父元素的`align-items`属性，如果没有父元素，则等同于`stretch`

```css
.item {
    align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

### 响应式布局

### 媒体查询

`CSS3`中的增加了更多的媒体查询，就像`if`条件表达式一样，我们可以设置不同类型的媒体条件，并根据对应的条件，给相应符合条件的媒体调用相对应的样式表

使用`@Media`查询，可以针对不同的媒体类型定义不同的样式，如：

```css
@media screen and (max-width: 1920px) { ... }
```

当视口在375px - 600px之间，设置特定字体大小18px

```css
@media screen (min-width: 375px) and (max-width: 600px) {
  body {
    font-size: 18px;
  }
}
```

@media only screen and

> only (限定某种设备)  
> screen 是媒体类型里的一种
> and 被称为关键字，其他关键字还包括 not (排除某种设备)

运算符

| 值   | 含义 |
|------|------|
| and  | 并且 |
| ,    | 或   |
| or   | 或   |
| not  | 否定 |
| only | 肯定 |

only 用于防止某些老旧浏览器应用某些特定的样式。通过添加 only，只有支持该媒体查询的浏览器才会应用这些样式。其他不支持该查询的浏览器会忽略这些样式。

| 类型        | 解释                               |
|-------------|------------------------------------|
| all         | 所有设备                           |
| braille     | 盲文                               |
| embossed    | 盲文打印                           |
| handheld    | 手持设备                           |
| print       | 文档打印或打印预览模式             |
| projection  | 项目演示，比如幻灯                 |
| screen      | 彩色电脑屏幕                       |
| speech      | 演讲                               |
| tty         | 固定字母间距的网格的媒体，比如电传打字机 |
| tv          | 电视                               |

