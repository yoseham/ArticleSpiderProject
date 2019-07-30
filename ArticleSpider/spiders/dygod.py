import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import DygodMovieItem
class DygodMoviesSpider(scrapy.Spider):
    name = 'dygod'
    allowed_domains = ['dygod.net']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    page_num = 0
    max_page_num = 20

    def parse(self, response):
        self.page_num = self.page_num + 1
        pre_url='https://www.dygod.net'
        post_urls = response.css(".co_content8 table.tbspan a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(pre_url, post_url),callback=self.parse_detail)

        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url and self.page_num<=self.max_page_num:
            yield Request(url=parse.urljoin(pre_url, next_url), callback=self.parse)


    def parse_detail(self,response):
        item=DygodMovieItem()
        content=[x.replace('\u3000','').replace('◎','').strip() for x in response.xpath("//div[@id='Zoom']/p/text()").extract()]
        item['translated_name'] = content[1].replace("片名","").replace("译名","").replace(
            '/','') if content[1].find("名")!=-1 else ""
        item['movie_name'] = content[2].replace("片名","").replace("译名","").replace(
            '/','') if content[2].find("名")!=-1 else ""
        item['movie_url'] = response.url
        item['image_url'] = response.css(".co_content8 #Zoom p img::attr(src)").extract()[0]
        item['tags'] = [x.strip() for x in content[5].replace("类别","").split("/")]
        item['abstract'] = content[content.index("简介")+1]
        yield item


    def start_requests(self):
        url = 'https://www.dygod.net/html/gndy/jddy/index.html'
        yield Request(url, headers=self.headers)