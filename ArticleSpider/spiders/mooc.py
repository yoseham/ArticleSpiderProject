import scrapy
from ArticleSpider.items import MoocItem
from urllib import parse
from scrapy import Request

class MoocSpider(scrapy.Spider):
    name = 'mooc'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    page_num = 0
    max_page_num = 20

    def parse(self, response):
        item = MoocItem()
        self.page_num = self.page_num + 1
        course_nodes = response.css('.course-list .course-card-container')
        for course in course_nodes:
            item['course_name'] = course.css('.course-card-name::text').extract()[0]
            item['course_type'] = course.css('.course-card-info span::text').extract()[0]
            item['course_url'] = parse.urljoin(response.url,course.css('.course-card::attr(href)').extract()[0])
            item['student'] = course.css('.course-card-info span::text').extract()[1]
            item['image_url'] = parse.urljoin(response.url,course.css('.course-banner::attr(data-original)').extract()[0])
            item['introduction'] = course.css('.course-card-desc::text').extract()[0]
            item['tags']=course.css('.course-label label::text').extract()
            yield item
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url and self.page_num<=self.max_page_num:
            yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers)


    def start_requests(self):
        url = 'https://www.imooc.com/course/list'
        yield Request(url, headers=self.headers)