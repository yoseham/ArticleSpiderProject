# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import pymysql


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


#系统调用
class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


#自定义json保存
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()


#同步机制
class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect('localhost','root','07597321','ArticleSpider',charset="utf8mb4",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        item.get_insert_sql(conn = self.conn,cursor = self.cursor)
        return item


#图片下载
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "image_url" in item:
            for ok,value in results:
                image_file_path = value['path']
            item["image_path"] = image_file_path
            return item


class ArticleVideoPipeline(MediaPipeline):
    def item_completed(self, results, item, info):
        if 'video_url' in item:
            for ok,value in results:
                video_file_path = value['path']
            item['video_path'] = video_file_path
            return item


class ElasticsearchPipeline(object):
    def process_item(self, item, spider):
        item.save_into_es()
        return item


