import pymysql

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='5245117',
                             db='finalpj',
                             charset='utf8mb4'
                             ) # 直接让它返回默认的元组

# 建表
def pymysql_create_table():
    try:
        with connection.cursor() as cursor:
            sql = '''
            create table if not exists anime(
            media_id varchar(8) primary key,
            name text not null,
            score float not null,
            score_num int not null,
            play bigint not null,
            follow int not null,
            barrage int not null,
            tags text not null,
            comments text
            );
            CREATE TABLE finalpj.media_tags (
            media_id INT NOT NULL,
            tag VARCHAR(255) NOT NULL,
            play BIGINT,
            PRIMARY KEY (media_id, tag)
            );
            '''
            cursor.execute(sql)
        connection.commit()
        print("建表成功")
    except:
        print("建表失败")

# 删表
def pymysql_drop_table():
    try:
        with connection.cursor() as cursor:
            sql = '''
            drop table anime;
            '''
            cursor.execute(sql)
        connection.commit()
        print("删表成功")
    except:
        print("删表失败")


