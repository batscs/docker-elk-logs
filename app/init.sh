echo "*/5 * * * * python3.11 /app/app.py -v $host_name $elastic_domain $elastic_api_key $elastic_index_name > /app/data/app.log" > /app/app.cron
crontab /app/app.cron
cron -f
