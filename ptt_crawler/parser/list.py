# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

__all__ = ("parse")

PREV_PAGE_BTN = re.compile(u".*上頁.*", re.UNICODE)


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    url = parse_prev_page_url(soup)

    if url is None:
        return None

    return {
        "prev_page_url": url,
        "article_list": parse_article_list(soup),
    }


def parse_prev_page_url(soup):
    links = soup.select("a.btn.wide")
    url = None

    for link in links:
        match = PREV_PAGE_BTN.match(link.getText())
        if match is not None:
            url = link.get("href")

    return url


def parse_article_list(soup):
    links = soup.select(".r-ent a")
    links = [link.get('href') for link in links]
    return links
