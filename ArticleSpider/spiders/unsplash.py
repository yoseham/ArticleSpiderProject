import scrapy, json
from ArticleSpider.items import UnsplashImageItem
import requests

# 翻译函数，word 需要翻译的内容
def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        # 相应失败就返回空
        return None

def get_reuslt(response):
    # 通过 json.loads 把返回的结果加载成 json 格式
    result = json.loads(response)
    return result['translateResult'][0][0]['tgt']


class UnsplashImageSpider(scrapy.Spider):
    # 定义Spider的名称
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    # 定义起始页面
    start_urls = ['https://unsplash.com/napi/photos?page=1&per_page=12']

    def __init__(self):
        self.page_index = 1

    def parse(self, response):

        # 解析服务器响应的JSON字符串
        if response.text:
            photo_list = json.loads(response.text)  # ①
        # 遍历每张图片
        print(photo_list[1])
        for photo in photo_list:

            item = UnsplashImageItem()
            if (photo['description']):
                item['image_name'] = get_reuslt(translate(photo['description']))
            elif(photo['alt_description']):
                item['image_name'] = get_reuslt(translate(photo['alt_description']))
            else:
                item['image_name'] = "无"
            item['image_url'] = photo['links']['download']
            yield item

        if self.page_index<=30:
            self.page_index += 1

            # 获取下一页的链接
            next_link = 'https://unsplash.com/napi/photos?page=' \
                        + str(self.page_index) + '&per_page=12'

            # 继续获取下一页的图片
            yield scrapy.Request(next_link, callback=self.parse)

