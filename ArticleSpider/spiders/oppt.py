import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import PPTItem
class PPTSpider(scrapy.Spider):
    name = '1ppt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    page_num=0
    max_page_num=20

    def start_requests(self):
        url = 'http://www.1ppt.com/moban/'
        yield Request(url, headers=self.headers)


    def parse(self, response):
        self.page_num= self.page_num +1

        pre_url = "http://www.1ppt.com/"
        post_urls = response.css(".tplist li")
        for post in post_urls:
            post_url=parse.urljoin(pre_url,post.css("a::attr(href)").extract()[0])
            yield Request(url=post_url,callback=self.parse_detail)
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()

        if next_url and self.page_num<=self.max_page_num:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)


    def parse_detail(self,response):

        item=PPTItem()

        item['tags'] = response.xpath('//li[text()="标签："]/a/text()').extract()
        item['content'] =response.css('.content p::text').extract()[-3]
        item['image_url']=response.css('.content p img::attr(src)').extract()[0]
        item['ppt_url']=response.url
        item['title']=response.css('.ppt_info h1::text').extract()[0]


        yield item