# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleItem ,ItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first()
            image_url = post_node.css("img::attr(src)").extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image":parse.urljoin(response.url,image_url)},callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)

    def parse_detail(self,response):
        # article_item = JobboleItem()
        # item_loader = ItemLoader(item=JobboleItem(), response=response)
        # # extract_first()更好
        # image_url = response.meta.get("front_image","")
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        # # response.css(".entry-header h1::text").extract()[0]
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·", "").strip()
        # # response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace('','').strip()
        # vote_num = (int)(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        # # response.css(".vote-post-up h10::text").extract()[0]
        # book_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # # response.css(".bookmark-btn::text").extract()[0]
        # comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # #response.css("a[href='#article-comment'] span::text").extract()[0]
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # # response.css(".entry").extract()[0]
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # # response.css(".entry-meta-hide-on-mobile a::text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        #
        # # article_item["title"] = title
        # # article_item["url"] = response.url
        # # article_item["url_id"] = get_md5(response.url)
        # # article_item["create_date"] = create_date
        # # article_item["image_url"] =[image_url]
        # # article_item["vote_num"] = vote_num
        # # article_item["book_num"] = vote_num
        # # article_item["comment_num"] = comment_num
        # # article_item["content"] = content
        # # article_item["tags"] = tags

        #itemLoader机制
        image_url = response.meta.get("front_image", "")
        item_loader = ItemLoader(item=JobboleItem(), response=response)
        item_loader.add_value('image_url',[image_url])
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_id',get_md5(response.url))
        item_loader.add_css('title','.entry-header h1::text')
        item_loader.add_css('create_date','.entry-meta-hide-on-mobile::text')
        item_loader.add_css('vote_num', '.vote-post-up h10::text')
        item_loader.add_css('book_num', '.bookmark-btn::text')
        item_loader.add_css('comment_num', "a[href='#article-comment'] span::text")
        item_loader.add_css('content', '.entry')
        item_loader.add_css('tags','.entry-meta-hide-on-mobile a::text' )

        article_item = item_loader.load_item()

        yield article_item
