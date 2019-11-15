import pymysql
import os

mysql_ip = os.getenv('MYSQL_HOST','localhost')

connection = pymysql.connect(
    host=mysql_ip,
    user="root",
    passwd="root",
    database="logstash_db",
    charset='utf8mb4')

cursor = connection.cursor()
#URL 인덱싱 하기. (검색 속도 증가..!)
sql = '''
            CREATE TABLE raw_table (
                id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                content TEXT(65535) NOT NULL,
                url VARCHAR(255) DEFAULT NULL,
                publisher VARCHAR(255) NOT NULL,
                tag VARCHAR(255) DEFAULT NULL,
                post_create_datetime TIMESTAMP,
                modification_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                insertion_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                is_deleted boolean not null default false,
                PRIMARY KEY(id),
                INDEX(url(255)),
                CONSTRAINT contacts_unique UNIQUE (url)
            )
'''
cursor.execute(sql)
connection.commit()
connection.close()
