from .fetcher import Fetcher


class Producer:
    def __init__(self, board, writer, topic='ptt_crawler'):
        self.topic = topic
        self.board = board
        self.writer = writer

    async def run(self, limit=10):
        pages = self.board.pages(limit=limit)
        try:
            async for page in pages:
                for link in page:
                    self.writer.pub(self.topic, str.encode(link))
        finally:
            del pages
