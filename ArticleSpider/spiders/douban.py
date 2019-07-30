import scrapy
from urllib import parse
from scrapy import Request
from ArticleSpider.items import DoubanMovieItem
class DoubanSpider(scrapy.Spider):
    # 配置信息
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    # 爬虫主函数
    def parse(self,response):
        item=DoubanMovieItem()
        movie_nodes=response.css("#wrapper #content li")
        for movie in movie_nodes:
            item['ranking'] = movie.css('.pic em::text').extract()[0]
            movie_name=""
            for name in movie.css('.hd .title::text').extract():
                movie_name+=" "+name.replace('/','').strip()
            item['movie_name'] = movie_name.strip()
            item['score'] = movie.css('.bd .rating_num::text').extract()[0]
            item['comment_num'] = movie.css('.bd .star span::text').re('(\d+)人评价')[0]
            item['quote']=movie.css('.bd .quote .inq::text').extract_first()
            item['year']=movie.css('.bd p::text').extract()[1].strip().split('/')[0].strip()
            item['country']=movie.css('.bd p::text').extract()[1].strip().split('/')[1].strip()
            item['tags']=movie.css('.bd p::text').extract()[1].strip().split('/')[2].strip().split(' ')
            item['image_url']=movie.css('.pic a img::attr(src)').extract()[0]
            item['movie_url']=movie.css('.info .hd a::attr(href)').extract()[0]
            yield item

        next_url = response.css(".paginator .next a::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers)


    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)


