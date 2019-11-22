#https://excelsior-cjh.tistory.com/93
from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import os

kkma = Kkma()# 단어 추출, 명사 추출 가능 .
stopwords = ['중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자"
,"아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]

text = '''우리나라 LEA 암호기술이 국제 표준으로 제정됐다는 건 매우 시의적절하며 의미심장

[보안뉴스= 조현숙 국가보안기술연구소 소장] 르그랑은 나에게 양피지에 담긴 암호문을 보여주며 말했다.

“첫눈에 쭈욱 보니 상상했던 것만큼 어렵진 않아. 누구나 곧 알아차리겠지만 이것은 암호야. 즉, 뜻을 전달하고 있는 거지. 그런데 키드 해적선장의 능력을 추측해 보건데, 그는 어려운 암호기술을 생각해낼 능력이 있는 것 같진 않아. 그래서 나는 곧 이 암호문은 단순한, 다만 해적선장의 조잡한 지성으로는 열쇠가 없으면 절대로 풀 수 없을 거라고 단정해 버렸지.” (애드거 앨런 포의 추리소설 <황금벌레(The Gold-Bug)> 중에서)

일반적으로 암호는 일반인이 즐겨 사용하는 기술은 아니다. 과거 해적이나 마약을 거래하는 상인들이 불법으로 취득한 물건을 처리하는 과정에서 주로 사용되었다. 초기의 암호기술은 단순했다. 애드거 앨런 포의 <황금벌레>나 ‘셜록 홈즈 시리즈’ 중 <춤추는 인형 암호> 같은 추리소설에서 나오는 것처럼 치환 방식을 주로 사용했다. 이러한 암호는 해당 암호문에서 많이 사용된 단어를 찾아내고 이를 통계학적으로 치환해보면 해석이 가능하다. 컴퓨터로 계산하면 쉽게 할 수 있지만, 100여 년 전까지만 해도 종이와 연필만으로 치환 작업을 했기에 많은 시간과 노력이 들었다.

암호기술은 점차 발전했고, 종이와 연필 대신 회전자를 이용한 기계식 암호장치가 개발되었다. 이 장비를 일명 ‘제퍼슨 디스크(Jefferson Disk)’라고도 하는데, 미국 제3대 대통령이자 독립운동가인 토머스 제퍼슨이 ‘미국 독립선언서’를 작성하는 과정에서 사용했다. 이러한 회전자 방식은 계속 개량되면서 유명한 독일군의 암호통신기 에니그마(Enigma)의 탄생으로 이어졌다. 물론 오늘 강한 창이 전쟁터에 나오면 내일은 이를 막을 방패가 나타나듯이, 영국 과학자 앨런 튜링은 에니그마로 만든 암호문을 해독할 수 있는 역사상 최초의 컴퓨터 콜로서스(Colossus)를 발명했다. 즉, 컴퓨터로 암호를 해석할 수 있게 된 것이다.

'''


sentences = kkma.sentences(text) # 문단에서 문장을 추출하는 부분 kkma 사용.
len(sentences)


# twitter 를 사용하여 단어 추출
twitter = Twitter()
nouns = []
for sentence in sentences:
    if sentence is not '':
        nouns.append(' '.join([noun for noun in twitter.nouns(str(sentence))
    if noun not in stopwords and len(noun) > 1]))

nouns

#명사로 이루어진 문장을 입력받아 sklearn의 TfidfVectorizer.fit_transform을 이용하여 tfidf matrix를 만든 후 Sentence graph를 return 한다.
tfidf = TfidfVectorizer()
tfidf_mat = tfidf.fit_transform(nouns).toarray()
graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
sent_graph  = graph_sentence

#단어들의 개수 세는 부분
cnt_vec = CountVectorizer()
cnt_vec_mat = normalize(cnt_vec.fit_transform(nouns).toarray().astype(float), axis=0)
vocab = cnt_vec.vocabulary_

words_graph = np.dot(cnt_vec_mat.T, cnt_vec_mat)
idx2word = {vocab[word] : word for word in vocab}

class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # diagonal 부분을 0으로
            link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}


rank = Rank()
sent_rank_idx = rank.get_ranks(sent_graph)

출처: https://excelsior-cjh.tistory.com/93 [EXCELSIOR]


#https://konlpy-ko.readthedocs.io/ko/v0.4.3/
import konlpy
from konlpy.utils import pprint
from konlpy.tag import Kkma
kkma = Kkma()
pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))

