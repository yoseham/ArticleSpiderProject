# import scrapy
# from urllib import parse
# from scrapy import Request
# from ArticleSpider.items import BaotuVideoItem
# import time
# from selenium import webdriver
#
# browser = webdriver.PhantomJS()
# # class BaotuSpider(scrapy.Spider):
# #     name = 'oschina'
# #     headers={
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
# #     }
# #
# #     def parse(self,response):
# #
# #
# #     def start_requests(self):
# #         url = 'https://www.oschina.net/blog'
# #         yield Request(url, headers=self.headers)
# #
# headers={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
#     }
# browser.get("https://www.oschina.net/blog")
# # for i in range(10):
#     # browser.execute_script(
#     #     "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
# print(browser.page_source)
#     # time.sleep(4)
#
#
