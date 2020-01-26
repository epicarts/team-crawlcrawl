import re
import csv
import os
from konlpy.tag import Komoran

komoran = Komoran(userdic='./user_dic.txt')

text = "그렇지만 암호화시킨 메일을 애플이 임의로 복호화 해서 저장해두고 있다는 것 자체는 중요한 문제일 수 있다. “특히 애플처럼 보안과 프라이버시 보호가 1순위의 가치인 것처럼 스스로를 포장하고 있는 회사가 할 짓은 전혀 아니죠."
def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)

def sentence_preprocessing(text):
    '''
    글을 넣으면
    1. 문장 나누기 (수동)
    2. 단어 추출 (okt.pos)
    '''
    text = xplit('. ', '? ', '! ', '\n', '.\n')(text.strip()) #수동으로 문장 구분

    sentences = []
    for sentence in text:
        sentence = re.sub('([a-zA-Z])','',sentence)#알파벳 제거
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)#
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\(\)\[\]\<\>`\'…》]','',sentence)
        if len(sentence) == 0:
            continue
        print(sentence)
        sentence = komoran.nouns(sentence)#분류
        
        #1글자인 단어 제외
        words = []
        for word in sentence:
            if len(word) == 1:
                continue
            words.append(word)
        #print(words)#['애플', '보안과', '프라이버시', '보호', '순위', '가치', '스스로', '포장', '회사']

        words_dot = ' '.join(words)# + '. '#점찍기
        sentences.append(words_dot)         
    return sentences

a = sentence_preprocessing(text)
print(a)