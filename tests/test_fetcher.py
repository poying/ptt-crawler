import sure
import requests
import asynctest
from unittest import mock
from tornado.testing import gen_test
from ptt_crawler.fetcher import Fetcher
from tornado.testing import AsyncTestCase
from ptt_crawler.fetcher.exceptions import RetryError


class FetcherTest(asynctest.case.TestCase):
    async def test_fetch(self):
        fetcher = Fetcher()
        mock_res = mock.MagicMock(text='lol', status_code=200)
        with mock.patch.object(requests, 'get', return_value=mock_res) as mock_fetch:
            res = await fetcher.fetch('http://google.com')
            res.should.equal('lol')

    async def test_fetch_retry(self):
        fetcher = Fetcher(retry=1, retry_timeout=0)
        count = [0]
        returns = [
            mock.MagicMock(text='wtf', status_code=500),
            mock.MagicMock(text='lol', status_code=200)
        ]
        def mock_get(url, verify=False, cookies=None):
            ret = returns[count[0]]
            count[0] = count[0] + 1
            return ret
        with mock.patch.object(requests, 'get', mock_get):
            res = await fetcher.fetch('http://google.com')
            (count[0]).should.equal(2)
            res.should.equal('lol')

    async def test_fetch_retry_too_many_times(self):
        fetcher = Fetcher(retry=0, retry_timeout=0)
        def mock_get(url, verify=False, cookies=None):
            return mock.MagicMock(text='wtf', status_code=500)
        with mock.patch.object(requests, 'get', mock_get):
            try:
                res = await fetcher.fetch('http://google.com')
            except RetryError as err:
                (err.retry_count).should.equal(1)
            else:
                raise Exception('WTF')
