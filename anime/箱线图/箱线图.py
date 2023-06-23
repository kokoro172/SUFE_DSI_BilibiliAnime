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

# 生成箱线图
def generate_boxplot(data, column_names, save_path):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    for i, ax in enumerate(axes.flatten()):
        if i > 4:
            break
        ax.boxplot(data[:, i])
        ax.set_title(column_names[i])
        ax.set_ylabel('Data')

    # 调整子图之间的间距
    fig.tight_layout()

    # 保存箱线图为文件
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
    save_path = "./boxplot.png"  # 图片保存路径和文件名
    generate_boxplot(result, column_names, save_path)

# 关闭数据库连接
connection.close()
