<!-- TOC -->
- [html](#html)
  - [html框架示例](#html框架示例)
  - [基础的四个标签](#基础的四个标签)
- [css](#css)
  - [语法](#语法)
  - [选择器](#选择器)

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

## 基础的四个标签

**HTML 标题**
\<h1> - \<h6>
`<h1>This is a heading</h1>`
**HTML 段落**
`<p>This is a paragraph.</p>`
**HTML 链接**
`<a href="http://www.w3school.com.cn">This is a link</a>`
**HTML 图像**
`<img src="w3school.jpg" width="104" height="142" />`

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

- 分组选择器
h1,h2,p都会应用这个样式

```css
h1, h2, p {
  text-align: center;
  color: red;
}
```
