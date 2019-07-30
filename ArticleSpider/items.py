# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose , TakeFirst,Join
from scrapy.loader import ItemLoader
from ArticleSpider.tools.mysql_scrapy import JobboleConnectMysql
import datetime
import re
from ArticleSpider.models.es_type import *
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
import redis
redis_cli = redis.StrictRedis()

es = connections.create_connection(hosts=["localhost"])

def gen_suggests(index,info_tuple):
    used_word = set()
    suggests = []
    for text,weight in info_tuple:
        if text:
            words = es.indices.analyze(index=index,body = {"text":text,"analyzer":"ik_max_word"})
            analyzed_words = set([r['token']for r in words['tokens'] if len(r['token'])>=2])
            new_words = analyzed_words - used_word
        else:
            new_words =set()
        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})

    return suggests

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobbloeFunction:
    #得到数值后函数处理
    def alter_title(value):
        return value + "Jobbloe"

    def date_convert(value):
        create_date = value.strip().replace("·", "").strip()
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        return create_date

    def get_num(value):
        match_re = re.match(".*?(\d+).*", value)
        if match_re:
            num = (int)(match_re.group(1))
        else:
            num = 0
        return num

    def remove_comment_tags(value):
        if "评论" in value:
            return None
        else :
            return value

    def return_value(value):
        return value

#自定义ItemLoader
class ItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


#input_processor是在收集数据的过程中所做的处理，output_processor是数据yield之后进行的处理
class JobboleItem(scrapy.Item):

    title = scrapy.Field()
    # title = scrapy.Field(
    #     input_processor = MapCompose(JobbloeFunction.alter_title)
    # )

    create_date = scrapy.Field(
        input_processor = MapCompose(JobbloeFunction.date_convert)
    )
    url = scrapy.Field()
    url_id = scrapy.Field()
    image_url = scrapy.Field(
        output_processor=MapCompose(JobbloeFunction.return_value)
    )
    image_path = scrapy.Field()
    vote_num = scrapy.Field(
        input_processor=MapCompose(JobbloeFunction.get_num)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(JobbloeFunction.get_num)
    )
    book_num = scrapy.Field(
        input_processor=MapCompose(JobbloeFunction.get_num)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(JobbloeFunction.remove_comment_tags),
        output_processor=Join(",")
    )
# 写入数据库
#     def get_insert_sql(self,cursor,conn):
#         JobboleConnectMysql()
#         insert_sql = """
#                     INSERT INTO Jobbole(title,create_date,url,url_id,image_url,
#                     image_path,vote_num,comment_num,book_num,content,tags)
#                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 """
#         cursor.execute(insert_sql,
#                             (self['title'], self['create_date'], self['url'], self['url_id'], self['image_url'],
#                              self['image_path'], self['vote_num'], self['comment_num'],
#                              self['book_num'], self['content'], self['tags']))
#         conn.commit()

    def save_into_es(self):
        article = JobboleArticleType()
        article.title = self['title']
        article.create_date = self['create_date']
        article.content = remove_tags(self['content'])
        article.url = self['url']
        if 'image_url' in self:
            article.image_url = self['image_url']
        article.vote_num = self['vote_num']
        article.comment_num = self['comment_num']
        article.tags = self['tags']
        article.meta.id = self['url_id']

        article.suggest = gen_suggests(index = JobboleArticleType._get_index(article),info_tuple=((article.title,10),(article.tags,5)))
        article.save()
        redis_cli.incr("jobbole_count")


class PPTItem(scrapy.Item):

    title = scrapy.Field()
    ppt_url = scrapy.Field()
    image_url = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()

    def save_into_es(self):
        ppt = PPTType()

        ppt.tags = self['tags']
        ppt.title = self['title']
        ppt.image_url = self['image_url']
        ppt.content = self['content']
        ppt.ppt_url = self['ppt_url']
        ppt.suggest = gen_suggests(index=PPTType._get_index(ppt),
                                       info_tuple=((ppt.title, 10), (ppt.tags, 5),(ppt.content,3)))
        ppt.save()
        redis_cli.incr("1ppt_count")


class BaotuVideoItem(scrapy.Item):
    video_name = scrapy.Field()
    video_url = scrapy.Field()
    image_url = scrapy.Field()

    def save_into_es(self):
        video=BaotuVideoType()
        video.image_url=self['image_url']
        video.video_url=self['video_url']
        video.video_name=self['video_name']
        video.suggest = gen_suggests(index=BaotuVideoType._get_index(video),
                                       info_tuple=((video.video_name, 10),))
        video.save()
        redis_cli.incr("baotu_count")


