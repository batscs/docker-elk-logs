<table>
  <tr>
    <td> <img src="https://github.com/batscs/cloudflare-dns-sync/assets/31670615/58296fbd-9a48-4263-a491-308e49035aba" alt="image" width="130" height="auto"> </td>
    <td><h1>bats' Docker-ELK-Logs</h1></td>
  </tr>
</table>

### Table of Contents  
[Introduction](#introduction)  
[Installation](#installation)  
[Dashboard](#dashboard)  
[Known Issues](#help)  

<a name="introduction"/>

## Introduction
Like what you see? 👀 Consider leaving a GitHub Star! ⭐  
  
![image](https://github.com/batscs/docker-elk-logs/assets/31670615/f964db21-f676-4634-8ae5-961c438f9228)

Container to scrape all of your SSH Auth Logs and send relevant data to ElasticSearch to display attempted failed logins to your Server.

If you need help or run into problems feel free to open an issue for this repository.

#### Features:
- Automatic deployment to a docker container using docker-compose
- Automatic of scraping of auth.log file contents from the host machine
- Automatic IP-Adress to GeoPoint convertion for ElasticSearch.
- Premade Dashboard deployment

#### Requirements:
- Docker
- Docker-Compose
- Linux Host Machine
- [Syslog Timestamp Configuration](#requirement)  

<a name="requirement"/>

#### Syslog Timestamp configuration

Edit your rsyslog.conf file, this location might vary depending on the OS, in Ubuntu the file is located at `/etc/rsyslog.conf`

Find the following line and uncomment the line as shown here, then save it.
```
#
# Use traditional timestamp format.
# To enable high precision timestamps, comment out the following line.
#
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
```

Restart the rsyslog service to apply the new config. All your new logs will be in the precise ISO8601 Timestamp.
```
systemctl restart rsyslog
```

<a name="installation"/>

## Installation

Download the `docker-compose.yml` file
```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/batscs/docker-elk-logs/main/docker-compose.yml
```

Configure the docker-compose.yml for your ELK-Stack Configuration
It is recommended to keep sshlogs-0001 as the index name for compatibility with the provided dashboard.
```yml
environment:
  - host_name=change_me
  - elastic_domain=http://elasticsearch:9200
  - elastic_api_key=change_me
  - elastic_index_name=sshlogs-0001
```

Run the Container
```bash
docker-compose up -d
```

<a name="dashboard"/>

## Dashboard
You can import the dashboard from the screenshot at the beginning of this README if you follow these steps:

1. Download the `dashboard.ndjson` file from this github repository.
2. Open your Kibana Web UI.
3. Go to Stack Management -> Kibana (on the left) -> Saved Objects
4. At the top right click on `Import` and upload the dashboard.ndjson file

<a name="help"/>

## Tips & Help

#### Docker Networking
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
