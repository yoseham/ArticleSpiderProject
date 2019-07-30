# # -*- coding: utf-8 -*-
# 拉勾反爬机制太强了，放弃
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.http import Request
# import scrapy
# import re
# from urllib import parse
# from scrapy import Request
# import time
# import datetime
# now = datetime.datetime.now()
# timeStamp = int(now.timestamp()*1000)
# geshi = "%Y%m%d%H%M%S"
# time1 = datetime.datetime.strftime(now,geshi)
# from ArticleSpider.items import LagouJobItem
# # class LagouSpider(CrawlSpider):
# #     name = 'lagou'
# #     allowed_domains = ['www.lagou.com']
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
# #     }
# #     rules = (
# #         Rule(LinkExtractor(allow=r'gongsi/\d+.html'), follow=True),
# #         # Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
# #         # Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
# #     )
# #     def start_requests(self):
# #         url = 'https://www.lagou.com/'
# #         yield Request(url, headers=self.headers)
# #     def parse_job(self, response):
# #         #解析拉勾职位
# #         item = {}
# #         #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
# #         #item['name'] = response.xpath('//div[@id="name"]').get()
# #         #item['description'] = response.xpath('//div[@id="description"]').get()
# #         return item
#
# class LagouSpider(scrapy.Spider):
#     name = 'lagou'
#     allowed_domains = ['www.lagou.com']
#     headers = {"Accept": "application/json",
#                "Accept-Encoding": "gzip, deflate, br",
#                "Accept-Language": "zh-CN,zh;q=0.9",
#                "Connection": "keep-alive",
#                "Host": "www.lagou.com",
#                "Cookie": "_ga=GA1.2.841469794.1541152606; user_trace_token=20181102175657-a2701865-de85-11e8-8368-525400f775ce; LGUID=20181102175657-a2701fbd-de85-11e8-8368-525400f775ce; index_location_city=%E5%B9%BF%E5%B7%9E; _gid=GA1.2.311675459.1542615716; _ga=GA1.3.841469794.1541152606; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542634073,1542634080,1542634122,1542634128; JSESSIONID=ABAAABAAAGCABCC1B87E5C12282CECED77A736D4CD7FA8A; X_HTTP_TOKEN=aae2d9e96d6a68f72d98ab409a933460; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221672c5c65c01c7-0e8e56366a6cce-3a3a5c0e-2073600-1672c5c65c3bf%22%2C%22%24device_id%22%3A%221672c5c65c01c7-0e8e56366a6cce-3a3a5c0e-2073600-1672c5c65c3bf%22%7D; sajssdk_2015_cross_new_user=1; _gat=1; LGSID=20181119231628-167f7db1-ec0e-11e8-a76a-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fm.lagou.com%2Fsearch.html; PRE_LAND=https%3A%2F%2Fm.lagou.com%2Fjobs%2F5219979.html; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6={timeStamp}; LGRID={time}-1c458fde-ec0e-11e8-895f-5254005c3644".format(
#                    timeStamp=timeStamp, time=time1),
#                "Referer": "https://www.lagou.com/zhaopin/",
#                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
#                "X-Requested-With": "XMLHttpRequest", }
#     def start_requests(self):
#         url = 'https://www.lagou.com/zhaopin/'
#         yield Request(url, headers=self.headers)
#     def parse(self,response):
#         #解析拉勾职位
#         job_list = response.css('.item_con_list li .position_link::attr(href)').extract()
#         print(job_list)
#         for job in job_list:
#             yield Request(url= job, callback=self.parse_detail,headers=self.headers)
#
#     def parse_detail(self,response):
#         # item = LagouJobItem()
#         # item['company_name'] = response.css('.fl-cn::text').extract_first()
#         # item['job_name'] = response.css(".job-name::attr(title)").extract_first()
#         # # salary = response.css(".job_request .salary::text").extract_first()
#         # # experiment=response.xpath("//*[@class='job_request']/p/span[3]/text()").extract_first()
#         # # item['salary_min'] = re.compile('.*?(\d+k)').match(str(salary)).groups()[0]
#         # # item['salary'] = salary
#         # # item['experiment_min'] = re.compile('.*?(\d+)').match(str(experiment)).groups()[0]
#         # # item['experiment'] = experiment
#         # item['job_tags'] = response.css('.position-label li::text').extract()
#         # item['job_type'] = response.xpath("//*[@class='job_request']/p/span[5]/text()").extract_first()
#         # item['address'] = response.css(".work_addr").extract_first()
#         # item['education_need'] = response.xpath("//*[@class='job_request']/p/span[4]/text()").extract_first()
#         # item['company_url'] = response.css('#job_company dt a::attr(href)').extract_first()
#         # item['job_url'] = response.url
#         # item['job_describe'] = response.css(".job_bt div").extract_first()
#         time.sleep(3)
#         print(response.text)
#
#         yield item

