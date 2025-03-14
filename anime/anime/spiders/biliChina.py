import scrapy
import json
from ..items import AnimeItem


class BiliSpider(scrapy.Spider):
    name = "biliChina"
    #allowed_domains = ["www.bilibili.com"]
    url_head = "https://api.bilibili.com/pgc/season/index/result?season_version=-1&is_finish=-1&copyright=-1&season_status=-1&year=-1&style_id=-1&order=3&st=4&sort=0&season_type=4&pagesize=20&type=1"
    start_urls = [url_head + "&page=1"]

    # 解析
    def parse(self, response):
        data = json.loads(response.text)  # 获取返回数据
        next_index = int(response.url[response.url.rfind("=") + 1:]) + 1
        print(f"下一页：{next_index}")

        if data['data']['size'] == 20 and next_index <= 150: # 20说明还有下一页
            next_url = self.url_head + "&page=" + str(next_index)
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            print(f"ERROR？当前页面size：{data['data']['size']}，next_index={next_index}")

        for i in data['data']['list']: # 对每一页进行逐个爬取
            media_id = i['media_id']
            detail_url = "https://www.bilibili.com/bangumi/media/md" + str(media_id) # 形成目标url
            item = AnimeItem()
            item['media_id'] = media_id
            # print(f"id= {media_id}") # 确认正常
            yield scrapy.Request(detail_url, callback=self.parse_detailA, meta={'item': item})

    # 对除评论以外的数据进行筛选存储
    def parse_detailA(self, response):
        item = response.meta['item']
        # 番剧名称
        item['name'] = response.xpath('//span[@class="media-info-title-t"]/text()').extract_first()
        # 播放量
        play = response.xpath(
            '//span[@class="media-info-count-item media-info-count-item-play"]/em/text()').extract_first()
        item['play'] = self.trans(play)
        # 追番数
        follow = response.xpath(
            '//span[@class="media-info-count-item media-info-count-item-fans"]/em/text()').extract_first()
        item['follow'] = self.trans(follow)
        # 弹幕数
        barrage = response.xpath(
            '//span[@class="media-info-count-item media-info-count-item-review"]/em/text()').extract_first()
        item['barrage'] = self.trans(barrage)
        # 番剧标签
        item['tags'] = response.xpath('//span[@class="media-tag"]/text()').extract()
        item['tags'] = ','.join(item['tags'])
        score = response.xpath('//div[@class="media-info-score-content"]/text()').extract_first()
        if score is None: # 防止出现没有评分的情况
            item['score'] = 0
        else:
            item['score'] = float(score)
        numbers = response.xpath('//div[@class="media-info-review-times"]/text()').extract_first()
        if numbers is None:
            item['score_num'] = 0
        else:
            item['score_num'] = int(numbers[:-2])

        detail_url = "https://api.bilibili.com/pgc/review/short/list?media_id=" + str(
            item['media_id']) + "&ps=30&sort=0"
        print(f"{item['name']} 已爬取完成")
        yield scrapy.Request(detail_url, callback=self.parse_detailB, meta={'item': item})

    # 对评论进行整合储存
    def parse_detailB(self, response):
        item = response.meta['item']
        data = json.loads(response.text)
        comment_data = data['data']['list']
        comments = []
        for i in range(len(comment_data)):
            comments.append(comment_data[i]['content'])
        str_comments = ','.join(comments)
        item['comments'] = str_comments

        yield item

    # 文字数据转化为数字
    def trans(self, string):
        if string[-1] == '万':
            return int(float(string[0:-1]) * 1e4)
        elif string[-1] == '亿':
            return int(float(string[0:-1]) * 1e8)
        else:
            return int(string)
