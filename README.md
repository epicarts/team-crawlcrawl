# team-crawlcrawl
* 2019 캡스톤 디자인 깃허브 페이지
* 여러 보안뉴스 사이트에서 자동으로 페이지를 크롤링하여, 엘라스틱서치에 저장 후 키바나로 시각화

# **docker 설치**
* 운영체제: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
* 설치 사전 준비
```sh
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
```

* Docker 설치하기
```sh
sudo apt-get install docker-ce
```

* docker-compose 설치하기
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

# **docker-compose-elasticsearch-kibana-crawling**
* elasticsearch == 7.3.2
* python == 3.6.8
* kibana == 7.3.2

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
