# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AnimePipeline:
    def __init__(self): #连接数据库
        self.connect = pymysql.Connect(host="localhost",user="root",password="5245117",port=3306,db="finalpj")
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            sql = "insert into anime (media_id,name,score,score_num,play,follow,barrage,tags,comments) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            self.cursor.execute(sql % (item['media_id'],item['name'],item['score'],item['score_num'],item['play'],item['follow'],item['barrage'],item['tags'],item['comments']))
            self.connect.commit()
            print(f"{item['name']} 的数据插入成功")
        except Exception as e:
            print(f"{item['name']}插入失败！原因"+str(e))

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()