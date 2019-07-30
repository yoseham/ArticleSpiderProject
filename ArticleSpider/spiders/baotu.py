import scrapy
from urllib import parse
from scrapy import Request
from  ArticleSpider.items import BaotuVideoItem
class BaotuSpider(scrapy.Spider):
    name = 'baotu'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    page_num = 0
    max_page_num = 20

    def parse(self,response):
        self.page_num=self.page_num+1
        item=BaotuVideoItem()
        video_nodes = response.css(".media-list .content-index")
        for video in video_nodes:
            item['video_url']='http:'+video.css('.video-play video::attr(src)').extract()[0]
            item['image_url'] = 'http:'+video.css('.video-play video::attr(imgurl)').extract()[0]
            item['video_name']=video.css('.show-image img::attr(alt)').extract()[0]
            yield item
        next_url = response.css(".pagelist .next::attr(href)").extract_first()
        if next_url and self.page_num<=self.max_page_num:
            yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers)


    def start_requests(self):
        url = 'https://ibaotu.com/shipin/7-0-0-0-0-1.html'
        yield Request(url, headers=self.headers)


