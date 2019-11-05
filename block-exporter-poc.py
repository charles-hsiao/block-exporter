import json
import time
import random

BLOCK_NUMBER = 0
SUM_TRANSACTIONS = 0

def get_latest_block():
    global BLOCK_NUMBER
    BLOCK_NUMBER += random.randint(0,3)
    return(BLOCK_NUMBER)

def poc():
    return(20)

def geth_collect_metrics(last_block_number):

    global SUM_TRANSACTIONS

    block_number = get_latest_block() 
    if last_block_number < block_number:
        for i in range(last_block_number, block_number):
            block_transaction_count = poc()
            SUM_TRANSACTIONS += block_transaction_count

    r = {
        "BlockNum": block_number,
        "TXsSum": SUM_TRANSACTIONS
    }
    return(r)

if __name__ == '__main__':
    LAST_BLOCK_COUNTER = 0

    # Refresh Block metrics
    while True:
        r = geth_collect_metrics(LAST_BLOCK_COUNTER)
        LAST_BLOCK_COUNTER = r['BlockNum']
        print(r)
        time.sleep(1)
