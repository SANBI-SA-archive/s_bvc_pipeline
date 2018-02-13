echo "1_BWAAlign.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 1_BWAAlign.sh
echo "1_BWAAlign.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "2_combineReads.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 2_combineReads.sh
echo "2_combineReads.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "3_picardValidate.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 3_picardValidate.sh
echo "3_picardValidate.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "4_createSamToBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 4_createSamToBam.sh
echo "4_createSamToBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "1_BWAAlign_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 1_BWAAlign_cleanup.sh
echo "1_BWAAlign_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "2_combineReads_Cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 2_combineReads_Cleanup.sh
echo "2_combineReads_Cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "5_indexBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 5_indexBam.sh
echo "5_indexBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "6_1_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 6_1_GATK.sh
echo "6_1_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 6_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 6_2_GATK.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 6_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "6_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 6_2_GATK.sh
echo "6_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "7_1_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 7_1_Realignment.sh
echo "7_1_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 7_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 7_2_Realignment.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/BWA/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/BWA/ 7_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "7_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 7_2_Realignment.sh
echo "7_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "4_createSamToBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 4_createSamToBam_cleanup.sh
echo "4_createSamToBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "5_indexBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 5_indexBam_cleanup.sh
echo "5_indexBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "8.1_baseQualRecalBWA.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 8.1_baseQualRecalBWA.sh
echo "8.1_baseQualRecalBWA.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "8.2_baseQualRecalBWA.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 8.2_baseQualRecalBWA.sh
echo "8.2_baseQualRecalBWA.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "6_1_GATK_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 6_1_GATK_cleanup.sh
echo "6_1_GATK_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "6_2_GATK_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 6_2_GATK_cleanup.sh
echo "6_2_GATK_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "9_picardSort.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 9_picardSort.sh
echo "9_picardSort.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "7_1_Realignment_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 7_1_Realignment_cleanup.sh
echo "7_1_Realignment_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "7_2_Realignment_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 7_2_Realignment_cleanup.sh
echo "7_2_Realignment_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "10_reIndexBamFiles.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 10_reIndexBamFiles.sh
echo "10_reIndexBamFiles.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "8.1_baseQualRecalBWA_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 8.1_baseQualRecalBWA_cleanup.sh
echo "8.1_baseQualRecalBWA_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "8.2_baseQualRecalBWA_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 8.2_baseQualRecalBWA_cleanup.sh
echo "8.2_baseQualRecalBWA_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "11_removePCRDuplicates.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 11_removePCRDuplicates.sh
echo "11_removePCRDuplicates.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "12_reIndexBamFiles2.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 12_reIndexBamFiles2.sh
echo "12_reIndexBamFiles2.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "9_picardSort_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 9_picardSort_cleanup.sh
echo "9_picardSort_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "13_getMappedReads.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 13_getMappedReads.sh
echo "13_getMappedReads.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "10_reIndexBamFiles_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 10_reIndexBamFiles_cleanup.sh
echo "10_reIndexBamFiles_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh
echo "14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "15_2_GenomeCoverage.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 15_2_GenomeCoverage.sh
echo "15_2_GenomeCoverage.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "16_ZeroCov.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 16_ZeroCov.sh
echo "16_ZeroCov.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
echo "14_2_VARIANT_CALLING_SAMTOOLS.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
sh 14_2_VARIANT_CALLING_SAMTOOLS.sh
echo "14_2_VARIANT_CALLING_SAMTOOLS.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_BWA.txt
