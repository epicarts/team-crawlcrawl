#kisa 자료실의 최신동향 크롤링
#정확도와 신뢰성이 있는 자료라서 크롤

from requests_html import HTMLSession

session = HTMLSession();
r = session.get('https://www.krcert.or.kr/data/trendView.do?bulletin_writing_sequence=35110')
tag_sel='body > div#wrap > div#contentWrap > div.widthWrap > div#contentDiv.contents > table.basicView > tbody > tr > th.bg_tht'
tag_sel2='body > div#wrap > div#contentWrap > div.widthWrap > div#contentDiv.contents > table.basicView > tbody > tr > td.cont'

f = open("kisa_data.txt", "w", encoding='UTF-8')

#Get News Title & Content Summary
for line in r.html.find(tag_sel):
	print(line.text)
	print("\n")
	f.write(line.text)

for line1 in r.html.find(tag_sel2):
	print(line1.text)
	print("\n")
	f.write(line1.text)

f.close()
