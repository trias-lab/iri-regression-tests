#!/bin/bash
#$1 - IRI version
#$2 - port
#$3 - is testnet?
#$4 - unpack DB?
#$5 - number of nodes to load
#$6 - python script
#$7 - enbale ipfs?
#$8 - enable batch transactions?
#$9 - enable transactions compression?


echo "starting node"
port=$2
cd iri/
for (( i=1; i<=$5; i++))
do
    node='node'$i
    dbFolder='DB_'$1
    echo $node
    rm -rf $node
    cp -rf target $node

    cd $node
    #TODO host mainnet/testnet DB somewhere
    if $4;
    then
        if $3;
        then
        echo "copy testnet db"
        cp -rf ../../testnet_files/testnetdb testnetdb
        cp -f ../../testnet_files/snapshot.txt snapshot.txt
        else #NO really working
        echo "copy mainnet db"
        cp -f ../testnet_files/testnetdb $node/testnetdb
        fi
    fi

    #TODO read version from config
    cmdOpt=''
    if $3
    then
    echo "start node.. testnet on port: "$port
    cmdOpt='--testnet'
        if $4
        then
        cmdOpt=$(cat ../../testnet_files/cli_opts)
        fi
    else
    echo "start node.. mainnet on port: "$port
    fi

    if [ -n "$8" ];
    then
        cmdOpt=${cmdOpt}" --testnet-no-coo-validation --snapshot=./Snapshot.txt --mwm 1 --walk-validator \"NULL\" --ledger-validator \"NULL\" --max-peers 40 --remote"
        if $8
        then
            cmdOpt=${cmdOpt}" --batch-txns"
        fi
    fi

    if [ -n "$9" ];
    then
        if $9
        then
            cmdOpt=${cmdOpt}" --compression-txns"
        fi
    fi

    echo "cmdOpt ="$cmdOpt
    java -jar iri-$1.jar -p $port -u $port -t `expr $port + $5` -n 'udp://localhost:'`expr $port - 1`' udp://localhost:'`expr $port + 1` $cmdOpt &> iri.log &
    echo $! > iri.pid
    cd ..
    ((port++))
done

#give time to the node to init
#TODO instead of sleep sample API until it is up
sleep 40
if [ -n "$6" ];
then
    echo "start python script.."
    python $6 $2 $7 $8 $9
    rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
fi

#stop node
echo "stop node.."
for (( i=1; i<=$5; i++))
do
    node='node'$i
    kill `cat $node/iri.pid`
    wait `cat $node/iri.pid`
done

#Check log for errors
for (( i=1; i<=$5; i++))
do
    node='node'$i
    grep -i "error" $node/iri.log | tee $node/iri.errors
    if [ -s $node/iri.errors ];
    then
        exit -1
    fi

done

