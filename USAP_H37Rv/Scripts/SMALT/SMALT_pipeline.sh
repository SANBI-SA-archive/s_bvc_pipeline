echo "1_SMALTAlign.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 1_SMALTAlign.sh
echo "1_SMALTAlign.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "2_sortSmaltSam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 2_sortSmaltSam.sh
echo "2_sortSmaltSam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "1_SMALTAlign_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 1_SMALTAlign_cleanup.sh
echo "1_SMALTAlign_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "3_addReadGroupsToSortedSam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 3_addReadGroupsToSortedSam.sh
echo "3_addReadGroupsToSortedSam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "2_sortSmaltSam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 2_sortSmaltSam_cleanup.sh
echo "2_sortSmaltSam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "4_picardValidate.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 4_picardValidate.sh
echo "4_picardValidate.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "5_createSamToBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 5_createSamToBam.sh
echo "5_createSamToBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "6_indexBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 6_indexBam.sh
echo "6_indexBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "3_addReadGroupsToSortedSam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 3_addReadGroupsToSortedSam_cleanup.sh
echo "3_addReadGroupsToSortedSam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "7_1_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 7_1_GATK.sh
echo "7_1_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 7_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 7_2_GATK.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 7_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "7_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 7_2_GATK.sh
echo "7_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "8_1_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 8_1_Realignment.sh
echo "8_1_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 8_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 8_2_Realignment.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/SMALT/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/SMALT/ 8_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "8_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 8_2_Realignment.sh
echo "8_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "5_createSamToBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 5_createSamToBam_cleanup.sh
echo "5_createSamToBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "6_indexBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 6_indexBam_cleanup.sh
echo "6_indexBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "9.1_baseQualRecalSMALT.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 9.1_baseQualRecalSMALT.sh
echo "9.1_baseQualRecalSMALT.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "9.2_baseQualRecalSMALT.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 9.2_baseQualRecalSMALT.sh
echo "9.2_baseQualRecalSMALT.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "7_x_GATK_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 7_x_GATK_cleanup.sh
echo "7_x_GATK_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "10_picardSort.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 10_picardSort.sh
echo "10_picardSort.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "8_x_Realignment_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 8_x_Realignment_cleanup.sh
echo "8_x_Realignment_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "9.1_baseQualRecalSMALT_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 9.1_baseQualRecalSMALT_cleanup.sh
echo "9.1_baseQualRecalSMALT_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "9.2_baseQualRecalSMALT_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 9.2_baseQualRecalSMALT_cleanup.sh
echo "9.2_baseQualRecalSMALT_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "11_reIndexBamFiles.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 11_reIndexBamFiles.sh
echo "11_reIndexBamFiles.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "12_removePCRDuplicates.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 12_removePCRDuplicates.sh
echo "12_removePCRDuplicates.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "13_reIndexBamFiles2.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 13_reIndexBamFiles2.sh
echo "13_reIndexBamFiles2.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "10_picardSort_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 10_picardSort_cleanup.sh
echo "10_picardSort_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "14_getMappedReads.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 14_getMappedReads.sh
echo "14_getMappedReads.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "12_removePCRDuplicates_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 12_removePCRDuplicates_cleanup.sh
echo "12_removePCRDuplicates_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "11_reIndexBamFiles_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 11_reIndexBamFiles_cleanup.sh
echo "11_reIndexBamFiles_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "15_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 15_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh
echo "15_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "16_2_GenomeCoverage.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 16_2_GenomeCoverage.sh
echo "16_2_GenomeCoverage.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "17_ZeroCov.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 17_ZeroCov.sh
echo "17_ZeroCov.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
echo "15_2_VARIANT_CALLING_SAMTOOLS.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
sh 15_2_VARIANT_CALLING_SAMTOOLS.sh
echo "15_2_VARIANT_CALLING_SAMTOOLS.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_SMALT.txt
