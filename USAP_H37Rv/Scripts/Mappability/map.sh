#!/bin/bash
cd /home/pagit/USAP/Reference/TEST/Mappability/
python /home/pagit/USAP/Tools/gma-0.1.5/bin/prepro.chr.py /home/pagit/USAP/Reference/TEST/Mappability/SCCmecIII_AB037671.fasta
cd /home/pagit/USAP/Reference/TEST/Mappability/
    for l in 100; do
      for o in 0; do
        for s in 0.02; do
          for i in 0; do
            for d in 0; do
              mkdir sccmeciii_ab037671.l$l.o$o.qA.s$s.i$i.d$d;
          cd sccmeciii_ab037671.l$l.o$o.qA.s$s.i$i.d$d;

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
              cat /home/pagit/USAP/Reference/TEST/Mappability/SCCmecIII_AB037671.fasta.ppd | /home/pagit/USAP/Tools/gma-0.1.5/bin/mapper runall -l $l -q A -s $s -i $i -d $d -o $o -t 20 -f ref.fa -b 70 -x /home/pagit/USAP/Reference/TEST/Mappability/SCCmecIII_AB037671.fasta -p /home/pagit/USAP/Tools/gma-0.1.5/bin 1> map.txt

              echo "sorting..."
              cat map.txt | sort > mapsort.txt

              echo "complete"
              echo "====================================="

              echo "analyzing..."
              cat mapsort.txt | /home/pagit/USAP/Tools/gma-0.1.5/bin/reducer analyzer -l $l -t 20 -o $o 1> mapred.txt 2> log


              echo "====================================="
              echo "reducer is done"
              echo "====================================="

            done; 
          done;
        done;
      done;
    done;
    