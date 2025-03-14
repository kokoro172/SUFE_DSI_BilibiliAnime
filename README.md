# 哔哩哔哩动画数据爬取分析
本项目为SUFE 数据科学导论的课程项目

基于Scrapy框架的Bilibili番剧数据采集系统，可自动抓取番剧基本信息、评分、播放量、弹幕及用户评论，并持久化存储到MySQL数据库。
## 🚀 功能特性

- **多维度数据采集**
  - 基础信息：番剧名称、媒体ID、标签、评分
  - 统计数据：播放量、追番人数、弹幕数
  - 用户内容：最新30条短评（可调整，仅尝试）

- **~~智能反反爬策略~~（不推荐）**
  - 自动请求头管理
  - 随机化请求延迟

- **高效数据存储**
  - MySQL批量插入
  - 数据清洗转换（万/亿级单位自动换算）
  - 异常数据过滤

## 📦 项目结构

```bash
anime/
├── spiders/
│   ├── bili.py         # 通用番剧爬虫
│   └── biliChina.py    # 中国区特供番剧爬虫
├── middlewares.py      # 爬虫中间件
├── pipelines.py        # 数据存储管道
├── items.py            # 数据模型定义
├── settings.py         # 配置文件
├── initialMySQL.py     # 数据库初始化脚本
└── main.py             # 爬虫启动入口
```

## ⚙️ 快速开始

### 前置要求

- Python 3.8+
- MySQL 5.7+
- Scrapy 2.11
- PyMySQL 

```bash
pip install scrapy pymysql
```

### 数据库配置

1. 创建数据库（需提前安装MySQL）
```bash
mysql -u root -p -e "CREATE DATABASE finalpj CHARACTER SET utf8mb4"
```

2. 初始化表结构

简单来说就是删表和建表

```bash
python initialMySQL.py
```

### 运行爬虫
**通过终端：** 在anime文件夹里面运行：
```bash
# 运行通用番剧爬虫
scrapy crawl bili

# 运行中国区特供番剧爬虫
scrapy crawl biliChina
```
**通过py文件：**
直接运行`main.py`
## 🔧 配置说明

修改 `settings.py` 配置项：
```python
import random

# 数据库配置（建议使用环境变量）
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'  # 务必修改!
MYSQL_DB = 'finalpj'

# 反爬相关配置
DOWNLOAD_DELAY = 0.1 + random.randrange(1, 5)/10               # 请求间隔(秒)
ROBOTSTXT_OBEY = False           # 是否遵守robots协议
CONCURRENT_REQUESTS = 8          # 并发请求数

# 其余配置详情请见settings.py
```

## 📊 数据说明及样例

| 字段名     | 说明               |
|-----------|-------------------|
| media_id  | 动画标识ID         |
| name      | 动画名称           |
| score     | 动画评分           |
| score_num | 评分人数           |
| play      | 动画播放量         |
| follow    | 追番人数           |
| barrage   | 弹幕数             |
| tags      | 标签               |
| comments  | 评论汇总           |

| media_id | name         | score | score_num | play    | follow  | barrage | tags               |comments|
|----------|--------------|-------|-----------|---------|---------|---------|--------------------|--------|
| 28232073  | Re：从零开始的异世界生活 第二季 后半 | 9.9  | 176198    | 100000000  | 9759000 | 1158000 | 小说改,穿越,奇幻,冒险     | 2023年3月25日从零开始的异世界生活 第三季 宣布制作！,第三季什么时候出啊啊啊,神作,9.9！！！！,123,值,1,1,无敌,优质动漫,我爱 爱蜜莉雅,好,好刀,從9.8变9.9，B站最高的9.9,无敌，永远的re zero,好... |
| 1733      | 罗小黑战记                  | 9.9  | 149345    | 560000000  | 7594000 | 2712000 | 原创,热血,萌系,治愈       | 自从看了这个动漫，也不抽烟不喝酒每天早睡早起。就为了能活过作者。,每一次更新播放量都会激增，为什么呢？因为大家都会选择从头再来一遍，也不一定是因为热爱，主要是前边剧情都忘...                         |
| 28223066  | 我的三体之章北海传          | 9.9  | 148840    | 120000000  | 2559000 | 1120000 | 小说改,科幻               | 神了，真的越来越好了,我翻了五分钟没翻出一个五星以下的，谁能告诉我9.9怎么来的？谁是叛徒？,艺画开天的三体想拍的好，首先就要越过这座大山。……………………果然，就还原度、配音...                       |
| 102312    | 碧蓝之海                    | 9.9  | 140275    | 170000000  | 4890000 | 1090000 | 社团,漫画改,搞笑,运动     | 有一说二，我要第二季,出第二季，我就去看那个说出第二季去裸奔的人（doge）,这番要是出第二季，我裸奔御通,我要第二季我要第二季我要第二季我要第二季,感谢此番，体脂笑没了,下一季,好...                   |
| 28221403  | 擅长捉弄的高木同学 第二季  | 9.9  | 123425    | 75092000   | 3684000 | 1760000 | 漫画改,恋爱,校园,搞笑     | 一人血书出第三季,。。嗯。你们懂得。。。一个19的蓝孩纸躺在床上傻笑的看着。。。和我差不多的举个手,我就想知道，这0.1分是谁扣的。,。,高木与西片的校园日常，如芦柑和罗勒的混合果酱，里面加了大量的糖。没有要推的主线，没有要解决的任务，我们只在生活的中期待下一个美好的小故事。,甜甜甜！,不喜欢,补个评分，我永远喜欢高木！,无敌,甜到掉牙了,吃糖喽,最喜欢的情侣之一,齁死我了,神中神,好耶！,真的太喜欢啦,酸酸甜甜的,我的一切幻想,好看,真的好看,真係神作,好！,太棒了,美好的初中生的暧昧，是会令人会心一笑的好番,神！,我心中最无敌的纯爱！,当赏,真美好啊！,神作，可惜完结了，还可以看漫画,满混满混，必须满昏，谁不打满昏看不起 |

## ⚠️ 注意事项

1. **合法合规使用**
   - 请遵守Bilibili的[Robots协议](https://www.bilibili.com/robots.txt)
   - 控制请求频率（建议>1秒/请求）
   - 禁止用于商业用途或大规模抓取

2. **数据安全**
   ```python
   # 敏感信息建议通过环境变量配置
   import os
   MYSQL_PASSWORD = os.getenv('MYSQL_PWD')  # 更安全的配置方式
   ```

3. **性能优化**
   - 启用AutoThrottle扩展（`settings.py`中取消注释相关配置）
   - 建议使用Redis实现分布式爬取

## 🤝 参与贡献

欢迎提交Issue或Pull Request：
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/improvement`)
3. 提交修改 (`git commit -m 'Add some feature'`)
4. 推送分支 (`git push origin feature/improvement`)
5. 新建Pull Request


