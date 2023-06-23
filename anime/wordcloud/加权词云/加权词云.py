import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 建立数据库连接
def create_connection():
    connection = pymysql.connect(host="localhost", user="root", password="5245117", port=3306, db="finalpj")
    return connection

# 从数据库获取数据
def get_data(connection, sql):
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("获取数据失败！原因：" + str(e))
        return None
    finally:
        cursor.close()

# 数据预处理
def preprocess_data(result):

    label_mapping = {}  # 标签对应播放量

    for row in result:
        tags = row[1].split(',')  # 分割标签
        play = row[0]  # 播放量

        for tag in tags:
            if tag not in label_mapping:  # 如果当前标签为新标签
                label_mapping[tag] = 0  # 初始化并加上播放量
            label_mapping[tag] += play

    return label_mapping




# 定义SQL语句
sql = "SELECT play, tags FROM anime"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 数据预处理
label_mapping = preprocess_data(result)



# 生成词云图
wordcloud = WordCloud(background_color='white').generate_from_frequencies(label_mapping)

# 绘制词云图
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Tag Word Cloud')

# 显示词云图
wordcloud.to_file("a.png")



# 关闭数据库连接
connection.close()
