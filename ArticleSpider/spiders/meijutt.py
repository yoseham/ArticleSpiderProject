import scrapy
from scrapy.http import Request
from ArticleSpider.items import MeiJuTTItem
from urllib import parse
class MeijuTTSpider(scrapy.Spider):
    name = 'meijutt'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }


    def parse(self, response):
        pre_url='https://www.meijutt.com'
        post_urls = response.css(".top-list li h5 a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url),callback=self.parse_detail)

    def parse_detail(self,response):
        item = MeiJuTTItem()
        item['tv_name']=response.css('.info-title h1::text').extract()[0]
        item['tv_url']=response.url
        item['image_url']=response.css('.o_big_img_bg_b img::attr(src)').extract()[0]
        item['tags']=response.css('li[style="position:static"] label a::text').extract()[0]
        item['abstract']="".join([x.strip() for x in response.css('.des_box .des::text').extract()])
        yield item


    def start_requests(self):
        url = 'https://www.meijutt.com/new100.html'
        yield Request(url, headers=self.headers)
