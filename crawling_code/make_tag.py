import konlpy
from konlpy.utils import pprint
from konlpy.tag import Kkma
kkma = Kkma()
pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))

#https://konlpy-ko.readthedocs.io/ko/v0.4.3/

from konlpy.tag import Komoran
komoran = Komoran()
print(komoran.morphs(u'우왕 코모란도 오픈소스가 되었어요'))
print(komoran.nouns(u'오픈소스에 관심 많은 멋진 개발자님들!'))
print(komoran.pos(u'한글형태소분석기 코모란 테스트 중 입니다.'))
