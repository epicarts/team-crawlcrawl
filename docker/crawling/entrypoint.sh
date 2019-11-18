echo "success entrypoint.sh!!!!!"
env | sed 's/^\(.*\)$/export \1/g' > /root/envs.sh
chmod +x /root/envs.sh

chmod 0644 /etc/cron.d/cron_config
crontab /etc/cron.d/cron_config
touch /var/log/crawler.log

cron && tail -f /var/log/crawler.log