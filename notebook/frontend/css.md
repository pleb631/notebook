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
