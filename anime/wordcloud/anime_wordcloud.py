import jieba
import wordcloud
import matplotlib.pyplot as plt
import pymysql
import numpy as np
from PIL import Image

num = 0
exclude = {'的','了','和','而','但','吧','在','啊','这','是'}
def getData(number):
    # 建立连接
    connect = pymysql.Connect(host="localhost",user="root",password="5245117",port=3306,db="finalpj")
    cursor = connect.cursor()
    if  number == 0: # 查询tags
        sql = '''select tags from anime where score != 0'''

    else:
        sql = '''select comments from anime where score != 0'''

    # 获取数据
    try:
        cursor.execute(sql)
    except Exception as e:
        print("获取失败！原因" + str(e))

    # 处理数据
    result = cursor.fetchall()
    return result

def generateWordcloud(result):
    text = ""
    for row in result:
        text += str(row[0])
    words = jieba.lcut(text)

    # 将分词结果转换为字符串
    wordcloud_text = " ".join(words)

    # 形状
    img = Image.open("love.png")
    mask = np.array(img)


    # 创建词云对象
    wd = wordcloud.WordCloud(width=2160, height=4096, background_color='white',
                             mask=mask,stopwords=exclude,collocations=False).generate(wordcloud_text)

    # 显示词云
    plt.imshow(wd, interpolation='bilinear') # 使用双线性插值
    wd.to_file(str(num)+"词云图片.jpg")
    print(f"{num}输出成功")

result = getData(num)
generateWordcloud(result)

num = 1
result = getData(num)
generateWordcloud(result)