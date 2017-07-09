# -*- coding: utf-8 -*-

import re
import time
import requests
from .parser import routes
from .article import Article
from .article_list import ArticleList

BASE_URL = "https://www.ptt.cc"
URL_FORMAT = "/bbs/{board}{path}"
REQUEST_FAILED_MESSAGE = "HTTP request failed! status: {status}, url: {url}"
UNKNOWN_PAGE_MESSAGE = "Unknown page {url}"
IS_URL = re.compile("^https?:\/\/")
PATH_WITH_BOARD_NAME = re.compile("^\/bbs\/(?:.+)\/")


class Board:
    def __init__(self, name="undefined", verify=True, max_attempts=0, attempt_delay=2):
        self.name = name
        self.verify = verify
        self.max_attempts = max_attempts
        self.attempt_delay = attempt_delay
        self.cookies = dict(over18="1")

    def articles(self, autoload=False):
        return ArticleList(self, autoload)

    def article(self, url):
        return Article(self, url)

    def get_data(self, url):
        url = self.get_url(url)
        parse = routes(url)
        if parse is None:
            raise Exception(UNKNOWN_PAGE_MESSAGE.format(url=url))
        attempts = 0

        while attempts <= self.max_attempts:
            try:
                r = requests.get(url, verify=self.verify, cookies=self.cookies)
            except requests.exceptions.ConnectionError:
                attempts = attempts + 1
                time.sleep(self.attempt_delay)
                continue

            if r.status_code >= 500 and r.status_code < 600:
                attempts = attempts + 1
                time.sleep(self.attempt_delay)
                continue

            if r.status_code is not 200:
                msg = REQUEST_FAILED_MESSAGE.format(url=url, status=r.status_code)
                raise Exception(msg)

            break

        return parse(r.text)

    def get_url(self, path):
        if IS_URL.search(path):
            return path

        if not PATH_WITH_BOARD_NAME.search(path):
            path = URL_FORMAT.format(board=self.name, path=path)

        return BASE_URL + path
