#!/bin/bash 

#GMA_DIR=/path/to/gma/dirctory
GMA_DIR=/sonas-hs/schatz/hpc/data/hlee/gma/gma-0.1.5
PREPRO=$GMA_DIR/bin/prepro.chr.py


cd $GMA_DIR/example/ecoli/input/ppd 
$PREPRO $GMA_DIR/example/ecoli/input/index/NC_000913.fna
#$PREPRO $GMA_DIR/example/ecoli/input/index/NC_000913.fa



