import re
import requests
from .routes import routes

BASE_URL = "https://www.ptt.cc"
OVER18_URL = "https://www.ptt.cc/ask/over18?from={from_url}"
URL_FORMAT = "/bbs/{board}/index.html"
REQUEST_FAILED_MESSAGE = "HTTP request failed! {url}"
NO_MORE_DATA_MESSAGE = "No more data!"
UNKNOWN_PAGE_MESSAGE = "Unknown page {url}"
OVER18_RE = re.compile("over18-notice")


class PttBoard:
    def __init__(self, name):
        self.name = name
        self.cookies = {}
        self.page_url = URL_FORMAT.format(board=name)
        self.at_last_page = False
        self.buffer = None
        self.buffer_cursor = 0
        self.buffer_lastindex = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_article()

    def next_article(self):
        if self.buffer_is_empty():
            self.next_page()
            if self.at_last_page:
                raise StopIteration

        article = self.buffer[self.buffer_cursor]
        self.buffer_cursor += 1

        return article

    def next_page(self):
        if self.at_last_page:
            raise Exception(NO_MORE_DATA_MESSAGE)

        data = self.get_data(self.page_url)

        if data is None:
            self.at_last_page = True
            self.buffer = None
            self.buffer_cursor = 0
            self.buffer_lastindex = -1
            return

        self.buffer_cursor = 0
        self.buffer = data["article_list"]
        self.buffer_lastindex = len(data["article_list"]) - 1
        self.page_url = data["prev_page_url"]

    def buffer_is_empty(self):
        return self.buffer_cursor >= self.buffer_lastindex

    def get_data(self, url):
        parse = routes(url)
        r = requests.get(BASE_URL + url, cookies=self.cookies)

        if self.is_over18_page(r.text):
            self.over18(url)
            return self.get_data(url)

        if parse is None:
            raise Exception(UNKNOWN_PAGE_MESSAGE.format(url=url))

        if r.status_code is not 200:
            raise Exception(REQUEST_FAILED_MESSAGE.format(url=url))

        return parse(r.text)

    def is_over18_page(self, body):
        return OVER18_RE.search(body)

    def over18(self, from_url):
        data = {"yes": "yes"}
        r = requests.post(OVER18_URL.format(from_url=from_url),
                          data=data, cookies=self.cookies)
        self.cookies = r.cookies
