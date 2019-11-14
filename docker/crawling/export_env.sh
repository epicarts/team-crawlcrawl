#!/bin/bash
# export all environment variables to use in cron
# crontab에 사용하기 위한 환경변수 추출
env | sed 's/^\(.*\)$/export \1/g' > /root/envs.sh
chmod +x /root/envs.sh
cron -f