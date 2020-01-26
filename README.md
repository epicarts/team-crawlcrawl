# team-crawlcrawl
> 보안뉴스 실시간 크롤링 및 데이터 시각화 (2019 캡스톤 디자인 프로젝트)

몇몇의 보안뉴스 사이트에서 자동으로 페이지를 크롤링하여, 엘라스틱서치에 저장 후 키바나로 시각화하였습니다.

![kibana](https://user-images.githubusercontent.com/17478634/73137801-6fecf780-409f-11ea-9dd2-98edc122db62.PNG)


## 개발환경
> Docker 를 사용하여 환경 구성

* logstash == 7.3.2
* elasticsearch == 7.3.2
* kibana == 7.3.2
* python == 3.6.8
* mysql == 8.0.18

## 프로젝트 구성도
![flowchart](https://user-images.githubusercontent.com/17478634/73138072-ee4a9900-40a1-11ea-8d69-46f2fddff5f8.PNG)
### 순서
	1. 뉴스 데이터를 일정시간 마다 자동으로 데이터 크롤링
	2. 수집한 데이터를 MySQL에 저장.
	3. MySQL에 저장된 뉴스 데이터에서 키워드 3개 추출 후 다시 MySQL에 저장. 
	4. Logstash를 사용하여 MySQL 데이터를 ElasticSearch에 저장
	5. Kibana를 통해서 ElasticSearh에 저장된 데이터를 시각화 
	6. 웹페이지를 통해 사용자에게 검색 서비스 제공(미구현)


# 실행 방법
* 운영체제: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
## 1. 설치 사전 준비
```sh
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
```
## 2. Docker 설치하기
```sh
sudo apt-get install docker-ce
```

## 3. Docker-compose 설치하기
* docker-compose 설치하기
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

# **docker-compose-elasticsearch-kibana-crawling**


# **docker-compose command**
`docker-compose up`
도커 컴포즈 실행 명령어 

`docker-compose up --build`
도커 컴포즈 실행 및 빌드

`docker ps`
현재 도커 컨테이너 상태를 보여줌

`docker exec -it 실행중인 컨테이너 이름 /bin/bash`
현재 실행되고 있는 도커 컨테이너의 bash 쉘 실행

# **nori analyzer**
- 한국에 분석 플러그인 노리(nori)
- userdict_ko.txt에 원하는 단어를 추가 시킬 수 있다. (docker-compose.yml 파일 참고)

# Kibana Dashboard 셋팅법
- 블로그 참고: 
