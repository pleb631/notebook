<!-- TOC -->
- [html](#html)
  - [html框架示例](#html框架示例)
  - [基础标签](#基础标签)
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

<!-- /TOC -->

[参考资料及查表](https://www.w3school.com.cn/index.html)

# html

## html框架示例

```html
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

</body>
</html>

```

- \<html> 与 \</html> 之间的文本描述网页
- \<body> 与 \</body> 之间的文本是可见的页面内容
- \<h1> 与 \</h1> 之间的文本被显示为标题
- \<p> 与 \</p> 之间的文本被显示为段落

## 基础标签

- \<html></html>称为根标签，所有的网页标签都在\<html></html>中。

- \<head> 标签用于定义文档的头部，它是所有头部元素的容器。头部元素有\<title>、\<script>、 \<style>、\<link>、 \<meta>等标签

- \<p></p>   段落标签

- \<div></div>  把一些独立的逻辑部分划分出来，放在一个\<div>标签中，这个\<div>标签的作用就相当于一个容器  <div  id="版块名称">…</div>给div命名

- \<span></span> span标签是没有语义的，它的作用就是为了设置单独的样式用的。

- \<h></h>   标题标签，标题标签一共有6个，h1、h2、h3、h4、h5、h6分别为一级标题、二级标题、三级标题、四级标题、五级标题、六级标题。

- \<strong>和\<em>标签，在浏览器中\<em> 默认用斜体表示，\<strong> 用粗体表示。

- \<ul></ul> 无序列表,ol 有序列表

  ```html
  <ul>
    <li>信息</li>
    <li>信息</li>
    ......
  </ul>
  ```

- 表单标签

  ```html
  <form>
  姓名：
  <input type="text" name="myName">
  <br/>
  密码：
  <input type="password" name="pass">
  </form>
  ```

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
