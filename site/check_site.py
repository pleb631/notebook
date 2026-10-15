"""Check generated navigation, stylesheet paths and relative article links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent / '_site'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.targets.append(value)


def check() -> None:
    pages = list(ROOT.rglob('*.html'))
    if not (ROOT / 'index.html').is_file():
        raise SystemExit('Build the site first: python site/build.py')
    missing = []
    for page in pages:
        parser = Links()
        parser.feed(page.read_text(encoding='utf-8'))
        for target in parser.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
                continue
            path = page.parent / unquote(url.path)
            if not path.exists():
                missing.append(f'{page.relative_to(ROOT)} -> {target}')
    if missing:
        raise SystemExit('Missing local link targets:\n' + '\n'.join(missing))
    print(f'Checked local links and assets in {len(pages)} HTML pages.')


if __name__ == '__main__':
    check()
