import sys
import tweepy

# http://blog.naver.com/PostView.nhn?blogId=nonamed0000&logNo=220912854545&parentCategoryNo=&categoryNo=26&viewDate=&isShowPopularPosts=false&from=section

CONSUMER_KEY = ' '
CONSUMER_SECRET = ' ' 
ACCESS_TOKEN_KEY = ' '
ACCESS_TOKEN_SECRET = ' ' 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token()

import tweepy

# 트위터 앱의 Keys and Access Tokens 탭 참조(자신의 설정 값을 넣어준다)
consumer_key = ###
consumer_secret = ###

# 1. 인증요청(1차) : 개인 앱 정보 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = ###
access_token_secret= ###

# 2. access 토큰 요청(2차) - 인증요청 참조변수 이용
auth.set_access_token(access_token, access_token_secret)

# 3. twitter API 생성  
[출처] #파이썬. Python으로 트위터 크롤링(twitter crawling)하기|작성자 안재형