from konlpy.tag import Komoran
komoran = Komoran()
print(komoran.morphs(u'우왕 코모란도 오픈소스가 되었어요'))
print(komoran.nouns(u'오픈소스에 관심 많은 멋진 개발자님들!'))
print(komoran.pos(u'한글형태소분석기 코모란 테스트 중 입니다.'))



from collections import Counter

def scan_vocabulary(sents, tokenize, min_count=2):
    counter = Counter(w for sent in sents for w in tokenize(sent))
    counter = {w:c for w,c in counter.items() if c >= min_count}
    idx_to_vocab = [w for w, _ in sorted(counter.items(), key=lambda x:-x[1])]
    vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
    return idx_to_vocab, vocab_to_idx



from collections import defaultdict

def cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurrence=2):
    counter = defaultdict(int)
    for s, tokens_i in enumerate(tokens):
        vocabs = [vocab_to_idx[w] for w in tokens_i if w in vocab_to_idx]
        n = len(vocabs)
        for i, v in enumerate(vocabs):
            if window <= 0:
                b, e = 0, n
            else:
                b = max(0, i - window)
                e = min(i + window, n)
            for j in range(b, e):
                if i == j:
                    continue
                counter[(v, vocabs[j])] += 1
                counter[(vocabs[j], v)] += 1
    counter = {k:v for k,v in counter.items() if v >= min_cooccurrence}
    n_vocabs = len(vocab_to_idx)
    return dict_to_mat(counter, n_vocabs, n_vocabs)




import csv
 
import os
import pymysql

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


from krwordrank.word import KRWordRank
from konlpy.tag import Kkma
from konlpy.tag import Twitter

twitter = Twitter()
kkma = Kkma()
sql = "SELECT id, content FROM raw_table WHERE tag IS false AND publisher='보안뉴스'"
false_tags  = select_mydb(sql)
len(false_tags)
stopwords = ['보안','중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자","아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]


min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
wordrank_extractor = KRWordRank(min_count, max_length)
beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10
verbose = True
false_tag
for false_tag in false_tags:
    doc_id = false_tag[0]#도큐먼트 id 추출
    content = false_tag[1]
    sentences = kkma.sentences(content)#추출된 내용의 문장을 리스트로 나눔.

    nouns = []
    for sentence in sentences:
        if sentence is not '':
            nouns.append(' '.join([noun for noun in twitter.nouns(str(sentence))
        if noun not in stopwords and len(noun) > 1]))
    nouns

    wordrank_extractor = KRWordRank(min_count, max_length)
    keywords, rank, graph = wordrank_extractor.extract(nouns, beta, max_iter, verbose)
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
        print(doc_id)
        print('%8s:\t%.4f' % (word, r))




from krwordrank.sentence import summarize_with_sentences

for false_tag in false_tags:
    keywords, sents = summarize_with_sentences(
                                            texts, 
                                            stopwords = stopwords,
                                            num_keywords=100, 
                                            num_keysents=10
                                            )
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:7]:
        #print('%8s:\t%.4f' % (word, r))
        print('#%s' % word)



false_tags[0]
is_exists

from krwordrank.word import KRWordRank

min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
wordrank_extractor = KRWordRank(min_count, max_length)

beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10
verbose = True
texts = sentences
keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, verbose)
texts
for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    print('%8s:\t%.4f' % (word, r))



from krwordrank.sentence import summarize_with_sentences



from konlpy.tag import Kkma
from konlpy.tag import Okt

kkma = Kkma()
okt = Okt()

import sys
import os
import re
sys.path.append(os.path.dirname('PyKoSpacing/'))
from pykospacing import spacing

def preprocessing(review, name):
    total_review = ''
    #인풋리뷰
    for idx in range(len(review)):
        r = review[idx]
        #하나의 리뷰에서 문장 단위로 자르기
        sentence = re.sub(name.split(' ')[0],'',r)
        sentence = re.sub(name.split(' ')[1],'',sentence)
        sentence = re.sub('\n','',sentence)
        sentence = re.sub('\u200b','',sentence)
        sentence = re.sub('\xa0','',sentence)
        sentence = re.sub('([a-zA-Z])','',sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',sentence)
        if len(sentence) == 0:
            continue
        sentence = okt.pos(sentence, stem = True)
        word = []
        for i in sentence:
            if not i[1] == 'Noun':
                continue
            if len(i[0]) == 1:
                continue
            word.append(i[0])
        word = ' '.join(word)
        word += '. '
        total_review += word
    return total_review
