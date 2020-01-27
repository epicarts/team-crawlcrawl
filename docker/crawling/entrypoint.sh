echo "start entrypoint.sh!!!!!"
dockerize -wait tcp://db:3306 -wait http://elasticsearch:9200 -timeout 50s
echo "start!! crawling docker image!!!!"

python create_mysql_table.py
python init_mapping.py

env | sed 's/^\(.*\)$/export \1/g' > /root/envs.sh
chmod +x /root/envs.sh
chmod 0644 /etc/cron.d/cron_config
crontab /etc/cron.d/cron_config
touch /var/log/crawler.log

cron && tail -f /var/log/crawler.log
echo "end entrypoint.sh!!!!!"
