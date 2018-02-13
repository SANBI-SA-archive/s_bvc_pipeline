echo "1_2_NOVOAlign_multi.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 1_2_NOVOAlign_multi.sh
echo "1_2_NOVOAlign_multi.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "2_picardValidate.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 2_picardValidate.sh
echo "2_picardValidate.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "3_createSamToBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 3_createSamToBam.sh
echo "3_createSamToBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "1_1_NOVOAlign_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 1_1_NOVOAlign_cleanup.sh
echo "1_1_NOVOAlign_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "4_indexBam.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 4_indexBam.sh
echo "4_indexBam.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "5_1_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 5_1_GATK.sh
echo "5_1_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 5_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 5_2_GATK.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 5_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "5_2_GATK.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 5_2_GATK.sh
echo "5_2_GATK.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "6_1_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 6_1_Realignment.sh
echo "6_1_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 6_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 6_2_Realignment.sh
echo "python /home/adippenaar/USAP_H37Rv/BIN/fixMisEncodedQuals.py /home/adippenaar/run_seqs_06_02_2018_out/Results/NOVO/Alignment_Files/ /home/adippenaar/USAP_H37Rv/Scripts/NOVO/ 6_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "6_2_Realignment.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 6_2_Realignment.sh
echo "6_2_Realignment.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "3_createSamToBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 3_createSamToBam_cleanup.sh
echo "3_createSamToBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "4_indexBam_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 4_indexBam_cleanup.sh
echo "4_indexBam_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "7.1_baseQualRecalNOVO.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 7.1_baseQualRecalNOVO.sh
echo "7.1_baseQualRecalNOVO.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "7.2_baseQualRecalNOVO.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 7.2_baseQualRecalNOVO.sh
echo "7.2_baseQualRecalNOVO.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "5_1_GATK_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 5_1_GATK_cleanup.sh
echo "5_1_GATK_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "8_picardSort.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 8_picardSort.sh
echo "8_picardSort.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "6_x_Realignment_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 6_x_Realignment_cleanup.sh
echo "6_x_Realignment_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "7.1_baseQualRecalNOVO_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 7.1_baseQualRecalNOVO_cleanup.sh
echo "7.1_baseQualRecalNOVO_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "7.2_baseQualRecalNOVO_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 7.2_baseQualRecalNOVO_cleanup.sh
echo "7.2_baseQualRecalNOVO_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "9_reIndexBamFiles.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 9_reIndexBamFiles.sh
echo "9_reIndexBamFiles.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "10_removePCRDuplicates.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 10_removePCRDuplicates.sh
echo "10_removePCRDuplicates.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "11_reIndexBamFiles2.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 11_reIndexBamFiles2.sh
echo "11_reIndexBamFiles2.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "8_picardSort_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 8_picardSort_cleanup.sh
echo "8_picardSort_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "12_getMappedReads.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 12_getMappedReads.sh
echo "12_getMappedReads.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "9_reIndexBamFiles_cleanup.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 9_reIndexBamFiles_cleanup.sh
echo "9_reIndexBamFiles_cleanup.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "13_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 13_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh
echo "13_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "14_2_GenomeCoverage.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 14_2_GenomeCoverage.sh
echo "14_2_GenomeCoverage.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "15_ZeroCov.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 15_ZeroCov.sh
echo "15_ZeroCov.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
echo "13_2_VARIANT_CALLING_SAMTOOLS.sh started: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
sh 13_2_VARIANT_CALLING_SAMTOOLS.sh
echo "13_2_VARIANT_CALLING_SAMTOOLS.sh ended: " >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
date +%Y-%m-%d%t%T >> /home/adippenaar/USAP_H37Rv/timeLog_NOVO.txt
