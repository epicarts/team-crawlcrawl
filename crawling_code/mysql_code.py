
import pymysql.cursors


import os


1. URL 은 프라이머리 키 다 .
2. 검색 속도를 빠르게 하기 위해서 URL 을 인덱싱한다. => 데이터베이스에서 미리 캐싱 특정 필드. ???  ==> 특정필드 : URL 

데이터를 가져옴. => 데이터베이스에서 분단위 .....? => 데이터 베이스 존나 ... 

3. SELECT * FROM logstash_db.raw_table WHERE URL='http://google.com'; => 값 가져옴. 없으면 넣고 있으면 안넣고 
4. 없으면, "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목ㅅ32323ㄴㅇ22', 'http://google.com')"
4. upsert 

=====================================
플랜 B
1. 가장 최근에 입력된 DATA (글이 생성된 시간 Datetime) 2019- 11 - 13 17:00
2. 디비 조회 없이. 시간 기준으로 ...  트위터 글은 하루단위로 가져옴. DB 최소화.


- 하루단위로 긁어온 트위터 클롤링(메모리) 
- 가장 최근에 쓰여진 RAW(DB)
=>> 날짜 기준으로 체크. =>  가장 최근에 씌여진 날짜보다 작으면 pop(데이터 뺴오기)

json 


가장 최근에 입력된 


mysql_ip = os.getenv('MYSQL_HOST','localhost')
es = Elasticsearch(elasticsearch_ip)


conn = pymysql.connect(host='localhost',
        user='root',
        password='root',
        db='logstash_db',
        charset='utf8mb4')

cursor = conn.cursor()
cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
cursor.commit()
cursor.close()

import pymysql


connection = pymysql.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="logstash_db",
  charset='utf8mb4'
)

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

DROP TABLE `logstash_db`.`raw_table`

import pymysql


connection = pymysql.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="logstash_db",
  charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목ㅅ32323ㄴㅇ22', 'http://google.com')"
    # connection is not autocommit by default. So you must commit to save
    # your changes.
        cursor.execute(sql)
        connection.commit()
        print("cursor.lastrowid: ",cursor.lastrowid)
finally:
    connection.close()


import pymysql


connection = pymysql.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="logstash_db",
  charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "SELECT * FROM raw_table WHERE id=5"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row_data in result:
            print(row_data[0])
            print(row_data[1])
finally:
    connection.close()


'''
INSERT INTO es_table (id, client_name) VALUES (<id>, <client name>);
UPDATE es_table SET client_name = <new client name> WHERE id=<id>;
INSERT INTO es_table (id, client_name) VALUES (<id>, <client name when created> O
'''

# publisher: 보안뉴스 에 가장 최근 post_create_datetime 와 URL을 가져오는 쿼리.
# sql = "SELECT post_create_datetime, URL FROM raw_table WHERE publisher='보안뉴스' ORDER BY post_create_datetime DESC limit 1"
# sql_result = select_mydb(sql)
# lately_post_create_datetime = sql_result[0][0]
# lately_url = sql_result[0][1]