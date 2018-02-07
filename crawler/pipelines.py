# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")


class CrawlerPipeline(object):
    def __init__(self):
        # 在初始化方法中打开文件
        self.fileName = open("tencent.json", "wb")

    def process_item(self, item, spider):
        while (item['title'] != '空'):
            # 把数据转换为字典再转换成json
            text = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # 写到文件中编码设置为utf-8
            self.fileName.write(text.encode("utf-8"))

            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = "insert jianshu(title,name,href,type,time) values ('" + item['title'] + "','" \
                  + item['name'] + "','" + item['href'] + "','" + item['type'] + "','" + item['time'] + "')"

            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()

            # 返回item
            return item

    def close_spider(self, spider):
        # 关闭数据库连接
        db.close()
        # 关闭时关闭文件
        self.fileName.close()
