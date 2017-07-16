from .pages import Pages


class Board:
    def __init__(self, name, fetcher):
        self.name = name
        self.fetcher = fetcher

    def pages(self, limit=10):
        return Pages(self.name, self.fetcher, limit=limit)
