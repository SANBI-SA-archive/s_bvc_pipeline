import sys
import os

def fixMisEncodedQuals(BWAAligned_aln,sciptsDir,scriptName):
    os.chdir 
    completed = []
    NEW_GATK_data = []
    for intervals_or_realignment_File in os.listdir(BWAAligned_aln):
        if ".intervals" in intervals_or_realignment_File and scriptName == "6_2_GATK.sh":
            completed.append(intervals_or_realignment_File.split("_")[0])
        elif ".intervals" in intervals_or_realignment_File and scriptName == "7_2_Realignment.sh":
            completed.append(intervals_or_realignment_File.split("_")[0])
            f_temp = open(sciptsDir+scriptName,'r')
            for GATK_command in f_temp:
                GATK_name = GATK_command.split("Alignment_Files/")[1]
                GATK_name = GATK_name.split("_")[0]
                if GATK_name not in completed:
                    print GATK_name
                    print completed
                    print GATK_name in completed
                    raw_input("This file needs base quality recalibration!")
                    NEW_GATK_data.append(GATK_command)
            f_temp.close()
            f_temp = open(sciptsDir+scriptName,'w')
            for x in NEW_GATK_data:
                f_temp.write(x)
                raw_input("now ADD fixmisencoded quals here using 2nd subprocess step")
            f_temp.close()
    
  
BWAAligned_aln = sys.argv[1]
sciptsDir = sys.argv[2]
scriptName = sys.argv[3]
 
fixMisEncodedQuals(BWAAligned_aln,sciptsDir,scriptName)

