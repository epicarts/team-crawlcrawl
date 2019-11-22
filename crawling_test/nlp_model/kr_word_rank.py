import os
import pymysql

from konlpy.tag import Kkma
from konlpy.tag import Okt
from konlpy.tag import Komoran

from krwordrank.word import KRWordRank

from time import sleep

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

sql = "SELECT id, content FROM raw_table WHERE tag IS false AND publisher='보안뉴스'"
false_tags  = select_mydb(sql)#tag가 없는 글 추출 

kkma = Kkma()#꼬꼬마 형태소 분석기
okt = Okt()
komoran = Komoran()

from krwordrank.word import summarize_with_keywords

stopwords = {'영화', '관람객', '너무', '정말', '보고', '우리', '아니','대상', '것이다', '있는', '것으로', '웨어'}

for false_tag in false_tags:
    doc_id = false_tag[0]#도큐먼트 id 추출
    content = false_tag[1]
    sentences = kkma.sentences(content)#추출된 내용의 문장을 리스트로 나눔.

    nouns = []
    for sentence in sentences:
        if sentence is not '':
            nouns.append(' '.join([noun for noun in komoran.nouns(str(sentence))
            #nouns.append(' '.join([noun for noun in kkma.nouns(str(sentence))
        if noun not in stopwords and len(noun) > 1]))

    keywords = summarize_with_keywords(nouns, min_count=3, max_length=10,
        beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    print(keywords)


#=========================태그 하나씩만 추출
from krwordrank.sentence import summarize_with_sentences

stopwords = {'영화', '관람객', '너무', '정말', '보고', '우리', '아니','대상', '것이다', '있는', '것으로', '웨어'}

for false_tag in false_tags:
    doc_id = false_tag[0]#도큐먼트 id 추출
    content = false_tag[1]
    sentences = kkma.sentences(content)#추출된 내용의 문장을 리스트로 나눔.

    nouns = []
    for sentence in sentences:
        if sentence is not '':
            nouns.append(' '.join([noun for noun in komoran.nouns(str(sentence))
            #nouns.append(' '.join([noun for noun in kkma.nouns(str(sentence))
        if noun not in stopwords and len(noun) > 1]))
        
    keywords, sents = summarize_with_sentences(
                                            nouns, 
                                            stopwords = stopwords,
                                            num_keywords=100, 
                                            num_keysents=10
                                            )
    print()
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:7]:
        print('%8s:\t%.4f' % (word, r))
        #print('#%s' % word)


#=========================태그 하나씩만 추출
stopwords = ['보안','중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자","아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]

min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10
verbose = True

#키워드 하나씩만 추출.
for false_tag in false_tags:
    doc_id = false_tag[0]#도큐먼트 id 추출
    content = false_tag[1]
    sentences = kkma.sentences(content)#추출된 내용을 문장별로 나눔.

    nouns = []
    for sentence in sentences:
        if sentence is not '':
            nouns.append(' '.join([noun for noun in kkma.nouns(str(sentence))
        if noun not in stopwords and len(noun) > 1]))

    wordrank_extractor = KRWordRank(min_count, max_length)
    keywords, rank, graph = wordrank_extractor.extract(nouns, beta, max_iter, verbose)
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
        print(doc_id)
        print('%8s:\t%.4f' % (word, r))
