import asyncio
from .base import Consumer
from elasticsearch import Elasticsearch


class ElasticsearchConsumer(Consumer):
    def __init__(
            self,
            index='ptt',
            doc_type='article',
            addresses=['127.0.0.1:80'],
            auth=None,
            verify=False,
            *args,
            **kwargs):
        super(ElasticsearchConsumer, self).__init__(*args, **kwargs)
        hosts = map(parse_address, addresses)
        self.es = Elasticsearch(hosts=hosts, auth=auth, verify_certs=verify)
        self.index = index
        self.doc_type = doc_type

    def _index(self, id, data):
        self.es.index(index=self.index,
                      doc_type=self.doc_type, id=id, body=data)

    async def process(self, id, url, data):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._index, id, data)


def parse_address(address):
    parts = address.split(':', 1)
    host, port = parts[0], parts[1:]
    return {'host': host, 'port': port}
