import argparse
import pprint
import re as regex
from elastic_api import ElasticAPI

# --------------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    prog="bats' ELK-Logs",
    description='Application to analye your ssh logs.',
    epilog='github.com/batscs/docker-elk-logs')

parser.add_argument('host_name')

parser.add_argument('elastic_domain')

parser.add_argument('elastic_api_key')

parser.add_argument('elastic_index_name')

parser.add_argument('-o', '--offline', action='store_true',
                    help="dont upload data to elasticsearch endpoint")

parser.add_argument('-v', '--verbose', action='store_true',
                    help="show debug & informational messages")

args = parser.parse_args()

# If false no debug prints will appear
debug = args.verbose

# If false no data will be submitted to ElasticSearch, used for debugging pre-upload
elastic_upload = not args.offline  # Default: True

# ElasticSearch Deployment Server
elastic_domain = args.elastic_domain

# ElasticSearch API Key with Kibana Authorization
elastic_api_key = args.elastic_api_key

# ElasticSearch Index Name
elastic_index_name = args.elastic_index_name

host_name = args.host_name

# --------------------------------------------------------------------------------------------------------------------------------

elastic = ElasticAPI(elastic_domain, elastic_api_key, elastic_index_name, debug=debug, connect=elastic_upload)
pp = pprint.PrettyPrinter(indent=4)

log_file = "/app/auth.log"

# --------------------------------------------------------------------------------------------------------------------------------

def main():

    data = analyze_logs(log_file)

    if debug: print(f"Logs fetched: {len(data)}")

    for value in data:
        elastic.append_data(value)

    elastic.submit_data()


# --------------------------------------------------------------------------------------------------------------------------------

def analyze_logs(log_file):
    result = []

    # Invalid User
    # Feb  8 02:17:00 mirage sshd[1877465]: Invalid user pi from 97.74.91.249 port 45894
    pattern1 = rf"(.*) {host_name} sshd.*: Invalid user (.*) from (.*) port (.*)\n"

    # Authenticating User
    # Feb  8 02:17:00 mirage sshd[1877463]: Connection closed by authenticating user root 97.74.91.249 port 45890 [preauth]
    pattern2 = rf"(.*) {host_name} sshd.*: Connection closed by authenticating user (.*) (.*) port (.*) \[preauth\]"

    # Publickey accepted
    # Feb  8 18:25:00 mirage sshd[2501738]: Accepted publickey for bats from 95.112.86.9 port 60687 ssh2: ED25519 SHA256:fCiUPT3Epk+PKYSDtCjQUHUGvaKwtX1kRsxxaJeb5v0
    pattern3 = rf"(.*) {host_name} sshd.*: Accepted publickey for (.*) from (.*) port (.*) ssh2: (.*)"

    for line in open(log_file):

        match1 = regex.search(pattern1, line)
        match2 = regex.search(pattern2, line)
        match3 = regex.search(pattern3, line)

        value = {}

        if bool(match1):
            value["@timestamp"] = match1.group(1)
            value["user"] = match1.group(2)
            value["ip"] = match1.group(3)
            value["geopoint"] = ip_to_geopoint(value["ip"])
            value["port"] = match1.group(4)
            value["type"] = "invalid_user"
            value["host"] = host_name
            result.append(value)
        elif bool(match2):
            value["@timestamp"] = match2.group(1)
            value["user"] = match2.group(2)
            value["ip"] = match2.group(3)
            value["geopoint"] = ip_to_geopoint(value["ip"])
            value["port"] = match2.group(4)
            value["type"] = "invalid_ssh"
            value["host"] = host_name
            result.append(value)
        elif bool(match3):
            value["@timestamp"] = match3.group(1)
            value["user"] = match3.group(2)
            value["ip"] = match3.group(3)
            value["geopoint"] = ip_to_geopoint(value["ip"])
            value["port"] = match3.group(4)
            value["pubkey"] = match3.group(5)
            value["type"] = "valid_pubkey"
            value["host"] = host_name
            result.append(value)

    # Clear Content of File (old ssh auth logs)
    open(log_file, "w").close()
    
    return result

# --------------------------------------------------------------------------------------------------------------------------------

def ip_to_geopoint(ip_address):
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result = json.loads(result)
    return str(result["latitude"]) + "," + str(result["longitude"])

# --------------------------------------------------------------------------------------------------------------------------------

# Execute main()-function if this script is being run as a standalone
if __name__ == '__main__':
    main()