class MeiJuTTItem(scrapy.Item):
    tv_name = scrapy.Field()
    tv_url = scrapy.Field()
    image_url = scrapy.Field()
    tags=scrapy.Field()
    abstract=scrapy.Field()

    def save_into_es(self):
        tv=MeiJuTVType()
        tv.image_url=self['image_url']
        tv.abstract=self['abstract']
        tv.tv_name=self['tv_name']
        tv.tags=self['tags']
        tv.tv_url=self['tv_url']
        tv.suggest = gen_suggests(index=MeiJuTVType._get_index(tv),
                                       info_tuple=((tv.tv_name, 10), (tv.tags, 5)))
        tv.save()
        redis_cli.incr("meijutt_count")


class DygodMovieItem(scrapy.Item):

    movie_name=scrapy.Field()
    translated_name=scrapy.Field()
    movie_url = scrapy.Field()
    image_url = scrapy.Field()
    tags=scrapy.Field()
    abstract=scrapy.Field()

    def save_into_es(self):
        movie=DygodMovieType()
        movie.tags=self['tags']
        movie.abstract=self['abstract']
        movie.image_url=self['image_url']
        movie.movie_url=self['movie_url']
        movie.translated_name=self['translated_name']
        movie.movie_name=self['movie_name']
        movie.suggest = gen_suggests(index=DygodMovieType._get_index(movie),
                                       info_tuple=((movie.movie_name, 10), (movie.tags, 5)))
        movie.save()
        redis_cli.incr("dygod_count")


class MoocItem(scrapy.Item):

    course_name=scrapy.Field()
    course_type=scrapy.Field()
    course_url = scrapy.Field()
    student = scrapy.Field()
    image_url = scrapy.Field()
    introduction=scrapy.Field()
    tags=scrapy.Field()

    def save_into_es(self):
        course=MoocType()
        course.image_url=self['image_url']
        course.tags=self['tags']
        course.student=self['student']
        course.course_name=self['course_name']
        course.course_type=self['course_type']
        course.course_url=self['course_url']
        course.introduction=self['introduction']
        course.suggest = gen_suggests(index=MoocType._get_index(course),
                                       info_tuple=((course.course_name, 10), (course.tags, 5),(course.introduction,3)))
        course.save()
        redis_cli.incr("mooc_count")

# class LagouJobItem(scrapy.Item):
#     company_name = scrapy.Field()
#     job_name=scrapy.Field()
#     salary_min=scrapy.Field()
#     salary = scrapy.Field()
#     experiment_min = scrapy.Field()
#     experiment = scrapy.Field()
#     job_type = scrapy.Field()
#     address = scrapy.Field()
#     education_need = scrapy.Field()
#     job_tags = scrapy.Field()
#     company_url = scrapy.Field()
#     job_url = scrapy.Field()
#     job_describe = scrapy.Field()



class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    comment_num = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 引用
    quote = scrapy.Field()
    # 时间
    year = scrapy.Field()
    # 国家
    country = scrapy.Field()
    # 电影链接
    movie_url = scrapy.Field()
    # 图片链接
    image_url = scrapy.Field()

    def save_into_es(self):
        movie = DoubanMovieType()
        movie.movie_name = self['movie_name']
        movie.ranking = self['ranking']
        movie.score=self['score']
        movie.tags = self['tags']
        movie.comment_num=self['comment_num']
        movie.image_url=self['image_url']
        movie.movie_url=self['movie_url']
        movie.quote=self['quote']
        movie.country=self['country']
        movie.year=self['year']
        index = DoubanMovieType._get_index(movie)
        movie.suggest = gen_suggests(index=DoubanMovieType._get_index(movie),
                                       info_tuple=((movie.movie_name, 10), (movie.tags, 5),(movie.quote,5)))
        movie.save()
        redis_cli.incr("douban_count")

class UnsplashImageItem(scrapy.Item):
    # 保存图片id
    image_name = scrapy.Field()
    # 保存图片下载地址
    image_url = scrapy.Field()

    def save_into_es(self):
        image = UnsplashImageType()
        image.image_url = self['image_url']
        image.image_name = self['image_name']
        image.suggest = gen_suggests(index=UnsplashImageType._get_index(image),
                                      info_tuple=((image.image_name, 10), ))
        image.save()
        redis_cli.incr("unsplash_count")
