from prometheus_client import start_http_server, Summary, Gauge
import requests
import json
import time

CONFIG_GETH_HOST = "127.0.0.1"
CONFIG_GETH_PORT = 22000

# Global variables
BLOCK_NUMBER = 0
SUM_TRANSACTIONS = 0

# prometheus metrics
geth_net_listening = Gauge('geth_net_listening', 'Is geth syncing or not')
geth_latest_block = Gauge('geth_latest_block', 'Latest block number')
geth_net_peer_count = Gauge('geth_net_peer_count', 'Geth peers count')
geth_txpool_status_queued = Gauge('geth_txpool_status_queued', 'Queued transactions in transaction pool')
geth_txpool_status_pending = Gauge('geth_txpool_status_pending', 'Pending transactions in transaction pool')
geth_transaction_processed = Gauge('geth_transaction_processed', 'Transaction processed summary')

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

def geth_collect_metrics(last_block_number):
    # Weather the nodes is listen to other nodes or not
    net_listening = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_listening", [])
    if net_listening != -1:
        geth_net_listening.set(int(net_listening))
    else:
        geth_net_listening.set(0)

    # The block height
    latest_block = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "eth_blockNumber", [])
    if latest_block != -1:
        geth_latest_block.set(int(latest_block, 16))

    # The connected peer count
    net_peerCount = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "net_peerCount", [])
    if net_peerCount != -1:
        geth_net_peer_count.set(int(net_peerCount, 16))
    else:
        geth_net_peer_count.set(0)

    # Get transcation pool status
    txpool_status = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "txpool_status", [])
    if txpool_status != -1:
        txpool_status_queued = int(txpool_status['queued'], 16)
        geth_txpool_status_queued.set(txpool_status_queued)
        txpool_status_pending = int(txpool_status['pending'], 16)
        geth_txpool_status_queued.set(txpool_status_queued)
        geth_txpool_status_pending.set(txpool_status_pending)
    else:
        geth_txpool_status_queued.set(0)
        geth_txpool_status_pending.set(0)

    # Block transaction count sum
    global SUM_TRANSACTIONS
    if latest_block != -1:
        if last_block_number < int(latest_block, 16):
            for i in range(last_block_number, int(latest_block, 16)):
                block_inf = geth_json_rpc(CONFIG_GETH_HOST, CONFIG_GETH_PORT, "eth_getBlockByNumber", [latest_block, True])
                if block_inf != -1:
                    block_transaction_count = len(block_inf['transactions'])
                    SUM_TRANSACTIONS += block_transaction_count
                    geth_transaction_processed.set(SUM_TRANSACTIONS)


    r = {
        "BlockNum": int(latest_block, 16),
        "TXsSum": SUM_TRANSACTIONS
    }

    return(r)

if __name__ == '__main__':
    LAST_BLOCK_COUNTER = 0

    # Start up the server to expose the metrics
    start_http_server(8000)

    # Refresh Block metrics
    while True:
        r = geth_collect_metrics(LAST_BLOCK_COUNTER)
        if r['BlockNum'] != -1:
            LAST_BLOCK_COUNTER = r['BlockNum']
        time.sleep(1)
