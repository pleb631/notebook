# 学习笔记

`notebook/` 保存 Markdown 笔记；推送到 `main` 后，GitHub Actions 自动构建网页并发布到 GitHub Pages。

## 目录

```text
notebook/                 # 笔记、图片和附件，支持任意层级目录
site/
  build.py                # 扫描笔记、生成导航和 HTML
  template.html           # 统一布局
  style.css               # 页面样式
  test_build.py           # 构建回归测试
  check_site.py           # 检查生成页面中的本地链接和资源
.github/workflows/
  pages.yml               # 自动构建和发布
```

## 启用自动发布

1. 上传本仓库到 GitHub，确保发布分支为 `main`。
2. 打开仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
3. 推送修改，或在 **Actions → Publish notebook → Run workflow** 手动运行。
4. 部署成功后，在 **Settings → Pages** 查看网站地址。项目仓库通常为 `https://<用户名>.github.io/<仓库名>/`。

之后新增、修改或删除 `notebook/` 内的笔记、图片和附件，只需提交并推送，页面和导航会自动更新。修改 `site/` 或工作流也会触发发布。使用其他分支时，同时修改 `pages.yml` 中的 `branches`，并检查 `github-pages` 环境的分支保护设置。

## 写笔记

- 分类使用文件夹，文章使用 `.md` 文件，中文名称和多层目录均可。
- 左侧各级分类可点击名称或箭头独立展开、收起；当前文章所在目录默认展开，其余分类默认收起。键盘可用 Tab 选中分类，再按 Enter 或空格切换。首页正文中的全部笔记目录保持展开。
- 左侧顶部可用“笔记目录 / 本页大纲”按钮切换视图，正文右侧不再单独放置目录。“本页大纲”列出当前文章的标题，点击跳到对应章节；切换按钮支持左右方向键和 Home / End。切换视图会保留当前页面中目录的展开状态；禁用 JavaScript 时两种目录均可直接浏览。
- 左下角“隐藏导航”按钮可收起整个左侧栏，让文档居中显示；点击“显示导航”即可恢复。按钮在滚动时保持可见，浏览器会记住当前站点的选择，刷新或打开其他笔记时继续生效。
- 笔记间链接使用相对路径，例如 `[贝叶斯滤波](appliedMath/贝叶斯滤波.md)`；构建后自动转换为网页链接，保留查询参数和章节锚点。
- 图片和附件放在 `notebook/` 内，以相对路径引用。目录结构会原样复制；`.ipynb` 等附件保留原文件，不转换为文章。以点开头的文件和目录不发布。
- 使用 `$...$` 和 `$$...$$` 编写公式，通过 MathJax 显示；浏览器需要能访问 MathJax CDN。
- 首页及文章目录由 `site/build.py` 自动生成到 `_site/index.html`，无需在 `notebook/` 内放置首页文件。调整首页介绍可修改构建脚本中的首页内容。
- 站点使用相对链接，兼容 GitHub Pages 的仓库子路径。本机绝对路径和仓库外资源需要改为网址或笔记内的相对路径。

## 本地预览

### 页面风格

默认使用参照 Typora Night 调整的固定深色主题，不跟随系统浅色模式。背景、正文、标题、代码高亮均集中在 `site/style.css` 顶部的 `:root` 中，可直接调整：

| 变量 | 用途 | 当前值 |
| --- | --- | --- |
| `--bg` / `--panel` | 正文背景 / 侧栏背景 | `#363b40` / `#2e3033` |
| `--text` / `--heading` | 正文 / 标题颜色 | `#b8bfc6` / `#dedede` |
| `--body-size` / `--body-leading` | 正文字号 / 行距 | `16px` / `1.75` |
| `--content-width` | 正文区域最大宽度（含左右内边距） | `914px` |
| `--code-size` / `--code-bg` | 代码字号 / 背景 | `15px` / `#333333` |
| `--code-keyword` / `--code-comment` | 关键字 / 注释颜色 | `#c88fd0` / `#da924a` |

标题不加横线、代码块采用小圆角、表格使用交替底色。代码字符串与函数颜色比原 Night 略亮，以改善对比度。修改后重新构建即可。

### 构建与预览

安装 Python 3.12 和 [Pandoc](https://pandoc.org/installing.html)（CI 使用 3.6.4），无需额外 Python 包。在仓库根目录运行：

```sh
python site/build.py
python -m http.server 8000 --directory _site
```

打开 `http://localhost:8000/`。每次构建会重新生成 `_site/`；该目录已加入 Git 忽略规则。Windows 如无法运行 `python`，可替换为 `py`。

运行回归测试：

```sh
python -m unittest discover -s site -p 'test_*.py'
```
