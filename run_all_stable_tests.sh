#!/usr/bin/env bash

#exit if error
set -e

#default version
if [ -z "$1" ];
then VER="1.4.2.4";
else VER=$1;
fi

echo "running tests"
bash 1_start_and_stop_a_node_without_database-mainnet.sh $VER

bash 1_start_and_stop_a_node_without_database-testnet.sh $VER

bash 2_start_and_stop_a_node_known_database-testnet.sh $VER

bash 3_create_a_transaction_on_Node_A_and_find_it_in_Node_B.sh $VER

bash 4_send_transactions_with_ipfs_without_batch_without_compression-testnet.sh $VER

bash 5_send_transactions_with_ipfs_with_batch_without_compression-testnet.sh $VER

bash 6_send_transactions_without_ipfs_without_bach_without_compression-testnet.sh $VER

bash 7_send_transactions_without_ipfs_with_bach_without_compression-testnet.sh $VER

bash 8_send_transactions_without_ipfs_with_bach_with_compression-testnet.sh $VER

echo "finished running tests successfully"
