# -*- coding: utf-8 -*-

from .article import Article

NO_MORE_DATA_MESSAGE = "No more data!"


class ArticleList:
    def __init__(self, board, autoload):
        self.board = board
        self.autoload = autoload
        self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_article()

    def next(self):
        return self.next_article()

    def next_article(self):
        if self.buffer_is_empty():
            self.next_page()
            if self.at_last_page:
                raise StopIteration

        article_url = self.buffer[self.buffer_cursor]
        self.buffer_cursor += 1

        article = Article(self.board, article_url)
        if self.autoload:
            article.load()

        return article

    def next_page(self):
        if self.at_last_page:
            raise Exception(NO_MORE_DATA_MESSAGE)

        count = 0

        while count == 0:
            try:
                data = self.board.get_data(self.page_url)
            except:
                data = None

            if data is None:
                self.at_last_page = True
                self.buffer = None
                self.buffer_cursor = 0
                self.buffer_lastindex = -1
                return

            count = len(data["article_list"])
            page_url = data["prev_page_url"]

        self.buffer_cursor = 0
        self.buffer = data["article_list"]
        self.buffer_lastindex = count - 1
        self.page_url = page_url

    def buffer_is_empty(self):
        return self.buffer_cursor > self.buffer_lastindex

    def reset(self):
        self.page_url = "/index.html"
        self.at_last_page = False
        self.buffer = None
        self.buffer_cursor = 0
        self.buffer_lastindex = -1
