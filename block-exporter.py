import requests
import json

#dict_headers = {
#    "Content-Type": "application/json"
#}

#my_data = {"jsonrpc": "2.0", "method": "web3_clientVersion", "params": [], "id": 1}
#my_data = {'jsonrpc': '2.0', 'method': 'web3_clientVersion', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'eth_syncing', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'txpool_status', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'rpc_modules', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'eth_blockNumber', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'net_listening', 'params': [], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'eth_getBlockByNumber', 'params': ['0x67c', True], 'id': 1}
#my_data = {'jsonrpc': '2.0', 'method': 'eth_pendingTransactions', 'params': [], 'id': 1}

#r = requests.post('http://127.0.0.1:22000', data = json.dumps(my_data), headers=dict_headers)
#response_dic = r.json()
#print(response_dic)

CONFIG_GETH_HOST = "127.0.0.1"
CONFIG_GETH_PORT = 22000

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
    #r = requests.post(geth_url, data = json.dumps(body), headers=headers)
    #return(r.json())
    # mock response now
    if method == "net_listening":
        r = True
    elif method == "eth_blockNumber":
        r = '0x67c'
    elif method == "net_peerCount":
        r = '0x6'
    elif method == "txpool_status":
        r = {u'queued': u'0x14', u'pending': u'0x0'}

    return(r) 

def geth_collect_metrics():
    net_listening = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_listening", [])
    print(net_listening)
    latest_block = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "eth_blockNumber", [])
    print(int(latest_block, 16))
    net_peerCount = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_peerCount", [])
    print(int(net_peerCount, 16))
    txpool_status = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "txpool_status", [])
    txpool_status_queued = int(txpool_status['queued'], 16)
    txpool_status_pending = int(txpool_status['pending'], 16)
    print(txpool_status_queued)
    print(txpool_status_pending)

if __name__ == '__main__':
    # Start up the server to expose the metrics
    #start_http_server(8000)
    # Refresh Block metrics
    #while True:
    #  process_request(random.random())
    geth_collect_metrics() 
