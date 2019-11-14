from twitterscraper import query_tweets, query_tweets_from_user
import datetime as dt

import re
from requests_html import HTMLSession


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

def news_crawl(r2):
    '''
    보안 뉴스의 데이터를 추출해서 json 형태로 리턴함.
    '''
    for line2 in r2.html.find('div#news_title02'):
        news_title = line2.text
        #print('제목: ', news_title)

    for line2 in r2.html.find('div#news_util01'):
        date = line2.text
        #print('날짜: ', date[8:])

    author = "unknown"
    for line2 in r2.html.find('div#news_content'):
        writer = re.search(r'\[[가-힣\s]*\]',line2.text)
        if(writer != None):
            #print('작성자: ', writer.group())
            author = writer.group()

            
    for line2 in r2.html.find('div#news_content'):
        content = re.sub(r'\[[가-힣\s]*[=][\sa-zA-Z0-9]*\]', '', line2.text)
        #print('내용: ', content)
    
    file_data = OrderedDict()
    file_data['author'] = author
    file_data['post_create_datetime'] = date[8:] + ":00" # 2015-01-01 12:10:00
    file_data['title'] = news_title
    file_data['content'] = content
    file_data['url'] = r2.url
    file_data['publisher'] = '보안뉴스'
    return file_data

if __name__ == '__main__':
    #일자 별로 수집하는 코드
    #enddate = dt.date.today() + dt.timedelta(days=1) # 하루 뒤를 더해 줘야함. 안그러면 시차 때문에 최근 글을 불러오지 못함.
    #list_of_tweets2 = query_tweets("@boannews", begindate=dt.date(2018, 1, 1), enddate=dt.date(2019, 7, 29))

    list_of_tweets = query_tweets_from_user("boannews")#특정 유저의 모든 데이터를 수집.
    finish = len(list_of_tweets) - 1

    for num, tweet in enumerate(list_of_tweets):
        #print(tweet.text)
        #print(tweet.timestamp)
        #print(tweet.text_html)
        tweet_text = tweet.text
        url = tweet_text[tweet_text.find("http://www.boannews.com/"):] # http://www.boannews.com/media/view.asp?idx=84215\xa0…
        boannews_url = url[:len(url)-2]# http://www.boannews.com/media/view.asp?idx=84215
        session = HTMLSession()
        r2 = session.get(boannews_url)# 보안뉴스 세션 열고 수집.

        #try except, 중간에 파싱결과 오류나면 pass하고 다음거..
        try:
            json_data = news_crawl(r2)# 수집한 데이터를 입맞대로 가공.
                    #sql query문으로 삽입
            sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], json_data['post_create_datetime'])
            query_mydb(sql=sql, val=val)
        except:
            print("예외 발생.")
            pass
        print("current: {} / finish: {} / url: {}".format(num, finish, boannews_url))