# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
from datetime import datetime


class AnimePipeline:
    def __init__(self): #连接数据库
        try:
            self.connect = pymysql.connect(
                host="localhost", user="root", password="5245117",
                port=3306, db="finalpj", charset="utf8mb4"
            )
            self.cursor = self.connect.cursor()
            print("✅ 数据库连接成功")
        except Exception as e:
            print(f"❌ 数据库连接失败: {str(e)}")
            raise

    def process_item(self, item, spider):
        try:
            sql = "insert into anime (media_id,name,score,score_num,play,follow,barrage,tags,comments) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            self.cursor.execute(sql % (item['media_id'],item['name'],item['score'],item['score_num'],item['play'],item['follow'],item['barrage'],item['tags'],item['comments']))
            self.connect.commit()
            print(f"{item['name']} 的数据插入成功")
        except Exception as e: # 一些特殊字符就去掉
            print(f"{item['name']}插入失败！原因"+str(e))
            try:
                item['comments'] = ""
                sql = "insert into anime (media_id,name,score,score_num,play,follow,barrage,tags,comments) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                self.cursor.execute(sql % (
                item['media_id'], item['name'], item['score'], item['score_num'], item['play'], item['follow'],
                item['barrage'], item['tags'], item['comments']))
                self.connect.commit()
                print(f"{item['name']} 的数据插入成功")
            except Exception as e:
                print(f"{item['name']}插入失败！原因" + str(e))


    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()

'''
# 保存json的源
class JsonChunkWriterPipeline:
    def __init__(self, chunk_size=1000):
        # 初始化配置
        self.chunk_size = chunk_size  # 每个文件最大条目数
        self.output_dir = "json_chunks"  # 输出目录
        self.file_prefix = "anime_data"  # 文件名前缀
        self.file_counter = 1  # 文件计数器
        self.item_counter = 0  # 当前文件条目计数器
        self.current_file = None  # 当前文件对象
        self.current_file_path = None  # 当前文件路径

        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)

        # 初始化第一个文件
        self._create_new_file()

    @classmethod
    def from_crawler(cls, crawler):
        # 从 settings.py 读取配置
        return cls(
            chunk_size=crawler.settings.getint('JSON_CHUNK_SIZE', 1000)
        )

    def _create_new_file(self):
        """创建新文件并初始化 JSON 数组"""
        if self.current_file:
            self.current_file.close()  # 关闭旧文件

        # 生成带时间戳和序号的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file_path = os.path.join(
            self.output_dir,
            f"{self.file_prefix}_{timestamp}_part{self.file_counter}.json"
        )

        # 写入空数组
        self.current_file = open(self.current_file_path, 'w', encoding='utf-8')
        self.current_file.write('[]')
        self.current_file.flush()

        # 重置计数器
        self.file_counter += 1
        self.item_counter = 0

    def process_item(self, item, spider):
        # 转换为字典
        item_dict = ItemAdapter(item).asdict()

        # 读取现有数据
        with open(self.current_file_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            # 追加新数据
            data.append(item_dict)

            # 写入文件
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()

        # 更新计数器
        self.item_counter += 1

        # 达到分块大小时创建新文件
        if self.item_counter >= self.chunk_size:
            self._create_new_file()

        return item

    def close_spider(self, spider):
        """爬虫关闭时确保文件正确关闭"""
        if self.current_file:
            self.current_file.close()
'''