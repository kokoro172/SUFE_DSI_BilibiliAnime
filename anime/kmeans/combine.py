import pymysql
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

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
def preprocess_data(data):
    # 将数据转换为NumPy数组
    data_array = np.array(data)
    # 分离特征和目标变量
    X = data_array[:, 0].reshape(-1, 1)  # follow作为特征
    y = data_array[:, 1]  # play作为目标变量
    return X, y

# 训练KNN回归模型
def train_knn(X_train, y_train, n_neighbors=5):
    knn = KNeighborsRegressor(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    return knn

# 预测
def predict(knn, X_test):
    y_pred = knn.predict(X_test)
    return y_pred

# 计算R2得分
def compute_r2_score(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    return r2

# 定义SQL语句
sql = "SELECT follow, play FROM anime"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 数据预处理
if result:
    X, y = preprocess_data(result)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练KNN回归模型
    knn = train_knn(X_train, y_train, n_neighbors=5)

    # 预测
    y_pred = predict(knn, X_test)

    # 计算R2得分
    r2 = compute_r2_score(y_test, y_pred)
    print("R2 Score:", r2)

# 关闭数据库连接
connection.close()
