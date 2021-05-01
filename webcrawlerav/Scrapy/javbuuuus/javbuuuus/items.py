# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 编号
    code = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 码
    censored = scrapy.Field()
    # 演员,多个
    stars = scrapy.Field()
    # 发行时间
    release_date = scrapy.Field()
    # 持续时间
    duration = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 制作商
    studio = scrapy.Field()
    # 发行商
    label = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 封面
    cover = scrapy.Field()
    # 预览图
    previews = scrapy.Field()
    # 系列
    series = scrapy.Field()
    # 磁链
    magnets = scrapy.Field()

class SehuatangItem(scrapy.Item):

    avid = scrapy.Field()
    title = scrapy.Field()
    magnets = scrapy.Field()
    avurl = scrapy.Field()
    magnetuploadtime = scrapy.Field()
    detail = scrapy.Field()
    coverimage = scrapy.Field()
