import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import quote

import build


class LinkTests(unittest.TestCase):
    def test_relative_links_keep_queries_and_fragments(self):
        source = '<a href="../数学/线性 规划.MD?x=1&amp;y=2#公式">笔记</a>'
        expected = quote('../数学/线性 规划.html', safe='/')
        self.assertEqual(build.rewrite_md_links(source),
                         f'<a href="{expected}?x=1&amp;y=2#公式">笔记</a>')

    def test_external_links_and_code_are_unchanged(self):
        source = '''<a href="https://example.com/a.md">外链</a>
<a href="//example.com/a.md">外链</a><a href="/a.md">绝对路径</a>
<code>href="example.md"</code><pre>&lt;a href="example.md"&gt;</pre>
<script>const example = '<a href="example.md">';</script>'''
        self.assertEqual(build.rewrite_md_links(source), source)

    def test_percent_encoded_links_are_not_double_encoded(self):
        source = '<a href="%E6%95%B0%E5%AD%A6.md#title">link</a>'
        self.assertEqual(build.rewrite_md_links(source), source.replace('.md', '.html'))


class BuildTests(unittest.TestCase):
    def test_real_pandoc_build_and_rebuild(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = Path(folder) / 'notebook'
            out = Path(folder) / '_site'
            nested = docs / '数学' / '子目录'
            nested.mkdir(parents=True)
            note = nested / '线性 规划.md'
            note.write_text('# 线性规划\n\n## 公式\n\n$x^2$\n\n'
                            '[自身](线性%20规划.md?from=note#公式)\n\n'
                            '![图片](plot.svg)\n\n```python\nprint(1)\n```', encoding='utf-8')
            (nested / 'plot.svg').write_text('<svg/>', encoding='utf-8')
            (docs / '.private.md').write_text('hidden', encoding='utf-8')
            originals = {p.relative_to(docs): p.read_bytes() for p in docs.rglob('*') if p.is_file()}
            with patch.object(build, 'DOCS', docs), patch.object(build, 'OUT', out), \
                    contextlib.redirect_stdout(io.StringIO()):
                build.build()
                home = (out / 'index.html').read_text(encoding='utf-8')
                page = (out / '数学' / '子目录' / '线性 规划.html').read_text(encoding='utf-8')
                self.assertIn('全部笔记', home)
                self.assertIn(quote('数学/子目录/线性 规划.html', safe='/'), home)
                self.assertIn('aria-current="page"', page)
                self.assertIn(quote('线性 规划.html', safe='/') + '?from=note#', page)
                self.assertIn('href="../../index.html"', page)
                self.assertIn('href="../../_assets/style.css"', page)
                self.assertIn('math inline', page)
                self.assertIn('mathjax', page.lower())
                self.assertIn('sourceCode', page)
                self.assertEqual((out / '数学' / '子目录' / 'plot.svg').read_text(), '<svg/>')
                self.assertFalse((out / '.private.html').exists())
                self.assertTrue((out / '.nojekyll').exists())
                self.assertFalse((docs / 'index.md').exists())
                self.assertEqual(originals, {p.relative_to(docs): p.read_bytes()
                                            for p in docs.rglob('*') if p.is_file()})
                # A deleted source must disappear from both HTML and navigation.
                note.unlink()
                build.build()
                self.assertFalse((out / '数学' / '子目录' / '线性 规划.html').exists())
                self.assertNotIn('线性 规划', (out / 'index.html').read_text(encoding='utf-8'))
                self.assertIn('共 0 篇笔记', (out / 'index.html').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
