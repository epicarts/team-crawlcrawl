from twitterscraper import query_tweets
import datetime as dt

import re
from requests_html import HTMLSession


import os

from collections import OrderedDict
import json

'''
    조회 할 수 있는 목록..
    # user name & id
    self.screen_name = screen_name
    self.username = username
    self.user_id = user_id
    # tweet basic data
    self.tweet_id = tweet_id
    self.tweet_url = tweet_url
    self.timestamp = timestamp
    self.timestamp_epochs = timestamp_epochs
    # tweet text
    self.text = text
    self.text_html = text_html
    self.links = links
    self.hashtags = hashtags
    # tweet media
    self.has_media = has_media
    self.img_urls = img_urls
    self.video_url = video_url
    # tweet actions numbers
    self.likes = likes
    self.retweets = retweets
    self.replies = replies
    self.is_replied = is_replied
    # detail of reply to others
    self.is_reply_to = is_reply_to
    self.parent_tweet_id = parent_tweet_id
    self.reply_to_users = reply_to_users
'''

# 하루 단위로 과거로 가면서 올라가면서 날짜 조회 => 날짜에 대한 제목 or URL 수집 => 비교.
# 있으면, 그 다음 부터 수집. 
# 없으면 하루 더 올라감. 메모리에 있는거 삭제. 
# 2019 11 12 조회(DB) => 제목 비교(DB). 없슴. => 2019 11 11 조회(DB) => 없슴. => 2019 11 10 조회(DB) 있슴. 있는거부터 수집하기.
# date => 가장 최근 date type => 가장 최근  
def news_crawl(r2):
    '''
    보안 뉴스의 데이터를 추출해서 json 형태로 리턴함.
    '''
    for line2 in r2.html.find('div#news_title02'):
        news_title = line2.text
        print('제목: ', news_title)

    for line2 in r2.html.find('div#news_util01'):
        date = line2.text
        #print('날짜: ', date[8:])

    author = "unknown"
    for line2 in r2.html.find('div#news_content'):
        writer = re.search(r'\[[가-힣\s]*\]',line2.text)
        if(writer != None):
            print('작성자: ', writer.group())
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


    
def duplication_check():
    return


if __name__ == '__main__':
    list_of_tweets = query_tweets("@boannews", begindate=dt.date(2019, 11, 1))

    for tweet in list_of_tweets:
        print(tweet.text)
        print(tweet.timestamp)
        print(tweet.text_html)
        tweet_text = tweet.text
        url = tweet_text[tweet_text.find("http://"):] # http://www.boannews.com/media/view.asp?idx=84215\xa0…
        boannews_url = url[:len(url)-2]# http://www.boannews.com/media/view.asp?idx=84215

        session = HTMLSession()
        r2 = session.get(boannews_url)# 보안뉴스 세션 열고 수집.
        json_data = news_crawl(r2)# 수집한 데이터를 입맞대로 가공.

        #sql query문으로 삽입
        sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], json_data['post_create_datetime'])
        query_mydb(sql=sql, val=val)
        

import pymysql


def query_mydb(sql, val):
    '''
        sql = "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목ㅅ32323ㄴㅇ22', 'http://google.com')"
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

