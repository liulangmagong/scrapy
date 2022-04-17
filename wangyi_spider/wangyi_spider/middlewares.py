# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.http import HtmlResponse
from time import sleep
from utils import proxys_uas_tool as pua
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class PROXYDownloaderMiddleware(object):
    # 拦截请求
    @staticmethod
    def process_request(request, spider):
        # UA伪装
        request.headers['User-Agent'] = random.choice(pua.user_agent_list)

        # 为了验证代理的操作是否生效  因为请求一致不异常就看不出来效果
        request.meta['proxy'] = 'http://183.146.213.198:80'
        return None

    # 拦截所有的响应
    @staticmethod
    def process_response(request, response, spider):
        return response

    # 拦截发生异常的请求
    @staticmethod
    def process_exception(request, exception, spider):
        if request.url.split(':')[0] == 'http':
            # 代理
            # 这个部分也可以写在拦截请求部分，但是就会导致正常的请求也会被替换，降低效率
            request.meta['proxy'] = 'http://' + random.choice(pua.PROXY_http)
        else:
            request.meta['proxy'] = 'https://' + random.choice(pua.PROXY_https)

        # 将修正之后的请求对象进行重新的请求发送
        return request


class WangyiSpiderDownloaderMiddleware:

    @staticmethod
    def process_request(request, spider):
        # UA伪装
        request.headers['User-Agent'] = random.choice(pua.user_agent_list)
        return None

    @staticmethod
    def process_response(request, response, spider):
        """
            该方法拦截五大板块对应的响应对象，进行篡改
            这个部分的代码逻辑和具体的页面无关，可循环使用
            注意要在settings中开启中间件
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # 获取了在爬虫类中定义的浏览器对象
        browser = spider.browser

        # 挑选出指定的响应对象进行篡改
        # 通过url指定request
        # 通过request指定response
        if request.url in spider.models_urls:
            # 五个板块对应的url进行请求
            # 使用实例化的浏览器对象进行请求
            browser.get(request.url)
            sleep(3)
            page_text = browser.page_source  # 包含了动态加载的新闻数据

            # response
            # 五大板块对应的响应对象
            # 针对定位到的这些response进行篡改
            # 实例化一个新的响应对象（符合需求：包含动态加载出的新闻数据），替代原来旧的响应对象
            # 如何获取动态加载出的新闻数据？
            # 基于selenium便捷的获取动态加载数据
            """
                1、实例化一个浏览器对象，并且加载它的驱动程序（只需要实例化一个即可，所以不能在这个函数中实例化）
                2、在爬虫文件的初始化（构造）方法中进行实例化操作
            """
            new_response = HtmlResponse(url=request.url, body=page_text,
                                        encoding='utf-8', request=request)

            return new_response
        else:
            # response
            # 其他请求对应的响应对象
            return response

    @staticmethod
    def process_exception(request, exception, spider):
        if request.url.split(':')[0] == 'http':
            # 代理
            # 这个部分也可以写在拦截请求部分，但是就会导致正常的请求也会被替换，降低效率
            request.meta['proxy'] = 'http://' + random.choice(pua.PROXY_http)
        else:
            request.meta['proxy'] = 'https://' + random.choice(pua.PROXY_https)

        # 将修正之后的请求对象进行重新的请求发送
        return request

    # 处理日志的方法
    @staticmethod
    def spider_opened(spider):
        spider.logger.info('Spider opened: %s' % spider.name)
