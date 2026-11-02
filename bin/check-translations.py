#!/usr/bin/env python3
"""Verify bilingual navigation and equivalent-page language links after building."""
from html.parser import HTMLParser
from pathlib import Path
import sys


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.lang = None
        self.switch = None
        self.nav = []
        self.in_nav = False
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'nav' and attrs.get('id') == 'navbar':
            self.in_nav = True
        if tag == 'a' and self.in_nav:
            if 'language-switch' in attrs.get('class', '').split():
                self.switch = attrs
            elif attrs.get('href', '').startswith('/'):
                self.nav.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
    for section in ('', 'publications/', 'projects/', 'cv/', 'repositories/'):
        for lang, prefix, other in [('zh-CN', '/', '/en/'), ('en', '/en/', '/')]:
            path = root / (prefix + section).lstrip('/') / 'index.html'
            assert path.is_file(), f'Missing translated page: {path}'
            page = Page(path)
            assert page.lang == lang, f'Incorrect document language: {path}'
            assert page.switch, f'Missing language switch: {path}'
            assert page.switch['href'] == other + section, f'Incorrect counterpart: {path}'
            assert page.switch.get('hreflang') == ('en' if lang == 'zh-CN' else 'zh-CN')
            assert len(page.nav) >= 5, f'Missing navigation: {path}'
            assert all(url.startswith('/en/') == (lang == 'en') for url in page.nav), f'Mixed-language navigation: {path}'
    print('PASS: 10 translated pages, document languages, navigation, and language-switch round trips')


if __name__ == '__main__':
    main()
