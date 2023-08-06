import http.client
import json
import time

client = None
headers = None
srv = None


def client_init(config_file: dict):
    global client
    global headers
    if config_file['https']:
        client = http.client.HTTPSConnection(config_file['host'], 443, check_hostname=not config_file['ignore_ssl'])
    else:
        client = http.client.HTTPConnection(config_file['host'], 80)
    headers = {"Authorization": f"Bearer {config_file['api_key']}", "Content-Type": "application/json",
               "Accept": "Application/vnd.pterodactyl.v1+json"}


def get_server():
    global srv
    srv = {
        "name": [],
        "id": [],
        "memory": [],
        "cpu": [],
        "disk": [],
        "rx": [],
        "tx": [],
        "uptime": [],
        "max_memory": [],
        "max_swap" :[],
        "max_disk": [],
        "io": [],
        "max_cpu": []
    }
    client.request("GET", "/api/client/", "", headers)
    servers = json.loads(client.getresponse().read())
    if "errors" in servers:
        print(servers)
        time.sleep(10)
        get_server()
    for x in servers['data']:
        srv["name"].append(x['attributes']['name'])
        srv["id"].append(x['attributes']['identifier'])
        srv["max_memory"].append(x['attributes']['limits']['memory'])
        srv["max_swap"].append(x['attributes']['limits']['swap'])
        srv["max_disk"].append(x['attributes']['limits']['disk'])
        srv["io"].append(x['attributes']['limits']['io'])
        srv["max_cpu"].append(x['attributes']['limits']['cpu'])


def get_metrics():
    for x in srv["id"]:
        client.request("GET", f"/api/client/servers/{x}/resources", "", headers)
        response = json.loads(client.getresponse().read())
        if "errors" in response:
            print(response)
            time.sleep(10)
            get_metrics()
        metrics = response["attributes"]['resources']
        srv["memory"].append(metrics["memory_bytes"]/1000000)
        srv["cpu"].append(metrics["cpu_absolute"])
        srv["disk"].append(metrics["disk_bytes"]/1000000)
        srv["rx"].append(metrics["network_rx_bytes"]/1000000)
        srv["tx"].append(metrics["network_tx_bytes"]/1000000)
        srv["uptime"].append(metrics["uptime"])
    return srv
