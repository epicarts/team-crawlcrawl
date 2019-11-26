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

def ahnlab_crawl(r2):
    '''
    안랩 asec의 데이터를 추출해서 json 형태로 리턴함.
    '''
    try:
        r2.html.render()
    except:
        pass
    tag_selector = 'body > div#wrap > section#container > div.content-wrap > article#content > div.inner > div.entry-content > p'
    tag_selector2 = 'body > div#wrap > section#container > div.content-wrap > article#content > div.inner > div.entry-content > div.tt_article_useless_p_margin > p'
    
    for line2 in r2.html.find('h1'):
        news_title = line2.text
        #print('title: ', news_title)

    content = ''

    for line2 in r2.html.find(tag_selector):
        content = content + '\n' + line2.text
  
    if content == '':
        #print('없어')
        for line2 in r2.html.find(tag_selector2):
            content = content + '\n' + line2.text
    #else:
        #print('있어')

    #print('content:', content)
    file_data = OrderedDict()
    file_data['author'] = 'AhnLab'
    file_data['title'] = news_title
    file_data['content'] = content
    file_data['url'] = r2.url
    file_data['publisher'] = 'AhnLab'
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

    list_of_tweets = query_tweets_from_user("AhnLab_SecuInfo")#보안 뉴스 글에서 5개 를 가져옴.

    p = re.compile('[a-z]')

    for tweet in list_of_tweets:
        
        tweet_text = tweet.text
        url = tweet_text[tweet_text.find("https://asec.ahnlab.com/"):]

        if p.match(url):
            ahnlab_url = url[:len(url)-1]
            #SQL에서 URL 중복 체크
            sql = "select EXISTS (select * from raw_table WHERE url=%s) as success"
            val = (ahnlab_url)
            is_exists = select_mydb(sql, val)[0][0] # ture: 1 / false: 0 반환

            if is_exists:   # 해당 URL이 있으면 패스 
                continue
                #print("Already Exists url")
            else:   # 해당 URL이 없으면 크롤링 후 삽입하기.
                session = HTMLSession()

                #try except, 중간에 파싱결과 오류나면 pass하고 다음거..
                try:
                    r2 = session.get(ahnlab_url)
                    #print('1번')
                    json_data = ahnlab_crawl(r2)# 수집한 데이터를 입맞대로 가공.
                            #sql query문으로 삽입
                    #print('2번')
                    sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], tweet.timestamp)
                    query_mydb(sql=sql, val=val)
                    
                except:
                    print("예외 발생.")
                    pass
        else:
            print('url 엄서요')
    print("안랩 ASEC 수집 완료")