#导入需要的库
# import requests
# import re
# import json
# SEARCH_ID_HEADERS = """
#         Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
#         Accept-Encoding: gzip, deflate, br
#         Accept-Language: zh-CN,zh;q=0.9
#         Cache-Control: max-age=0
#         Connection: keep-alive
#         Host: [url]www.lagou.com[/url]
#         Referer: [url]https://www.lagou.com/[/url]
#         Upgrade-Insecure-Requests: 1
#         User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
# """
# IMG_HEADERS = """
#         Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
#         Accept-Encoding: gzip, deflate, br
#         Accept-Language: zh-CN,zh;q=0.9
#         Cache-Control: max-age=0
#         Connection: keep-alive
#         Host: a.lagou.com
#         Upgrade-Insecure-Requests: 1
#         User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
# """
# HEADES = """
#         Accept: application/json, text/javascript, */*; q=0.01
#         Accept-Encoding: gzip, deflate, br
#         Accept-Language: zh-CN,zh;q=0.9
#         Connection: keep-alive
#         Content-Length: 26
#         Content-Type: application/x-www-form-urlencoded; charset=UTF-8
#         Host: [url]www.lagou.com[/url]
#         Origin: [url]https://www.lagou.com[/url]
#         Referer: [url]https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=[/url]
#         User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
#         X-Anit-Forge-Code: 0
#         X-Anit-Forge-Token: None
#         X-Requested-With: XMLHttpRequest
# """
# # 把header信息转换成dict
# SEARCH_ID_HEADERS = re.findall('(\S+): (\S+)', SEARCH_ID_HEADERS)
# SEARCH_ID_HEADERS = dict(SEARCH_ID_HEADERS)
# IMG_HEADERS = re.findall('(\S+): (\S+)', IMG_HEADERS)
# IMG_HEADERS = dict(IMG_HEADERS)
# HEADES = re.findall('(\S+): (\S+)', HEADES)
# HEADES = dict(HEADES)
# # 创建一个用来保存cookies地方
# cookie = {}
# # 创建一个session
# session = requests.session()
# # 获取第一个和第二个cookies信息
# img_url_two = "https://a.lagou.com/collect?v=1&_v=j31&a=798985105&t=pageview&_s=1&dl=https%3A%2F%2Fwww.lagou.com%2F&dr=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D&ul=zh-cn&de=UTF-8&dt=%E6%8B%89%E5%8B%BE%E7%BD%91-%E4%B8%93%E4%B8%9A%E7%9A%84%E4%BA%92%E8%81%94%E7%BD%91%E6%8B%9B%E8%81%98%E5%B9%B3%E5%8F%B0_%E6%89%BE%E5%B7%A5%E4%BD%9C_%E6%8B%9B%E8%81%98_%E4%BA%BA%E6%89%8D%E7%BD%91_%E6%B1%82%E8%81%8C&sd=24-bit&sr=1920x1080&vp=846x921&je=0&_u=MEAAAAQBK~&jid=546309307&cid=1391633655.1547948848&tid=UA-41268416-1&_r=1&z=966384896"
# requ = session.get(url=img_url_two, headers=IMG_HEADERS)
# cookie.update({
#     "user_trace_token": requ.cookies["user_trace_token"],
#     "LGRID": requ.cookies["LGRID"],
# })
# # 获取第三个cookies信息
# SEARCH_ID_URL = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
# requ = session.get(url=SEARCH_ID_URL, headers=SEARCH_ID_HEADERS)
# cookie.update({
#     "SEARCH_ID": requ.cookies["SEARCH_ID"],
# })
# for j in range(0, 20):
#     data = {
#         "first": "true",
#         "pn": str(j + 1),
#         "kd": "python",
#     }
#     Ajax_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
#     requ = session.post(url=Ajax_url, headers=HEADES, data=data, cookies=cookie)
#     jsonText = json.loads(requ.content.decode('utf-8'))
#     # 请求回来的是一个json
#     for i in range(0, len(jsonText['content']['positionResult']['result'])):
#         if jsonText["content"] != None:
#             print(jsonText['content']['positionResult']['result'][i]['companyFullName'] + "   ------>>>>>   " +
#                   jsonText['content']['positionResult']['result'][i]['positionName'] + "    ------>>>>>>" +
#                   jsonText['content']['positionResult']['result'][i]['salary'] + "    ------>>>>>>" +
#                   jsonText['content']['positionResult']['result'][i]['formatCreateTime'] + "    ------>>>>>>" +
#                   jsonText['content']['positionResult']['result'][i]['firstType'])
#         else:
#             # 有些地方没有这个content
#             print("json没有content")