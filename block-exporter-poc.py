import json
import time
import random

def poc():
    return(20)

def geth_collect_metrics(block_counter, last_block_counter, sum_transaction):
    if last_block_counter < block_counter:
        for i in range(last_block_counter, block_counter):
            block_transaction_count = poc()
            sum_transaction += block_transaction_count

    r = {
        "BlockNum": block_counter,
        "TXsSum": sum_transaction
    }
    return(r)

if __name__ == '__main__':
    LAST_BLOCK_COUNTER = 0
    BLOCK_COUNTER = 0
    SUM_TRANSACTIONS = 0
    #Refresh Block metrics
    while True:
        BLOCK_COUNTER += random.randint(0,3) 
        r = geth_collect_metrics(BLOCK_COUNTER, LAST_BLOCK_COUNTER, SUM_TRANSACTIONS)
        SUM_TRANSACTIONS = r['TXsSum']
        LAST_BLOCK_COUNTER = BLOCK_COUNTER
        print(r)
        time.sleep(1)
