import sys
import logging
import ptt_crawler
from ptt_crawler.consumer import ElasticsearchConsumer

logger = logging.getLogger(ptt_crawler.__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

consumer = ElasticsearchConsumer(channel='ptt_indexer')

consumer.run()
