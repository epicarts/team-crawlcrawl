from konlpy.tag import Komoran
import nltk

import os
import pymysql

import re

'''
코드 설명

1. 데이터베이스에서 tag 필드가 NULL 인것을 찾음.
2. 데이터베이스의 Content에서 값을 이용하여 키워드를 붙임.
3. 각각 id 값을 기준으로 다시 데이터베이스 tag 필드에 넣음.

* LOGSTASH랑 엮어서 쓰므로 주의 필요

추가 설명
1. 키워드 추출은 빈도수 기준으로 추출
2. stop_words.txt은 제외할 단어 목록
3. user_dic.txt는 사용자 단어 목록 
'''

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

def preprocess(sentence):
    sentence = re.sub('\xa0','',sentence)
    sentence = re.sub('\n','',sentence)
    sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\(\)\[\]\<\>`\'…》]','',sentence)
    sentence = re.sub('([a-zA-Z])','',sentence)#알파벳 제거
    sentence = re.sub('([0-9])','',sentence)#알파벳 제거

    return sentence

def morp_d(token_data):
    '''
    [[[id],[title],[content]], [[id2],[title2],[content2]]...]  2차원 배열 형태로 저장되어 있음.
    '''
    keywords = []

    komoran = Komoran(userdic='/code/crawling_code/nlp_model/user_dic.txt')#사용자 단어 사전 불러오기

    file = open("/code/crawling_code/nlp_model/stop_words.txt", 'r', encoding='utf-8')#포함하지 않을 단어 목록 불러오기
    stop_words = file.read()
    file.close()

    for i in range(0, len(token_data)):
    
        try:
            #추가: 안하면 komoran.nouns에서 오류가 남.
            token_data[i][1] = preprocess(token_data[i][1])#알파벳이나, 특수문자, 엔터키 제거.
            token_data[i][2] = preprocess(token_data[i][2])#알파벳이나, 특수문자, 엔터키 제거. 
            token_data[i][1] = komoran.nouns(token_data[i][1])
            token_data[i][2] = komoran.nouns("\n".join([s for s in token_data[i][2].split("\n") if s]))   # komoran은 공백에서 오류 발생, 공백 제거
            words = []
            for word in token_data[i][2]:   # 한 글자 단어 or 불용어 제거
                if ((len(word) == 1) or (word in stop_words)):
                    continue
                words.append(word)

            token_data[i][2] = words
            text = nltk.Text(token_data[i][2], name='NMSC')
            keywords.insert(i, text.vocab().most_common(3))   # 빈도 수 상위 3 단어를 키워드(태그)로 지정
        except:
            #print(token_data[i][1], token_data[i][2])
            pass

    # for i in range(0, len(token_data)):
    #     print('ID: ', token_data[i][0],'\n')
    #     print('Title: ', token_data[i][1], '\n')
    #     print('keywords: ', keywords[i], '\n')
    #     print('\n\n\n')
    return token_data, keywords

if __name__ == '__main__':
    
    #데이터베이스에서 tag에 아무런 값이 들어가 있지 않은 글들을 추출함.
    sql = "SELECT id, title, content FROM raw_table WHERE tag IS NULL"#AND publisher='보안뉴스'"
    false_tags  = select_mydb(sql)#tag가 없는 글 추출 

    if false_tags:
        print("%d개: 키워드(태그) 붙이는 중" % len(false_tags))
        false_tags_list = list(map(list, false_tags))#데이터베이스에서 가져올 때 튜플형식으로 가져오기 때문에 리스트로 변환
        token_data, keywords = morp_d(false_tags_list)#token_data: 각 토큰들에 대한 데이터들 / keyword: 키워드 리스트 [('보안', 4), ('업데이트', 3), ('권고', 3)]

        try:
            for i in range(0, len(token_data)):
                sql_id = token_data[i][0]#데이터 베이스 id 값
                sql_tags_list = [keyword for keyword, count in keywords[i]]# [('보안', 4), ('업데이트', 3), ('권고', 3)] => ["보안", "업데이트", 권고"]
                sql_tags = ' '.join(sql_tags_list)#["보안", "업데이트", 권고"] => '보안 업데이트 권고'

                #데이터 베이스에 넣기.
                sql = "UPDATE raw_table SET tag='%s' WHERE ID=%s" % (sql_tags, sql_id)
                query_mydb(sql=sql)
        except:
            pass
        print("키워드(태그) 붙이기 완료 되었습니다.")
    else:
        print("키워드(태그)를 붙일 데이터가 없습니다.")