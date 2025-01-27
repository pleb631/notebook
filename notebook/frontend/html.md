<!-- TOC -->
- [html](#html)
  - [排版标签](#排版标签)
    - [标题标签h](#标题标签h)
    - [段落标签p](#段落标签p)
    - [水平线标签hr](#水平线标签hr)
    - [换行标签br](#换行标签br)
    - [div和span标签](#div和span标签)
  - [图像标签img](#图像标签img)
  - [链接标签](#链接标签)
  - [table](#table)
    - [创建表格](#创建表格)
    - [表格属性](#表格属性)
    - [表头单元格标签th](#表头单元格标签th)
    - [表格标题caption](#表格标题caption)
    - [合并单元格](#合并单元格)
  - [列表标签](#列表标签)
    - [无序列表ul](#无序列表ul)
    - [有序列表ol](#有序列表ol)
    - [自定义列表](#自定义列表)
  - [表单标签](#表单标签)
    - [input控件](#input控件)
    - [label标签](#label标签)
    - [textarea控件(文本域)](#textarea控件文本域)
      - [select下拉列表](#select下拉列表)
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

## 排版标签

### 标题标签h

其基本语法格式如下：

```html
<h1>标题文本</h1>
<h2>标题文本</h2>
<h3>标题文本</h3>
<h4>标题文本</h4>
```

### 段落标签p

**作用语义：**

可以把 HTML 文档分割为若干段落。在网页中要把文字有条理地显示出来，离不开段落标签，就如同我们平常写文章一样，整个网页也可以分为若干个段落，而段落的标签就是

```html
<p>  文本内容  </p>
```

是HTML文档中最常见的标签，默认情况下，文本在一个段落中会根据浏览器窗口的大小自动换行。

### 水平线标签hr

在网页中常常看到一些水平线将段落与段落之间隔开，使得文档结构清晰，层次分明。这些水平线可以通过插入图片实现，也可以简单地通过标签来完成，就是创建横跨网页水平线的标签。其基本语法格式如下：

---

```html
<hr/>是单标签
```

在网页中显示默认样式的水平线。

### 换行标签br

在HTML中，一个段落中的文字会从左到右依次排列，直到浏览器窗口的右端，然后自动换行。如果希望某段文本强制换行显示，就需要使用换行标签

```html
<br/>
```

### div和span标签

`div`和`span`是没有语义的,都是布局用的

```html
<div> 这是头部 </div>
<span>今日价格</span>
```

- div标签一行只能放一个div
- span标签一行上可以放好多个span

## 图像标签img

要想在网页中显示图像就需要使用图像标签，接下来将详细介绍图像标签以及和他相关的属性。

语法如下：

```html
<img src="图像URL" />
```

## 链接标签

在HTML中创建超链接非常简单，只需用标签把文字包括起来就好。

语法格式：

```html
<a href="跳转目标" target="目标窗口的弹出方式">文本或图像</a>
```

> href：用于指定链接目标的url地址，（必须属性）当为标签应用href属性时，它就具有了超链接的功能
>
> target：用于指定链接页面的打开方式，其取值有_self和_blank两种，其中_self为默认值，__blank为在新窗口中打开方式。

**注意：**

1. 外部链接 需要添加 `http://`
2. 内部链接 直接链接内部页面名称即可 比如 `< a href="index.html">` 首页
3. 如果当时没有确定链接目标时，通常将链接标签的href属性值定义为"#"(即href="#")，表示该链接暂时为一个空链接。
4. 不仅可以创建文本超链接，在网页中各种网页元素，如图像、表格、音频、视频等都可以添加超链接。
5. 下载链接：如果href里面地址是一个文件或压缩包，会下载这个文件
6. 锚点链接：跳转作用

## table

### 创建表格

在HTML网页中，要想创建表格，就需要使用表格相关的标签。

**创建表格的基本语法：**

```html
<table>
  <tr>
    <td>单元格内的文字</td>
    ...
  </tr>
  ...
</table>
```

在上面的语法中包含基本的三对HTML标签，分别为 table、tr、td，他们是创建表格的基本标签，缺一不可，下面对他们进行具体地解释

1. table用于定义一个表格标签。
2. tr标签 用于定义表格中的行，必须嵌套在 table标签中。
3. td 用于定义表格中的单元格，必须嵌套在标签中。
4. 字母 td 指表格数据（table data），即数据单元格的内容。

### 表格属性

常用属性有border、cellpadding、cellspacing、align，默认为0

**案例1：**

```html
// border为表格外边宽，cellspacing为单元格间距，cellpadding为单元边沿与其内容之间的空白
<table width="500" height="300" border="1" cellpadding="20" cellspacing="0" align="center">
   <tr>  <th>姓名</th>   <th>性别</th> <th>年龄</th>  </tr>
   <tr>  <td>刘德华</td> <td>男</td> <td>55</td>  </tr>
   <tr>  <td>郭富城</td> <td>男</td> <td>52</td>  </tr>
   <tr>  <td>张学友</td> <td>男</td> <td>58</td>  </tr>
   <tr>  <td>黎明</td>   <td>男</td> <td>18</td>  </tr>
   <tr>  <td>刘晓庆</td> <td>女</td> <td>63</td>  </tr>
</table>
```

### 表头单元格标签th

作用：一般表头单元格位于表格的第一行或第一列，并且文本加粗居中

语法：只需用表头标签替代相应的单元格标签即可。

```html
<table width="500" border="1" align="center" cellspacing="0" cellpadding="0">
  <tr>  
   <th>姓名</th> 
   <th>性别</th>
   <th>电话</th>
  </tr>
  <tr>
   <td>小王</td>
   <td>女</td>
   <td>110</td>
  </tr>
  <tr>
   <td>小明</td>
   <td>男</td>
   <td>120</td>
  </tr> 
 </table>
```

> th 也是一个单元格，只不过和普通的 td单元格不一样，它会让自己里面的文字居中且加粗

### 表格标题caption

```html
<table>
   <caption>我是表格标题</caption>
</table>
```

**注意：**

1. caption 元素定义**表格标题**，通常这个标题会被居中且显示于表格之上。
2. caption 标签必须紧随 table 标签之后。

### 合并单元格

合并单元格是我们比较常用的一个操作，但是不会合并的很复杂。

- 跨行合并：rowspan="合并单元格的个数"
- 跨列合并：colspan="合并单元格的个数"

注意

1. 先确定是跨行还是跨列合并
2. 根据先上后下，先左后右的原则找到目标单元格，然后写上 合并方式 还有 要合并的单元格数量。
3. 删除多余的单元格单元格

```html
<table>
  <thead>
    <tr>
      <th>月份</th>
      <th>存款</th>
      <th rowspan="3">节假日的储蓄！</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>一月</td>
      <td>￥3000</td>
      <td rowspan="0">￥6000</td>
    </tr>
    <tr>
      <td>二月</td>
      <td>￥4000</td>
    </tr>
  </tbody>
</table>
```

## 列表标签

前面我们知道表格一般用于数据展示的，但是网页中还是有很多跟表格类似的布局，如下图~~ 我们用什么做呢？

答案是列表， 那什么是列表？  表格是用来显示数据的，那么列表就是用来布局的。 因为非常整齐和自由

### 无序列表ul

无序列表的各个列表项之间没有顺序级别之分，是并列的。其基本语法格式如下：

```html
<ul>
  <li>列表项1</li>
  <li>列表项2</li>
  <li>列表项3</li>
  ......
</ul>
```

### 有序列表ol

有序列表即为有排列顺序的列表，其各个列表项按照一定的顺序排列定义，有序列表的基本语法格式如下：

```html
<ol>
  <li>列表项1</li>
  <li>列表项2</li>
  <li>列表项3</li>
  ......
</ol>
```

所有特性基本与ul 一致。  但是实际中比 无序列表 用的少很多。

### 自定义列表

定义列表常用于对术语或名词进行解释和描述，定义列表的列表项前没有任何项目符号。其基本语法如下：

```html
<dl>
  <dt>名词1</dt>
  <dd>名词1解释1</dd>
  <dd>名词1解释2</dd>
  ...
  <dt>名词2</dt>
  <dd>名词2解释1</dd>
  <dd>名词2解释2</dd>
  ...
</dl>
```

## 表单标签

表单目的是为了收集用户信息。

在我们网页中， 我们也需要跟用户进行交互，收集用户资料，此时也需要表单。

> 在HTML中，一个完整的表单通常由表单控件（也称为表单元素）、提示信息和表单域3个部分构成。
> 包含了具体的表单功能项，如单行文本输入框、密码输入框、复选框、提交按钮、重置按钮等。
> 一个表单中通常还需要包含一些说明性的文字，提示用户进行填写和操作。
> 他相当于一个容器，用来容纳所有的表单控件和提示信息，可以通过他定义处理表单数据所用程序的url地址，以及数据提交到服务器的方法。如果不定义表单域，表单中的数据就无法传送到后台服务器。

### input控件

- 语法：

```html
<input type="属性值" value="你好">
```

- 标签为单标签
- type属性设置不同的属性值用来指定不同的控件类型
- 除了type属性还有别的属性

1. type属性

   - 这个属性通过改变值，可以决定了你属于那种input表单。
   - 比如 `type = 'text'`  就表示 文本框 可以做 用户名,昵称等。
   - 比如 `type = 'password'`  就是表示密码框用户输入的内是不可见的。

    ```html
    用户名: <input type="text" /> 
    密  码：<input type="password" />
    ```

2. value属性值

    ```html
    用户名:<input type="text"  name="username" value="请输入用户名">
    ```

   - value 默认的文本值。有些表单想刚打开页面就默认显示几个文字，就可以通过这个value 来设置。

3. name属性

    ```html
    用户名:<input type="text"  name=“username” />
    ```

    > name表单的名字， 这样，后台可以通过这个name属性找到这个表单。页面中的表单很多，name主要作用就是用于区别不同的表单。

    - name属性后面的值，是我们自己定义的。
    - radio如果是一组，我们必须给他们命名相同的名字name这样就可以多个选其中的一个啦

    ```html
    <input type="radio" name="sex"  />男
    <input type="radio" name="sex" />女
    ```

   - name属性，我们现在用的较少， 但是，当我们学ajax 和后台的时候，是必须的。

4. checked属性

   - 表示默认选中状态。较常见于单选按钮和复选按钮。

   ```html
   性    别:
   <input type="radio" name="sex" value="男" checked="checked" />男
   <input type="radio" name="sex" value="女" />女
   ```

    > 上面这个，表示就默认选中了男这个单选按钮

### label标签

label标签为 input 元素定义标注（标签）。

**作用：**

> 用于绑定一个表单元素, 当点击label标签的时候, 被绑定的表单元素就会获得输入焦点。

**如何绑定元素呢？**

1. 第一种用法就是用label直接包括input表单。

    ```html
    <label> 用户名： <input type="type" name="usename" value="请输入用户名">   </label>
    ```

2. 第二种用法 for 属性规定 label 与哪个表单元素绑定。

    ```html
    <label for="sex">男</label>
    <input type="radio" name="sex"  id="sex">
    ```

> 当我们鼠标点击 label标签里面的文字时，光标会定位到指定的表单里面

### textarea控件(文本域)

- 语法：

```html
<textarea >
  文本内容
</textarea>
```

- 作用：

  > 通过textarea控件可以轻松地创建多行文本输入框.cols="每行中的字符数" rows="显示的行数" ,实际开发不用

#### select下拉列表

**语法：**

```html
<select>
  <option>选项1</option>
  <option>选项2</option>
  <option>选项3</option>
  ...
</select>
```

- 注意：

1. 至少包含一对 option
2. 在option中定义selected ="selected"时，当前项即为默认选中项。
3. 实际开发会用的比较少

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
