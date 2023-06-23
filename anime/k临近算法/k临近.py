import pymysql
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import MultiLabelBinarizer


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

# 构建K近邻算法模型
def build_knn_model(X_train, y_train, n_neighbors):
    knn_model = KNeighborsRegressor(n_neighbors=n_neighbors)
    knn_model.fit(X_train, y_train)
    return knn_model

# 计算预测准确率（R2 score）
def calculate_accuracy(y_true, y_pred):
    accuracy = r2_score(y_true, y_pred)
    return accuracy

# 定义SQL语句
sql = "SELECT score, play, follow, tags FROM anime WHERE score != 0"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 处理数据
if result:
    data = np.array(result)
    X = data[:, :3]  # 提取score, play, follow三列数据

    # 将标签字段解析为多个类别
    tags = []
    for row in result:
        tags.extend(row[3].split(','))

    # 使用MultiLabelBinarizer进行独热编码
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(tags)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 构建K近邻算法模型
    k = 5  # 设置K值
    knn_model = build_knn_model(X_train, y_train, n_neighbors=k)

    # 在测试集上进行预测
    y_pred = knn_model.predict(X_test)

    # 计算模型的预测准确率
    accuracy = calculate_accuracy(y_test, y_pred)

    print("预测准确率（R2 score）：", accuracy)

# 关闭数据库连接
connection.close()
