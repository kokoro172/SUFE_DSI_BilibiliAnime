import pymysql


if __name__=='__main__':
    # 连接数据库
    connect = pymysql.connect(
        host="localhost", user="root", password="5245117",
        port=3306, db="finalpj", charset="utf8mb4"
    )
    cursor = connect.cursor()

    # 首先取数
    select_sql = """
            SELECT media_id, play, tags 
            FROM anime 
            WHERE tags IS NOT NULL AND tags != ''
            """
    cursor.execute(select_sql)
    rows = cursor.fetchall()

    # 分割标签创建新数据
    insert_data = []
    for row in rows:
        media_id, play, tags = row
        # 拆分标签
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        # 对于每一组id和播放量，把拆开的标签分别组合成新的行
        for tag in tag_list:
            insert_data.append((media_id, tag, play))

    # 插入新表
    if insert_data:
        insert_sql = """
                INSERT IGNORE INTO media_tags (media_id, tag, play)
                VALUES (%s, %s, %s)
                """
        cursor.executemany(insert_sql, insert_data)
        connect.commit()
        print(f"成功插入 {len(insert_data)} 条记录")

    # 收尾-断连
    cursor.close()
    connect.close()
    print("数据库连接已关闭")
