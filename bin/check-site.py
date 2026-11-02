#!/usr/bin/env python3
"""Check the built site's entry points and local HTML asset/navigation links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and (key == 'src' or (key == 'href' and tag in ('a', 'link'))):
                self.targets.append(value)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
    errors = []
    for page in ('index.html', 'publications/index.html', 'projects/index.html',
                 'cv/index.html', 'repositories/index.html', '404.html'):
        if not (root / page).is_file():
            errors.append(f'Missing page: {page}')
    pages = list(root.rglob('*.html'))
    for page in pages:
        parser = Links()
        parser.feed(page.read_text(encoding='utf-8'))
        for target in parser.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            dest = root / path.lstrip('/') if path.startswith('/') else page.parent / path
            if dest.is_dir():
                dest = dest / 'index.html'
            if not dest.is_file():
                errors.append(f'{page.relative_to(root)}: missing {target}')
    if errors:
        print('\n'.join(sorted(set(errors))))
        return 1
    print(f'PASS: required pages and local links in {len(pages)} HTML files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
