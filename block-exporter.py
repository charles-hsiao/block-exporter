from prometheus_client import start_http_server, Summary, Gauge, Counter
import requests
import json

CONFIG_GETH_HOST = "127.0.0.1"
CONFIG_GETH_PORT = 22000

# prometheus metrics
geth_net_listening = Gauge('geth_net_listening', 'Is geth syncing or not')
geth_latest_block = Counter('geth_latest_block', 'Latest block number')
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
    r = requests.post(geth_url, data = json.dumps(body), headers=headers)
    res_dict = r.json()
    return(res_dict['result'])
    # mock response now
    #if method == "net_listening":
    #    r = True
    #elif method == "eth_blockNumber":
    #    r = '0x67c'
    #elif method == "net_peerCount":
    #    r = '0x6'
    #elif method == "txpool_status":
    #    r = {u'queued': u'0x14', u'pending': u'0x0'}

    return(r) 

def geth_collect_metrics():
    net_listening = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_listening", [])
    geth_net_listening.set(int(net_listening))

    latest_block = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "eth_blockNumber", [])
    geth_latest_block.inc(int(latest_block, 16))

    net_peerCount = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_peerCount", [])
    geth_net_peer_count.set(int(net_peerCount, 16))   

    txpool_status = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "txpool_status", [])
    txpool_status_queued = int(txpool_status['queued'], 16)
    txpool_status_pending = int(txpool_status['pending'], 16)
    geth_txpool_status_queued.set(txpool_status_queued)
    geth_txpool_status_pending.set(txpool_status_pending)

if __name__ == '__main__':
    # Start up the server to expose the metrics
    start_http_server(8000)
    #Refresh Block metrics
    while True:
        geth_collect_metrics() 
