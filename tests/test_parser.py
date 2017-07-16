import os
import sure
from unittest import TestCase
from ptt_crawler.parser import parse
from ptt_crawler.parser.exceptions import ParserNotFoundError


class ParserTest(TestCase):
    def test_article_parser(self):
        filepath = os.path.join(os.path.dirname(__file__), './fixtures/article.html')
        with open(filepath) as html:
            article = parse('https://www.ptt.cc/bbs/Beauty/M.1499790734.A.833.html', html)
            article.get('meta', {}).should.equal({
                'author': 'TyuzuChou (子瑜我老婆)',
                'board': 'Beauty',
                're': False,
                'time': 'Wed Jul 12 00:32:12 2017',
                'title': '橋本環奈',
                'type': '正妹'
            })
            article.get('content').should.be.a(str)
            article.get('comments').should.be.a(list)

    def test_list_parser(self):
        filepath = os.path.join(os.path.dirname(__file__), './fixtures/list.html')
        with open(filepath) as html:
            listPage = parse('https://www.ptt.cc/bbs/Beauty/index2219.html', html)
            listPage.get('prev_page_url').should.equal('/bbs/Beauty/index2218.html')
            listPage.get('article_list').should.be.a(list)

    def test_parser_not_found(self):
        parse.when.called_with('wtf', '囧rz').should.throw(ParserNotFoundError)
