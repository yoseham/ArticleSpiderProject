
from scrapy.cmdline import  execute
import sys
import os

#copy path
#sys.path.append("/home/yang/PycharmProjects/ArticleSpider")
#abspath当前文件路径，dirname文件夹路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","jobbole"])
# execute(["scrapy","crawl","zhihu"])
execute(["scrapy","crawl","1ppt"])
# execute(["scrapy","crawl","douban"])
# execute(["scrapy","crawl","baotu"])
# execute(["scrapy","crawl","meijutt"])
# execute(["scrapy","crawl","dygod"])

# execute(["scrapy","crawl","mooc"])
# execute(["scrapy","crawl","lagou"])
# execute(["scrapy","crawl","unsplash"])