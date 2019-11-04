from prometheus_client import start_http_server, Summary, Gauge
import requests
import json
import time

CONFIG_GETH_HOST = "127.0.0.1"
CONFIG_GETH_PORT = 22000

# prometheus metrics
geth_net_listening = Gauge('geth_net_listening', 'Is geth syncing or not')
geth_latest_block = Gauge('geth_latest_block', 'Latest block number')
geth_net_peer_count = Gauge('geth_net_peer_count', 'Geth peers count')
geth_txpool_status_queued = Gauge('geth_txpool_status_queued', '')
geth_txpool_status_pending = Gauge('geth_txpool_status_pending', '')

def geth_json_rpc(geth_host, geth_port, method, params):
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': 1
    }

    geth_url = "http://" + geth_host + ":" + str(geth_port)
    try:
        r = requests.post(geth_url, data = json.dumps(body), headers=headers)
    except requests.ConnectionError as e:
        return(-1)
    else:
        res_dict = r.json()
        return(res_dict['result'])

def geth_collect_metrics():
    net_listening = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_listening", [])
    if net_listening != -1:
        geth_net_listening.set(int(net_listening))

    latest_block = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "eth_blockNumber", [])
    if latest_block != -1:
        geth_latest_block.set(int(latest_block, 16))

    net_peerCount = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_peerCount", [])
    if net_peerCount != -1:
        geth_net_peer_count.set(int(net_peerCount, 16))

    txpool_status = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "txpool_status", [])
    if txpool_status != -1:
        txpool_status_queued = int(txpool_status['queued'], 16)
        geth_txpool_status_queued.set(txpool_status_queued)
        txpool_status_pending = int(txpool_status['pending'], 16)
        geth_txpool_status_queued.set(txpool_status_queued)
        geth_txpool_status_pending.set(txpool_status_pending)

if __name__ == '__main__':
    # Start up the server to expose the metrics
    start_http_server(8000)
    #Refresh Block metrics
    while True:
        geth_collect_metrics()
        time.sleep(1)
