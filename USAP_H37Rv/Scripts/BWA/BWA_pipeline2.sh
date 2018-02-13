date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "11_removePCRDuplicates.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 11_removePCRDuplicates.sh
echo "11_removePCRDuplicates.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "12_reIndexBamFiles2.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 12_reIndexBamFiles2.sh
echo "12_reIndexBamFiles2.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "9_picardSort_cleanup.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 9_picardSort_cleanup.sh
echo "9_picardSort_cleanup.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "13_getMappedReads.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 13_getMappedReads.sh
echo "13_getMappedReads.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "10_reIndexBamFiles_cleanup.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 10_reIndexBamFiles_cleanup.sh
echo "10_reIndexBamFiles_cleanup.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh
echo "14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "15_2_GenomeCoverage.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 15_2_GenomeCoverage.sh
echo "15_2_GenomeCoverage.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "16_ZeroCov.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 16_ZeroCov.sh
echo "16_ZeroCov.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
echo "14_2_VARIANT_CALLING_SAMTOOLS.sh started: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
sh 14_2_VARIANT_CALLING_SAMTOOLS.sh
echo "14_2_VARIANT_CALLING_SAMTOOLS.sh ended: " >> /home/pagit/USAP/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/pagit/USAP/timeLog_BWA.txt
