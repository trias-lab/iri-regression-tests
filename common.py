import os
import time
import commands

# send milestone
def send_milestone():
    ret = os.system("java -jar ../../private-iota-testnet/target/iota-testnet-tools-0.1-SNAPSHOT-jar-with-dependencies.jar Coordinator localhost 14700")
    if ret == 0:
        print "Send milestone successfully"
    else:
        print "Send milestone failed"
        exit(-1)

    time.sleep(10)


def start_cli(enable_ipfs=True, enable_batch=False, enable_compression=False):
    # change config
    file="../../scripts/iota_api/conf"
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            if "enableIpfs" in line:
                if enable_ipfs == True:
                    file_data += "enableIpfs = True\n"
                else:
                    file_data += "enableIpfs = False\n"
            elif "enableBatching" in line:
                if enable_batch == True:
                    file_data += "enableBatching = True\n"
                else:
                    file_data += "enableBatching = False\n"
            elif "enableCompression" in line:
                if enable_compression == True:
                    file_data += "enableCompression = True\n"
                else:
                    file_data += "enableCompression = False\n"
            else:
                file_data += line

    with open(file, "w") as f:
        f.write(file_data)


    cur_dir = os.getcwd()
    os.chdir("../../scripts/iota_api")
    os.system("python ./app.py &> /tmp/app.log &")
    os.chdir(cur_dir)

    time.sleep(20)


def stop_cli():
    os.system('ps -aux | grep "[p]ython ./app" | awk \'{print $2}\' | xargs kill -9')


# send transactions one by one
def put_file(txn_num=1):
    for i in range(txn_num):
        ret = os.system('curl -X POST http://127.0.0.1:5000/put_file -H \'Content-Type: application/json\' -H \'cache-control: no-cache\' -d \'{"from": "A","to": "j","amnt": 1}\'')
        if ret == 0:
            print "Send command successfully ", i
        else:
            print "Send command failed ", i
            exit(-1)


# send transactions in batches
def put_cache(txn_num=1):
    for i in range(txn_num):
        ret = os.system('curl -X POST   http://127.0.0.1:5000/put_cache -H \'Content-Type: application/json\' -H \'cache-control: no-cache\' -d \'{"from": "A","to": "j","amnt": 1}\'')
        if ret == 0:
            print "Send command successfully ", i
        else:
            print "Send command failed ", i
            exit(-1)


# get current txn count
def get_transactions_count():
    tx_count = commands.getoutput("grep -a \"totalTransactions =\" ./node1/iri.log  | tail -n 1 | awk '{print $25}'")
    return tx_count


def check_transactions_count(old_tx_count, COUNT):
    for i in range(30):
        new_tx_count = get_transactions_count()
        print "new_tx_count = ", new_tx_count
        if int(new_tx_count) == int(old_tx_count) + COUNT:
            print "IOTA transaction count added successfully"
            return
        else:
            print "waiting for IOTA transaction count..."
            time.sleep(1)

    print "Error! transaction number added failed!"
    exit(-1)