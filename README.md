# docker-elk-logs

## Introduction
![image](https://github.com/batscs/docker-elk-logs/assets/31670615/f964db21-f676-4634-8ae5-961c438f9228)

## Requirement

`/etc/rsyslog.conf`

```
#
# Use traditional timestamp format.
# To enable high precision timestamps, comment out the following line.
#
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
```

```
systemctl restart rsyslog
```

## Installation
It is recommended to keep sshlogs-0001 as the index name for compatibility with the provided dashboard.
```yml
environment:
  - host_name=change_me
  - elastic_domain=http://elasticsearch:9200
  - elastic_api_key=change_me
  - elastic_index_name=sshlogs-0001
```

```bash
docker-compose up -d
```

## Dashboard

## Tips & Help

#### ElasticSearch-Server on Host Machine
If your ElasticSearch Server is running on the same machine as this container, you can use the container name (or service name) instead of a hardcoded IP/Domain. You must ensure both containers are running in the same network to ensure connectivity.

Add the network at the very bottom of this `docker-compose.yml`.
```yml
networks:
  elk-net:
    external: true
    name: name_of_elastic_network
    driver: bridge
```

And let this container use the network.
```yml
services:
  bats-elk-logs:
    # ...
    networks:
      - elk-net
    environment:
      - elastic_domain=http://<name_of_elasticsearch_container>:9200
    # ...
```
