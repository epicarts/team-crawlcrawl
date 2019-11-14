#안랩의 최신보안뉴스 크롤링.
#여러 뉴스사이트에서 보안 관련된 뉴스를 가져와 안랩의 최신보안뉴스에 게시해놓은 기사를 크롤링하였다.
#안랩이 가져온 기사인만큼 정확도와 신뢰도가 높다고 판단하여 해당 기사를 크롤링
  

from requests_html import HTMLSession

import urllib.parse as url_parse

session = HTMLSession()
f = open("ahnlab_news.txt", "w", encoding='UTF-8')
r = session.get('https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsView.do?curPage=&menu_dist=1&seq=28695&key=&dir_group_dist=&dir_code=&searchDate=')


class AhnLab_Crawler:
    def __init__(self):
        self.Module_Name = "AhnLab Crawler"
        self.Version = 0.1
        
        self.session = HTMLSession()
        self.tag_selector = 'body > div.wrap > div#container > form#secuNewsViewForm > div.contents > div.bbsView > div.bbsViewCont > p'
        self.site_url = 'https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsView.do?curPage=&menu_dist=1&seq=28695&key=&dir_group_dist=&dir_code=&searchDate='
        
    def Print_Module_Name(self):
        print( self.Module_Name +"\r\n" )

    def run(self, search_str):        
        r = self.session.get( self.site_url)
        r.html.render()
        return r.html.find( self.tag_selector )

        
    
if __name__ == "__main__":
    
    test = AhnLab_Crawler()

    for line in r.html.find('h1.tit'):
        print(line.text)
        print("")
        f.write(line.text)


    retn_data = test.run("")

    f.write("\n")
    for line in retn_data:
        print(line.text)
        f.write(line.text)

f.close()
