import pymysql
import os
'''
테이블 생성해주는 python 코드 
'''
mysql_ip = os.getenv('MYSQL_HOST','localhost')

connection = pymysql.connect(
    host=mysql_ip,
    user="root",
    passwd="root",
    database="logstash_db",
    charset='utf8mb4')

cursor = connection.cursor()
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
                is_deleted boolean not null DEFAULT false,
                PRIMARY KEY(id),
                INDEX(url(255)),
                CONSTRAINT contacts_unique UNIQUE (url)
            )
'''
try:
    cursor.execute(sql)
    connection.commit()
    print("Create database table")
except:
    print("Can't create database table")
    pass
finally:
    connection.close()
