# 开发者:wkw
# 开发时间：2023/6/23 13:11
import pymysql
import matplotlib.pyplot as plt
import numpy as np

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

# 生成直方图
def generate_histogram(data, column_names, save_path):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    for i, ax in enumerate(axes.flatten()):
        if i > 4:
            break
        ax.hist(data[:, i], bins=10)
        ax.set_title(column_names[i])
        ax.set_xlabel('Data')
        ax.set_ylabel('Frequency')

    # 调整子图之间的间距
    fig.tight_layout()

    # 保存直方图为文件
    plt.savefig(save_path)
    plt.close()

# 定义SQL语句
sql = "select score,score_num,play,follow,barrage from anime where score !=0"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 处理数据
if result:
    result = np.array(result)
    column_names = ['score', 'score_num', 'play', 'follow', 'barrage']
    save_path = "./histogram.png"  # 图片保存路径和文件名
    generate_histogram(result, column_names, save_path)

# 关闭数据库连接
connection.close()
