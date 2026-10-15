from __future__ import annotations

import html
import os
import re
import shutil
import stat
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'notebook'
OUT = ROOT / '_site'
TEMPLATE = ROOT / 'site' / 'template.html'


def relative_url(target: Path, current: Path) -> str:
    return quote(Path(os.path.relpath(target, current.parent)).as_posix(), safe='/')


def page_tree(files: list[Path], current: Path, collapsible: bool = True) -> str:
    """Render navigation at arbitrary directory depths."""
    def render(directory: Path) -> str:
        lines = ['<ul>']
        for page in (p for p in files if p.parent == directory):
            url = relative_url(page.with_suffix('.html'), current.with_suffix('.html'))
            name = '首页' if page == DOCS / 'index.md' else (
                '目录' if page.name == 'index.md' else page.stem.replace('_', ' '))
            active = ' class="active" aria-current="page"' if page == current else ''
            lines.append(f'<li><a{active} href="{html.escape(url, quote=True)}">{html.escape(name)}</a></li>')
        directories = sorted({directory / page.relative_to(directory).parts[0]
                              for page in files if page.is_relative_to(directory)
                              and len(page.relative_to(directory).parts) > 1},
                             key=lambda path: path.name.casefold())
        for child in directories:
            name = html.escape(child.name)
            if collapsible:
                opened = ' open' if current.is_relative_to(child) else ''
                lines.append(f'<li><details{opened}><summary class="nav-section">{name}</summary>'
                             f'{render(child)}</details></li>')
            else:
                lines.append(f'<li><div class="nav-section">{name}</div>{render(child)}</li>')
        lines.append('</ul>')
        return '\n'.join(lines)

    return render(DOCS)


def rewrite_md_links(page: str) -> str:
    # Edit actual HTML attributes, preserving code examples and scripts.
    edits: list[tuple[int, int, str]] = []
    line_offsets = [0] + [match.end() for match in re.finditer('\n', page)]

    class LinkParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            raw = self.get_starttag_text()
            for match in re.finditer(r'''\s(href)\s*=\s*(['"])(.*?)\2''', raw, re.IGNORECASE | re.DOTALL):
                target = html.unescape(match.group(3))
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or target.startswith(('/', '#')):
                    continue
                if parts.path.lower().endswith('.md'):
                    url = urlunsplit(('', '', quote(parts.path[:-3] + '.html', safe='/%'),
                                       parts.query, parts.fragment))
                    line, column = self.getpos()
                    start = line_offsets[line - 1] + column
                    edits.append((start + match.start(3), start + match.end(3),
                                  html.escape(url, quote=True)))

        handle_startendtag = handle_starttag

    parser = LinkParser(convert_charrefs=False)
    parser.feed(page)
    for start, end, value in reversed(edits):
        page = page[:start] + value + page[end:]
    return page


def build() -> None:
    if not DOCS.is_dir():
        raise SystemExit('Missing notebook directory')
    if not shutil.which('pandoc'):
        raise SystemExit('Pandoc is required. Install it from https://pandoc.org/installing.html')
    def remove_readonly(function, path, error):
        # OneDrive can mark generated directories read-only on Windows.
        if not isinstance(error, PermissionError):
            raise error
        os.chmod(path, stat.S_IWRITE)
        function(path)

    if OUT.exists():
        shutil.rmtree(OUT, onexc=remove_readonly)
    OUT.mkdir(parents=True)
    sources = [path for path in DOCS.rglob('*')
               if path.is_file() and not any(part.startswith('.') for part in path.relative_to(DOCS).parts)]
    files = sorted((path for path in sources if path.suffix.lower() == '.md'),
                   key=lambda p: (p.name != 'index.md', p.relative_to(DOCS).as_posix().casefold()))
    for source in sources:
        if source.suffix.lower() != '.md':
            target = OUT / source.relative_to(DOCS)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (OUT / '_assets').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'site' / 'style.css', OUT / '_assets' / 'style.css')
    shutil.copy2(ROOT / 'site' / 'sidebar.js', OUT / '_assets' / 'sidebar.js')
    (OUT / '.nojekyll').touch()
    # This virtual source provides URLs for the home without writing to notebook/.
    home = DOCS / 'index.md'
    nav_files = [home, *[page for page in files if page != home]]
    for source in nav_files:
        relative = source.relative_to(DOCS)
        target = OUT / relative.with_suffix('.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        css_link = relative_url(OUT / '_assets' / 'style.css', target)
        home_link = relative_url(OUT / 'index.html', target)
        args = [
            'pandoc', '--from=markdown+tex_math_dollars+autolink_bare_uris', '--to=html5',
            '--standalone', '--toc', '--toc-depth=3', '--mathjax',
            f'--template={TEMPLATE}',
            f'--variable=site-nav:{page_tree(nav_files, source)}',
            f'--variable=css-path:{css_link}',
            f'--variable=sidebar-script:{relative_url(OUT / "_assets" / "sidebar.js", target)}',
            f'--variable=home-link:{home_link}',
            f'--metadata=title:{"首页" if source == DOCS / "index.md" else source.stem}',
            '--metadata=lang:zh-CN',
        ]
        if source == home:
            args.append(f'--variable=page-index:{page_tree([p for p in files if p != source], source, collapsible=False)}')
            content = f'# 学习笔记\n\n共 {len(files)} 篇笔记。通过左侧导航或下方目录浏览。\n'
            # An existing root index note can optionally provide the home content.
            if source in files:
                content = source.read_text(encoding='utf-8')
        else:
            args.insert(1, str(source))
            content = None
        result = subprocess.run(args, input=content, text=True, encoding='utf-8', capture_output=True)
        if result.returncode:
            raise SystemExit(f'Failed to build {relative}:\n{result.stderr}')
        rendered = result.stdout
        target.write_text(rewrite_md_links(rendered), encoding='utf-8')
    print(f'Built {len(files)} notes and an automatic home page in {OUT}')


if __name__ == '__main__':
    build()
