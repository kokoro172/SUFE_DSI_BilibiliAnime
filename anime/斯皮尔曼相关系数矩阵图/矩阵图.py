import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
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

# 生成斯皮尔曼相关系数矩阵图
def generate_correlation_matrix(data, column_names, save_path):
    corr_matrix = np.corrcoef(data, rowvar=False)  # 计算相关系数矩阵

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", xticklabels=column_names, yticklabels=column_names, ax=ax)

    ax.set_title('Spearman Correlation Matrix')  # 设置标题

    # 保存图像
    plt.savefig(save_path)
    plt.close()

# 定义SQL语句
sql = "select score, score_num, play, follow, barrage from anime where score != 0"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 处理数据
if result:
    result = np.array(result)
    column_names = ['score', 'score_num', 'play', 'follow', 'barrage']
    save_path = "./correlation_matrix.png"  # 图片保存路径和文件名
    generate_correlation_matrix(result, column_names, save_path)

# 关闭数据库连接
connection.close()
