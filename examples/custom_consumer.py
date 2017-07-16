import logging
import ptt_crawler
from ptt_crawler.consumer import Consumer

logger = logging.getLogger(ptt_crawler.__name__)
logger.setLevel(logging.INFO)

class CustomConsumer(Consumer):
    async def process(self, id, url, data):
        # do somthing
        pass

consumer = CustomConsumer()
consumer.run()
