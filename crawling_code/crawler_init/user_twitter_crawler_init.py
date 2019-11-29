from twitterscraper import query_tweets_from_user

import os

from collections import OrderedDict
import json

import pymysql

def query_mydb(sql, val=None):
    '''
        sql = "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목', 'http://google.com')"
    '''
    mysql_ip = os.getenv('MYSQL_HOST','localhost')

    connection = pymysql.connect(
    host=mysql_ip,
    user="root",
    passwd="root",
    database="logstash_db",
    charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, val) # sql 구문 삽입
            connection.commit()
    finally:
        connection.close()
        
def select_mydb(sql, val=None):
    '''
        sql = "SELECT * FROM raw_table WHERE id=5"
    '''
    mysql_ip = os.getenv('MYSQL_HOST','localhost')

    connection = pymysql.connect(
    host=mysql_ip,
    user="root",
    passwd="root",
    database="logstash_db",
    charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, val) # sql 구문 삽입
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

if __name__ == '__main__':
    '''
    파라미터로 유저를 크롤링 할 유저를 넘겨줌
    https://twitter.com/kisa118 
    the_boan
    '''
    user_list = ["kisa118", "softwarecatalog"]#수집할 트위터 유저 리스트, "the_boan"
    for user in user_list:

        list_of_tweets = query_tweets_from_user(user=user)#특정 유저의 모든 데이터를 수집.

        for tweet in list_of_tweets:
            #SQL에서 URL 중복 체크
            sql = "select EXISTS (select * from raw_table WHERE url=%s) as success"
            val = (tweet.tweet_url)
            is_exists = select_mydb(sql, val)[0][0] # ture: 1 / false: 0 반환

            if is_exists: # 해당 URL이 있으면 패스 
                continue
            else:# 해당 URL이 없으면 데이터 넣기.
                dict_data = OrderedDict()
                dict_data['author'] = tweet.username
                dict_data['post_create_datetime'] = tweet.timestamp # 2015-01-01 12:10:00
                dict_data['title'] = tweet.text[:255]
                dict_data['content'] = tweet.text
                dict_data['url'] = tweet.tweet_url
                dict_data['publisher'] = user+'_twitter'
                try:
                    sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (dict_data['title'], dict_data['author'], dict_data['content'], dict_data['url'], dict_data['publisher'], dict_data['post_create_datetime'])
                    query_mydb(sql=sql, val=val)
                except:
                    print("예외 발생.")
                    pass
        print(user + " 수집 완료")
