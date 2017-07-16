# -*- coding: utf-8 -*-
# flake8: noqa

import re
from .list import parse as parse_list
from .exceptions import ParserNotFoundError
from .article import parse as parse_article

ARTICLE_RE = re.compile('\/bbs\/[-_\w]+\/(?:\w+\.){4}html$')
LIST_RE = re.compile('\/index\d*\.html$')


def parse(url, html):
    parse = get_parser(url)
    if parse is None:
        raise ParserNotFoundError('Can\'t find parser for resource: ' + url)
    return parse(html)


def get_parser(url):
    return article_page(url) \
        or list_page(url)


def article_page(url):
    if ARTICLE_RE.search(url):
        return parse_article


def list_page(url):
    if LIST_RE.search(url):
        return parse_list
