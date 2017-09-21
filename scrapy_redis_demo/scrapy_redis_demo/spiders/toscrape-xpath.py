# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
#from scrapy_redis_demo.scrapy_redis.spiders import RedisCrawlSpider


# [Diff] inherited by RedisCrawlSpider
class ToScrapeSpiderXPath(RedisCrawlSpider):
    """ This class is copy from https://github.com/scrapy/quotesbot/blob/master/quotesbot/spiders/toscrape-xpath.py
    """
    
    name = 'scrapy_redis_demo'
    # [Diff] Waiting redis lpush start_urls
    redis_key = '{0}:start_urls'.format(name)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
