import pymysql
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

# 进行K-means聚类分析
def perform_kmeans_clustering(data, n_clusters):
    # 对play和follow进行对数压缩变换
    data[:, 1] = np.log(data[:, 1])
    data[:, 2] = np.log(data[:, 2])

    # 进行数据归一化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # 执行K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(scaled_data)

    # 获取聚类结果
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    return labels, centroids

# 生成3D散点图
def generate_3d_scatterplot(data, labels, centroids, save_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制数据点
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, cmap='viridis', s=50)

    # 绘制聚类中心
    ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', marker='x', s=100)

    ax.set_xlabel('Score')
    ax.set_ylabel('Log(Play)')
    ax.set_zlabel('Log(Follow)')

    # 保存图像
    plt.savefig(save_path)
    plt.close()

# 定义SQL语句
sql = "SELECT score, play, follow FROM anime where score > 0"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 处理数据
if result:
    data = np.array(result)
    n_clusters = 4
    save_path = "./kmeans_clusters4.png"  # 图片保存路径和文件名

    # 执行K-means聚类分析
    labels, centroids = perform_kmeans_clustering(data, n_clusters)

    # 生成3D散点图
    generate_3d_scatterplot(data, labels, centroids, save_path)

# 关闭数据库连接
connection.close()
