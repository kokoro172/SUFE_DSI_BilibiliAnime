# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    media_id = scrapy.Field() # 动画对应的id
    name = scrapy.Field() # 标题
    score = scrapy.Field() # 评分
    score_num = scrapy.Field() #评分人数
    play = scrapy.Field() # 总播放量
    follow = scrapy.Field() # 追番人数
    barrage = scrapy.Field() # 弹幕数量
    tags = scrapy.Field() # 番剧标签（列表）
    comments = scrapy.Field() # 评论（text）