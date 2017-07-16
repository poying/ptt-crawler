import logging
import ptt_crawler
from ptt_crawler.consumer import ElasticsearchConsumer

logger = logging.getLogger(ptt_crawler.__name__)
logger.setLevel(logging.INFO)

consumer = ElasticsearchConsumer(channel='ptt_indexer')

consumer.run()
