from requests_html import HTMLSession

class BoanNews_Crawler:
	def init(self):
		self.Module_Name = "BoanNews Crawler"
		self.Version = 0.1

		self.session = HTMLSession();
    self.site_url = '<https://www.boannews.com/media/s_list.asp?skind=5>'

def Print_Module_Name(self):
    print( self.Module_Name +"\\r\\n" )
    
def run(self, search_str):     
    r = self.session.get( self.site_url)
    
    return r.html.find('.news_txt')