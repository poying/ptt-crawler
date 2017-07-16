ptt-crawler
===========

## 環境要求

* Python 版本 >= `3.5`
* nsqd service

## Quick start

1. 爬文章列表並將 URL 存進 NSQ

```bash
$ ptt beauty --page-limit=10
```

2. 從 NSQ 取得文章 URL，爬文章內容並存進 Elasticsearch

```bash
$ python example/elasticsearch_consumer.py
```

## 建立 Consumer Class

目前 `ptt_crawler` 只有 `ElasticsearchConsumer`，如果要將文章放到其他 database 或是做其他事情，必須建立 `Consumer` 子類別。

```python
from ptt_crawler.consumer import Consumer

class CustomConsumer(Consumer):
    async def process(self, id, url, data):
        # custom logic
        pass
```
