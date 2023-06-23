import pymysql
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


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


def preprocess_data(result):
    labels_id = {}
    label_mapping = {}  # 标签对应播放量
    tagID = 0
    for row in result:
        tags = row[3].split(',')  # 分割标签
        play = row[0]  # 播放量

        for tag in tags:
            if tag not in labels_id:  # 如果当前标签为新标签
                labels_id[tag] = tagID
                tagID += 1
                label_mapping[labels_id[tag]] = 0  # 初始化并加上播放量
            label_mapping[labels_id[tag]] += int(play)

    return labels_id, label_mapping



# 定义SQL语句
sql = "SELECT play, score_num, follow, tags FROM anime"

# 建立数据库连接
connection = create_connection()

# 从数据库获取数据
result = get_data(connection, sql)

# 处理数据
if result:
    result = np.array(result)
    play = result[:, 0].astype(int)
    score_num = result[:, 1].astype(int)
    follow = result[:, 2].astype(int)
    tags = result[:, 3]

    # 处理标签数据
    labels_id, label_mapping = preprocess_data(result)
    tags_encoded = np.zeros((tags.shape[0], len(labels_id)), dtype=int)
    for i, row in enumerate(tags):
        tags_list = row.split(',')
        for tag in tags_list:
            tag_id = labels_id[tag]
            tags_encoded[i, tag_id] = 1

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(np.column_stack((score_num, follow, tags_encoded)), play, test_size=0.2, random_state=42)

    # 使用随机森林回归模型进行训练和预测
    model_score_num = RandomForestRegressor()
    model_score_num.fit(X_train[:, 0].reshape(-1, 1), y_train)
    predicted_score_num = model_score_num.predict(X_test[:, 0].reshape(-1, 1))
    r2_score_score_num = r2_score(y_test, predicted_score_num)
    print("R2 Score (score_num -> play):", r2_score_score_num)

    model_follow = RandomForestRegressor()
    model_follow.fit(X_train[:, 1].reshape(-1, 1), y_train)
    predicted_follow = model_follow.predict(X_test[:, 1].reshape(-1, 1))
    r2_score_follow = r2_score(y_test, predicted_follow)
    print("R2 Score (follow -> play):", r2_score_follow)

    model_tags = RandomForestRegressor()
    model_tags.fit(X_train[:, 2:], y_train)
    predicted_tags = model_tags.predict(X_test[:, 2:])
    r2_score_tags = r2_score(y_test, predicted_tags)
    print("R2 Score (tags -> play):", r2_score_tags)

# 关闭数据库连接
connection.close()

