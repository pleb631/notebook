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
