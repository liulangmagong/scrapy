# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class WangyiSpiderPipeline:
    fp = None

    def open_spider(self, spider):
        """
        重写父类的一个方法：该方法只在开始爬虫的时候被调用一次
        :param spider:
        :return:
        """
        print('开始爬虫......')
        self.fp = open('/Users/wangshiyang/yuewen/python/project/scrapy/wangyi_spider/wangyi.txt', 'w',
                       encoding='utf-8')

    def process_item(self, item, spider):
        """
            专门用来处理item类型对象
            该方法可以接收爬虫文件提交过来的item对象
            该方法每接收到一个item就会被调用一次
        :param item:
        :param spider:
        :return:
        """
        title = item['title']
        type_news = item['type_news']
        follow_num = item['follow_num']
        keywords = item['keywords']
        content = item['content']

        self.fp.write(
            title + ':' + '(新闻类型：' + type_news + ' ' + '跟帖数量：' + follow_num + ' ' + '标签：' + keywords + ')' + ' ' + content + '\r\n')

        # 就会传递给下一个即将被执行的管道类
        return item

    def close_spider(self, spider):
        print('结束爬虫！')
        self.fp.close()


class mysqlPileLine(object):
    """
        管道文件中一个管道类对应将一组数据存储到一个平台或者载体中
        自定义的管道类一定是要模拟自动生成的类
        注意要现在 mysql 数据库中创建好对应的表
    """
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306,
                                    user='root', password='Asd19941215',
                                    db='scrapy',  # 要使用的数据库  下边sql语句中指定表
                                    charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(
                'insert into wangyi values("%s","%s","%d","%s","%s")' % (
                    item["title"], item["type_news"], int(item["follow_num"]), item["keywords"], item["content"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

# 爬虫文件提交的item类型的对象最终会提交给哪一个管道类？
# 先执行的管道类
