from twitterscraper import query_tweets, query_tweets_from_user
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



#일자 별로 수집하는 코드
#enddate = dt.date.today() + dt.timedelta(days=1) # 하루 뒤를 더해 줘야함. 안그러면 시차 때문에 최근 글을 불러오지 못함.
#list_of_tweets2 = query_tweets("@boannews", begindate=dt.date(2018, 1, 1), enddate=dt.date(2019, 7, 29))
if __name__ == '__main__':
    '''
        0. query_tweets_from_user를 사용하여 글쓴 사람의 최근 글 5개를 뽑아옴.
        1. 데이터 베이스에서 URL 이 있는지 검사
        2. 이미 있으면 수집안하고 다음 tweet 객체로 이동
        3. 없으면 보안뉴스 페이지에 접속하여 크롤링

        단점: 디비 혹사...
    '''

    lately_twitter_limit = 5 #가장 최근 긁어올 개수.
    list_of_tweets = query_tweets_from_user("boannews", limit=lately_twitter_limit)#보안 뉴스 글에서 5개 를 가져옴.

    for tweet in list_of_tweets:
        #print(tweet.text)
        #print(tweet.timestamp)
        #print(tweet.text_html)
        tweet_text = tweet.text
        url = tweet_text[tweet_text.find("http://www.boannews.com/"):] # http://www.boannews.com/media/view.asp?idx=84215\xa0…
        boannews_url = url[:len(url)-2]# http://www.boannews.com/media/view.asp?idx=84215

        #SQL에서 URL 중복 체크
        sql = "select EXISTS (select * from raw_table WHERE url=%s) as success"
        val = (boannews_url)
        is_exists = select_mydb(sql, val)[0][0] # ture: 1 / false: 0 반환

        if is_exists: # 해당 URL이 있으면 패스 
            continue
            #print("Already Exists url")
        else:# 해당 URL이 없으면 크롤링 후 삽입하기.
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
    print("보안뉴스 수집 완료")
