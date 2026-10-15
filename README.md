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
- 笔记间链接使用相对路径，例如 `[贝叶斯滤波](appliedMath/贝叶斯滤波.md)`；构建后自动转换为网页链接，保留查询参数和章节锚点。
- 图片和附件放在 `notebook/` 内，以相对路径引用。目录结构会原样复制；`.ipynb` 等附件保留原文件，不转换为文章。以点开头的文件和目录不发布。
- 使用 `$...$` 和 `$$...$$` 编写公式，通过 MathJax 显示；浏览器需要能访问 MathJax CDN。
- 首页及文章目录由 `site/build.py` 自动生成到 `_site/index.html`，无需在 `notebook/` 内放置首页文件。调整首页介绍可修改构建脚本中的首页内容。
- 站点使用相对链接，兼容 GitHub Pages 的仓库子路径。本机绝对路径和仓库外资源需要改为网址或笔记内的相对路径。

## 本地预览

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
