# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 新闻标题
    title = scrapy.Field()
    # 新闻类型
    type_news = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # 跟帖数量
    follow_num = scrapy.Field()
    # 新闻标签
    keywords = scrapy.Field()

