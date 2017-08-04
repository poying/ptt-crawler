import sys
import nsq
import time
import asyncio
import logging
import tornado
import ptt_crawler
from .page import Page
from .pages import Pages
from .board import Board
from .fetcher import Fetcher
from .producer import Producer

__all__ = ['Page', 'Pages', 'Board', 'Fetcher', 'crawl']
logger = logging.getLogger(ptt_crawler.__name__)


def crawl(board, page_limit=10, retry=10, retry_timeout=1, topic='ptt_crawler', nsqd='127.0.0.1:4150', verbose=False):
    '''
    options:
        --page-limit=<int>
        --retry=<int>
        --retry-timeout=<float>
        --topic=<str>
        --nsqd=<str>
        -v, --verbose
    '''
    if verbose:
        setup_logger()

    tornado.platform.asyncio.AsyncIOMainLoop().install()
    fetcher = Fetcher(retry=retry, retry_timeout=retry_timeout)
    board = Board(board, fetcher)
    writer = nsq.Writer(nsqd.split(','))
    producer = Producer(board, writer, topic)
    time.sleep(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(producer.run(limit=page_limit))


def setup_logger():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
