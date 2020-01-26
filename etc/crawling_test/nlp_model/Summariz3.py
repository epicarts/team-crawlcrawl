#https://blog.theeluwin.kr/post/146188165713/summariz3 참고


from konlpy.tag import Kkma

kkma = Kkma()
kkma.sentences
kkma.sentences("이세돌은 알파고를 이겼다. 이세돌은 강하다. 알파고도 짱쎔.")# 문장 찾기로 이용.
# ['이세 돌은 알 파고를 이겼다.', '이세 돌은 강하다.', '알 파고도 짱 쎔.'] <- 자동으로 pos 분류가 됨

from konlpy.tag import Okt
okt = Okt()
okt.nouns("미쿠 미쿠 하게 해줄게")#['미쿠', '미쿠'] <= 단어 분류기
kkma.nouns("미쿠 미쿠 하게 해줄게")#['미쿠', '미쿠'] <= 단어 분류기

okt.nouns("이세돌은 알파고를 이겼다. 이세돌은 강하다. 알파고도 짱쎔.")#['이세돌', '알파', '이세돌', '알파', '고도']
kkma.nouns("이세돌은 알파고를 이겼다. 이세돌은 강하다. 알파고도 짱쎔.")# ['이세', '이세돌', '돌', '파고']


#이를 토대로 우리가 좀 더 원하는건 okt(twitter) 인듯


from collections import Counter


kkma_candidates = kkma.sentences(content)
nouns = okt.nouns(content)

from krwordrank.sentence import summarize_with_sentences


keywords, sents = summarize_with_sentences(
                                        nouns,
                                        num_keywords=100, 
                                        num_keysents=1
                                        )


import re
from collections import Counter


#널리 알려진 한국어 형태소 분석기들 중에선 빠르고 적절하며 원문을 보존하며 문장 구분을 해주는 기능이 구현된게 없고 
def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)

xplit('. ', '? ', '! ', '\n', '.\n')("This is a sentence. Here is another sentence.\nHello, world!")

class Sentence:

    @staticmethod
    def co_occurence(sentence1, sentence2):
        p = sum((sentence1.bow & sentence2.bow).values())
        q = sum((sentence1.bow | sentence2.bow).values())
        return p / q if q else 0

    def __init__(self, text, index=0):
        self.index = index
        self.text = text
        self.nouns = okt.nouns(self.text)
        self.bow = Counter(self.nouns)

    def __eq__(self, another):
        return hasattr(another, 'index') and self.index == another.index

    def __hash__(self):
        return self.index




user_candidates = xplit('. ', '? ', '! ', '\n', '.\n')(content.strip()) #수동으로 문장 구분

result = []
for sentence in user_candidates:
    sentence = re.sub('([a-zA-Z])','',sentence)#알파벳 제거
    sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)#
    sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\(\)\[\]\<\>`\'…》]','',sentence)
    if len(sentence) == 0:
        continue
    sentence = okt.pos(sentence, stem = True)#분류
    result.append(sentence)


len(result)
len(user_candidates)

get_sentences
for user_candidate in user_candidates:
    candidate = user_candidate.strip() #앞뒤 빈칸 제거




len(user_candidates)
len(kkma_candidates)

for i in user_candidates:
    print(i)

for i in kkma_candidates:
    print(i)

    
sentences = []


def get_sentences(text):
    candidates = xplit('. ', '? ', '! ', '\n', '.\n')(text.strip())
    sentences = []
    index = 0
    candidates

    for candidate in candidates:
        candidate = candidate.strip()
        if len(candidate):
            sentences.append(Sentence(candidate, index))
            index += 1
    return sentences


sentences = get_sentences(content)
sentences


content = '''다크웹 아동음란물 사건 보도되면서 다크웹에 관심 높아지고 유입 늘어ㅋㅋㅋㅋ ㅋㅎㅎㅎ
 신종 랜섬웨어 ‘Recoil’ 다크웹에서 유통 정황
 
 [보안뉴스 원병철 기자] 지난 10월, 32개국 경찰이 공조해 검거된 다크웹 아동음란물 유통 사이트의 운영자와 상당수의 이용자가 한국인으로 밝혀지면서 다크웹에 대한 사람들의 관심이 높아졌다. 특히, 다크웹에서 아동음란물은 물론 마약에 랜섬웨어까지 유통하는 것으로 알려지면서 이에 대한 위험성이 높아지고 있다.
 
 
 ▲다크웹에서 거래되는 신종 랜섬웨어 ‘Recoil’[자료=보안뉴스]
 
 익명의 보안전문가에 따르면 11월 둘째 주, 신종 랜섬웨어인 ‘Recoil’ 랜섬웨어를 판매하는 사이트가 다크웹에서 발견됐다. 실제로 유포됐는지는 아직 확인되지 않았지만, 이미 다크웹에서 랜섬웨어가 판매되는 일이 비일비재했으며, 이렇게 판매된 랜섬웨어는 시간이 지나면 필드에서 발견됐기 때문에 Recoil 랜섬웨어 역시 가까운 시일 내에 유통될 것으로 보인다.
 
 
 ▲판매자가 설명한 랜섬웨어 ‘Recoil’의 주요 특징[자료=보안뉴스]
 
 판매자는 Recoil 랜섬웨어를 판매하면서 △탐지되지 않으며(Undetectable) △매우 빠르고(Very Fast) △사이즈도 작다(Small in Size)는 등 랜섬웨어의 ‘장점’을 설명하면서 가격을 ‘1,000달러(약 116만원)’로 책정했다. 아울러 궁금증이 있으면 언제든 물어보라고 친절하게 덧붙였다. 제보자에 따르면 판매자가 데모로 공개한 랜섬웨어 감염 영상은 2019년 11월 11일에 제작됐다.
 
 한편, 이번 아동음란물 사건으로 인해 일반인에까지 다크웹이 알려지면서 다크웹에 유입되는 사람들도 늘고 있는 것으로 알려졌다. 과거 웹하드와 토렌트 등 파일공유 서비스를 이용하던 사람들이 다크웹에 관심을 갖기 시작한 것으로 보인다. 실제로 최근 텔레그램 링크공유방에서는 다크웹 한국 마약거래 사이트 주소도 공유되고 있으며, 다크웹 한국 채널중 한 곳은 누적 방문자수가 60만 명을 돌파한 것으로 알려졌다.
 [원병철 기자(boanone@boannews.com)]
 <저작권자: 보안뉴스(www.boannews.com) 무단전재-재배포금지>'''


sentence = content


 def sentence_reprocessing(review, name):
    total_review = ''
    #인풋리뷰
    for idx in content:
        r = review[idx]
        #하나의 리뷰에서 문장 단위로 자르기
        sentence = re.sub('\n','',sentence)
        sentence = re.sub('\u200b','',sentence)
        sentence = re.sub('\xa0','',sentence)
        sentence = re.sub('([a-zA-Z])','',sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\(\)\[\]\<\>`\'…》]','',sentence)
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