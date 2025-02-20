#!/bin/bash

cd ../example/yeast/output/local/

for tech in illumina; do  #solid iontorrent roche pacbio pacbio-ed

    rm -rf yeast.$tech
    mkdir yeast.$tech
    cd yeast.$tech
    rm *
    date >> ../timestamp.txt
    echo "tech:$tech" >> ../timestamp.txt

    cat ../../../input/ppd/chr9.fa.ppd | /local2/work/hlee/schatzlab-public/gma/bin/mapper tech --$tech -b 70 -x ../../../input/index/NC_000913.fna -p ../../../../../bin 1> map.txt

    echo "sorting..."
    cat map.txt | sort > mapsort.txt

    echo "complete"
    echo "====================================="

    echo "analyzing..."
    cat mapsort.txt | /local2/work/hlee/schatzlab-public/gma/bin/reducer tech --$tech 1> mapred.txt

    echo "====================================="
    echo "reducer is done"
    echo "====================================="

done;


cd ../../../../../script/


