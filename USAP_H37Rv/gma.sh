#!/bin/bash
GMA_DIR=/home/pagit/USAP/Tools/gma-0.1.5
PREPRO=$GMA_DIR/bin/prepro.chr.py
cd $GMA_DIR/example/ecoli/input/ppd 
$PREPRO $GMA_DIR/example/ecoli/input/index/NC_000913.fna

MAPPER=$GMA_DIR/bin/mapper 
REDUCER=$GMA_DIR/bin/reducer
PPD=$GMA_DIR/example/ecoli/input/ppd/NC_000913.fna.ppd


cd $GMA_DIR/example/ecoli/output/local

for l in 100; do
  for o in 0; do
    for s in 0.02; do
      for i in 0; do
        for d in 0; do

          #rm -rf ecoli.l$l.o$o.qA.s$s.i$i.d$d;
          mkdir ecoli.l$l.o$o.qA.s$s.i$i.d$d;
          cd ecoli.l$l.o$o.qA.s$s.i$i.d$d;
          #rm *
          date >> ../timestamp.txt
          echo "l:$l" >> ../timestamp.txt
          echo "q:$q" >> ../timestamp.txt
          echo "s:$s" >> ../timestamp.txt
          echo "i:$i" >> ../timestamp.txt
          echo "d:$d" >> ../timestamp.txt
          echo "o:$o" >> ../timestamp.txt
          echo "t:$t" >> ../timestamp.txt
          echo "f:$f" >> ../timestamp.txt
          echo "b:$b" >> ../timestamp.txt
          echo "x:$x" >> ../timestamp.txt
          echo "m:$m" >> ../timestamp.txt
          echo "p:$p" >> ../timestamp.txt
          echo "--" >> ../timestamp.txt

          cat $PPD | $MAPPER runall -l $l -q A -s $s -i $i -d $d -o $o -t 20 -f ref.fa -b 70 -x $GMA_DIR/example/ecoli/input/index/NC_000913.fna -p $GMA_DIR/bin 1> map.txt

          echo "sorting..."
          cat map.txt | sort > mapsort.txt

          echo "complete"
          echo "====================================="

          echo "analyzing..."
          #cat mapsort.txt | $REDUCER analyzer -l $l -t 20 -o $o 1> mapred.txt
          cat mapsort.txt | $REDUCER analyzer -l $l -t 20 -o $o 1> mapred.txt 2> log
          #cat mapsort.txt | $REDUCER analyzer -l $l -t 20 -o $o &> log
          


          echo "====================================="
          echo "reducer is done"
          echo "====================================="

        done; 
      done;
    done;
  done;
done;



