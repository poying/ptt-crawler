from .page import Page
from .parser import parse


class Pages:
    def __init__(self, board, fetcher, limit=10):
        self.board = board
        self.fetcher = fetcher
        self.limit = limit
        self.page = 0
        self.at_last_page = False
        self.prev_page_url = 'https://www.ptt.cc/bbs/{}/index.html'.format(self.board)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        page = await self.next_page()
        if page is None:
            raise StopAsyncIteration
        return page

    async def next_page(self):
        if self.page >= self.limit or self.prev_page_url is None:
            return None
        url = self.prev_page_url
        res = await self.fetcher.fetch(url)
        data = parse(url, res)
        self.page = self.page + 1
        self.prev_page_url = 'https://www.ptt.cc{}'.format(data.get('prev_page_url', None))
        links = map(lambda path: 'https://www.ptt.cc{}'.format(path), data.get('article_list', []))
        return Page(url, links=links)
