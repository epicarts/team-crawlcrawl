from NAVER_News_Crawler import NaverNews_Crawler
from BOAN_News_Crawler import BoanNews_Crawler

class CrawlerController:
	def init(self):
		self.version = 0.1
		self.ProgramName = "Web Crawler"

		self.Crawler_Handles = []
    self.Handles_Len = 0
    self.search_string = ""
    
	def Load_Module(self):
		#Load Naver News Crawler
    self.Crawler_Handles.append( NaverNews_Crawler() )
	    
    #Load Boan News Crawler
    self.Crawler_Handles.append( BoanNews_Crawler() )
	
    #Set Handles Count
    self.Handles_Len = len( self.Crawler_Handles )

	def Print_Result(self, data):
    for idx_num, news in enumerate( data ):
      print( "[{}] {}".format(idx_num, news.text) )
      print("")

	def Set_Search_String(self, input_str):
    #Set Search String
    self.search_string = input_str

	def Run(self):
    #Check Search String
    if self.search_string == "":
      print("[Error!!] Run Set_Search_String() First")
      return
    
	  #Execute crawler modules sequentially
	  for i in range(0, self.Handles_Len ):
      self.Crawler_Handles[i].Print_Module_Name()

      data = self.Crawler_Handles[i].run( self.search_string )
      self.Print_Result(data)

if name == "main":
	clsHandler = CrawlerController()
	clsHandler.Load_Module()

	clsHandler.Set_Search_String("랜섬웨어")
	clsHandler.Run()