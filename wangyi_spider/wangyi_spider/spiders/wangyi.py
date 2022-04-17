# -*- coding: utf-8 -*-
import re
import scrapy
from selenium import webdriver
from wangyi_spider.items import WangyiSpiderItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['https://news.163.com']
    start_urls = ['https://news.163.com/']

    # 存储四大板块对应详情页的URL
    models_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 实例化一个浏览器对象  主要用于爬取动态加载的内容
        self.browser = webdriver.Chrome(
            executable_path='/Users/wangshiyang/Documents/myself-doc/code/爬虫课件/第八章：scrapy框架/wangyiPro/chromedriver')

    def parse(self, response, **kwargs):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [2, 3]
        for index in alist:
            # 解析获取模块的URL
            model_url = li_list[index].xpath('./a/@href').extract_first()
            type_news = li_list[index].xpath('./a/text()').extract_first()
            self.models_urls.append(model_url)
            # 依次对每一个板块对应的页面进行请求
            for url in self.models_urls:  # 对每一个板块的url进行请求发送
                yield scrapy.Request(url=url,
                                     callback=self.parse_model,
                                     meta={
                                         "type_news": type_news
                                     })

    # 每一个板块对应的新闻标题相关的内容都是动态加载
    def parse_model(self, response):
        # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
        # response.xpath()
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            follow_num = div.xpath('./div/div[3]/a/div/span[1]/text()').extract_first()
            keywords = div.xpath('./div/div[2]/div//text()').extract()
            keywords = str(keywords).replace("\n", "").replace(" ", "").replace("'\\n\\n',", "").replace(",'\\n\\n'",
                                                                                                         "")

            item = WangyiSpiderItem()
            item['type_news'] = response.meta['type_news']
            item['title'] = title
            item['follow_num'] = follow_num
            item['keywords'] = keywords

            # 对新闻详情页的url发起请求
            yield scrapy.Request(url=new_detail_url,
                                 callback=self.parse_detail,
                                 meta={'item': item})

    @staticmethod
    def parse_detail(response):
        # 解析新闻内容
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        content = re.sub('[a-zA-Z’!"#$%&\'()*+-/:;<=>?@★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", content)
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        # 注意打开的浏览器一定要关闭  爬虫结束的时候执行
        self.browser.quit()