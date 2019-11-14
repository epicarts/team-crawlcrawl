from requests_html import HTMLSession

session = HTMLSession();
r = session.get('http://isaa.re.kr/index.php?page=view&pg=1&idx=161&hCode=BOARD&bo_idx=4&sfl=&stx=')
tag_sel='body > div#wrapper > div#container > div#content > div#con_area > table.board_Vtable > thead > tr > th'

f = open("isaa_news.txt", "w", encoding='UTF-8')

#Get News Title & Content Summary
for line in r.html.find(tag_sel):
	print(line.text)
	print("\n")
	f.write(line.text)

for line1 in r.html.find('div.board_content'):
	print(line1.text)
	print("\n")
	f.write(line1.text)

f.close()
