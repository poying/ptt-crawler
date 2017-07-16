ptt-crawler
===========

## 環境要求

* Python 版本 >= `3.5`
* nsqd service

## 安裝

```bash
$ pip install git+https://github.com/poying/ptt-crawler.git
```

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

consumer = CustomConsumer()
consumer.run()
```

## 開發

1. 取得程式碼 `$ git clone git@github.com:poying/ptt-crawler.git`
2. 切換目錄 `$ cd ptt-crawler`
3. 建立乾淨的執行環境 `$ virtualenv --python=$(which python) .env`
4. 進入執行環境 `$ source .env/bin/activate`
5. 安裝相依套件 `$ pip install -r requirements.dev.txt`
6. 在新的 branch 修改程式碼 `$ git checkout -b <branch_name>`
7. ...寫扣 寫扣 寫扣...
8. 整理程式碼風格 `$ make format`
9. commit、push、發 PR

## License

MIT: https://poying.mit-license.org/
