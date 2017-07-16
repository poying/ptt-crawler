import time
import asyncio
import logging
import requests
from .exceptions import RequestError, RetryError

logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, verify=False, retry=0, retry_timeout=1):
        self.retry = retry
        self.retry_timeout = retry_timeout
        self.verify = verify
        self.cookies = dict(over18='1')

    async def fetch(self, url):
        res = None
        count = 0
        retry = self.retry
        retry_timeout = self.retry_timeout
        while True:
            res = await asyncio.get_event_loop().run_in_executor(None, self._fetch, url)
            if res is None and retry >= count:
                count = count + 1
                logger.warning(
                    'Retry to fetch %s after %d second(s)', url, retry_timeout)
                await asyncio.sleep(retry_timeout)
            else:
                break
        if res is None:
            raise RetryError('Failed to fetch resource: {}'.format(url), count)
        return res

    def _fetch(self, url):
        logger.info('Fetch resource: %s', url)
        ret = None
        try:
            res = requests.get(url, verify=self.verify, cookies=self.cookies)
        except requests.exceptions.ConnectionError as err:
            pass
        else:
            if res.status_code is 200:
                ret = res.text
            elif not (res.status_code >= 500 and res.status_code < 600):
                logger.warning(
                    'Failed to fetch resources: %s (%s)', url, res.text)
                raise RequestError(
                    'Failed to fetch resource: {}'.format(url), res)
        return ret
