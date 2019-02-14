import sys
from common import send_milestone, get_transactions_count, start_cli, put_cache, put_file, check_transactions_count, stop_cli

TX_NUM = 100
total_tx_num = 0

# 0. parse arguments
if sys.argv[2] == "true":
    enable_ipfs = True
else:
    enable_ipfs = False

if sys.argv[3] == "true":
    enable_batch = True
else:
    enable_batch = False

if sys.argv[4] == "true":
    enable_compression = True
else:
    enable_compression = False

print enable_ipfs, enable_batch, enable_compression

# 1. milestone
print("\nsending milestone...")
send_milestone()

# 2. cli
print("\nstart cli...")
start_cli(enable_ipfs, enable_batch, enable_compression)

# 3. tx count
tx_count = get_transactions_count()
print("current tx count ", tx_count)

# 4. put_cache
if enable_batch:
    print("\nstart put_cache...")
    put_cache(TX_NUM)
    total_tx_num += TX_NUM

# 5. put_file
print("\nstart put_file...")
put_file(TX_NUM)
total_tx_num += TX_NUM

# 6. check tx count
print("\nchecking transaction count...")
check_transactions_count(tx_count, total_tx_num)

# 7. stop cli
print("\nstopping cli...")
stop_cli()
