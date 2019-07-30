# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://www.zhihu.com/topics'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        post_nodes=response.css(".zm-topic-cat-main li a::attr(href)").extract()
        for post in post_nodes:
            yield Request(url=parse.urljoin(response.url,post), callback=self.parse_nodes)

    def parse_nodes(self,response):
        post_nodes=response.css(".zm-topic-cat-sub .item a::attr(href)").extract()
        for post in post_nodes:
            yield Request(url=parse.urljoin(response.url,post), callback=self.parse_detail)

    def parse_detail(self,response):
        post_nodes = response.css(".zm-topic-cat-sub .item a::attr(href)").extract()
        for post in post_nodes:
            yield Request(url=parse.urljoin(response.url,post), callback=self.parse_detail)






