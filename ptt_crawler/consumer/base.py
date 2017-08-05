import re
import nsq
import asyncio
import logging
import tornado
import multiprocessing
from ptt_crawler.parser import parse
from ptt_crawler.fetcher import Fetcher
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
PARSE_ID = re.compile('((?:\w+\.){3}\w+)')


class Consumer(metaclass=ABCMeta):
    def __init__(
            self,
            fetcher=Fetcher(),
            workers=multiprocessing.cpu_count() * 2,
            nsqd=[],
            nsqlookupd=[],
            retry=10,
            retry_timeout=60,
            topic='ptt_crawler',
            channel='ptt_crawler'):
        self.topic = topic
        self.retry_timeout = retry_timeout
        self.fetcher = fetcher
        self.nsqd = nsqd
        self.nsqlookupd = nsqlookupd
        self.workers = workers
        self.channel = channel

    @abstractmethod
    async def process(self, id, url, data):
        pass

    async def _process(self, message):
        url = message.body.decode()
        logger.info('process %s', url)
        try:
            res = await self.fetcher.fetch(url)
            match = PARSE_ID.search(url)
            id = match and match.group(1)
            data = parse(res)
            if id is None or data is None:
                raise Exception('Failed to parse the article: {}'.format(res))
            self.process(id, url, data)
            message.finish()
        except Exception as err:
            logger.warning('%s. Retry to process %s after %f second(s)',
                           err, url, self.retry_timeout)
            message.requeue(delay=self.retry_timeout)

    def _handle(self, message):
        message.enable_async()
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(asyncio.async, self._process(message))

    def run(self):
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        nsq.Reader(
            message_handler=self._handle,
            nsqd_tcp_addresses=self.nsqd,
            lookupd_http_addresses=self.nsqlookupd,
            topic=self.topic,
            channel=self.channel,
            max_in_flight=self.workers)
        executor = ThreadPoolExecutor(max_workers=self.workers)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(executor)
        loop.run_forever()
