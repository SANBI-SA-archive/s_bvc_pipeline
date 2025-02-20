#dont force GATK or NovoAlign to be initialized, warn user that these need to be manually installed.
#skip these if user does not want to use them.
#allow user to provide location of these and dont ask again if functional - store in userSettings.txt

#Warning if GATK error on negative strand - this is due to corrupt reference fasta file - re-copy and re-index
'''
To add:
    Run only samtools 
    Run only GATK
    Run both 
Extra tools
Filter
Phylogeny
'''
'''
Copyright 2016 Ruben van der Merwe
This program is distributed under the terms of the GNA General Public Licence (GPL).
    
This file is part of USAP.

USAP is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

USAP is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with USAP. If not, see <hgttp://www.gnu.org/licenses/>.
'''    
import sys
import os
import subprocess
from subprocess import Popen, PIPE
import time
from time import strftime

try:
    import readline
except:
    print "import error, no library called realine"
try:
    import glob
except:
    print "import error, no library called glob"

try:
    import re
except:
    print "import error, no library called re"

###############################################################################################################################################
def complete(text,state):
    return (glob.glob(text+"*")+[None])[state]

def interface():
    disclaimer = '''
    USAP V1.0
    Copyright 2016 Ruben van der Merwe
    This program is distributed under the terms of the GNA General Public Licence (GPL).
    
    This file is part of USAP.

    USAP is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    USAP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with USAP. If not, see <http://www.gnu.org/licenses/>.'''
    #####################################################################################################
    print disclaimer
    print
    print "_____________________________________________________________________________________________"
    print "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
    print "USAP - Universal sequence analysis pipeline for whole genome sequence data                   "
    print "V1.0, Created by Ruben G. van der Merwe, 1 August 2016, email: rubengvdm@hotmail.com         "
    print "Copyright Ruben van der Merwe 2016                                                           "
    print "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
    print "_____________________________________________________________________________________________"
    print ""
    #####################################################################################################
    #For Debugging:
    #####################################################################################################
    if "-d" in sys.argv:
        debugMode = True
    else:
        debugMode = False
    skipSetup = False 
    controlPoint = 1
    if debugMode:
        controlPoint = int(raw_input("controlpoints are 1 = index, 2 = fastqc, 3 = trimming, 4 = 2nd Fastqc, 5 = alignment , 6 = calculate genomecoverage from bed files, 7 = compres 0-cov files from zerocov.sh, 8 = annotation, 9 = filter, 10 = pheno predict, 11 = lineage determination, 12 = summary table."))
        ans = "1" 
    else:
        controlPoint = 1
        while True:
            ans = raw_input("Enter 1 to run the NGS pipeline, 2 to enter tool menu or Q to exit : ")
            if ans == "1" or ans == "2" or ans.lower() =="q":
                break
            else:
                print "Please select input: 1,2 or Q."
        if ans.upper() == "Q":
            exit(0)
        if ans == '2':
            return "2", 0, 0, 0, 0, 
    ####################################################################### 

##        mappers = "Load_From_UserSettingsFile"
##        variantTools = "Load_From_UserSettingsFile"            
        #Now the mappers and variant tools will be loaded from previous run from usersettings file. 
        #return "1", skipSetup, controlPoint, mappers, variantTools, spaceSavingMode, debugMode, auto

##        flagX = False
##        while flagX == False:
##            ans = raw_input("Would you like run this program in space saving mode (will remove certain redundant files) ? <Y/N>")
##            if ans.upper() not in ["Y","N"]:
##                continue
##            if ans.upper() == "Y":
##                spaceSavingMode = True
##                break
##            elif ans.upper() == "N":
##                spaceSavingMode = False
##                break
##        return "1", skipSetup, controlPoint, spaceSavingMode, debugMode, auto
    
    
    spaceSavingMode = True           
    #return "1", skipSetup, controlPoint, mappers, variantTools, spaceSavingMode, debugMode, auto
    return  ans, skipSetup, controlPoint, spaceSavingMode, debugMode
###############################################################################################################################################
############################################################################################################################################################
def phyloAll(dirX, genCovDir, output, useCovData):
    '''
    snp based phylogeny:
    use whole genome SNPS, use WT not mutated, but use special char for deletion if there is no coverage
    If the read is present and WT- assign WT
    If the read is absent - assign deletion "-"
    The coverage MUST be above thereshold value
    This tool takes as input the VCF file and the zero-coverage file from USAP
    '''
    def isThisBPDeleted(dirX,vcf_name,snpPos):
        '''Assumtion: sorted lists'''
        if "_" in vcf_name:
            temp_vcf_name = vcf_name.split("_")[0]
        else:
            temp_vcf_name=vcf_name.split(".")[0]+"_genomecov=0_collapsed.txt"
        
        for covFile in os.listdir(dirX):
            if covFile.split("_")[0] == temp_vcf_name and "0_collapsed.txt" in covFile:
                break
        fileX = covFile
        os.chdir(dirX)
        f = open(fileX,'r')
        iterations = 0
        for line in f:
            iterations += 1
            del_range = line.split()
            #print "the snp pos is", snpPos
            #print "the deletion range is now"
            #print del_range
            #raw_input("press enter")
            if len(del_range) == 1:
                if snpPos == int(del_range[0]):
                    #print "iterations:",iterations
                    return True
                if snpPos < int(del_range[0]):
                    #print "iterations:",iterations
                    return False
            elif len(del_range) == 2:
                if snpPos >= int(del_range[0]) and snpPos <= int(del_range[1]):
                    #print "iterations:",iterations
                    return True
                if snpPos < int(del_range[1]):
                    #print "iterations:",iterations
                    #print "returning false"
                    return False
        #print "returning false"
        return False
        f.close()
        
    def loadAllRefereceSNPS (main):
        '''
        this creates a dictionary of all the bp position snp info...
        '''
        genome = {} # {100:"A",200:"G"}
        totalLoaded = 0
        totalSNPS = 0
        #fileArray = []
        os.chdir(main)
        #print main        
        for fileX in os.listdir(main):
            if fileX.endswith(".vcf"):
                totalLoaded +=1
                print "reading file: ",fileX
                inFile = open(fileX, 'r')
                header = inFile.readline().split("\t")
                pos = -1
                novoPos = []
                bwaPos = []
                smaltPos = []
                positionList = []
                for element in header:
                    pos += 1
                    if "mut_BWA" in element:
                        bwaPos.append(pos)
                    elif "mut_NOVO" in element:
                        novoPos.append(pos)
                    elif "mut_SMALT" in element:
                        smaltPos.append(pos)
                for x in [novoPos,bwaPos,smaltPos]:
                    if x <> []:
                        for y in x:
                            positionList.append(y)
                #print positionList
                #raw_input()
                            
                countPositions = []
                
                for x in inFile:           
                    line = x.split("\t")
                    pos = line[0]
                    countPositions.append(pos)
                    #take best from novo bwa smalt
                    #only use snps!
                    
                    if pos not in genome:
                        for tempPos in positionList:
                            tempRef = line[tempPos-1]
                            tempMut = line[tempPos]
                            if tempRef.lower() in ["a","t","g","c","u"] and tempMut.lower() in ["a","t","g","c","u"]: #both are snps, not indels
                                genome[pos] = tempRef
                                break                            
                inFile.close()
                totalSNPS += len(countPositions)
        #print len(countPositions), len(countPositions2)
        print "A total of ",totalLoaded,"files were loaded which contains a total of",totalSNPS,"SNPS."
        return genome
    
    def convertDictToSortedList (dictX): 
        listX = []
        for x in dictX:
            listX.append([x,dictX[x]])
        #listX.sort() #sorts by first element
        listX = sorted(listX, key = lambda i : int(i[0]))
        #for x in listX:
        #    print x
        #    raw_input()
        return listX
    
    def loadVariantsFromAnnotatedVCF(fileX,dirX):
        #returns all the variants for one file only
        genome = {}
        totalLoaded = 0
        os.chdir(dirX)
        if fileX.endswith(".vcf"):
            totalLoaded +=1
    ##        print "getting variants from: ",fileX
            inFile = open(fileX, 'r')
            header = inFile.readline().split("\t")
            pos = -1
            novoPos = []
            bwaPos = []
            smaltPos = []
            positionList = []
            for element in header:
                pos += 1
                if "mut_BWA" in element:
                    bwaPos.append(pos) #there can be two positions now...gatk and samtools 
                elif "mut_NOVO" in element:
                    novoPos.append(pos)
                elif "mut_SMALT" in element:
                    smaltPos.append(pos)
            for x in [novoPos,bwaPos,smaltPos]:
                if x <> []:
                    for y in x:
                        positionList.append(y) #novo novo bwa bwa smalt smalt
            #print positionList
            #raw_input()
            for x in inFile:
                line = x.split("\t")
                pos = line[0]
                #take best from novo bwa smalt
                #only use snps!
                if pos not in genome:
                    flag = False
                    for tempPos in positionList:
                        tempRef = line[tempPos-1]
                        tempMut = line[tempPos]
##                        print pos, tempRef, tempMut
##                        raw_input("Does this match the vcf??") 
                        if tempRef.lower() in ["a","t","g","c","u"] and tempMut.lower() in ["a","t","g","c","u"]: #both are snps, not indels
                            flag = True
                            break
                        if flag:
                            break
                    if not flag:
                        continue                
                    genome[pos] = tempMut  #[tempRef,tempMut]
            inFile.close()
        print "A total of",len(genome), "SNVs were loaded from file", fileX 
        return genome
    
    
    def overlayRefAndCurrentFileSNPs_with_genome_cov_lookup(vcf_name,dirX,refGenomeDict,currGenomeDict,genCovDir, useCovData): #takes 1 SORTED list one and dict
        # output the overlayed
        print "generating SNV string for file", vcf_name
        '''
        open the corresponding 0-cov file - load it into memmory.
        then for each snp in the ref genome, if its not present in the curr genome
            then check if it has coverage in the 0-cov file
                if it has cov - write the WT pos
                if not - write a "-" corresponding to a deletion.
        '''
        resultList = []
        deletionList = [] #store the positions of deletions
        for snp in refGenomeDict: # this is not sorted - its a dictionary
            if snp[0] in currGenomeDict: #Then it has coverage and it is in the ref AND this sample
                if str(currGenomeDict[snp[0]]) in ["a","t","g","c","A","T","G","C"]:
                    resultList.append([snp[0],currGenomeDict[snp[0]]])
                else:
                    print "error 1 reading file", currGenomeDict[snp[0]]
                    raw_input()
                    
            else:
                if str(snp[1][0][0]) not in ["a","t","g","c","A","T","G","C"]:
                    print "error 2 reading file", snp[1][0][0]
                    print snp[1]
                    print snp[1][0]
                    print snp[1][0][0]
                    raw_input()
                if not useCovData: #then assume read is present, use the reference NT
                    resultList.append([snp[0],snp[1]])                
                elif isThisBPDeleted(genCovDir,vcf_name,int(snp[0])):
                    #print snp
                    #print "IT DOES NOT HAVE COVERAGE"
                    #raw_input()
                    resultList.append([snp[0],"-"])
                    deletionList.append([snp[0],vcf_name])
                else:
                    resultList.append([snp[0],snp[1]])
        resultList = sorted(resultList, key = lambda i : int(i[0]))
        
        #test if it is sorted
        previousPos = -1
    
    
        f= open("SNPs_with_no_mapping.txt",'a')
        for x in deletionList:
            for y in x:
                f.write(str(y)+"\t")
            f.write("\n")
        f.close()
                                
        for x in resultList:
    ##        print "this has to be sorted", x
    ##        raw_input()
            if int(x[0]) < int(previousPos):
                print "the result list is not sorted"
                print "the previous pos was",previousPos,"the new pos",x[0]
                raw_input()
            if len(x[1]) > 1:
                print "multiple base pair found, this should not happen2"
                print x[1]
                raw_input()
            previousPos = x[0]
    
        finalSeq = ''
        for x in resultList:
            finalSeq += x[1]    
        return finalSeq
    ##############################################################################################
    def overlayRefAndCurrentFileSNPs(refGenomeDict,currGenomeDict): #takes 1 SORTED list one and dict
        # output the overlayed
        resultList = []
        for snp in refGenomeDict: # this is not sorted - its a dictionary
            if snp[0] in currGenomeDict:
                if str(currGenomeDict[snp[0]]) in ["a","t","g","c","A","T","G","C"]:
                    resultList.append([snp[0],currGenomeDict[snp[0]]])
                else:
                    print "error 1 reading file", currGenomeDict[snp[0]]
                    raw_input()
                    
            else:
                if str(snp[1][0][0])  in ["a","t","g","c","A","T","G","C"]:
                    resultList.append([snp[0],snp[1]])
                else:
                    print "error 2 reading file", snp[1][0][0]
                    print snp[1]
                    print snp[1][0]
                    print snp[1][0][0]
                    raw_input()
                    
        resultList = sorted(resultList, key = lambda i : int(i[0]))
        
        #test if it is sorted
        previousPos = -1
        
        for x in resultList:
    ##        print "this has to be sorted", x
    ##        raw_input()
            if int(x[0]) < int(previousPos):
                print "the result list is not sorted"
                print "the previous pos was",previousPos,"the new pos",x[0]
                raw_input()
            if len(x[1]) > 1:
                print "multiple base pair found, this should not happen1"
                print x[1]
                raw_input()
            previousPos = x[0]
    
        finalSeq = ''
        for x in resultList:
            finalSeq += x[1]    
        return finalSeq   
        ######################################################################################################  
    
    totalLoaded = 0
    os.chdir(output)
    f= open("SNPs_with_no_mapping.txt",'w')
    f.close()

    #First make a list of all snps storing snp pos and reference bp
 
    allRefSNPs = loadAllRefereceSNPS(dirX) #all snps - for use as a reference SNP data  - dictionary of all snps which exist -
    print "Processing ",len(allRefSNPs),"variants"
    refGenomeList = convertDictToSortedList(allRefSNPs) #convert dict to sorted LIST
    #print type(refGenomeList)
    #print len(refGenomeList)
    #print "total snps according to len of refgenomelist = ",len(refGenomeList)
    #print "ok"

    os.chdir(output) 
    snpFile = open('allSNPForPhylo.fasta', 'w')  #This clears the file
    snpFile.close()                              #This clears the file
    fileCount = 0
    for fileX in os.listdir(dirX):
        if fileX.endswith(".vcf"):
            fileCount += 1
    
    for fileX in os.listdir(dirX):

        if not fileX.endswith(".vcf"):
            print "skipping file:",fileX
            continue
        print "Reading file: ",fileX
        totalLoaded += 1
        print "progress:",str(totalLoaded)," / ",str(fileCount),"--> ",str(int(round((float(totalLoaded)/fileCount),2)*100)),"% complete..."
        currGenome = loadVariantsFromAnnotatedVCF(fileX,dirX) # a dictionary
        resultSeq = overlayRefAndCurrentFileSNPs_with_genome_cov_lookup(fileX,dirX,refGenomeList,currGenome, genCovDir, useCovData)    
        
        print "testing overlayed list"
        print len(currGenome), "SNVs vary in this file"
        print len(resultSeq), "total string length"
        #raw_input("press enter")
        
        os.chdir(output) 
        snpFile = open('allSNPForPhylo.fasta', 'a+')
        snpFile.write(">"+str(fileX)+"\n")
        snpFile.write(resultSeq+"\n")
    print totalLoaded,"files processed"
    print "Whole genome SNP multi-fasta generated as allSNPForPhylo.fasta in folder",output
    snpFile.close()
############################################################################################################################################################    
class variant(object):
    def __init__(self, position, chromosome):
        self.position = position
        self.chromosome = chromosome
        self.varAlgoDict = {} #GATK : DATA, SAMTOOLS : DATA, etc
        self.msum_GATK = 0
        self.msum_SAMTOOLS = 0
        self.mutsGATK = ""
        self.mutsSAMTOOLS = ""
        self.sharedAnno = ""
    def getPos(self):
        return self.position
    def addSharedAnno(self, data): #independant of mapper data, general anno data
        self.sharedAnno = data
##    def getSharedAnnoo(self):
##        return self.sharedAnno
    def addUniqueAnno(self, varAlgoName_mapperNameCombo, data): #dependant on mapper data, ex aa change, aa pos
        self.varAlgoDict[varAlgoName_mapperNameCombo]["anno"] = data
        #cosists of: [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef.upper(),codonsMut.upper(),str(int(codonPosition)+1)]
        #Which is actually: AA_change_type, AA_change, AA_Codon_Pos, ref_codon, mut_codon, gene_pos
    def retrieveUniqueAnno(self,varAlgoName_mapperNameCombo):
        if varAlgoName_mapperNameCombo not in self.varAlgoDict:
            return ""
        else:
            return self.varAlgoDict[varAlgoName_mapperNameCombo]["anno"]
    def retrieveHeteroFreq(self,varAlgoName_mapperNameCombo):
        if varAlgoName_mapperNameCombo not in self.varAlgoDict:
            return ""
        else:
            return self.varAlgoDict[varAlgoName_mapperNameCombo]["hetero"]
    def addMapperData(self, varAlgoName, mapperName, ref,mut,qual,info):
        key = mapperName+"_"+varAlgoName
        if True:
        #if key not in self.varAlgoDict:
            if "GATK" in varAlgoName:
                self.msum_GATK += 1 
                #to do: this should be individual count for each variant in the list
            if "SAMTOOLS" in varAlgoName:
                self.msum_SAMTOOLS += 1
            ''' 
            variant object here is
            BWA_GATK : [{dict}] <----------IMPORTANT NOTE HERE THAT IT IS A LIST OF DICTIONARIES!
            i.e one list for each variant found at this posisition for this mapper+variant caller combo
            This was introduced to address the issue where mutation can be C -> A,T
            so have one list for C->A and one for C->T and whatever others.
            here dict has keys 
            and each key has a list corresponding to each variant found in it.
            '''
            self.varAlgoDict[key] = {}
            self.varAlgoDict[key]["anno"] = ['','','','','','']
            self.varAlgoDict[key]["ref"] = ref
            self.varAlgoDict[key]["mut"] = mut
            self.varAlgoDict[key]["qual"] = qual
            self.varAlgoDict[key]["info"] = info
            if "GATK" in varAlgoName:
                try:
                    temp = info.split(":")
                    self.varAlgoDict[key]["hetero"] = float(temp[1].split(",")[1])/float(temp[2])
                except:
                    print "Error calculating GATK hetero freq for", info
                    self.varAlgoDict[key]["hetero"] = "Calculation error"
                try:
                    self.varAlgoDict[key]["numreads"] = int(temp[2])
                except:
                    print "Error calculating numreads for", info
                    self.varAlgoDict[key]["numreads"] = "Calculation error"
            elif "SAMTOOLS" in varAlgoName:
                try:
                    temp = info.split(":")[-1].split(",")
                    self.varAlgoDict[key]["hetero"] = float(temp[1])/(float(temp[0])+float(temp[1]))
                    self.varAlgoDict[key]["numreads"] = int(temp[0])+int(temp[1])
                except:
                    print "Error calculating samtools hetero freq for", info
                    self.varAlgoDict[key]["hetero"] = "Calculation error" 
                    print "Error calculating numreads for", info
                    self.varAlgoDict[key]["numreads"] = "Calculation error"
##        else:
##            print "Error, trying to add data for file with already existing key combo"
##            print self.varAlgoDict
##            print self.varAlgoDict[key]
##            raw_input("this should not be able to happen, debug point X53632")
##            self.varAlgoDict[key]["anno"] = '','','','','',''
##            self.varAlgoDict[key]["ref"]= ref
##            self.varAlgoDict[key]["mut"] = mut
##            self.varAlgoDict[key]["qual"] =  qual
##            self.varAlgoDict[key]["info"] = info
##            if "GATK" in varAlgoName:
##                try:
##                    temp = info.split(":")
##                    self.varAlgoDict[key]["hetero"].append(float(temp[1].split(",")[1])/float(temp[2]))
##                except:
##                    print "Error calculating GATK hetero freq for", info
##                    self.varAlgoDict[key]["hetero"] = "Calculation error"
##                try:
##                    self.varAlgoDict[key]["numreads"] = int(temp[2])
##                except:
##                    print "Error calculating numreads for", info
##                    self.varAlgoDict[key]["numreads"] = "Calculation error"
##            elif "SAMTOOLS" in varAlgoName:
##                try:
##                    temp = info.split(":")[-1].split(",")
##                    self.varAlgoDict[key]["hetero"] = float(temp[1])/(float(temp[0])+float(temp[1]))
##                    self.varAlgoDict[key]["numreads"] = int(temp[0])+int(temp[1])
##                except:
##                    print "Error calculating samtools hetero freq for", info
##                    self.varAlgoDict[key]["hetero"] = "Calculation error"
##                    print "Error calculating numreads for", info
##                    self.varAlgoDict[key]["numreads"] = "Calculation error"
        return
    
    def updateMutations(self,mapperOrderList):
        for key in self.varAlgoDict:
            if "GATK" in key:
                self.mutsGATK += self.varAlgoDict[key]["mut"]+"/"
            if "SAMTOOLS" in key:
                self.mutsSAMTOOLS += self.varAlgoDict[key]["mut"] +"/"
                
    def getDataToWrite(self, pos, keyComboOrder,known_feature_properties, pos_to_feature_num_dict, featureNum_to_Anno_DataDict):
        #print keyComboOrder        
        #raw_input("This is the key combo order")
        #print "these are in this specific variant for varAlgoDict", self.varAlgoDict.keys()
        #only add the ietms found in keyComboOrder
        #returns everything that needs to be written to file as a list, in correct order 
        data = []
        data.append(self.position)
        data.append(self.chromosome)
        keyOrder = "ref","mut","qual","info","hetero","numreads"
        for combo in keyComboOrder:
            for key in keyOrder:
##                print self.varAlgoDict.keys()
##                print type(self.varAlgoDict[combo])
##                print self.varAlgoDict[combo]
##                print self.varAlgoDict[combo][key]
                if combo not in self.varAlgoDict: # and combo in params.usedKeyCombos:
                    #print "dont have this combo and def not this key:", combo, key
                    data.append("")
                    continue
                else:
                    #print "have this combo, adding data", combo, key
                    data.append(self.varAlgoDict[combo][key])
        data.append(self.msum_GATK )
        data.append(self.msum_SAMTOOLS)
        data.append(self.mutsGATK)
        data.append(self.mutsSAMTOOLS)

        #add unique anno data
        for keyCombo in keyComboOrder:
            annoData = self.retrieveUniqueAnno(keyCombo)
            if annoData:
                for x in annoData:
                    data.append(x) #This adds data for the: AA_change_type, AA_change, AA_Codon_Pos, ref_codon, mut_codon, gene_pos
            else:
                for z in range(6):
                    data.append("")
        #Now to add genomic annotation data
        
        anno_ranges = ""
        anno_type = ""
        orientation = ""
        anno_features = ""
        if self.sharedAnno == "intergenic":
            anno_type = "intergenic"
        else: #not intergenic
            if annotationAllowed:
                key = pos_to_feature_num_dict[pos]
                annotatedData = featureNum_to_Anno_DataDict[key[0]]
##                print annotatedData
##                print "-"*20
##                p = -1
##                for x in annotatedData:
##                    p+=1
##                    print p, x
##                raw_input("this is what annodata looks like now, make sure writing to file correct, extract the nessisary info from below")
                anno_ranges = annotatedData[0][0]
                anno_type = annotatedData[1]
                orientation = annotatedData[2]
                anno_features = annotatedData[3] #sort this in same order as known_feature_properties which comes from the embl anno file, iterate over it to get consistent order
                #calculatedData = annotatedData[1] #iterate over this - use mapper heading to mark it
            else:
                annotatedData = ["","","","","",""]

            #for key in params.usedKeyCombos:

            
        data.append(anno_ranges)
        data.append(anno_type)
        data.append(orientation)

        #Write the annotation features in consistent sorted order
        temp = {}
        for x in anno_features:
            temp[x[0]] = x[1].replace("\t","")
        for known_feature in known_feature_properties:
            if known_feature in temp:
                data.append(temp[known_feature])
            else:
                data.append("")
##        for x in calculatedData:
##            for y in x:
##                data.append(y)
        toRemove = ['\r','"',"'","\n"]
        dataToWrite = []
        for x in data:
            tempString = str(x)
            for d in toRemove:
                tempString=tempString.replace(d,'')
            dataToWrite.append(tempString)
            #f.write(tempString+"\t") 
##            dataString+=(str(x)+"\t")
##        dataString+="\n"
        return dataToWrite
###################################################################
                
                
            
    
############################################################################################################################################################
    
class paramaters(object):
    def __init__(self, binDir, globalDir, userPrefcpu, userPrefmem, inputDir, outputDir, readsType, userRef, trimMethod, BQSRPossible, emblFile, variantTools, filterSettings):
        self.epsilon = 0.2
        self.useBWA = filterSettings[0]
        self.useNOVO = filterSettings[1]
        self.useSMALT = filterSettings[2]
        self.gatkFlag = filterSettings[3]
        self.samtoolsFlag = filterSettings[4]
        self.mapperCount_GATK = filterSettings[5]
        self.mapperCount_SAMTOOLS = filterSettings[6]
        self.qualityCutOff_GATK = filterSettings[7]
        self.qualityCutOff_SAMTOOLS = filterSettings[8]
        self.minCoverage_GATK = filterSettings[9]
        self.minCoverage_SAMTOOLS = filterSettings[10]
        self.readFreqCutoff_GATK = filterSettings[11]
        self.readFreqCutoff_SAMTOOLS = filterSettings[12] 
        self.filterMappabilityPositions = filterSettings[13]
        self.filterCustomPositions = filterSettings[14]
        self.filterOnKeywords = filterSettings[15]
        self.junkTerms = filterSettings[16]
        self.minCov = filterSettings[17]
        self.minMappedReads = filterSettings[18]
##        if globalDir[-1] <> "/":
##            globalDir+= "/"
##        if outputDir[-1] <> "/":
##            outputDir+="/"
        self.usedKeyCombos = []
        self.inits = []
        self.emblFile = emblFile
        self.multiMode = True
        self.binDir = binDir
        self.globalDir = globalDir
        self.reference = os.path.join(self.globalDir+"/Reference/"+userRef+"/FASTA/")
        self.mappabilityDir = os.path.join(self.globalDir+"/Reference/"+userRef+"/Mappability/")
        self.exclusionListFolder = os.path.join(self.globalDir+"/Reference/"+userRef+"/EXCLUDE/")
        self.keywordsToRemove = os.path.join(self.globalDir+"/Reference/"+userRef+"/KEYWORDSTOREMOVE/")
        self.EMBL = os.path.join(self.globalDir+"/Reference/"+userRef+"/EMBL/")
        self.dbSNP = os.path.join(self.globalDir+"/Reference/"+userRef+"/dbSNP/")
        self.pheno = os.path.join(self.globalDir+"/Reference/"+userRef+"/PhenotypeDB/")
        self.lineage = os.path.join(self.globalDir+"/Reference/"+userRef+"/LineageMarkers/")
        self.exclusionList = os.path.join(self.globalDir+"/Reference/"+userRef+"/ExclusionList/")
        self.reads = "mixed"
        self.cores = userPrefcpu
        self.mem = str(userPrefmem)
        self.fastQ = inputDir
        self.outputDir = outputDir
        self.readsType = readsType
        self.trimMethod = trimMethod
        self.fastaList = []
        self.coreSplit = [1,1,1]
        self.BQSRPossible = BQSRPossible
        #############################################
        self.tools = self.globalDir+"/Tools/"
        if outputDir[-1] == "/":
             self.main = outputDir #output dir for all results
        else:
            self.main = outputDir+"/"   #output dir for all results

        self.mapperOut = self.main+"Results/" 
        self.BWAAligned = self.mapperOut+"BWA/"
        self.NOVOAligned = self.mapperOut+"NOVO/"
        self.SMALTAligned = self.mapperOut+"SMALT/"

        self.BWAAligned_aln = self.BWAAligned+"Alignment_Files/"
        self.NOVOAligned_aln = self.NOVOAligned+"Alignment_Files/"
        self.SMALTAligned_aln = self.SMALTAligned+"Alignment_Files/"
        ###################################
        if self.trimMethod == "No_Trim":
            self.trimmedFastQ = self.fastQ
        else:
            self.trimmedFastQ = os.path.join(outputDir+"FastQ_"+self.trimMethod+"/")
        self.fastQCStatsDir1 = os.path.join(outputDir+"fastQCStats/")
        self.fastQCStatsDir2 = os.path.join(outputDir+"fastQCStats_Trimmed/")

        #tool settings and paths
        self.insertmin = 0
        self.insertmax = 500
        self.java7 = self.tools+"jre1.7.0_51/bin/java"
        self.inits.append(self.java7)
        self.spolpred = self.tools+"spolpred/spolpred.run"
        self.inits.append(self.spolpred)
        self.smaltBinary = self.tools+"smalt-0.7.5/src/smalt"
        self.inits.append(self.smaltBinary)
        self.bwa = self.tools+"bwa-0.6.2/bwa"
        self.inits.append(self.bwa)
#        self.novoalign = self.tools+"novocraftV3-02-13/novoalign"
        self.novoalign = self.tools+"novocraft/novoalign"
        self.inits.append(self.novoalign)
        self.novoIndex = self.tools+"novocraft/novoindex"
        self.inits.append(self.novoIndex)
        self.SortSamDir = self.tools+"picard-tools-1.107/SortSam.jar"
        self.inits.append(self.SortSamDir)
        self.picardDirOnPc = self.tools+"picard-tools-1.107/ValidateSamFile.jar"
        self.inits.append(self.picardDirOnPc)
        self.picardAddReadGroup = self.tools+"picard-tools-1.107/AddOrReplaceReadGroups.jar"
        self.inits.append(self.picardAddReadGroup)
        #self.gatkHomeDir = self.tools+"GenomeAnalysisTK-3.4-46/GenomeAnalysisTK.jar"
        #raw_input("depending on version of usap switch this back to 3.5 GATL")
        #self.gatkHomeDir = self.tools+"GATK3.5/GenomeAnalysisTK.jar"
        self.gatkHomeDir = self.tools+"GATK/GenomeAnalysisTK.jar"
        self.inits.append(self.gatkHomeDir)
        self.scripts_trimming = self.globalDir+"/Scripts/Trimming/"
        self.scripts_BWA = self.globalDir+"/Scripts/BWA/"
        self.scripts_NOVO = self.globalDir+"/Scripts/NOVO/"
        self.scripts_SMALT = self.globalDir+"/Scripts/SMALT/"
        self.scripts_StrainIdentification = self.globalDir+"/Scripts/StrainIdentification/"
        self.markDuplicates = self.tools+"picard-tools-1.107/MarkDuplicates.jar"
        self.inits.append(self.markDuplicates)
        self.fastQCPath = self.tools+"FastQC/fastqc"
        self.inits.append(self.fastQCPath)
        self.picardCreateSequenceDictionary = self.tools+"picard-tools-1.107/CreateSequenceDictionary.jar"
        self.inits.append(self.picardCreateSequenceDictionary)
        self.bedtools = self.tools+"bedtools2-2.25/bin/genomeCoverageBed"
        self.inits.append(self.bedtools)
        self.fastXTrimmer = self.tools+"fastx_toolkit/fastx_trimmer"
        self.inits.append(self.fastXTrimmer)
        self.fastXClipper = self.tools+"fastx_toolkit/fastx_clipper"
        self.inits.append(self.fastXClipper)
        self.trimOMatic = self.tools+"Trimmomatic-0.32/trimmomatic-0.32.jar"
        self.inits.append(self.trimOMatic)
        self.trimOMaticParams = "2:30:10 LEADING:20 TRAILING:20 SLIDINGWINDOW:4:20 MINLEN:36" 
        #self.qualimap = self.tools+"qualimap_v2.0/qualimap"
        #self.inits.append(self.qualimap)
        self.SAIDIR = self.BWAAligned #to save space, allows deleting initial fastq files)
        #self.msort = os.path.join(self.tools+"msort/msort")
        #self.inits.append(self.msort)
        #self.shuffle =  self.binDir+"/shuffleSequences_fastq.pl"
        #self.inits.append(self.shuffle)
##        self.bcftools = self.tools+"samtools-0.1.19/bcftools/bcftools"
        self.bcftools = self.tools+"bcftools-1.3/bcftools"
        self.inits.append(self.bcftools)
##        self.samtools = self.tools+"samtools-0.1.8/samtools"
        self.samtools = self.tools+"samtools-1.3/samtools"
        self.inits.append(self.samtools)




#BEGINNING OF PHENOTYPE MATHCING
###############################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
'''
This includes VCF compression of same AA codon postions SNP to correctly match to DB.
For indels only using position and ref/mut data since the AA codon and AABP info is not correctly calculated
'''

'''
this program primarily makes use of gene coordinate data
if absence of gene coordinate data it will make use of genomic posisiton
failing this it will make use of AA codon postion
'''
'''
input database format:
Col1: position
Col2: ref    for example A or AA or AAA....
Col3: mut    for exmplae - or C or CC or CCC....
Col4...N: Information cols to be added to output (phenotype, reference etc)

ref:mut A -> - means delete bp A
ref:mut A -> C means snp change A to C
ref:mut ATC --> AC means delete T
ref:mut ATC --> ATGGC means insert GG

  
Makes use of SNPs, indel and large Deletions for report
Thus filtered SNP, filtered indels, Novoalign Gen cov

overview:
for each filename in snp vcf folder:
    fileData = []
    store all dr positions and dr gene ranges
    for each snp file:
        match to database
    for each indel file:
        match 
    for each large del file 
        match
    store fileData results (snp, indel, largedel)
store master summary

'''
def translate(seq):
    seq = seq.upper()
    gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }
 
    #print seq
    protSeq = ''
    for x in range(0,len(seq),3):
        if gencode.has_key(seq[x:x+3]) == True:
            protSeq += gencode[seq[x:x+3]]
        else:
       #     print "Warning, sequence is not a multiple of 3...truncating sequence..."
       #     raw_input()
            return protSeq
 
    return protSeq
    
def loadAllKnownVariants(variantListName):
    #Store all known phenotypes

##    os.chdir(variantListDir)
    f= open(variantListName,'r')
    f.readline()
    allVariantsByPos = {}
    allKnownGenes = {}
    PHENO_ORDER = []
    for line in f:
        temp = line.split("\t")
        tempPheno = temp[9]
        if tempPheno not in PHENO_ORDER:
            PHENO_ORDER.append(tempPheno)
        pos = temp[1] #may have more than one type of muation at same pos
        if "/" in pos:
            pos = pos.split("/")[0]
        gene = temp[3]
        if pos == "" or pos == "-": #then add to gene dictionary instead
            if gene == "" or gene == "-":
                print temp
                raw_input("This data point is problematic, no pos or gene data!")
            if gene not in allKnownGenes:
                allKnownGenes[gene] =  [temp]
            else:
                allKnownGenes[gene].append(temp)
        elif pos not in allVariantsByPos:
            allVariantsByPos[pos] = [temp] #create a list of lists
        else:
            allVariantsByPos[pos].append(temp) #add to list
    f.close()
    PHENO_ORDER.sort()
    return allVariantsByPos, allKnownGenes, PHENO_ORDER
def extractVariantsFromFilteredVariants(fileX,FILTERED_VARIANTS, annotationAllowed):
    def convertAALetterChange(s):
        #To convert A:I,I,I to A/I
        s = s.replace('"','')
        if ":" not in s:
            return ""
        ref = s[0]
        data = s[2:]
        data = data.split(",")
        mut = data[2]
        if mut == "-":
            mut = data[1]
        if mut == "-":
            mut = data[2]  
        return ref+"/"+mut #may sometimes return A/Syn
    ##############################################################
    variantData = []
    os.chdir(FILTERED_VARIANTS)
    f = open(fileX,'r')
    totalVariants = 0
    print "Loading Variant data from file: ", f.name
    header = f.readline()
    keyWordPositionDict = extractKeyPositionsFromHeaderForPheno(header)
##    print keyWordPositionDict
##    print header
    for line in f:
        totalVariants += 1
        dataForFilter = extractDataFromAnnoFileLineForPheno(line,keyWordPositionDict)
        Pos = dataForFilter["pos"]

        #Establish the reference base complete
        #################################
##        print dataForFilter.keys()
##        raw_input("debugging point 456456456")
        tempOrder = ["ref_NOVO_GATK","ref_BWA_GATK","ref_SMALT_GATK","ref_BWA_SAMTOOLS","ref_NOVOALIGN_SAMTOOLS","ref_SMALT_SAMTOOLS"]
        for tempKey in tempOrder:
            if tempKey not in dataForFilter:
                continue
            else:
                ref = dataForFilter[tempKey] #Prefer NOVOAlign data
                break
        #Establish the mutation
        #################################
        for tempKey in tempOrder:
            if tempKey.replace("ref","mut") not in dataForFilter:
                continue
            else:
                mut = dataForFilter[tempKey.replace("ref","mut")] #Prefer NOVOAlign data
                break
        #################################
        if not annotationAllowed: 
            AALetterChange = "" 
            Codon = "" 
            RefCodon = "" 
            MutCodon = "" 
            Locus = ""
            GenePos = ""
        elif dataForFilter["feature_type"] == "intergenic":  
            Locus = dataForFilter["locus_tag"].replace(" ","")            
            AALetterChange = "intergenic" 
            Codon = "intergenic"  
            RefCodon = "intergenic"  
            MutCodon = "intergenic"  
            GenePos = "intergenic"
        else:
            #### GATK
            if "AA_change_NOVO_GATK" in dataForFilter:
                AALetterChange = dataForFilter["AA_change_NOVO_GATK"]#convertAALetterChange(temp[17])
                Codon = dataForFilter["AA_Codon_Pos_NOVO_GATK"]
                RefCodon = dataForFilter["ref_codon_NOVO_GATK"]
                MutCodon = dataForFilter["mut_codon_NOVO_GATK"]
                GenePos = dataForFilter["gene_pos_NOVO_GATK"]
            else:
                AALetterChange = ""
            if AALetterChange == "":
                if "AA_change_BWA_GATK" in dataForFilter:
                    AALetterChange = dataForFilter["AA_change_BWA_GATK"]#convertAALetterChange(temp[17])
                    Codon = dataForFilter["AA_Codon_Pos_BWA_GATK"]
                    RefCodon = dataForFilter["ref_codon_BWA_GATK"]
                    MutCodon = dataForFilter["mut_codon_BWA_GATK"]
                    GenePos = dataForFilter["gene_pos_BWA_GATK"]
                else:
                    AALetterChange = ""
            if AALetterChange == "":
                if "AA_change_SMALT_GATK" in dataForFilter:
                    AALetterChange = dataForFilter["AA_change_SMALT_GATK"]#convertAALetterChange(temp[17])
                    Codon = dataForFilter["AA_Codon_Pos_SMALT_GATK"]
                    RefCodon = dataForFilter["ref_codon_SMALT_GATK"]
                    MutCodon = dataForFilter["mut_codon_SMALT_GATK"]
                    GenePos = dataForFilter["gene_pos_SMALT_GATK"]
                else:
                    AALetterChange = ""
                
            ###### SAMTOOLS
            if AALetterChange == "":
                if "AA_change_NOVO_SAMTOOLS" in dataForFilter:
                    AALetterChange = dataForFilter["AA_change_NOVO_SAMTOOLS"]#convertAALetterChange(temp[17])
                    Codon = dataForFilter["AA_Codon_Pos_NOVO_SAMTOOLS"]
                    RefCodon = dataForFilter["ref_codon_NOVO_SAMTOOLS"]
                    MutCodon = dataForFilter["mut_codon_NOVO_SAMTOOLS"]
                    GenePos = dataForFilter["gene_pos_NOVO_SAMTOOLS"]
                else:
                    AALetterChange = ""
            if AALetterChange == "":
                if "AA_change_BWA_SAMTOOLS" in dataForFilter:
                    AALetterChange = dataForFilter["AA_change_BWA_SAMTOOLS"]#convertAALetterChange(temp[17])
                    Codon = dataForFilter["AA_Codon_Pos_BWA_SAMTOOLS"]
                    RefCodon = dataForFilter["ref_codon_BWA_SAMTOOLS"]
                    MutCodon = dataForFilter["mut_codon_BWA_SAMTOOLS"]
                    GenePos = dataForFilter["gene_pos_BWA_SAMTOOLS"]
                else:
                    AALetterChange = ""
            if AALetterChange == "":
                if "AA_change_SMALT_SAMTOOLS" in dataForFilter:
                    AALetterChange = dataForFilter["AA_change_SMALT_SAMTOOLS"]#convertAALetterChange(temp[17])
                    Codon = dataForFilter["AA_Codon_Pos_SMALT_SAMTOOLS"]
                    RefCodon = dataForFilter["ref_codon_SMALT_SAMTOOLS"]
                    MutCodon = dataForFilter["mut_codon_SMALT_SAMTOOLS"]
                    GenePos = dataForFilter["gene_pos_SMALT_SAMTOOLS"]
                else:
                    AALetterChange = ""
                    Codon = ""
                    RefCodon = ""
                    MutCodon = ""
                    GenePos = ""

            Locus = dataForFilter["locus_tag"].replace(" ","")    
            if len(ref) > 1 or len(mut) > 1: #This is an indel and the calculated data is not accurate ans should not be used for pheno predict 
                AALetterChange = "INDEL"
##            else:       
##                tempRefAALetter = translate(RefCodon) # the reference AA letter
##                newAALetterChange = translate(MutCodon) #the new mutated aa letter
##                if tempRefAALetter <> newAALetterChange:
##                    AALetterChange = tempRefAALetter+"/"+newAALetterChange
##                else:
##                    AALetterChange = AALetterChange #there is no change its a synonomous change, will keep original style data syn,syn,syn
        try:
            variantData.append([Pos,ref,mut,Codon,RefCodon,MutCodon,Locus,AALetterChange,GenePos]) 
        except:
            print "No variants found in filtered file:", f.name, "in folder", FILTERED_VARIANTS
            return [] 
    f.close()
    if debugMode:
        print len(variantData), "variants loaded"
    return variantData
def extractKeyPositionsFromHeaderForPheno(header):
    #Here keyWordList contains names of the columns we want to filter based on the column value
    keyWordDict = {}
    s = '''pos
    ref_BWA_GATK
    mut_BWA_GATK
    ref_BWA_SAMTOOLS
    mut_BWA_SAMTOOLS
    ref_NOVO_GATK
    mut_NOVO_GATK
    ref_NOVO_SAMTOOLS
    mut_NOVO_SAMTOOLS
    ref_SMALT_GATK
    mut_SMALT_GATK
    ref_SMALT_SAMTOOLS
    mut_SMALT_SAMTOOLS
    mut_per_mapper_GATK
    mut_per_mapper_SAMTOOLS
    AA_change_type_BWA_GATK
    AA_change_BWA_GATK
    AA_Codon_Pos_BWA_GATK
    ref_codon_BWA_GATK
    mut_codon_BWA_GATK
    gene_pos_BWA_GATK
    AA_change_type_BWA_SAMTOOLS
    AA_change_BWA_SAMTOOLS
    AA_Codon_Pos_BWA_SAMTOOLS
    ref_codon_BWA_SAMTOOLS
    mut_codon_BWA_SAMTOOLS
    gene_pos_BWA_SAMTOOLS
    AA_change_type_NOVO_GATK
    AA_change_NOVO_GATK
    AA_Codon_Pos_NOVO_GATK
    ref_codon_NOVO_GATK
    mut_codon_NOVO_GATK
    gene_pos_NOVO_GATK
    AA_change_type_NOVO_SAMTOOLS
    AA_change_NOVO_SAMTOOLS
    AA_Codon_Pos_NOVO_SAMTOOLS
    ref_codon_NOVO_SAMTOOLS
    mut_codon_NOVO_SAMTOOLS
    gene_pos_NOVO_SAMTOOLS
    AA_change_type_SMALT_GATK
    AA_change_SMALT_GATK
    AA_Codon_Pos_SMALT_GATK
    ref_codon_SMALT_GATK
    mut_codon_SMALT_GATK
    gene_pos_SMALT_GATK
    AA_change_type_SMALT_SAMTOOLS
    AA_change_SMALT_SAMTOOLS
    AA_Codon_Pos_SMALT_SAMTOOLS
    ref_codon_SMALT_SAMTOOLS
    mut_codon_SMALT_SAMTOOLS
    gene_pos_NOVO_GATK
    gene_pos_BWA_GATK
    gene_pos_SMALT_GATK
    gene_pos_NOVO_SAMTOOLS
    gene_pos_BWA_SAMTOOLS
    gene_pos_SMALT_SAMTOOLS
    Anno_feature_range
    feature_type
    orientation
    drugResistanceMutations
    gene
    locus_tag
    product
    '''
    temp = s.split()
    for x in temp:
        keyWordDict[x] = None

    keyWordPositionDict = {}

    temp = header.split("\t")
    pos = -1
    for element in temp:
        pos += 1
        if element in keyWordDict:
            keyWordDict[element] = True
            keyWordPositionDict[element] = pos #Dictionary of positions in the annofile that need to extract values from for filtering
    for key in keyWordDict:
        if keyWordDict[key] == None:
            keyWordPositionDict[key] = None
    return keyWordPositionDict
        ################################################################################################3
def extractDataFromAnnoFileLineForPheno(line,keyWordPositionDict):
    dataForFilter = {}
    line = line.split("\t")
    for keyWord in keyWordPositionDict:
        colPos = keyWordPositionDict[keyWord]
        if colPos <> None:
            try:
                dataForFilter[keyWord] = line[colPos]
            except:
                print line, len(line)
                print colPos
                print keyWord
                raw_input("list index out of range error, debug poing 556707")
    return dataForFilter
        
def findPhenoMarkersSNP_indel(fileX,FILTERED_VARIANTS,variantPositionDict, allGenesDict,MTB, annotationAllowed):  
    '''
    OVERVIEW AND ORDER OF OPERATION:
        
    FIRST CHECK IF THE POSITION MATHCES
        SECOND CHECK IF THE CODONPOS MATCH
        THRID CHECK IF THE CODON BP INFO MATCH   
        IF NO CODON BP INFO 
            CHECK IF THE REF/MUT DATA MATCHES <--- important
    CHECK IF GENE MATCHES
        CHECK IF CODON POS MATCH
        CHECK IF CODON BP INFO MATCH
        IF NO CODON BP INFO
            CHECK IF REF/MUT DATA MATCHES <--- important
            
    at this point...need to check the vcf data and what data to use to match first
    it goes:
        position, codonnum, codonbp, if no match check if syn/nonsyn - if nonsyn report new mutation at known codon --> possible DR
        if no pos match (then could be due to gaps in the db now check on gene level)
        gene, codonnum if not match codon num check of syn or nonsyn if nonsyn report new mut at knon gene --> possible DR
        if match codonnum check if match codonbp - not if not check if s/nonsyn if s report new mut at knwon codon --> possible DR 
        '''
        
    #find all phenotype associated markers in SNP and INDEL files for this sample
    PHENO_data = []
    tempFileName = fileX #fileX.split("_")[0]+"_gatk_snps_FILTERED.vcf"
    totalNGSData = extractVariantsFromFilteredVariants(tempFileName,FILTERED_VARIANTS, annotationAllowed)
    #print totalNGSData # last position is the genepos
    #print FILTERED_VARIANTS
    #print fileX
    #print len(totalNGSData)
    #print type(totalNGSData)
    #print totalNGSData[0]
    
    if MTB:
        #Special check for M.tb PZA resistance, will be skipped if not M.tb used as reference.
        pzaDict = {}
        pzaDict[35] = ["L/R"]
        pzaDict[37] = ["E/V"]
        pzaDict[65] = ["S/S"]
        pzaDict[96] = ["K/K"]
        pzaDict[110] = ["D/G"]
        pzaDict[114] = ["T/M"]
        pzaDict[130] = ["V/A"]
        pzaDict[163] = ["V/A"]
        pzaDict[170] = ["A/V"]
        pzaDict[180] = ["V/I"]
    else:
        pzaDict = {}
  
    for variantData in totalNGSData: #Both snps and indel data
        temp_PHENO_data = [] #might be multiple hits to the database, will use the best one basked on rank
        if MTB: 
            if ("Rv1908c" in variantData) and len(variantData[1]) <> len(variantData[2]) and len(variantData[1])%3 <> len(variantData[2])%3: # Then its a frameshift
                genePos = variantData[-1]
                #Two cases, one - it is a new non-syn change -all all except known markers not involved in DR
                #two - it is an indel - simply check if the lenghts mismatch
                #[[2, ['2288764', 'pncA', 'Rv2043c', '478', 'T/G', '', 'PYRAZINAMIDE', '160', 'ACA/CCA', '', 'T/P', '', 'TBDreaMDB', '', '', '', '', '', '', '', '', '', '', '', '3\n']]]
                if debugMode:
                    print "Adding assume katG DR to list"
                temp_PHENO_data.append([1,["", variantData[0], 'katG', 'Rv1908c', genePos,"INDEL",variantData[1]+"/"+variantData[2],variantData[1],variantData[1],'ISONIAZID', 'ASSUME_DR\n']])                     
            
            if ("Rv2043c" in variantData) and (len(variantData[1]) <> len(variantData[2])):
                genePos = variantData[-1]
                #Two cases, one - it is a new non-syn change -all all except known markers not involved in DR
                #two - it is an indel - simply check if the lenghts mismatch
                if debugMode:
                    print "found possible pncA mutation", variantData, fileX                    
                if variantData[3] in pzaDict:
                    if variantData[7] == pzaDict[variantData[3]]: #skip known non dr causing markers
                        if debugMode:
                            raw_input("Found a case of a non DR causing mutation in pncA skipping this one")
                        continue
                    else: #score all other pnca mutations as DR
                        #[[2, ['2288764', 'pncA', 'Rv2043c', '478', 'T/G', '', 'PYRAZINAMIDE', '160', 'ACA/CCA', '', 'T/P', '', 'TBDreaMDB', '', '', '', '', '', '', '', '', '', '', '', '3\n']]]
                        if debugMode:
                            print "Adding assume DR to list"
    
                        temp_PHENO_data.append([1,["", variantData[0], 'pncA', 'Rv2043c', genePos,"INDEL",variantData[1]+"/"+variantData[2],variantData[1],variantData[1],'PYRAZINAMIDE', 'ASSUME_DR\n']]) 
                        #if debugMode:
                        #    print fileX
                        #    raw_input("pnca resistance found")
                        #return PHENO_data
                else: #score all other pnca mutations as DR
                    temp_PHENO_data.append([1,["", variantData[0], 'pncA', 'Rv2043c', genePos,"INDEL",variantData[1]+"/"+variantData[2],variantData[1],variantData[1],'PYRAZINAMIDE', 'ASSUME_DR\n']])
                    #if debugMode:
                    #    print fileX
                    #    raw_input("pnca resistance found")

        
        #print "^"*15
        #print snpData
        bestMatch = [-1,-1] #The best matching dabase entry for this vcf mutation --> #LEVEL, DATA
        #Here level is the quality of the match 
            #level 0 is exact match on Pos, CodonNum, CodonBP+MutBP
            #level 1 is excact match on Pos + AA Letter Change OR ref+mut BP change 
            #level 2 is codon position match of a new non-synonoumous mutation but without exact match...also must be synonoumous
            #level 3 is non-syn change in gene that is at a new codon
        
        #EXTRACT DATA FOR THIS POSITION FROM DB
        vcfPos = variantData[0]
        vcfRef = variantData[1]
        vcfMut = variantData[2] #one per line, already been split if more than 1.
        vcfAACodonNum = variantData[3]
        #vcfRefCodon = variantData[4]
        vcfMutCodon = variantData[5] #can be a list
        vcfLocus = variantData[6]
        vcfLastAALetterChange = variantData[7] #can be a list
        
        #check if position matches
        if vcfPos in variantPositionDict: #FIRST CHECK IF THE POSITION MATHCES
            if debugMode:
                print "known position found", vcfPos
            #can either be an excat match or a new/similar mutation at same pos or a synonomous mutation
            #iterate over position dictionary for best match
            knownVariantCount = 0
            for knownVariant in variantPositionDict[vcfPos]: #can be >1 known mutation at this pos
                knownVariantCount += 1
                #if debugMode:
                #    print vcfPos
                #    print "comparing to", knownVariant
                #
                #    print "================"
                #    print variantData
                #    print "VS"
                #    print knownVariant
                #    print "================"
                #    print "KNOWNVARIANT NUM FOR THIS POS", knownVariantCount,"/",len(variantPositionDict[vcfPos]), "previous bestmatch level", bestMatch[0]
                #    raw_input()
                #each element contains: [chromosomePos, locus,locus_tag,gene_coordinates,refBP,mutBP,Drug(phenotype),extrainfo1...extrainfoN  
                #EXTRACT DB DATA FOR THIS KNOWN VARIANT POSITION
                #print knownVariant
                #raw_input()
                DBLocus = knownVariant[2]
                DBlocus_tag = knownVariant[3]
                DBGene_coordinates  = knownVariant[4] 
                DBReference = knownVariant[6]  #can be "-","A","AA","A.....A"
                ###########
                #uncompact DB mutation A/C or ACACACA/G
                slashCount = 0
                for char in DBReference:
                    if char == "/":
                        slashCount += 1
                if slashCount > 1:
                    DBReference = "FORMAT_ERROR"
                    DBMutation = "FORMAT_ERROR"
                elif slashCount ==1:
                    DBReference = knownVariant[6].split("/")[0]   #can be "-","A","AA","A.....A"
                    DBMutation = knownVariant[6].split("/")[1]
               
                DBPPhenotype = knownVariant[9]
                DBAACodonNum = knownVariant[5]
                if "/" in knownVariant[7]:
                    DBAACodonRef = knownVariant[7].split("/")[0]
                    DBAACodonMut = knownVariant[7].split("/")[1]
                else:
                    DBAACodonRef = ""
                    DBAACodonMut = ""
                DBAALetterChange = knownVariant[8]
                #print knownVariant
                #print "database variables are initialized as follows"
                #print [DBAACodonNum],[DBAACodonRef],[DBAACodonMut],[DBAALetterChange]
                
                #QUALITY CONTROL - all variants with nucleoptide position info MUST have AA codonNum info
                #if DBAACodonNum == "" or DBAACodonNum == "-":
                #    print knownVariant
                #    raw_input("Have position match but no AA num info - fix the database now")
                #if DBReference <> vcfRef:
                #    print "Fix this, should not happen!"
                #    print "error, mismatch between ref sequences:"
                #    print vcfRef, DBReference
                #    print "from:", snpData
                #    print "DB data was ",knownVariant
                #    raw_input()
                #END QUAL CONTROL
                
                #Assume that have aa codon num info...
                #CHECK IF THE CODONPOS MATCH
                if vcfAACodonNum == DBAACodonNum and DBAACodonNum <> "": #it is a knwon codon position 
                    if debugMode:
                        print "known position, known codon position"
                        #THRID CHECK IF THE CODON BP INFO MATCH 
                        print [vcfMutCodon], [DBAACodonMut], vcfMutCodon == DBAACodonMut
##                    print vcfLastAALetterChange
                    if vcfMutCodon == DBAACodonMut:
                        if debugMode:
                            print "found exact match:",knownVariant # on Pos+ CodonNum + CodonBP"
                        bestMatch = [0,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                        #print bestMatch
                    elif "[" in vcfMutCodon: #then we have more than one mutated codon possibility
                        for vcfMutCodonIter in vcfMutCodon.replace("[","").replace("]","").replace(" ","").replace("'","").split(","):
                            if debugMode:
                                print "matching ", [vcfMutCodonIter],'and',[DBAACodonMut]
                            if vcfMutCodonIter == DBAACodonMut:
                                if debugMode:
                                    print "found exact match:",knownVariant # on Pos+ CodonNum + CodonBP"
                                bestMatch = [0,knownVariant]
                                temp_PHENO_data.append(bestMatch)
                            
                    elif vcfLastAALetterChange == DBAALetterChange: #There is now AA bp info but the aa change A:Y is known
                        if debugMode:
                            print "found exact match:",knownVariant # on Pos + CodonNum + AALETTER CHANGE" , variantData, knownVariant
                        bestMatch = [1,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                    elif "[" in vcfLastAALetterChange:
                        for vcfLastAALetterChangeIter in vcfLastAALetterChange.replace("[","").replace("]","").replace(" ","").replace(":","/").replace("'","").split(","):
                            if vcfLastAALetterChangeIter == DBAALetterChange: #There is now AA bp info but the aa change A:Y is known
                                if debugMode:
                                    print "found exact match:",knownVariant # on Pos + CodonNum + AALETTER CHANGE" , variantData, knownVariant
                                bestMatch = [1,knownVariant]
                                temp_PHENO_data.append(bestMatch)
            
                    elif ":" in vcfLastAALetterChange and "syn" not in vcfLastAALetterChange:
                        print "new codon change found at known codon", knownVariant
                        bestMatch = [2,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                        #raw_input()
                    #else:
                    #    print "Error 676, ignoring syn change or no info on AA change in VCf", [vcfLastAALetterChange]
                    #    print variantData
                    #    print "the best match thusfar is", bestMatch
                    #    raw_input()
                                
                                
                #IF NO CODON BP INFO 
                #CHECK IF THE REF/MUT DATA MATCHES <--- important
                elif DBAACodonNum == "" or DBAACodonNum == "-": 
                    #print "no DBAACodon info, matching to pos and ref/mut"
                    #print [vcfRef],[DBReference], [vcfMut],[DBMutation], vcfRef == DBReference , vcfMut == DBMutation
                    #raw_input() 
                    #Check if match using only chr pos and ref and mut data, nothing else - usally for indels or promoter mutations
                    if vcfRef == DBReference and vcfMut == DBMutation: #an exact nucleotide match to the lookupdatabase
                        slashCount = 0
                        for char in DBMutation:
                            if char == "/":
                                slashCount += 1
                        if slashCount > 1:
                            raw_input("Instance where using multiple slahses but prog did not use codonBP info... will have to fix this entry in the DB")
                        if debugMode:
                            print "Exact mutation found:", knownVariant #,"and", variantData
                        bestMatch = [1,knownVariant]
                        temp_PHENO_data.append(bestMatch)      
                else:
                    continue
                    #print "Close match found..."
                    #print "matching error begin here:"
                    #print bestMatch 
                    #print variantData
                    #print knownVariant
                    #print "should not happen - getting to this point means that the chr postion matches but not the aa codon number...this means a database formatting error"
                    #raw_input()      
        #Getting to here means that there is no nucleotide info for this postion or did not fully match a known postion      
        #lets see if we can find a better match than the by-position method above        
        elif vcfLocus in allGenesDict and bestMatch[0] <> 0 and bestMatch[0] <> 1: #The genes match, now check if AA codon and AA change match
            #print "known gene found", bestMatch
            #Iterate over the gene dictionary data:
            knownVariantCount = 0
            for knownVariant in allGenesDict[vcfLocus]:
                #print "comparing to (gene)", knownVariant
                knownVariantCount += 1
                #print "KNOWNVARIANT NUM FOR THIS GENE", knownVariantCount
                #THERE IS NO POSITION DATA FOR THIS 
                #DBLocus = knownVariant[2]
                #DBlocus_tag = knownVariant[3]
                #DBGene_coordinates  = knownVariant[4]
                DBReference = knownVariant[6]  #can be "-","A","AA","A.....A"
                ###########
                #uncompact DB mutation A/C or ACACACA/G
                slashCount = 0
                for char in DBReference:
                    if char == "/":
                        slashCount += 1
                if slashCount > 1:
                    DBReference = "FORMAT_ERROR"
                    DBMutation = "FORMAT_ERROR"
                elif slashCount ==1:
                    DBReference = knownVariant[6].split("/")[0]   #can be "-","A","AA","A.....A"
                    DBMutation = knownVariant[6].split("/")[1]
                #DBMutation = knownVariant[5]   #can be "-","A","AA","A.....A"
                #DBPPhenotype = knownVariant[9]
                DBAACodonNum = knownVariant[5]
                if "/" in knownVariant[7]:
                    #DBAACodonRef = knownVariant[7].split("/")[0]
                    DBAACodonMut = knownVariant[7].split("/")[1]
                else:
                    #DBAACodonRef = ""
                    DBAACodonMut = ""
                DBAALetterChange = knownVariant[8]
                
##                if debugMode:
##                    print "found a matching PhenoType associated gene", vcfLocus,"in", fileX
##                    print "comparing to",knownVariant
                ################################################################
                if vcfAACodonNum == DBAACodonNum: #it is a knwon codon position 
                    print "known position, known codon position"
                    #THRID CHECK IF THE CODON BP INFO MATCH 
                    if vcfMutCodon == DBAACodonMut:
                        print "found exact match:",knownVariant # on Pos+ CodonBP"
                        bestMatch = [0,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                        print
                        #raw_input()
                    elif "[" in vcfMutCodon:
                        for vcfMutCodonIter in vcfMutCodon:
                            if vcfMutCodonIter == DBAACodonMut.replace("[","").replace("]","").replace(" ","").replace("'","").split(","):
                                if debugMode:
                                    print "found exact match:",knownVariant # on Pos+ CodonBP"
                                bestMatch = [0,knownVariant]
                                temp_PHENO_data.append(bestMatch)
                        #raw_input()
                        
                    elif vcfLastAALetterChange == DBAALetterChange: #There is now AA bp info but the aa change A:Y is known
                        if debugMode:
                            print "found exact match:", knownVariant # on Pos + CodonNum + AALETTER CHANGE" 
                        bestMatch = [1,knownVariant]
                        temp_PHENO_data.append(bestMatch)

                    elif "[" in vcfLastAALetterChange:
                        for vcfLastAALetterChangeIter in vcfLastAALetterChange.replace("[","").replace("]","").replace(" ","").replace(":","/").replace("'","").split(","):
                            if vcfLastAALetterChangeIter == DBAALetterChange: #There is now AA bp info but the aa change A:Y is known
                                if debugMode:
                                    print "found exact match:", knownVariant # on Pos + CodonNum + AALETTER CHANGE" 
                                bestMatch = [1,knownVariant]
                                temp_PHENO_data.append(bestMatch)
                    else:
                        if ":" in vcfLastAALetterChange and "syn" not in vcfLastAALetterChange:
                            bestMatch = [2,knownVariant]
                            temp_PHENO_data.append(bestMatch)
                    #IF NO CODON BP INFO 
                        #CHECK IF THE REF/MUT DATA MATCHES <--- important
                elif DBAACodonNum == "" or DBAACodonNum == "-": 
                    #Check if match using only chr pos and ref and mut data, nothing else - usally for indels or promoter mutations
                    if vcfRef == DBReference and vcfMut == DBMutation: #an exact nucleotide match to the lookupdatabase
                        slashCount = 0
                        for char in DBMutation:
                            if char == "/":
                                slashCount += 1
                        if slashCount > 1:
                            raw_input("Instance where using multiple slahses in phenoDB but program did not use codonBP info... will have to fix this entry in the DB")
                            
                        if debugMode:
                            print "Exact mutation found:", knownVariant,"and", variantData
                        bestMatch = [1,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                
                    elif ":" in vcfLastAALetterChange and "syn" not in vcfLastAALetterChange and bestMatch[0] <> 2:
                        bestMatch = [3,knownVariant]
                        temp_PHENO_data.append(bestMatch)
                        #raw_input("new mutation at new codon in gene")
                    else:
                        print "Error 767, ignoring syn change or no info on AA change in VCf", [vcfLastAALetterChange]
                        print variantData
                        raw_input()
                ###########################################################################
        
        #From all the data points detected for this variant, select only the relevant ones
        #These could be same pos with more than one phenotype
        #also to remove multiple hits to the same AA change - to just store the optimal match
        if temp_PHENO_data <> []:
            PHENO_data.append(temp_PHENO_data) 
        #print variantData
        #for hit in temp_PHENO_data: 
        #    print hit
        #print "bestMatch is"
        #print bestMatch
        #raw_input()
##    print "this is pheno data"
##    print PHENO_data
##    raw_input()
    return PHENO_data # a list of DR matches from snp and indel data.

def findPhenoMarkersLARGE_DEL(inputFile,FILTERED_DELETIONS,variantPositionDict, allGenesDict, MTB):
    '''
    scan the list of known positions and genes for matches
    '''
    fileX = None
    DR_status_list = []
    os.chdir(FILTERED_DELETIONS)
    for fileX in os.listdir(FILTERED_DELETIONS):
        if fileX.split("_")[0] == inputFile.split("_")[0]:
            #del_file=fileX
            break  
    #print FILTERED_DELETIONS
    #raw_input() 
    if fileX == None:
        return []        
    f = open(fileX,"r")
    #print "Rv2043c" in allGenesDict
    for line in f:
        #print [line]
        #raw_input()
        deleted_rvNum = line.split("\t")[14]
        deleted_rvNum = deleted_rvNum.strip()
        deleted_rvNum = deleted_rvNum.replace("'","")
        deleted_rvNum = deleted_rvNum.replace('"',"")

        if deleted_rvNum == "":
            continue
        #print [deleted_rvNum]
        #print deleted_rvNum in allGenesDict
        if deleted_rvNum not in allGenesDict:
            continue
            
        elif MTB and deleted_rvNum == "Rv2043c":
            DR_status_list.append([0,["PYRAZINAMIDE","pncA","deletion (Make sure coverage of the genome is acceptable (>30), if not - this could be an error)"]])
        elif MTB and deleted_rvNum == "Rv1908c":
            DR_status_list.append([0,["ISONIAZID","katG","deletion (Make sure coverage of the genome is acceptable (>30), if not - this could be an error)"]])
        else:
            DR_status_list.append([3,deleted_rvNum])
    f.close()
    return DR_status_list
    
def processData(fileX,outputFolder,snp_and_indel_Data,largeDelData,DR_Order,DR_CLASS,MTB):
    #print largeDelData
    #raw_input()
    all_DR_data_per_DR = {}
    #shortNames = ["RIF",
    #"CAP",
    #"PZA",
    #"AMI",
    #"CYC",
    #"EMB",
    #"ETH",
    #"INH",
    #"KAN",
    #"FLQ",
    #"FLQ" ,
    #"PAS",
    #"RBU",
    #"STR",
    #"BEDAQUILINE",
    #"CLOFAZIMINE",
    #"LINEZOLID"]
    for drug in DR_Order:
        all_DR_data_per_DR[drug] = []
    #print out DR in DR order as in DR_order list
    #
    #print largeDelData
    #raw_input()
    #largeDelData is either [-1.-1] or [0, pnca-deletion] or [3,rvnum]
    #one line per file
    #format is:
    #RIF	Capr	PZA	AMI	Cyclos	EMB	ETH	INH	Kana	Moxi	Oflox	PAS	RBU	SM
    '''
    --------------------------------------
    These are the keywords used in kvarq
    Ethambutol
    Fluoroquinolones
    Isoniazid
    Rifampicin
    Streptomycin
    ----------------------------------------------------------
    
    These are the resistances from the DB
            
    PYRAZINAMIDE
    ISONIAZID
    RIFAMPICIN
    PARA-AMINOSALISYLIC_ACID
    CAPREOMYCIN
    ETHIONAMIDE
    BEDAQUILINE
    CLOFAZIMINE
    ETHAMBUTOL
    FLUOROQUINOLONES
    STREPTOMYCIN
    LINEZOLID
    AMIKACIN
    KANAMYCIN
    --------------------------------------------------------
    '''
    os.chdir(outputFolder)
    if MTB:
        f = open("DR_pred_results_new_format.txt",'a')
        f.write(fileX+"\t")
    
    #print "*"*100
    for all_var_hits in snp_and_indel_Data:
        #print "-" * 20
        #Fist the best hist - might be more than one since could be more than one phenotype
        phenoBestHits = {}
        for hit in all_var_hits:
            #print hit
            pheno = hit[1][9]
            if pheno not in phenoBestHits:
                phenoBestHits[pheno] = hit #Store the data for this phenotype, its the only one found
            elif phenoBestHits[pheno][0] > hit[0]:
                phenoBestHits[pheno] = hit #A better raking match was found for thite phenotype, override the previous hit
        #raw_input("will now write the best data to file")
        for pheno in phenoBestHits:
            if phenoBestHits[pheno][0] >= 2:
                #print "skipping this new variant found", phenoBestHits[pheno]
                #raw_input("press enter")
                continue
            #print phenoBestHits
            #print fileX
            #f.write(str(phenoBestHits[pheno][1])+"\t")
            #for x in range(len((phenoBestHits[pheno][1]))):
            #    print x, [phenoBestHits[pheno][1][x]]
            #raw_input()
            toWrite = [phenoBestHits[pheno][1][9],phenoBestHits[pheno][1][2],phenoBestHits[pheno][1][3],"AA_POS:"+phenoBestHits[pheno][1][5],phenoBestHits[pheno][1][7]]
            if phenoBestHits[pheno][1][5] == "" or phenoBestHits[pheno][1][5] == "-" : #if there is no codon info
                toWrite = [phenoBestHits[pheno][1][9],phenoBestHits[pheno][1][2],phenoBestHits[pheno][1][3],"Gene_POS:"+phenoBestHits[pheno][1][4],phenoBestHits[pheno][1][6]] 
            elif phenoBestHits[pheno][1][5] == "INDEL":#its an indel
                #print phenoBestHits[pheno][1]
                toWrite = [phenoBestHits[pheno][1][9],phenoBestHits[pheno][1][2],phenoBestHits[pheno][1][3],"Indel_POS_in_Gene:"+phenoBestHits[pheno][1][4],phenoBestHits[pheno][1][6]] 
                  
            if MTB:
                f.write(str(toWrite)+"\t")
            
            all_DR_data_per_DR[pheno].append(toWrite)
            #f.write(str(phenoBestHits[pheno][1][:-1]+[phenoBestHits[pheno][1][-1].replace("\n","")])+"\t")
            
    for deletion in largeDelData:
        if deletion[0] == 0:
            toWrite = str(deletion[1])
            if MTB:
                f.write(toWrite+"\t") 
            all_DR_data_per_DR[deletion[1][0]].append(toWrite)       
    if MTB:
        f.write("\n")     
        f.close()
    
    f = open("PHENO_RESULTS.txt",'a')
    f.write(fileX)
    drug = False
    for drug in DR_Order:
        f.write("\t")
        for x in all_DR_data_per_DR[drug]:
            #print x[1:]
            f.write(str(x[1:])+",")
        #f.write(str(all_DR_data_per_DR[drug])+"\t")
    if not drug:
        f.write("[]")
    if MTB:
        f.write("\t"+DR_CLASS+"\n")
    else:
        f.write("\n")
    f.close()
    return
    
def processData_short_codes(fileX,outputFolder,DR,DR_ORDER): #Only used for M.tb
    #DR is a tab separated string "RIFAMPACIN/tSTREPTOMYCIN etc
    #largeDelData is either [-1.-1] or [0.pnca-deletion] or [3,rvnum]
    #print "this is DR"
    #print [DR]
    #raw_input("Line 691")
    os.chdir(outputFolder)
    f = open("DR_pred_results_codes.txt",'a')
    f.write(fileX.split("\t")[0]+"\t")
    DR_Classification = "DS"
    foundDR_Flag= False
    for drug in DR_ORDER: 
        #print "processing", drug
        if drug in DR:
            f.write("R\t")
            DR_Classification = "DR"
        else:
            f.write("S\t")  
    #if "RIFAMPICIN" in DR or "ISONIAZID" in DR:
    #    DR_Classification = "DR"
    #    foundDR_Flag = True
    if "RIFAMPICIN" in DR and "ISONIAZID" in DR:
        DR_Classification = "MDR"
        foundDR_Flag = True
    #Changed to remove streptomycin since not used anymore and not part of who definition        
    if "RIFAMPICIN" in DR and "ISONIAZID" in DR and "FLUOROQUINOLONES" in DR and ("CAPREOMYCIN" in DR or "AMIKACIN" in DR or "KANAMYCIN" in DR): # or "STREPTOMYCIN" in DR):   
        DR_Classification = "XDR"
        foundDR_Flag = True
    #if not foundDR_Flag:
    #    f.write("S\t")  
    #Changed to remove streptomycin since not used anymore and not part of who definition
    #if "RIFAMPICIN" in DR and "ISONIAZID" in DR and "FLUOROQUINOLONES" in DR and ("CAPREOMYCIN" in DR or "AMIKACIN" in DR or "KANAMYCIN" in DR) and "ETHAMBUTOL" in DR and "ETHIONAMIDE" in DR and "STREPTOMYCIN" in DR and "PYRAZINAMIDE" in DR:
    if "RIFAMPICIN" in DR and "ISONIAZID" in DR and "FLUOROQUINOLONES" in DR and ("CAPREOMYCIN" in DR or "AMIKACIN" in DR or "KANAMYCIN" in DR) and "ETHAMBUTOL" in DR and "ETHIONAMIDE" in DR and "PYRAZINAMIDE" in DR:
        DR_Classification = "XXDR" 
    
    f.write(DR_Classification+"\n")
    f.close()
    return DR_Classification

def processData_for_pheno(fileX,outputFolder,snp_and_indel_Data,largeDelData):
    #print snp_and_indel_Data
    #raw_input(">>>>>>>>>>>>>>>")
    #largeDelData is either [-1.-1] or [0.pnca-deletion] or [3,rvnum]
    DR = ""
    if largeDelData <> []:
        for x in largeDelData:
            if x[0] == 0:
                if "PYRAZINAMIDE" in x[1] and "PYRAZINAMIDE" not in DR:
                    DR += "PYRAZINAMIDE\t"
                elif "ISONIAZID" in x[1] and "ISONIAZID" not in DR:
                    DR += "ISONIAZID\t"
                break
    for all_var_hits in snp_and_indel_Data:
        #print "-" * 20
        #Fist the best hist - might be more than one since could be more than one phenotype
        phenoBestHits = {}
        for hit in all_var_hits:
            #print hit
            pheno = hit[1][9]
            if pheno not in phenoBestHits:
                phenoBestHits[pheno] = hit #Store the data for this phenotype, its the only one found
            elif phenoBestHits[pheno][0] > hit[0]:
                phenoBestHits[pheno] = hit #A better raking match was found for thite phenotype, override the previous hit
        #raw_input("will now write the best data to file")
        #print "best result was"
        for pheno in phenoBestHits:
            DR+=pheno+"\t"
    return DR
    
def MATCH_PHENO_TO_VARIANTS(variantListName,FILTERED_VARIANTS,FILTERED_DELETIONS,outputFolder,MTB,debugMode, annotationAllowed):
    #############################
    variantPositionDict, allGenesDict, PHENO_ORDER = loadAllKnownVariants(variantListName)
    os.chdir(outputFolder)
    f=open("PHENO_RESULTS.txt",'w')
    f.write("SAMPLE_NAME")
    for x in PHENO_ORDER:
        f.write("\t"+x)
    if MTB:
        f.write("\tDR_CLASS\n")
    else:
        f.write("\n")
    f.close()
    #################    MTB SPECIFIC DR SUMMARY FILE   ################
    if MTB:
        f0 = open("DR_pred_results_new_format.txt",'w')
        f0.close()
        f1 = open("DR_pred_results_codes.txt",'w')
        f1.write("SAMPLE")
        for drug in PHENO_ORDER:
            f1.write("\t"+drug)
        f1.write("\tDR_CLASS\n")
        f1.close()
        
    ####################################################################

    for fileX in os.listdir(FILTERED_VARIANTS): 
        if not fileX.endswith(".vcf"):
            continue
        print "checking pheno matches for file", fileX
        
        snp_and_indel_Data = findPhenoMarkersSNP_indel(fileX,FILTERED_VARIANTS,variantPositionDict,allGenesDict,MTB, annotationAllowed)
        
        #This is a list of [level,DB reference line] , so [1,text text text]
        if annotationAllowed:
            largeDelData = findPhenoMarkersLARGE_DEL(fileX,FILTERED_DELETIONS,variantPositionDict, allGenesDict, MTB)
        else:
            largeDelData = []

        if MTB:
            PHENO = processData_for_pheno(fileX,outputFolder,snp_and_indel_Data,largeDelData)
            DR_CLASS = processData_short_codes(fileX,outputFolder,PHENO,PHENO_ORDER)
        #print "this is snp_and_indel_Data"
        #print snp_and_indel_Data
        processData(fileX,outputFolder,snp_and_indel_Data,largeDelData,PHENO_ORDER,DR_CLASS,MTB)
    return
########################################################################################################################################################################################################################
#END of phenotype matching
########################################################################################################################################################################################################################
def autoAnnotateEMBL(emblDir, annotationFile, outputDir, VCF_Location_List,mapperOrderList, annotationAllowed):
    def hetero_combo_finder(maxN,prev,data,currLevel, epsilon, chain,steps,results,step_results):
        if currLevel >= maxN:
##            print "reached end, result chain is", chain
##            print "steps were", steps
            #assume maxN always = 3
            passFilters = True
            if (chain[0] < 0.95) and (chain[1] < 0.95) and not (abs(chain[0] - chain[1]) <= epsilon):
##                print "Failure at comparison point 1"
                passFilters = False

            if (chain[0] < 0.95) and (chain[2] < 0.95) and not (abs(chain[0] - chain[2]) <= epsilon):
##                print "Failure at comparison point 2"
                passFilters = False

            if (chain[1] < 0.95) and (chain[2] < 0.95) and not (abs(chain[1] - chain[2]) <= epsilon):
##                print "Failure at comparison point 3"
                passFilters = False
            if passFilters and steps not in step_results:
                step_results.append(steps)
                results.append(chain)
            return results,step_results#maxN,prev,data,currLevel,currLevelPos, epsilon, chain
        #foundHit = False
        listPos = -1
##        print "the full data is now:",data
        for currData in data[currLevel]:
            #print currData
            listPos += 1
            if chain == []:
                prev = currData
            else:
##                print "getting the new prev"
##                print chain
                for temp in chain:
                    if temp <> None and temp <> "WT":
                        prev = temp
                        break
##                print "here it is", prev
            chainNew = chain[:]
            stepsNew = steps[:]
            passFilter = False
            
            if (abs(currData - prev) <= epsilon) or (currData >= 0.95) or (prev >= 0.95):
                if currData < 0.04:
                    continue
                if prev < 0.04:
                    continue
##                print "prev and current data is:", prev, currData
                #raw_input("gogo froggy")
                #print (prev > 0.004 and currData > 0.004):
                #chainNew.append(currData)
                chainNew.append(currData)
                stepsNew.append(listPos)
                results,step_results = hetero_combo_finder(maxN,currData,data,currLevel+1, epsilon, chainNew,stepsNew, results,step_results)
                #foundHit = True
            else:
##                print "NOT adding", currData
##                print "prev is ",prev
                continue 
        return results,step_results
    
    def recalculate_AA_changes(fileVariantData_GATK_AND_SAMTOOLS, keyCombos, pos_to_feature_num_dict , featureNum_to_Anno_DataDict):
        #fileVariantData_GATK_AND_SAMTOOLS is a  variant object
        '''
        for each line and for each mapper, change the codon and AA change to be the correct info taking into account the snps before and after its pos
        this does not condence the snps because there could be differencs between the mappers
        '''
        def convertAALetterChange(s):
            #To convert A:I,I,I to A/I
            s = s.replace('"','')
            if ":" not in s:
                return ""
            ref = s[0]
            data = s[2:]
            data = data.split(",")
            mut = data[2]
            if mut == "-":
                mut = data[1]
            if mut == "-":
                mut = data[2]  
            return ref+"/"+mut #may sometimes return A/Syn

        def merge(lastRefCodon,lastMutCodon,currentMutCodon):
            result = ""
            for pos in range(3):
                if lastMutCodon[pos] <> lastRefCodon[pos]:
                    result += lastMutCodon[pos]
                elif currentMutCodon[pos] <> lastRefCodon[pos]:
                    result += currentMutCodon[pos]
                else: 
                    result += lastRefCodon[pos]
            return result
            
        def calculateMutResult(refCodon, mutCodon1,mutCodon2,mutCodon3):
            result = merge(refCodon,mutCodon1,mutCodon2)
            if mutCodon3 <> "":
                result = merge(refCodon,result,mutCodon3)
            refAA = translate(refCodon)
            mutAA = translate(result)
            if refAA <> mutAA:
                new_syn_nonSyn = "nonSyn"
            else:
                new_syn_nonSyn = "Syn"
            return result,refAA+":"+mutAA, new_syn_nonSyn

        def calculateMutResult2(refCodon, mutCodon):
            result = mutCodon 
            refAA = translate(refCodon)
            mutAA = translate(result)
            if refAA <> mutAA:
                new_syn_nonSyn = "nonSyn"
            else:
                new_syn_nonSyn = "Syn"
            return result,refAA+":"+mutAA, new_syn_nonSyn
        

        ##############################################################
        maxPos = len(fileVariantData_GATK_AND_SAMTOOLS)
        #if not params.allow_dececonvolution_of_hetero_variants:
        #    epsilon = 1
        #else:
        #    epsilon = params.hetero_epsilon
        allPositions = []
        for pos in fileVariantData_GATK_AND_SAMTOOLS:
            allPositions.append(pos)
        allPositions.sort()           
        
        #first check if 2 or more positions occur 
        #then check if these are at the same codon
        pos = -1
        #print fileVariantData_GATK_AND_SAMTOOLS
        #raw_input("here is the total data")

        ''' 
        GUIDE IS:
        syn_non_syn1 = mapperData[0]
        aaChange1 = mapperData[1]
        codon1 = mapperData[2]
        refCodon1 = mapperData[3]
        mutCodon1 = mapperData[4]
        genePos1 = mapperData[5]
        and hetero freq is obtained using .retrieveHeteroFreq
        '''
                        
        prevCodon = "@"
##        print "this is allPositions", allPositions
##        print fileVariantData_GATK_AND_SAMTOOLS
        while pos < maxPos-1:
            pos +=1
            knownPos = allPositions[pos]
            prevPos = allPositions[pos-1]
##            print "debug point 1233225", pos, knownPos, prevPos
            if not (knownPos+1 in fileVariantData_GATK_AND_SAMTOOLS or knownPos+2 in fileVariantData_GATK_AND_SAMTOOLS):
                #print "SKIPPING AHEAD, not a case of same codon mutation", knownPos
                continue #must have mutation one or 2 bases ahead, else this does not need merging of data
                
            #For each variant algo calculate the hetero freq
            for varAlgoName_mapperNameCombo in keyCombos:   #extract the mapper data for this position and up to two positions ahead
                variant1_var_List = []
    
                #print varAlgoName_mapperNameCombo
                #print "there are ", len(fileVariantData_GATK_AND_SAMTOOLS[knownPos]),"mutations found"
                for varX in fileVariantData_GATK_AND_SAMTOOLS[knownPos]:
                    if varX.sharedAnno == 'intergenic':
                        #print "skipping intergenic variant reannotation, cannot be at same codon as next bp"
                        continue 
                    if varAlgoName_mapperNameCombo not in varX.varAlgoDict:
                        #print "skiiping due to no mapper data"
                        continue
                    if "INDEL" in varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo): #in mapperData1: #print "skipping indel variant reannotation"
                        #print "skipping due to indel"
                        continue
                    if varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) == "Calculation error":
                        #print "skipping variant reannotation due to heterogeneity calc error"
                        continue 
                    if not varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) or varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) == ['', '', '', '', '', ''] or varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) == "INDEL" or pos+1 > maxPos: # at the 3rd codon pos, next pos cannot be part of this codon
                        #print "skipping variant reannotation due to missing mapper data"
                        continue
                    currentCodon = varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo)[2]
                    #if the difference is == 1 and it is at the same codon then skip, already updated this codon and if not skip then will be looking only at last 2 bp and not all 3.
                    if knownPos - prevPos == 1 and currentCodon == prevCodon:
                        #print "skipping variant that has already been reannotated, same codon"
                        continue #it should not check the same codon again using only the last two positions
                    
                    #getting to this point means that either mutations at all 3, or 1 and 3 or 1 and 2 but not only at 2 and 3.
                    prevCodon = currentCodon
                    variant1_var_List.append(varX)
##                print variant1_var_List
                    
                variant2_var_List = []
                if knownPos+1 in fileVariantData_GATK_AND_SAMTOOLS:
                    for varX in fileVariantData_GATK_AND_SAMTOOLS[knownPos+1]:
                        if varAlgoName_mapperNameCombo not in varX.varAlgoDict:
                            continue
                        if varX.sharedAnno == 'intergenic':
                            continue #since all 3 will then be intergenic
                        #variant2_ref_list.append(varX.varAlgoDict[varAlgoName_mapperNameCombo]["ref"])
                        #mapperData2  = varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo)
                        if "INDEL" in varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo):
                            continue
                        #mapperData2_hetero = varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) 
                        if varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) == "Calculation error":
                            #print "skipping var2 due to hetero freq calc error"
                            continue
                        if not varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) or varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo)  == ['', '', '', '', '', ''] or varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo)  == "INDEL" or pos+1 > maxPos: # at the 3rd codon pos, next pos cannot be part of this codon
                            continue
                        variant2_var_List.append(varX)
##                print "var2 list is now", variant2_var_List

                variant3_var_List = []
                if knownPos+2 in fileVariantData_GATK_AND_SAMTOOLS:
                    for varX in fileVariantData_GATK_AND_SAMTOOLS[knownPos+2]:
                        if varAlgoName_mapperNameCombo not in varX.varAlgoDict:
                            continue
                        if varX.sharedAnno == 'intergenic':
                            continue #since all 3 will then be intergenic
                        #mapperData3  = varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo)
                        if "INDEL" in [varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo)]:
                            continue
                        #mapperData3_hetero = varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) 
                        if varX.retrieveHeteroFreq(varAlgoName_mapperNameCombo) == "Calculation error":
                            continue
                        if not varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) or varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) == ['', '', '', '', '', ''] or varX.retrieveUniqueAnno(varAlgoName_mapperNameCombo) == "INDEL" or pos+2 > maxPos: # at the 3rd codon pos, next pos cannot be part of this codon
                            continue
                        variant3_var_List.append(varX)
##                print variant3_var_List
                ####################################################
                #Now have a list of variants for pos, pos+1 and pos+2 
                    #variant1_var_List here is [var, var ,var, var, var...] for first position
                    #variant2_var_List here is [var, var ,var, var, var...] for second position
                    #variant3_var_List here is [var, var ,var, var, var...] for third position

                if variant1_var_List == [] or (variant2_var_List == [] and variant3_var_List == []):
                    continue
                #positions are correctly spaced, now check if codons match

                codon1 = variant1_var_List[0].retrieveUniqueAnno(varAlgoName_mapperNameCombo)[2]
                if variant2_var_List <> []:
                    codon2 = variant2_var_List[0].retrieveUniqueAnno(varAlgoName_mapperNameCombo)[2]
                else:
                    codon2 = False
                if variant3_var_List <> []:
                    codon3 = variant3_var_List[0].retrieveUniqueAnno(varAlgoName_mapperNameCombo)[2]
                else:
                    codon3 = False
                if codon3 <> codon1:
                    codon3 = False
                    variant3_var_List = []
                if not((codon1 == codon2 or codon1 == codon3) and codon1 <> False):
                    continue #not at the same codon
                else:
                    pass
                #print "codons are now: ", codon1, codon2, codon3

                orientation = "intergenic"
                if knownPos in pos_to_feature_num_dict:
                    key = pos_to_feature_num_dict[knownPos]
                    if key <> []:
                        key=key[0]
##                        print featureNum_to_Anno_DataDict[key]
                        mainAnnoData = featureNum_to_Anno_DataDict[key]
                        orientation = featureNum_to_Anno_DataDict[key][2] 
                    else:
                        orientation = "intergenic"
                    
                #Create 3 lists containing the hetero freq of each option for positions 1 2 and 3 in the codon
                gene_start = int(mainAnnoData[0][0][0])
                gene_end = int(mainAnnoData[0][0][1])
                #genePos = int(knownPos) - int(gene_start)

                if orientation == "+":
                    genePos = int(knownPos) - gene_start + 2
##                    print genePos,":",
                    aaPos = ((genePos-1) / 3) +1
##                    print aaPos
                    AASlotPos1 = (genePos-1) % 3
                    AASlotPos2 = (genePos) % 3
                    AASlotPos3 = (genePos+1) % 3
                
                if orientation == "-":
                    #for neg orientation
                    genePos = gene_end - int(knownPos) + 1
##                    print genePos,":",
                    aaPos = ((genePos-1) / 3) +1
##                    print aaPos
                    AASlotPos1 = (genePos-1) % 3
                    AASlotPos2 = (genePos-2) % 3
                    AASlotPos3 = (genePos-3) % 3
##                print "[] [] [] pos is:", AASlotPos1 , AASlotPos2,  AASlotPos3

                
                variant_heteroFreq_List = [[],[],[]]
                variant_ref_list = [[],[],[]]
                variant_mut_list = [[],[],[]]
                variant_mapperData_list = []

##                if orientation == "-" and variant3_var_List == []: #then fill up from the back,
##                    temp1 = variant1_var_List[:]
##                    temp2 = variant2_var_List[:]
##                    temp3 = variant3_var_List[:]
##
##                    variant1_var_List = temp3[:]
##                    variant2_var_List = temp1[:]
##                    variant3_var_List = temp2[:]
   
                lpos = AASlotPos1
##                print codon1
##                print codon2
##                print codon3
##                
##                print mainAnnoData
##                print "AA slot is ", AASlotPos1, AASlotPos2, AASlotPos3
##                print "pos is", knownPos
                #so here is the problem, adding variants to the wrong position, cannot assume always starting at [X][][]
##                print "var 1 2 3 lists are"
##                print variant1_var_List
##                print variant2_var_List
##                print variant3_var_List
##                print " ok?"
                lpos = -1
                if orientation == "-":
                    for allDetectedVariantsForPos1to3 in [variant1_var_List,variant2_var_List,variant3_var_List]:
                        lpos +=1
                        if allDetectedVariantsForPos1to3 == []:
                            continue
                        codonForThisMut = [AASlotPos1,AASlotPos2,AASlotPos3][lpos]
##                        print allDetectedVariantsForPos1to3
##                        print lpos, codonForThisMut
                        for variant in allDetectedVariantsForPos1to3:
                            variant_heteroFreq_List[codonForThisMut].append(variant.retrieveHeteroFreq(varAlgoName_mapperNameCombo))
                            variant_ref_list[codonForThisMut].append(variant.varAlgoDict[varAlgoName_mapperNameCombo]["ref"])
                            variant_mut_list[codonForThisMut].append(variant.varAlgoDict[varAlgoName_mapperNameCombo]["mut"])
                            variant_mapperData_list.append(variant.retrieveUniqueAnno(varAlgoName_mapperNameCombo))
                        

                else:    #pos orientation
                    for allDetectedVariantsForPos1to3 in [variant1_var_List,variant2_var_List,variant3_var_List]:
                        lpos +=1
                        if allDetectedVariantsForPos1to3 == []:
                            continue
                        codonForThisMut = [AASlotPos1,AASlotPos2,AASlotPos3][lpos]
##                        print allDetectedVariantsForPos1to3
##                        print lpos
                        for variant in allDetectedVariantsForPos1to3:
                            variant_heteroFreq_List[codonForThisMut].append(variant.retrieveHeteroFreq(varAlgoName_mapperNameCombo))
                            variant_ref_list[codonForThisMut].append(variant.varAlgoDict[varAlgoName_mapperNameCombo]["ref"])
                            variant_mut_list[codonForThisMut].append(variant.varAlgoDict[varAlgoName_mapperNameCombo]["mut"])
                            variant_mapperData_list.append(variant.retrieveUniqueAnno(varAlgoName_mapperNameCombo))

                #Subtract the amount from 1 to get the freq of WT, this is stored as 0-th element of each list
                level = -1
                for sublist in variant_heteroFreq_List:
                    level += 1
                    p = 1
                    for element in sublist:
                        p -= element
                    variant_heteroFreq_List[level] = [round(p,4)] + sublist
                
                maxN = 3
                prev = None
                currLevel = 0
                epsilon = params.epsilon
                chain = []
                results = []
                steps = []
                step_results = []
                

                results, step_results = hetero_combo_finder(maxN, prev, variant_heteroFreq_List, currLevel, epsilon, chain, steps, results, step_results)

                levelOptions = [variant_ref_list[0]+variant_mut_list[0]]
                levelOptions.append(variant_ref_list[1]+variant_mut_list[1])
                levelOptions.append(variant_ref_list[2]+variant_mut_list[2])
##                print "the main anno data is now"
##                print mainAnnoData
##                print mainAnnoData[0]
##                print mainAnnoData[0][0]
##
##                
##                print genePos
##                print "input data", variant_heteroFreq_List
##                print "="*40
##                print results
##                print step_results
##
##                print "%"*20
##                print "this appears to be wrong:"
##                print variant_ref_list
##                print variant_mut_list
##                print "is it?"
##                print orientation
##                raw_input("remove this debug point")

                
##                print levelOptions #these are the options for base1, base2 and base3. [] is when no options
                allMutatedCodons = []
                prevRefCodon = ""
                for x in [variant_mapperData_list]: 
                    if x[0][3] <> "":
                        prevRefCodon = x[0][3]
                        break
                    
                if orientation == "-":
##                    print prevRefCodon, "reversing to now be",
                    prevRefCodon = reverse_complement(prevRefCodon)[::-1]
##                    print prevRefCodon
##                print "var mapper list is", variant_mapperData_list
##                print "prev rev codon is now", prevRefCodon
##                print "lvl options are", levelOptions
##                print "step results are", step_results
                for order in step_results:
                    s = []
                    for temp_pos in range(3):
                        if levelOptions[temp_pos] <> []:
                            result = levelOptions[temp_pos][order[temp_pos]]
                            #to do: also get the hetero freq composition and num reads composition and store 
                        else:
                            result = prevRefCodon[temp_pos]
                        s.append(result)
                    if orientation == "-":
##                        print "reversing string"
##                        print s
                        s = reverse_complement(s[::-1])
##                        print s
##                        raw_input("there you have it 562532")
                    allMutatedCodons.append(s)
##                print "all detected mutations are: ", allMutatedCodons
                new_mutCodonList = []
                new_AA_letter_list = []
                new_syn_nonSyn_list = []

##                print "prev ref codon:", prevRefCodon

                for mutCodon in allMutatedCodons:
                    #calculate new ATG -> ATC, new AA letter change, new syn/non syn
                    if orientation == "+" and prevRefCodon == mutCodon[0]+mutCodon[1]+mutCodon[2]:
##                        print "skipping ref to ref false pos change"
                        continue
                    elif orientation == "-" and reverse_complement(prevRefCodon)[::-1] == mutCodon[0]+mutCodon[1]+mutCodon[2]:
##                        print "skipping ref to ref false pos change"
                        continue
##                    print prevRefCodon, mutCodon[0]+mutCodon[1]+mutCodon[2], "becomes", 
                    new_mutCodon, new_AA_letter,new_syn_nonSyn = calculateMutResult2(prevRefCodon, mutCodon[0]+mutCodon[1]+mutCodon[2])
                    new_mutCodonList.append(new_mutCodon)
                    new_AA_letter_list.append(new_AA_letter)
                    new_syn_nonSyn_list.append(new_syn_nonSyn)
##                    print new_AA_letter

##                print allMutatedCodons
##                print "the original ref codon was:", prevRefCodon
##                print new_mutCodonList
##                print new_AA_letter_list
##                print new_syn_nonSyn_list
##                print [variant1_var_List,variant2_var_List,variant3_var_List]
                        
                #all the variants at pos1, 2 and 3 get the same list of possible mut codons.
                for allDetectedVariantsForPos1to3 in [variant1_var_List,variant2_var_List,variant3_var_List]:
                    for variant in allDetectedVariantsForPos1to3:
                        data1 = variant.retrieveUniqueAnno(varAlgoName_mapperNameCombo)
##                        print "updating a variant!!, position is: ", variant.position
##                        print "old variant aa change was ",data1
##                        print "new variant aa chagne is ",new_mutCodonList
##                        raw_input()
                        
                        #update the snp positions of new_annoData to reflect this new data
                        data1[0] = new_syn_nonSyn_list
                        data1[4] = new_mutCodonList
                        data1[1] = new_AA_letter_list
                        for tempPos, e in enumerate(data1):
                            if type(e) == list and len(e) == 1:
                                data1[tempPos] = e[0]
                        variant.varAlgoDict[varAlgoName_mapperNameCombo]["anno"] = data1
##                        print "data1 is:", data1
        return allPositions
        ##############################################################
    ####################################################################
    def load_embl_feature_coordinates(annotationFile,dirX):
        def extractFeatureType(line):
            line = line.replace("FT", "")
            flag1 = False
            flag2 = False
            s = ""
            for char in line:
                if char <> " ":
                    s += char
                    flag1 = True
                if flag1 and char == " ":
                    return s
            return "ERROR"
        #######################################################    
        def extractRanges(line,nums):
            orientation = ""
            flag1 = False
            flag2 = False 
            #print "Processing feature:", [line]
            start = ""
            end = ""
            if not "complement" in line:
                orientation = "+"
            elif "complement" in line:
                orientation = "-"    
            for char in line:
                if char == "." and flag1:
                    flag2 = True
                    continue
                if char in nums and not flag2: 
                    start += char
                    flag1 = True
                elif char in nums and flag2:
                    end += char
                elif flag1 and flag2 and char  ==",":
                    break #Stops the ability to add more than one range 
                elif char not in nums:
                    continue
            #if flag:
            #    print start, end, orientation
            #    raw_input("debug point ____^^^^____")
            return [start,end,orientation]
        ##################################################################
        #store the ranges
        #store the data for these ranges
        embl_ref_seq = ''
        pos_to_feature_num_dict = {} # Tier1 Key: a dict of entire genome linking to a feature range, 1:Gene1, 2:Gene1, ...1300:Gene1, 1331:Gene2
        featureNum_to_Anno_DataDict = {} #Tier2 Key: a dict of feature/gene number to the annotation data GeneNum:[Anno]
        featureNum_to_seq_DataDict = {} #Tier2 Key: a dict of feature/gene number to the SEQUENCE data GeneNum:[Anno]

        #print "loading EMBL file..."
        os.chdir(dirX)
        foundAnnoFile = False
        try:
            f = open(annotationFile)
            foundAnnoFile = True
        except:
            foundAnnoFile = False
        if not foundAnnoFile:
            try:
                print "Loading file:",dirX+annotationFile+".embl"
                f = open(dirX+annotationFile+".embl")
                foundAnnoFile = True
            except:
                foundAnnoFile = False
        if not foundAnnoFile:
            print "No annotation EMBL file could be loaded..."
            raw_input("press enter to continue")
            return {}, {}, {}, {} #return pos_to_feature_num_dict, featureNum_to_Anno_DataDict, featureNum_to_seq_DataDict, known_feature_properties
            
        embl_data = []
        line = f.readline()
        if "ID" not in line:
            print "EMBL file format error, the genome length in BP was never found"
            raw_input()
            return "ERROR"
        elif "ID  " in line:
            gen_len = line.split(" BP")[0]
            gen_len = gen_len.split(";")[-1]
            gen_len = gen_len.replace(" ","")
            try:
                gen_len = int(gen_len)
            except:
                print "EMBL file format, the ID line should contain a ID header for example:"
                print "ID   AL123456; SV 3; ; DNA; ; UNC; 4411532 BP."
                print "However, this line was not present or the format is incorrect"
                raw_input()
                return "ERROR"
                
        for x in range(gen_len): #Initialize entire genome to contain no anno data
            pos_to_feature_num_dict[x] = []
                       
        orientation = "+"
        line = "START"
        nums = ["1","2","3","4","5","6","7","8","9","0"] 
        feature_types = []
        known_feature_properties = []
        featureNumber = 1
        while line and "SQ  " not in line: # and "SQ\t" not in line:   
            #if "FT" not in line and ".." not in line:
            #    line = f.readline() #a[pos]
                
            #print "HERE IS CURRENT LINE EVALUATED", [line]
            if "FT" in line and "source" in line:
                line = f.readline() #a[pos]
                continue
            if "FT" not in line or ".." not in line:
                #print "skipping line", line
                #print "-"*50
                line = f.readline()
                continue
            #else:
                #print "Evaluating this line:", [line]
            featureNumber += 1
            feature_type = extractFeatureType(line) 
            #print "detected as", feature_type
            if feature_type not in feature_types:
                feature_types.append(feature_type)
            runOnceFlag = False
            ranges = []
            multiJoin = 0
            alreadyHaveRange = False
            while line and ("," in line or runOnceFlag == False) and ("FT" in line and ".." in line):
                runOnceFlag = True 
                multiJoin += 1
                if not alreadyHaveRange: #stops the ability to have more than one range per feature, such as for pseudogenes
                    start,end,orientation = extractRanges(line,nums) 
                    ranges.append([start,end])
                alreadyHaveRange = True
                line = f.readline()
                #print "moving on to this line1", [line]
                continue
            if multiJoin > 1 and  ("FT" in line and ".." in line):
                start,end,orientation = extractRanges(line,nums)
                ranges.append([start,end])
                line = f.readline()
                #print "now moving on to this next line2", [line]
                continue
            #else:
            #    print "not multijoin situation for line", line
                
            temp_features = []
            #print "current line is", line
            #print "/" in line
            #print "=" in line
            #while (line) and ("/" in line) and ('="' in line): # add additional features
            while (line) and ("/" in line) and ('=' in line) and ("%)" not in line) and ("Identities" not in line): # add additional features
                #meta_data = True
                temp_feature_type = line.split("/")[1].split("=")[0]
                '''
                if temp_feature_type not in known_feature_properties:
                    print "TO ADD:", line
                    print "temp line", [line]
                    print "new feature type found:"
                    print temp_feature_type
                    raw_input()
                '''
                
                if temp_feature_type not in known_feature_properties:
                    known_feature_properties.append(temp_feature_type)
                temp_feature_detail = line.split("=")[1].replace("\n"," ")
                
                line = f.readline()
                if line and "/" in line and "=" in line:
                    temp_features.append([temp_feature_type,temp_feature_detail])
                    continue
                while "FT                   " in line : #add addional data for a long line
                    temp_feature_detail += line.replace( "FT                   ","")
                    temp_feature_detail = temp_feature_detail.replace("\n","")
                    line = f.readline()
                    if line and "/" in line and "=" in line:
                        temp_features.append([temp_feature_type,temp_feature_detail])
                        break
                    continue
                continue
            temp_features.append([temp_feature_type,temp_feature_detail])
            #if ['895821', '898084'] in ranges:
            #print "this is the info for a single entry"
            #print feature_type
            #print ranges
            #print orientation
            #print temp_features
            #raw_input("exact or not?")

            for rangeX in ranges: #store the gene feature number in lookup key dict for rapid access
                for position in range(int(rangeX[0]),int(rangeX[1])):
                    if position+1 in pos_to_feature_num_dict: #already have data for this genomic position
                        #print featureNumber, pos_to_feature_num_dict[position+1]
                        if featureNumber not in  pos_to_feature_num_dict[position+1]:
                            pos_to_feature_num_dict[position+1].append(featureNumber) #A genomic location can code for more than one gene
                    else:
                        pos_to_feature_num_dict[position+1] = [featureNumber] #store the anno+seq lookup key for this genoimic position
                    #also need to know what each key is for, store the anno and seq data for this loopkup key:
                    if featureNumber not in featureNum_to_Anno_DataDict:
                        featureNum_to_Anno_DataDict[featureNumber] = [ranges,feature_type,orientation,temp_features]
                        #remember to also append the sequence to this list now also 
                    
            #embl_data.append([ranges,feature_type,orientation,temp_features])
            #print embl_data
            #raw_input()
   
        ################## LOAD REF INTO MEM ###############################
        #print "before search for SQ"
        #print [line]
        #raw_input()
        if "SQ  " in line:
            line = f.readline()
            while line:
                for char in line:
                    if char.lower() not in ["a","t","g","c","u"]:
                        continue
                    embl_ref_seq += char
                line = f.readline()
            
        #Store the seq of each featureKeyNumber so {1:ATGTCA}
        counterX = 0
        for featureElement in featureNum_to_Anno_DataDict:
            counterX +=1
            #print counterX
            try:
                ranges = featureNum_to_Anno_DataDict[featureElement][0]
                orientation = featureNum_to_Anno_DataDict[featureElement][2]
            except:
                print "ERROR X6375!"
                print featureElement
                print featureNum_to_Anno_DataDict[featureElement]
                raw_input()
            
            
            seq = retrieve_embl_seq(ranges, embl_ref_seq, orientation) #fetch this seq and store it in mem
            #raw_input("currently fixing this part, for bovis fetching the seq is not working")
            if seq == "":
                print "error loaing embl sequence file"
                print "ranges are", [ranges]
                
                #print "embl ref seq is",[embl_ref_seq]
                #print "orientation is ",[orientation]
                raw_input("ERROR, SEQ LEN 0 RETURNED FOR THIS ENTRY")
##            print [seq]
##            print "was for", featureNum_to_Anno_DataDict[featureElement]
##            raw_input("does seq match?")
            featureNum_to_seq_DataDict[featureElement] = seq
            
        print len(featureNum_to_seq_DataDict), "reference genomic features loaded"
        #embl_data = sorted(embl_data, key = lambda x: int(x[0][0][0]))
        f.close()
        #print known_feature_properties
        known_feature_properties.sort()
        return pos_to_feature_num_dict, featureNum_to_Anno_DataDict, featureNum_to_seq_DataDict, known_feature_properties

    ###################################################################
    def obtain_file_list(VCF_Location_List):
        #Returns dictionary of all VCF files (allows missing data)
        unique = {}
        for VCF_Dir in VCF_Location_List:
            os.chdir(VCF_Dir)
            for fileX in os.listdir(VCF_Dir):
                if not fileX.endswith(".vcf"):
                    continue
                if fileX.split("_")[0] not in unique:
                    unique[fileX.split("_")[0]] = [fileX]
                else:
                    unique[fileX.split("_")[0]].append(fileX)
        return unique #R100_GATK, R100_SAMTOOLS, R212_GATK, R212_SAMTOOLS --> Allows just gatk or just samtools or both
    ###################################################
    def getMapperOverlap(mapperDataDictList_GATK_AND_SAMTOOLS):
        #HERE mapperDataDictList_GATK_AND_SAMTOOLS is a list of two elements one for each variant detection algo
        # These two lists look the same, each is:
        #[ {pos: data, pos: data} , {pos: data, pos: data}, {pos: data, pos: data} ]
        #Which is the data for each mapper bwa novo and smalt
        #
        #Thus we have           BWA-GATK,       NOVO-GATK,      SMALT-GATK      in one list
        # And the other list is BWA-SAMTOOLS,   NOVO-SAMTOOLS,  SMALT-SAMTOOLS
        
        allSNPPositions = {}
        overlapData = []
        mapperAmount1 = 0
        mapperAmount2 = 0
        mapperDataDictList_GATK = mapperDataDictList_GATK_AND_SAMTOOLS[0]
        mapperDataDictList_SAMTOOLS = mapperDataDictList_GATK_AND_SAMTOOLS[1]
        #Each is of len 3: b,n,s
        
        for dataDict in mapperDataDictList_GATK: #for position dict in bwa,novo,smalt
            mapperAmount1 += 1
            for pos in dataDict: #For each pos in this dict 
                if pos not in allSNPPositions:
                    allSNPPositions[pos] = True

        for dataDict in mapperDataDictList_SAMTOOLS: #for position dict in bwa,novo,smalt
            mapperAmount2 += 1
            for pos in dataDict: #For each pos in this dict 
                if pos not in allSNPPositions:
                    allSNPPositions[pos] = True
        mapperAmount = max(mapperAmount1,mapperAmount2)
                    
        for pos in allSNPPositions: #for each known variant position in the pooled variants from gatk and samtools
            if pos == "":
                continue
            pos = str(pos)
            mapperCount_GATK = 0
            mapperCount_SAMTOOLS = 0
            mutations_GATK = ""
            mutations_SAMTOOLS = ""
            alreadyHaveBodyData = False
            snpLineData = []
            bodyData = None
##            print "the pos is ", pos
##            for x in mapperDataDictList_GATK:
##                if pos in x:
##                    raw_input("found in gatk")
##            for x in mapperDataDictList_SAMTOOLS:
##                if pos in x:
##                    raw_input("found in SAMTOOLS")
            for mapperDataDict in mapperDataDictList_GATK: #Check if this snp present in any of the mappers for GATK variants
                if pos in mapperDataDict:
                    if not alreadyHaveBodyData:
                        bodyData = mapperDataDict[pos]# .replace("\n","\t")
                        alreadyHaveBodyData = True
                    temp = mapperDataDict[pos].split("\t")
                    snpLineData.append([temp[3],temp[4],temp[5],temp[9].replace("\n","\t"),"GATK"])
                    mutations_GATK += temp[4]+"/" # the alt data from the 4th coloumb
                    mapperCount_GATK +=1
                else:
                    snpLineData.append(["\t","\t","\t","\t","t"])
                    mutations_GATK    += "*/"

##            print "this is after gatk, the data is now: ", snpLineData
            for mapperDataDict in mapperDataDictList_SAMTOOLS: #Check if this snp present in any of the mappers for SAMTOOLS variants
                if pos in mapperDataDict:
                    if not alreadyHaveBodyData:
                        bodyData = mapperDataDict[pos]# .replace("\n","\t")
                        alreadyHaveBodyData = True
                    temp = mapperDataDict[pos].split("\t")
                    snpLineData.append([temp[3],temp[4],temp[5],temp[9].replace("\n","\t"),"SAMTOOLS"])
                    mutations_SAMTOOLS += temp[4]+"/" # the alt data from the 4th coloumb
                    mapperCount_SAMTOOLS +=1
                else:
                    snpLineData.append(["\t","\t","\t","\t","t"])
                    mutations_SAMTOOLS    += "*/"
            temp = bodyData.split("\t")
            posX = temp[1]
            chrom = temp[0]

            #Mapper1: col 3(ref),4(alt),5(qual),7(info1),9(info2)
            #Mapper2: col 3(ref),4(alt),5(qual),7(info1),9(info2)
            #Mapper3: col 3(ref),4(alt),5(qual),7(info1),9(info2)
            
            overlapData.append([int(posX),chrom, snpLineData, [str(mapperCount_GATK),str(mapperCount_SAMTOOLS)], mutations_GATK[:-1],mutations_SAMTOOLS[:-1]]) #mutations[:-1]+"\tMSum="+str(mapperCount)])
##            print overlapData
##            raw_input("This is the current overlap data")

        overlapData.sort()
##        for x in overlapData:
##            print x
##            raw_input("TESTING 6667")
        
        return overlapData, mapperAmount
    
    #######################################################################
    def reverse_complement(seq):
        seq = seq[::-1]
        temp = ""
        ura = False
        for char in seq:
            char = char.upper()
            if char == "A":
                temp+=("T")
            elif char == "T":
                temp+=("A")
            elif char == "C":
                temp+=("G")
            elif char == "G":
                temp+=("C")
            elif char == "U":
                ura = True
                temp += "A"
            else:
                print "Error base error",[char],"found in",
                print [seq]
                temp+=("?")
    ##            raw_input()
        if ura:
            seq = seq.replace("U","T")
        return temp
        
    def translate(seq):
        seq = seq.upper()
        gencode = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
        }
     
        #print seq
        protSeq = ''
        for x in range(0,len(seq),3):
            if gencode.has_key(seq[x:x+3]) == True:
                protSeq += gencode[seq[x:x+3]]
            else:
           #     print "Warning, sequence is not a multiple of 3...truncating sequence..."
                return protSeq
        return protSeq
                   
    def getSynorNonSynonMutation(orientation,snpPosition,ref,mutList2,annotationStartSite,annotationEndSite,seq,annoData,varX):
        if "," not in mutList2 and len(mutList2) > 1:
            changeType ="INDEL"
            aminoAcidChange = "INDEL"
            changedAminoAcidPosition = "INDEL"
            codonsRef = ref #"INDEL
            codonsMut = mutList2 #"INDEL" 
            if orientation == "+":
                codonPosition = snpPosition - annotationStartSite
            elif orientation == "-":
                codonPosition = annotationEndSite - snpPosition
            #codonPosition = "INDEL" no store the position in gene
            return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef,codonsMut,str(int(codonPosition)+1)]
        elif "," in mutList2: #should no longer be an issue, now changed loading of vcf data to split into seperate lines
            temp = mutList2.split(",")
            if len(temp[0]) >1 or len(temp[1]) >1:
                changeType ="INDEL"
                aminoAcidChange = "INDEL"
                changedAminoAcidPosition = "INDEL"
                codonsRef = ref #"INDEL
                codonsMut = mutList2 #"INDEL" 
                if orientation == "+":
                    codonPosition = snpPosition - annotationStartSite
                elif orientation == "-":
                    codonPosition = annotationEndSite - snpPosition
                #codonPosition = "INDEL" 
                return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef,codonsMut,str(int(codonPosition)+1)]
                #codonsRef = "INDEL"
                #codonsMut = "INDEL"
                #codonPosition = "INDEL"
                #return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef,codonsMut,codonPosition]
            else:
                changeType ="ERROR_Multiple_Bases"
                aminoAcidChange = "ERROR_Multiple_Bases"
                changedAminoAcidPosition = "ERROR_Multiple_Bases"
                codonsRef = "ERROR_Multiple_Bases"
                codonsMut = "ERROR_Multiple_Bases"
                codonPosition = "ERROR_Multiple_Bases"
                return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef,codonsMut,codonPosition]
           
        mutList2 = mutList2.replace(",","")
        mutList2 = mutList2.replace('"',"")
        codonsMut = ""
        codonsRef = ""
        codonPosition = snpPosition - annotationStartSite #This means we start from 0, so pos 0 is the fist codon
        changedAminoAcidPosition = (codonPosition/3)+1
        #Thus we have:
        #012 345 678 --> BP Pos
        #111 222 333 --> AA Pos
        changeType = "EMPTY" # indicates no data was added and there was error
        coding_dna = seq
        
        if len(ref) > 1:
            changeType ="INDEL"
            aminoAcidChange = "INDEL"
            changedAminoAcidPosition = "INDEL"
            codonsRef = "INDEL"
            codonsMut = "INDEL"
            #codonPosition = "INDEL"
            if orientation == "+":
                codonPosition = snpPosition - annotationStartSite
            elif orientation == "-":
                codonPosition = annotationEndSite - snpPosition
            return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef,codonsMut,codonPosition]
        try:
            if coding_dna[codonPosition].lower() <> ref.lower():
                raw_input("fixing problem here that it uses the variant info from a previous line")
                print "genomic position is ",snpPosition
                print "the codon position is supposedly", codonPosition
                print coding_dna
                print "ERROR, ref does not match the calculated embl NT, fasta and embl mismatch?"
                print coding_dna[codonPosition]
                print "REF",[ref.lower()], orientation
                print "variant position is", snpPosition
                print "mutations are", mutList2
                print annoData
                print varX.position
                print "this is the posistion!"
                for key in varX.varAlgoDict:
                    print key
                    print varX.varAlgoDict[key]
                raw_input("press enter")
        except:
            print codonPosition, len(coding_dna)
            print orientation,snpPosition,ref,mutList2,annotationStartSite,annotationEndSite,annoData
            print "Error, index out of range, debug point 2083"
            print "This error is probably due EMBL file with wrong format - multiple start and end positions are not permitted."
            raw_input()
            
        temp_coding_dna = coding_dna    
        if orientation == "-":
            changedAminoAcidPosition = ((len(coding_dna)-1 - codonPosition) /3) +1
            #Then the coding DNA loaded above is in protein coding orientation, and thus must be rev comp to get the ref FASTA seq so lets do that now
            temp_coding_dna = reverse_complement(coding_dna)
            #Now the DNA seq matches the reference FASTA seq and we can add the mutated DNA at the correct position 
            #Keep in mind we must rev compl the DNA back to coding orientation before we can translate to protein to get the changed AA and AA position
                    
        protein = translate(temp_coding_dna)
        mutCount = 0
        for mut in mutList2: #one snp at a time... G/G/G
            if mut == "/":
                continue
            if mut.upper() not in ["A","T","G","C","*",] or len(mut) > 1:
                print "error, mutation is not in [A,T,G,C]"
                print "mut is, ",mut
                print "mutlistis ", mutList2
                raw_input()
            mutCount +=1
            if mut == "*":
                if changeType == "EMPTY":
                    changeType = "-"
                    aminoAcidChange = "-"
                    continue
                else:
                    changeType += ",-"
                    aminoAcidChange += ",-"
                    continue
            if coding_dna[codonPosition].lower() == mut.lower(): 
    ##                    print "FASTA_AND_EMBL_MISMATCH"
                if changeType == "EMPTY":    
                    changeType = 'FASTA_AND_EMBL_MISMATCH'
                    aminoAcidChange = "None"
                else:
                    if "FASTA_AND_EMBL_MISMATCH" in changeType:
                        changeType += ",FASTA_AND_EMBL_MISMATCH"
                    else:
                        changeType += ",None"
                        aminoAcidChange += ",None"
                continue
            mutatedCoding_dna = str(coding_dna) #make a copy so that we can introduce a mutation 
            #Keep in mind the dna is linear from left to right and codonPosition just shows which pos in string is mutated, regardless of orientation
            #Here we introdude the mutation into the dna
            if codonPosition == 0:
                mutatedCoding_dna = mut.lower()+mutatedCoding_dna[1:]
            else:        
                mutatedCoding_dnaA = mutatedCoding_dna[:codonPosition]
                mutatedCoding_dnaB = mutatedCoding_dna[codonPosition+1:]                
                mutatedCoding_dna = mutatedCoding_dnaA+mut.lower()+mutatedCoding_dnaB
            if orientation == "-":
                mutatedCoding_dna = str(reverse_complement(mutatedCoding_dna)) # need to reverse it back to protien coding orientation before translating to protein
            codonsMut = ""
            codonsRef = ""

            #Here we store the 3 bases for the affected aa codon, both original and mutated codons. so idea is to keep all shifts like: ATG-->AGG
            # SPECIAL NOTE!!! THE CODONS STORE ARE IN READING FRAME ORIENTATION!! SO watch out, change from GCC in  ref gene which is negative orientation
            # will and should show as GGC in mutatedcodon 
            ###########################################################################################################################
            if orientation == "+":
                state = codonPosition % 3
                if state == 0: #mutation is at first codon out of 3 possibles [X][][]
                    codonsMut = mutatedCoding_dna[codonPosition]
                    codonsRef = str(coding_dna)[codonPosition]
                    if codonPosition+1 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?" 
                    else:
                        codonsMut += mutatedCoding_dna[codonPosition+1]
                        codonsRef += str(coding_dna)[codonPosition+1]
                    if codonPosition+2 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?" 
                    else:
                        codonsMut += mutatedCoding_dna[codonPosition+2]
                        codonsRef += str(coding_dna)[codonPosition+2]
                        
                elif state == 1: #mutation is at second codon out of 3 possibles [][X][]
                    codonsMut = mutatedCoding_dna[codonPosition-1] #add one upstream of current
                    codonsRef = str(coding_dna)[codonPosition-1] # add one upstream of current
                    codonsMut += mutatedCoding_dna[codonPosition] #add current pos
                    codonsRef += str(coding_dna)[codonPosition] # add current pos
                    if codonPosition+1 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?"
                    else:
                        codonsMut += mutatedCoding_dna[codonPosition+1] #add one upstream
                        codonsRef += str(coding_dna)[codonPosition+1] #add one upstream
                        
                elif state == 2: #mutation is at third codon out of 3 possibles [][][X]
                    codonsMut = mutatedCoding_dna[codonPosition-2]+mutatedCoding_dna[codonPosition-1]+mutatedCoding_dna[codonPosition]
                    codonsRef = str(coding_dna)[codonPosition-2]+str(coding_dna)[codonPosition-1]+str(coding_dna)[codonPosition]
                ######################################################################################################################3    
##                print "This was calculated::"
##                print codonsMut
##                print codonsRef
##                raw_input("6665")
            elif orientation == "-":
                mutatedBP = len(mutatedCoding_dna)-1 - codonPosition # snpPosition-annotationSEndSite
                state = mutatedBP % 3

                if state == 0: #mutation is at first codon out of 3 possibles [X][][]
                    codonsMut = mutatedCoding_dna[mutatedBP]
                    codonsRef = str(reverse_complement(coding_dna))[mutatedBP]
                    if mutatedBP+1 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?" 
                    else:
                        codonsMut += mutatedCoding_dna[mutatedBP+1]     
                        codonsRef += str(reverse_complement(coding_dna))[mutatedBP+1]       
                    if mutatedBP+2 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?" 
                    else:
                        try:
                            codonsMut += mutatedCoding_dna[mutatedBP+2]
                            codonsRef += str(reverse_complement(coding_dna))[mutatedBP+2]
                        except:
                            print "Error indexing"
                            print "mutated BP =",mutatedBP
                            print mutatedBP+1
                            print mutatedBP+2
                            print "len is",[len(mutatedCoding_dna)]
                            print "len is",[len(reverse_complement(coding_dna))]
                            raw_input("here is error:")
                            print mutatedCoding_dna[mutatedBP]
                            print mutatedCoding_dna[mutatedBP+1]
                            print mutatedCoding_dna[mutatedBP+2]
                            raw_input()
    ##                raw_input("state 0 results above")
                            
                elif state == 1: #mutation is at second codon out of 3 possibles [][X][]
                    codonsMut = mutatedCoding_dna[mutatedBP-1] #add one upstream of current
                    codonsRef = str(reverse_complement(coding_dna))[mutatedBP-1] # add one upstream of current
                    codonsMut += mutatedCoding_dna[mutatedBP] #add current pos
                    codonsRef += str(reverse_complement(coding_dna))[mutatedBP] # add current pos
                    if mutatedBP+1 >= len(mutatedCoding_dna):
                        codonsMut += "?"
                        codonsRef += "?"
                    else:
                        codonsMut += mutatedCoding_dna[mutatedBP+1] #add one upstream
                        codonsRef += str(reverse_complement(coding_dna))[mutatedBP+1] #add one upstream
                        
                elif state == 2: #mutation is at third codon out of 3 possibles [][][X]
                    codonsMut = mutatedCoding_dna[mutatedBP-2]+mutatedCoding_dna[mutatedBP-1]+mutatedCoding_dna[mutatedBP]
                    codonsRef = str(reverse_complement(coding_dna))[mutatedBP-2]+str(reverse_complement(coding_dna))[mutatedBP-1]+str(reverse_complement(coding_dna))[mutatedBP]
            try:
                mutatedProtein = translate(mutatedCoding_dna)
##                print "-" * 15
##                print mutatedCoding_dna
##                print "." * 15
##                print "THIS IS THE PROTEIN"
##                print mutatedProtein
##                raw_input("6666")
            except:
                 print "error during annotation "
                 print "mut is ", mut
                 print "this is mutList", mutList2
                 print snpPosition
                 print str(mutatedCoding_dna)
                 raw_input()
                
            pos = 0
            protein = str(protein)
            mutatedProtein = str(mutatedProtein)
            
            if len(protein) <> len(mutatedProtein):
                print "protein len mismatches"
                #print rvNumber
                print len(protein),len(mutatedProtein)
                print protein
                print "and"
                print mutatedProtein
                raw_input()
            
            if str(protein) == str(mutatedProtein):
    ##            print "protein and mutated protein are:"
    ##            print [protein]
    ##            print [mutatedProtein]
    ##            raw_input()
                if changeType == "EMPTY":
                    changeType = "syn"
                    aminoAcidChange = "None"                  
                else:
                    changeType += ",syn"
                    aminoAcidChange += ",None"
            else: #there is a AA change
    ##            print "non Syn mutation"
                while protein[pos] == mutatedProtein[pos] and pos < len(protein)-1:
                    pos += 1
                    #print protein[pos], mutatedProtein[pos],  protein[pos] == mutatedProtein[pos], pos
                if protein[pos] <> mutatedProtein[pos]:
                    mutatedAACodon = pos+1 #plus one because we started counting from 0
                else:
                    print "could not find any protein differences? error, fix"
                    raw_input()

                #Failsafe to make sure the actual changed AA matches the calculated AA change position
                if mutatedAACodon <> changedAminoAcidPosition:
                    print "error, aa codon problem" #errorReport()
                    print protein
                    print "and"
                    print mutatedProtein

                    print  "Codons are",mutatedAACodon, changedAminoAcidPosition
                    print "and mut seq is"
                    print mutatedCoding_dna
                    print "anno is", annoData
                    print orientation
                    print snpPosition
                    print ref
                    print mutList2
                    print annotationStartSite,annotationEndSite
##                    print seq
                    print annoData
                    raw_input()

                if changeType == "EMPTY": #Then its the first entry in the mutated AA list and syn/nonSyn list
                    changeType = "nonSyn"
                    aminoAcidChange = protein[pos]+":"+mutatedProtein[pos]
                    
                else: #its not the frist entry and we need a comma to separate them
                    changeType += ",nonSyn"                        
                    aminoAcidChange += ","+mutatedProtein[pos]
                
##                print changeType,aminoAcidChange,changedAminoAcidPosition, orientation
##                print codonsRef.upper(),codonsMut.upper(),codonPosition
##                raw_input("debug point 9978")
##        return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef.upper(),codonsMut.upper(),codonPosition]
            if orientation == "-":
                codonPosition = annotationEndSite - snpPosition
        return [changeType,aminoAcidChange,changedAminoAcidPosition,codonsRef.upper(),codonsMut.upper(),str(int(codonPosition)+1)]


    #def retrieveEMBLData(pos,embl_data):
    #    #this returns all the ranges for this feature, not just the hit one
    #    posX = int(pos)
    #    maxPos = len(embl_data)-1
    #    minPos = 0
    #    debugLimit = 100
    #    debugCount = 0
    #    while True:
    #        debugCount += 1
    #        hit = False
    #        current = minPos + (maxPos-minPos)/2  
    #        annoData = embl_data[current]
    #        posRanges = annoData[0]
    #        if debugCount >= debugLimit:
    #            print "stuck!"
    #            print annoData
    #            print "---------------current, min max pos---------------"
    #            print "looking for:", posX
    #            print "currentPos:", current,"->", posRanges
    #            print "MIN:",minPos,"->",embl_data[minPos][0]
    #            print "MAX:",maxPos,"->",embl_data[maxPos][0]
    #            raw_input()
    #            
    #        for rangeX in posRanges:
    #            start = int(rangeX[0])
    #            end = int(rangeX[1])
    #            if posX >= start and posX <= end:
    #                hit = True
    #                break
    #        if hit:
    #            return annoData, posRanges
    #        
    #        elif minPos == maxPos or maxPos-minPos <= 7:
    #            for tempPos in range(minPos,maxPos+1):
    #                try:
    #                    posRanges = annoData[0]
    #                    for rangeX in posRanges:
    #                        start = int(rangeX[0])
    #                        end = int(rangeX[1])
    #                        if posX >= start and posX <= end:
    #                            hit = True
    #                            return annoData, posRanges                        
    #                except:
    #                    print "should not happen"
    #                    raw_input("ERROR!")
    #            if not hit:
    #                #raw_input("THERE IS NO HIT!!!")
    #                return "ncDNA", [posX]
    #        ###########################
    #        elif posX > end:
    #            #print "posx, end:"
    #            #print posX, end
    #            #print "value is to the right, raising lower limit", current
    #            minPos = current
    #            #raw_input("stuck in infinate loop!")           
    #                            
    #            continue
    #        elif posX < start:
    #            #print "posX, start:"
    #            #print "Value is to the left, dropping upper limit", current
    #            maxPos = current
    #            #raw_input("stuck in infinate loop!")    
    #            continue
    #    return
        #########################################################
    def retrieve_embl_seq(found_ranges, embl_ref_seq, orientation):
        def countBP(s):
            count = 0
            for x in s:
                if x.lower() in ["a","t","g","c","u"]:
                    count+=1
            return count
        def rem_non_bp(line):
            s = ""
            for x in line:
                if x not in ["a","t","g","c","u"]:
                    continue
                else:
                    s += x
            return s
        ########################  
        seq = ""
        for found_range in found_ranges:
            start = int(found_range[0])-1
            if start <= 0:
                start = 1
            #Changes on 5 december 2015 to -1
            end = int(found_range[1])
            #print start,end, found_range
            #print embl_ref_seq[start-1:end]
            #raw_input("debug777444")
            seq += embl_ref_seq[start-1:end]
        return seq 
                    
    def getAnnoData(fileX, variantDataGATK_SAMTOOLS, known_feature_properties, pos_to_feature_num_dict, featureNum_to_Anno_DataDict, featureNum_to_seq_DataDict, annotationAllowed,gatkFlag,samtoolsFlag, mapperOrderList):
        #here overlapData is a list of variant objects, not in sorted order
        keyCombos = []
        for mapper in mapperOrderList: #here to access each mapper data,  need to access with varAlgoName+mapperName
            for varAlgoName in ["GATK","SAMTOOLS"]:
                keyCombos.append(mapper+"_"+varAlgoName) #keyCombo  
        total = len(variantDataGATK_SAMTOOLS)
        oldProgress = 0
        count = 0.0
        for pos in variantDataGATK_SAMTOOLS: #here overlapData i thnk overlap data is a dict here of {pos: variant}
            count+=1
            progress =  (100*count) / total
            if progress % 10 == 0:
                if oldProgress <> progress:
                    print str(int(progress))+"% of annotation completed for:",fileX
                    oldProgress = progress
            if annotationAllowed:
                #print pos, int(pos) in pos_to_feature_num_dict, len(pos_to_feature_num_dict)
                key = pos_to_feature_num_dict[pos]           
                #print pos, key
                #print featureNum_to_Anno_DataDict[key] 
            else:
                key = []
            if key == []:
                if annotationAllowed:
                    for varX in variantDataGATK_SAMTOOLS[pos]:
                        varX.addSharedAnno("intergenic")  
                    #variantDataGATK_SAMTOOLS[pos].addSharedAnno("intergenic")
                else:
                    for varX in variantDataGATK_SAMTOOLS[pos]:
                        varX.addSharedAnno("-")  
                    #variantDataGATK_SAMTOOLS[pos].addSharedAnno("-")
                continue
            else: #there is annotation data to add 
                #print key, key[0]
                key=key[0] #Need to modify this if there can be more than one annotation for a single pos, like multi genes from same DNA, ie dont use [0],. iterate over all the items in key[0]
            #print featureNum_to_Anno_DataDict[key]
            #print pos, key
            #raw_input()
            annoData = featureNum_to_Anno_DataDict[key] 
            ranges = []
            for x in annoData[0]:
                for y in x:
                    ranges.append(int(y))
            ranges.sort()
            orientation = annoData[2]
            if orientation not in ["+","-"]:
                print [orientation]
                raw_input("annotation data format error, orientation is not a +/-")         
            seq = featureNum_to_seq_DataDict[key]
            #Next calculate the SNP effect: NTPos, NTChange, AAPos and AA change, Syn/NonSyn
            mutationData = []
##            prevRef = ""
##            prevMut = ""
            #For each mapper data for this position in the genome find the aa change etc
            for key in keyCombos:
                if key not in params.usedKeyCombos:
                    params.usedKeyCombos.append(key)
            for key in params.usedKeyCombos:
                for varX in variantDataGATK_SAMTOOLS[pos]:
                    #print pos, varX.varAlgoDict, key, key in varX.varAlgoDict
                    if key in varX.varAlgoDict: #if the current variant object has this mapper and var algo combination, add anno data to it
                        ref = varX.varAlgoDict[key]["ref"]
                        mut = varX.varAlgoDict[key]["mut"] 
                        annotationStartSite = ranges[0]-1 #lowest value 
                        annotationEndSite = ranges[-1] #highest value 
##                         if ref == prevRef and mut == prevMut: # no need to recalculate, copy prev results
                        #mutationDataOld = mutationData #Because its the same pos in genome and exact same mutation as prev calculation
                        #varX.addUniqueAnno(key,mutationDataOld)
                        #prevRef = ref
                        #prevMut = mut
                        #else: # calc new anno data based on ref and mut
                        if int(varX.position) <> int(pos):
                            print "FATAL ERROR!"
                            print [pos]
                            print [varX.position]
                            raw_input("This should never happen")
                        mutationData = getSynorNonSynonMutation(orientation,pos,ref,mut,annotationStartSite,annotationEndSite,seq,annoData,varX)
                        varX.addUniqueAnno(key,mutationData)
                        #prevRef = ref
                        #prevMut = mut
                #else:
                #    no dont add any data here, its does not have this key, sohuld catch this in write data to add the extra spaces and tabs.
                #    variantDataGATK_SAMTOOLS[pos].addUniqueAnno(key,["","","","","",""])
        return keyCombos
        ################################################################################################  

    def writeData(outputDir,fileX,fileVariantData_GATK_AND_SAMTOOLS,known_feature_properties,mapperOrderList, annotationAllowed,gatkFlag,samtoolsFlag, allPositions, keyCombos, featureNum_to_Anno_DataDict, pos_to_feature_num_dict):
        '''
        overlapData:
        [4013, 'gi|444893469|emb|AL123456.3|', [['T', 'C', '1564.77', '1/1:0,40:40:99:1593,120,0\t'], ['T', 'C', '1681.77', '1/1:0,40:40:99:1710,120,0\t'], ['T', 'C', '1625.77', '1/1:0,40:40:99:1654,120,0\t']], '3', 'C/C/C']
        annotatedData:
        [[[['3281', '4437']], 'CDS', '+', [['pfam', '"Q59586" '], ['function', '"The RECF protein is involved in DNA metabolism and recombination; it is required for DNA replication andnormal sos inducibility. RECF binds preferentially tosingle-stranded, linear DNA. It also seems to bind ATP."'], ['product', '"DNA replication and repair protein RecF (single-strand DNA binding protein)"'], ['funcCat', '"information pathways" '], ['locus_tag', '"Rv0003" '], ['mass', '"42180.2" '], ['GO', '"GO:0003697,GO0005524,GO0005737,GO0006260,GO0006281,GO0 009432"']]], [['nonSyn', 'I:T', 245, 'atc', 'acc', 733], ['nonSyn', 'I:T', 245, 'atc', 'acc', 733], ['nonSyn', 'I:T', 245, 'atc', 'acc', 733]], [1.0, 1.0, 1.0]][pos],annotatedData[pos])
        now updated that the 2nd last ellement contains list of numreads mapped
        now upadre that last element contains the variant algo used - gakt / samtools
        '''
        #Write the header components
        os.chdir(outputDir)
        newFileName = fileX+"_ANNO.vcf"
        f = open(newFileName,'w')
        header = "pos\tchromosome\t"
        for key in keyCombos: # BWA_GATK, SMALT_SAMTOOLS etc
            #if key not in params.usedKeyCombos:
            #    continue
            #header += key+"\t"
            #if gatkFlag and "GATK" in key:
            if "GATK" in key:
                header += "ref_"+key+"\t"+"mut_"+key+"\t"+"qual_"+key+"\t"+"info_"+key+"\t"+"hetero_freq_"+key+"\t"+"num_Reads_"+key+"\t"
            #if samtoolsFlag and "SAMTOOLS" in key:
            if "SAMTOOLS" in key: 
                header += "ref_"+key+"\t"+"mut_"+key+"\t"+"qual_"+key+"\t"+"info_"+key+"\t"+"hetero_freq_"+key+"\t"+"num_Reads_"+key+"\t"

        if not annotationAllowed:
            #if gatkFlag: 
            header += "mapper_sum_GATK\t"
            #if samtoolsFlag:
            header += "mapper_sum_SAMTOOLS\t"
            #if gatkFlag: 
            header += "mut_per_mapper_GATK\t"
            #if samtoolsFlag:
            header += "mut_per_mapper_SAMTOOLS\t"
        else:
            #if gatkFlag:
            header+="mapper_sum_GATK\t"    
            #if samtoolsFlag:
            header+="mapper_sum_SAMTOOLS\t"
            #if gatkFlag:
            header+="mut_per_mapper_GATK\t"    
            #if samtoolsFlag:
            header+="mut_per_mapper_SAMTOOLS\t"
            
        for key in keyCombos:
            #if key not in params.usedKeyCombos:
            #    continue
            #if gatkFlag and "GATK" in key:
            if "GATK" in key:
                header += "AA_change_type_"+key+"\t"+"AA_change_"+key+"\t"+"AA_Codon_Pos_"+key+"\t"+"ref_codon_"+key+"\t"+"mut_codon_"+key+"\t"+"gene_pos_"+key+"\t"
            #if samtoolsFlag and "SAMTOOLS" in key:
            if "SAMTOOLS" in key:
                header += "AA_change_type_"+key+"\t"+"AA_change_"+key+"\t"+"AA_Codon_Pos_"+key+"\t"+"ref_codon_"+key+"\t"+"mut_codon_"+key+"\t"+"gene_pos_"+key+"\t"
        if annotationAllowed:
            header += "Anno_feature_range\tfeature_type\torientation\t"
            for x in known_feature_properties:
                header += x+"\t" 
        header+="\n"
        f.write(header)
        headerData = header.replace("\n","").split("\t")
        
        #Write the data for this file
        for variant_pos in allPositions:
            for varX in fileVariantData_GATK_AND_SAMTOOLS[variant_pos]:
                toWrite = varX.getDataToWrite(variant_pos,keyCombos,known_feature_properties,  pos_to_feature_num_dict, featureNum_to_Anno_DataDict)
##                print headerData
##                print toWrite
##                raw_input("This is what is written...")
                for x in toWrite[:-1]:
                    f.write(str(x)+"\t")
                f.write(str(toWrite[-1])+"\n")
        return
  
    def loadVariantData(fileX,filesToAnno,VCF_Location_List_File_List,mapperOrderList): #OOP version
        '''
        The data structure here is as follows:
        Central dictionary of all known positions --> fileVariantData
        This dict contains pos:variant objects
        Each variant object contains one position - var.position
        and up to 6 variants
            3 for gatk --> bwa gatk, novo gatk, smalt gatk
            3 for samtools --> bwa samtools, novo samtools, smalt samtools
        Each variant is also a dictionary
        Uses key of mapper+variantAlgoName as key
        ex variant[bwa+gatk] = {}
         can access each element of the dict by keys
         variant[bwa+gatk]["mut"]
         variant[bwa+gatk]["numreads"] etc
        '''
        #load the variants for each mapper into one dictof variant objects using pos as key
        fileVariantData = {}
        #for x in VCF_Location_List_File_List:
        #    print x
        #    raw_input("check 8888899999")
        for element in VCF_Location_List_File_List: #UP TO 3 DIRS - BWA NOVO SMALT
            VCF_Location = element[0]
            vcf_files = element[1]
            os.chdir(VCF_Location)
            for vcfFile in vcf_files:
                if vcfFile.split("_")[0] == fileX: 
                    #Here get the var detec algo name
                    if "GATK" in vcfFile.upper(): #.split("_")[0]: #match
                        varAlgoName = "GATK"
                    elif "SAMTOOLS" in vcfFile.upper(): #.split("_")[0]: #match
                        varAlgoName = "SAMTOOLS"
                    # here get the mapper name...
                    if "BWA" in VCF_Location:
                        mapperName = "BWA"
                    elif "NOVO" in VCF_Location:
                        mapperName = "NOVO"
                    elif "SMALT" in VCF_Location:
                        mapperName = "SMALT"
                    else:
                        print "error", VCF_Location
                        raw_input("should not happedn, vcf location does not contain any mapper names?")
                        exit()
                    try:
                        f = open(vcfFile,'r')
                    except:
                        print "Error, could not open file", vcfFile,"in folder",VCF_Location
                        exit()
                    for line in f:
                        if line[0] == "#":
                            continue
                        temp = line.split("\t")
                        if temp == "":
                            continue
                        if temp[1] == "":
                            continue
                        try:
                            pos = int(temp[1])
                            ref = temp[3]
                            mut = temp[4]
                            qual = temp[5]
                            info = temp[9]
                        except:
                            for iterX in [pos,ref,mut,qual,info]:
                                iterX = "" 
                            print "Error, vcf file is not in known format for file", vcfFile, "in folder", VCF_Location
                            raw_input("press enter to continue")
                        
                        if "," in mut:
                            #add a new variant for each mutation found
                            #cannot just share same info, need to calculate 
                            #important to calc correct hetero freq 
                            if "GATK" in varAlgoName:
                                multiVarInfo = info.split(":")[1].split(",")
                                subMutPos = 0
                                currentRefCount = multiVarInfo[0]
                                #print multiVarInfo
                                for sub_mutation in mut.split(","): 
                                    subMutPos += 1
                                    #print "mut pos is now", subMutPos," out of",len(mut.split(","))
                                    if subMutPos > len(mut.split(",")): #dont use the last one, its just the total reads
                                        break
                                    currentMutCount = multiVarInfo[subMutPos] #Start from 1 since it goes [ref,mut1,mut2,mut3 etc]
                                    newInfo = info.split(":")[0]+":"+currentRefCount+","+multiVarInfo[subMutPos]+":"+info.split(":")[2]+":"+info.split(":")[-2]+":"+info.split(":")[-1]+"\n" 
                                    
                                    if pos not in fileVariantData:
                                        varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                        varX.addMapperData(varAlgoName, mapperName, ref,sub_mutation,qual,newInfo)
                                        fileVariantData[pos] = [varX]
                                    else:
                                        #then this is is already in the mapper data for this key combo
                                        #it simply means that samtools or GAtK found both a snp and indel at this position
                                        #will just add both as separete variables since both can be true
                                        varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                        varX.addMapperData(varAlgoName, mapperName, ref,sub_mutation,qual,newInfo)
                                        fileVariantData[pos].append(varX)
                            elif "SAMTOOLS" in varAlgoName:
                                multiVarInfo = info.split(":")[-1].split(",")
                                subMutPos = 0
                                currentRefCount = multiVarInfo[0]
                                for sub_mutation in mut.split(","):
                                    subMutPos += 1
                                    #print "mut pos is now", subMutPos," out of",len(mut.split(","))
                                    currentMutCount = multiVarInfo[subMutPos] #Start from 1 since it goes [ref,mut1,mut2,mut3 etc]
                                    newInfo = info[:len(info.split(":")[0])+len(info.split(":")[1])+1] + ":"+currentRefCount+","+currentMutCount+"\n"
                                    if pos not in fileVariantData:
                                        varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                        varX.addMapperData(varAlgoName, mapperName, ref,mut,qual,newInfo)
                                        fileVariantData[pos] = [varX]
                                    else:
                                        #ADDING EXISTING POS FOR SAMTOOLS
                                        varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                        varX.addMapperData(varAlgoName, mapperName, ref,sub_mutation,qual,newInfo)
                                        fileVariantData[pos].append(varX)
                        else:
                            if pos not in fileVariantData:
                                varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                varX.addMapperData(varAlgoName, mapperName, ref,mut,qual,info)
                                fileVariantData[pos] = [varX]
                            else:
                                #Assumption here is will only have 6 variants at the same pos, one for each mapper and var combo
                                #only variants with "," will be split into new variants
                                #load the existing variant for this pos and update the mapper info to 
                                #varX = variant(temp[1],temp[0]) #add pos and chr, #Create a new variant object for this position
                                varX = fileVariantData[pos][0]
                                varX.addMapperData(varAlgoName, mapperName, ref,mut,qual,info)
                                #fileVariantData[pos].append(varX)
                    f.close()
        for foundPos in fileVariantData:
            for variantX in fileVariantData[foundPos]:
                variantX.updateMutations(mapperOrderList)
        return fileVariantData #returns the data from each mapper for this file as a variant object
        #########################################

    def annotateMain(EMBLDIR,annotationFile,outDir,VCF_Location_List,mapperOrderList,debugMode,annotationAllowed):
        #########################################
        print "Obtaning file list to annotate..."
        filesToAnno = obtain_file_list(VCF_Location_List) #unique file names {} --> allows both gatk and samtools --> R100_GATK R100_SAMTOOLS
        print "Loading reference..."
        #Updatged to allow the annotation data to be missing
        if annotationAllowed:
            pos_to_feature_num_dict, featureNum_to_Anno_DataDict, featureNum_to_seq_DataDict, known_feature_properties = load_embl_feature_coordinates(annotationFile,EMBLDIR)
        else:
            pos_to_feature_num_dict = {}
            featureNum_to_Anno_DataDict = {}
            featureNum_to_seq_DataDict = {}
            known_feature_properties = {}


            
        print "Reference loaded into system memory"
        #if debugMode:
            #print known_feature_properties
            #raw_input("These are the extracted features from the loaded EBML file.")
            
        #Test to see if I can retreve the correct data for a snp position
        #testSNPpos = 897209
        #print pos_to_featu re_num_dict[testSNPpos]
        #for x in pos_to_feature_num_dict[testSNPpos]:
        #    print featureNum_to_Anno_DataDict[x]
        #    print featureNum_to_seq_DataDict[x]
        #raw_input("DONE")
        
        VCF_Location_List_File_List = []
        for VCF_Location in VCF_Location_List: 
            VCF_Location_List_File_List.append([VCF_Location,[f for f in os.listdir(VCF_Location) if f.endswith('.vcf')]]) # and "SAMTOOLS" not in f]]) #[BWA,vcfs], [NOVO, vcfs], [smalt. vcfs]
            
            VCF_Location_List_File_List.sort() 
        
        if filesToAnno == {}:
            raw_input("Error, no files found to annotate")

        for fileX in filesToAnno: # BOTH GATK AND SAMTOOLS SUPPORTED
            if not annotationAllowed:
                print "Summarizing data for file: ",fileX,"..."
            else:
                print "Annotating file: ",fileX,"..."
            #here files to anno is shortname: f1,f2...f6 --> (bwa-gatk, bwa-samtools etc)
            #print filesToAnno, fileX

            samtoolsFlag = False
            gatkFlag = False
            for subfile in filesToAnno[fileX]:
                if "SAMTOOLS" in subfile.upper():
                    samtoolsFlag = True
                if "GATK" in subfile.upper():
                    gatkFlag = True
            startTime = time.time()
            
            fileVariantData_GATK_AND_SAMTOOLS = loadVariantData(fileX,filesToAnno,VCF_Location_List_File_List,mapperOrderList) #Return vcf data lists for each mapper in list of TWO lists, one for samtools, one for gatk

            for pos in fileVariantData_GATK_AND_SAMTOOLS:
                for varX in fileVariantData_GATK_AND_SAMTOOLS[pos]:
                    if int(pos) <> int(varX.position):
                        print "FATAL ERROR THIS SHOULD NEVE HAPPEDDDDDD"
                        print pos, varX.position
                        raw_input()
 
            keyCombos = getAnnoData(fileX, fileVariantData_GATK_AND_SAMTOOLS, known_feature_properties, pos_to_feature_num_dict, featureNum_to_Anno_DataDict, featureNum_to_seq_DataDict, annotationAllowed, gatkFlag, samtoolsFlag, mapperOrderList)
            #A list consisting of lists of [annoData, mutationData,heteroDataList,numReads]
##            key =  pos_to_feature_num_dict[24692]
##            print key
##            print featureNum_to_Anno_DataDict[key[0]]
##            raw_input("this must work")
            
            allPositions = recalculate_AA_changes(fileVariantData_GATK_AND_SAMTOOLS, keyCombos, pos_to_feature_num_dict, featureNum_to_Anno_DataDict)
            print "annotation time:",round((time.time() - startTime),2), "seconds"
            print "Writing data to file..."
            writeData(outDir,fileX,fileVariantData_GATK_AND_SAMTOOLS,known_feature_properties,mapperOrderList, annotationAllowed,gatkFlag,samtoolsFlag, allPositions, keyCombos, featureNum_to_Anno_DataDict, pos_to_feature_num_dict)
        print "annotation complete."
        return pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties 
    
    pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties  = annotateMain(emblDir, annotationFile, outputDir, VCF_Location_List,mapperOrderList,debugMode, annotationAllowed)        
    return pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties 

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
                    #End of automated annotation
#########################################################################################
#########################################################################################
#########################################################################################

      
def getFastaName(inputFileName):
    fileExt = inputFileName.split(".")[-1]
    return inputFileName[:len(inputFileName)-len(fileExt)-1]

def fastQCSH(trimComplete):
    if trimComplete:
        inputDir = params.trimmedFastQ
        outputDir = params.fastQCStatsDir2
        fastqcScriptName = "FastQC2.sh"
    else:
        inputDir = params.fastQ
        outputDir = params.fastQCStatsDir1
        fastqcScriptName = "FastQC1.sh" 
    
    fileArray = []
    totalLoaded = 0
    os.chdir(params.outputDir)  
      
    try:
        os.makedirs(outputDir)
    except:
        print "Directory",outputDir,"already exists, proceeding"
        
    for fileX in os.listdir(inputDir):    
        if fileX.endswith(".fastq") or fileX.endswith(".fastq.gz"):
            totalLoaded +=1
            print "reading file: ",fileX
            if fileX.endswith(".fastq.gz") and params.trimMethod == "Fixed_Amount_Trim":
                print "ERROR: This trimming method can only be used on uncompressed FASTQ files, a .gz file extention was detected, please uncompress the files and try again"
                return False
            fileArray.append(str(fileX))              
    print "A total of ",totalLoaded,"FASTQ files were loaded"
    fileArray.sort()
    
    os.chdir(params.scripts_trimming)
    f = open(fastqcScriptName,'w')
    f.write(params.fastQCPath+" -j "+params.java7+" --nogroup --extract -t "+str(params.cores)+" ")
    for x in fileArray:
        f.write(inputDir+x)
        f.write(' ')
    f.write('-o '+outputDir)
    
    print "FastQC script created as",fastqcScriptName
    f.close()
    return True
    ################################################

###############################################################################
#MAPPER SCRIPTS
###############################################################################

def partitionFastQList(fastQDir):
    data = []
    def sampleName(fileX):
        return fileX.split("_")[0]

    os.chdir(fastQDir)
    for fileX in os.listdir(fastQDir):
        if fileX.endswith(".fastq") or fileX.endswith("fastq.gz"):
            data.append(fileX)
    data.sort()
    singleData = []
    pairedData = []
    previous = ''
    pos = 0
    flag = True
    while pos <= len(data)-1:
        if pos == 0 or flag:
            previous = data[pos]
            if pos == len(data)-1:
                singleData.append(previous.replace("\n",""))
            pos+=1
            flag = False
            continue

        current = data[pos]
        if sampleName(current) == sampleName(previous):
            pairedData.append(previous.replace("\n",''))
            pairedData.append(current.replace("\n",''))
            pos+=1
            flag=True
            continue
        else:
            if pos == len(data) -1:
                singleData.append(previous.replace("\n",''))
                singleData.append(current.replace("\n",''))
                pos+=2
                continue
            else:
                singleData.append(previous.replace("\n",''))
                flag=True
                continue
    return [singleData, pairedData] 

##def loadReferenceFasta(directoryX):
##    #searches for the file name of the reference .fasta file in the directory given
##    #returns the file name (string)
##    #find the ref name
##    refName = None
##    
##    os.chdir(directoryX)
##    countX = 0
##    for fileX in glob.glob('*.fasta'):
##        countX +=1 
##        refName = fileX
##        #print "using reference file: ",refName
##    if countX > 1:
##        print "you have more than one .fasta reference HERE - change the python file - more or less at the end file in ", directoryX
##        print "please manually exit using control+C and try again"
##        raw_input()
##        countX = 0
##        for fileX in glob.glob('*.fasta'):
##            countX +=1 
##            refName = fileX
##            print "using refence file: ",refName
##        if countX > 1:
##            print "you have more than one .fasta reference file in ", directoryX
##            print "please manually exit using control+C and try again"
##            raw_input()
##    if refName == None:
##        print "error loading reference fasta file from the specified directory"
##        raw_input()
##    #print "using "+directoryX+refName+" as reference."
##    return refName


def partitionFileList(fileArray, trimArray ,ID ,SM, bins):
    '''
    this splits a list of files into 5 groups,
    the output is a list of lists which contains 5 lists
    the last one contains all the extras which did not fit into the division of 5
    so will have up to 4 more at times
    if there are less than 5 files, all are added to the first list
    so in other words whatever_List[0]
    '''
    lenX =len(fileArray)
    print "splitting ", lenX,"files up into ",bins,"lists..."
    splitList = [] #the file array into 5
    splitTrimArray =[]
    splitID = []
    splitSM = []
    
    for x in range(bins):
        splitList.append([])  #has 5 sublists
        splitTrimArray.append([])
        splitID.append([])
        splitSM.append([]) 

    roughAmount = lenX/5
    print "dividing into ",roughAmount,"`s"
    pos = -1
    for x in range(bins):
        for y in range(roughAmount):
            pos += 1
            splitList[x].append(fileArray[pos])
            splitTrimArray[x].append(trimArray[pos])
            splitID[x].append(ID[pos])
            splitSM[x].append(SM[pos])
##            print listX[pos]
    print "final position: ", pos
    rest = lenX-pos-1
    print "need more", rest

    for x in range(rest):
        pos+=1
        splitList[0].append(fileArray[pos])
        splitTrimArray[0].append(trimArray[pos])
        splitID[0].append(ID[pos])
        splitSM[0].append(SM[pos])
    print "rest went up to pos ", pos
        
    return splitList, splitTrimArray, splitID, splitSM

##################################################################
#2 Find trim cutoff and write to sh file to perform trimming to new dir: /params.trimmedFastQ/
# Looks for trim data in fastQCStats dir
#output the trimming commangs to autrim.sh 

def tidyName2(name,trim):
    #takes filename - outputs trim file name
    sampleName = ""
    for char in name:
        if char == "_":
            break
        else:
            sampleName += char              
    if "R1" in name[2:] or "Read1" in name[2:]:
        sampleName+="_R1"
    elif "R2" in name[2:] or "Read2" in name[2:]:
        sampleName +="_R2"
    else:
        print "ERROR RENAMING FILES, R1 or R2 not in fileNAME, fix and restart"
        raw_input()
    return sampleName+'_trim'+'.fastq'   #str(trim)+'.fastq'

def tidyNameX(name,trim):
    #takes filename - outputs trim file name
    #find location of "pool_"
    sampleName = ""
    count = 0
    for char in name:
        if char == "_":
            count+=1
        if count == 3:
            if char <> "_":
                sampleName+=char
        elif count>3:
            break
        
    if "R1" in name:
        sampleName+="_R1"
    elif "R2" in name:
        sampleName +="_R2"
    else:
        print "ERROR RENAMING FILES, R1 or R2 not in fileNAME, fix and restart"
        raw_input()
    return sampleName+'_trim'+'.fastq' #+str(trim)+'.fastq'

def tidyName(name,trim):
    pos = 0
    copyPos = 0
    newName = ''
    print name
    while pos < len(name) and (str.lower(name[pos]) <> "p" or (str.lower(name[pos]) <> "_" and str.lower(name[pos+1]) <> "_")):
        pos +=1
       # print pos
       # print name[pos]
        if pos+6 < len(name):
            if str.lower(name[pos]) == "_" and name[pos+1] =="_":
               # print "the file used __"
               # raw_input()
                temp = pos+2
                while name[temp] <> "_" and temp < len(name):
                    temp+=1
            
                copyPos = temp
                break
            if str.lower(name[pos]) == 'p' and name[pos+5] == '_':
                copyPos = pos+5
                break
            elif str.lower(name[pos]) == 'p' and name[pos+6] == '_':
                copyPos = pos+6
                break
        else:
            print "file handling error, using long name instead"
           # raw_input()
            return name +'_trim'+'.fastq'  #str(trim)+'.fastq'
    newName = name[copyPos+1:(len(name)-6)]

    newName = newName +'_trim'+'.fastq' #str(trim)+'.fastq'
    return newName


########################################################################
#to combine the names of read1 and read 2 into one file name#
########################################################################

def extractFileNameData(fastQFileArray):
    '''
    input: Sorted list of fastq files
    output: List of identifiers needed to add readgroups to bam files
    lits are ID, SM and LB corresponding to each fastq file.
    Assumes file names are in the format: SAMENAME_POOL_LIBRARY_R1.fastq
    If not - pool and library info gets atrificially generated using sample name
    '''
    ID = []
    SM = []
    LB = []
    barcodes = []
    skipFullFileNameData = False
    for fileName in fastQFileArray:
        tempID = ""
        tempSM = "12345"
        tempLB = "unknown"
        if "_" not in fileName:
            #print "Filename error, files must be named using the convention of SampleIdentifier_poolIdentifier_LibraryIdentifier_ReadIdentifier.fastq"
            #print "for example: 'R1234_Pool4_Library24_R1.fastq'"
            #print "or with optional additional barcode info: R1234_Pool4_Library24_TCATTC_R1.fastq"
            #print "Please rename all files using this naming convention and re-run USAP."
            #print "the '_' separator was missing from file:", fileName
            #raw_input("Press enter to exit the program.")
            #exit(0)
            print "the '_' separator was not found file file", fileName, "assuming this is NOT paired-end sequence file..."
            fileNameData = fileName.split(".")
            barcodes.append("")
            tempID = fileNameData[0]
        else:
            fileNameData = fileName.split("_")
            try:
                if fileNameData[3] <> "R1" and fileNameData[3] <> "R2":
                    barcodes.append(fileNameData[3])
            except:
                barcodes.append("")
            
            try:
                tempID = fileNameData[0]
                tempSM = fileNameData[1]
                tempLB = fileNameData[2]
                
            except:
                print fileNameData
                print "Filename error, files must be named using the convention of SampleIdentifier_poolIdentifier_LibraryIdentifier_ReadIdentifier.fastq"
                print "for example: R1234_Pool4_Library24_R1.fastq"
                print "or with optional additional barcode info: R1234_Pool4_Library24_TCATTC_R1.fastq"
                print "Please rename all files using this naming convention where possible and re-run USAP."
                ans = ""
                if not skipFullFileNameData:
                    while ans not in ["Y","y","n","N","A","a"]:
                        ans = raw_input("Would you like to continue anyway ? Y/N/A (not reccomended, SM '12345' and library 'unknown' will be used for readgroup info)")
                        if ans == "A" or ans == "a":
                            skipFullFileNameData = True 
                        if ans.upper() == "Y" or ans.upper == "A" :
                            tempID = fileNameData[0]
                            tempSM = "12345"
                            tempLB = "unknown"
                        elif ans.upper() == "N":
                            raw_input("Press enter to exit the program.")
                            exit(0)
                else:
                    tempID = fileNameData[0]
                    tempSM = "12345"
                    tempLB = "unknown"

            if tempLB == "R1" or tempLB == "R2" or ".fastq" in tempLB:
                tempLB = "unknown"
            if tempSM == "R1" or tempSM == "R2" or ".fastq" in tempLB:
                tempSM = "12345"
##        print "Read group info extraction analysis:"
##        print fileName
##        print "ID:",tempID
##        print "SM:",tempSM
##        print "LB:",tempLB
##        raw_input()
        ID.append(tempID)
        SM.append(tempSM)
        LB.append(tempLB)
    ###############################################################
    trimArray = []
    if params.trimMethod == "Fixed_Amount_Trim":
        for fileT in fastQFileArray:
            pos = 8 #this many characters from the right
            trimAmount = []
            try:
##                while fileT[len(fileT)-pos] not in str(range(10)):
##                    pos-=1
                while fileT[len(fileT)-pos] <> ".":
                    trimAmount.append(fileT[len(fileT)-pos])
                    pos-=1
                j = ""
                j=j.join(trimAmount)
                trimArray.append(j)
            except:
                trimArray.append(str(0))
    return ID,SM,LB,barcodes,trimArray
    
 
def BWAAlign_combine(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)

    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]
    
    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #change dirX to params.trimmedFastQ
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) #change dirX to params.trimmedFastQ
    '''
    
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE 
    #reads can be either "pairedEnd",  "singleEnd", "mixed"  
    if params.reads == "singleEnd":
        fileArray = trimmedFilesSE
        ID = IDSE
        SM = SMSE
        LB
    if params.reads == "pairedEnd":
        fileArray = trimmedFilesPE
        ID = IDPE
        SM = SMPE
    if params.reads == "mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE
    
    os.chdir(params.scripts_BWA)
    BWA = "1_BWAAlign.sh"
    BWA_Cleanup = "1_BWAAlign_cleanup.sh"
    f = open(BWA,'w')
    f2 = open(BWA_Cleanup,'w')

    carryOverList_new = []
    #updated for multi mode
    #Updated for multi ref fasta
    for referenceBWA in params.fastaList:
        referenceBWA_shortName = getFastaName(referenceBWA)
        for pos in range(len(fileArray)): #fileName in fileArray:
##            f.write(params.bwa+' aln -t '+str(params.coreSplit[0])+' '+params.reference+referenceBWA+' '+params.trimmedFastQ+fileArray[pos]+" > "+params.BWAAligned_aln+fileArray[pos][:-6]+"_bwa.sai")
            f.write(params.bwa+' aln -t '+str(params.coreSplit[0])+' '+params.reference+referenceBWA+' '+params.trimmedFastQ+fileArray[pos]+" > "+params.BWAAligned_aln+fileArray[pos][:-9]+"_bwa.sai")
            f.write('\n')
            f2.write("rm "+params.BWAAligned_aln+fileArray[pos][:-9]+"_bwa.sai\n")
            carryOverList_new.append(fileArray[pos][:-9]+"_bwa.sai")
    f.close()
    f2.close()
   
    combineReads = "2_combineReads.sh"
    combineReads_Cleanup = "2_combineReads_Cleanup.sh"
    os.chdir(params.scripts_BWA)
    f2 = open(combineReads,'w')
    f3 = open(combineReads_Cleanup,'w')

##    referenceBWA = loadReferenceFasta(params.bwaRef)

    if params.reads == "singleEnd" or params.reads == "mixed":
##        print params.fastaList
##        raw_input("OK?")
##        for referenceBWA in params.fastaList:
##            print referenceBWA
##            raw_input()
        pos = 0
        for pos in range(len(fileArraySE)):
            readGroup = "'@RG\\tID:"+IDSE[pos]+"\\tSM:"+SMSE[pos]+"\\tLB:"+LBSE[pos]+"\\tPL:Illumina'"
##            f2.write(params.bwa+" samse -r '@RG\\tID:"+IDSE[pos]+"\\tSM:"+SMSE[pos]+"\\tPL:Illumina' "+params.reference+referenceBWA+" "+params.BWAAligned_aln+carryOverList_new[pos]+" "+params.trimmedFastQ+fileArraySE[pos]+" > "+params.BWAAligned_aln+IDSE[pos]+"_"+referenceBWA+"_bwa.sam")
            f2.write(params.bwa+" samse -r "+readGroup+" "+params.reference+referenceBWA+" "+params.BWAAligned_aln+carryOverList_new[pos]+" "+params.trimmedFastQ+fileArraySE[pos]+" > "+params.BWAAligned_aln+IDSE[pos]+"_bwa.sam") 
            f2.write('\n')
            f3.write("rm "+params.BWAAligned_aln+IDSE[pos]+"_bwa.sam\n")
    
    if params.reads == "pairedEnd" or params.reads == "mixed":
        for referenceBWA in params.fastaList:
            referenceBWA_shortName = getFastaName(referenceBWA)
            pos = 0
            while pos <= len(fileArrayPE)-2:
                if IDPE[pos] <> IDPE[pos+1]:
                    print "error is ", IDPE[pos], "and ", IDPE[pos+1]
                    print "bwa sampe error - the two files are not matching - cannot proceed - please manually quit and fix the error"
                    raw_input()
                    exit
                readGroup = "'@RG\\tID:"+IDPE[pos]+"\\tSM:"+SMPE[pos]+"\\tLB:"+LBPE[pos]+"\\tPL:Illumina'"
##                f2.write(params.bwa+" sampe -r '@RG\\tID:"+IDPE[pos]+"\\tSM:"+SMPE[pos]+"\\tPL:Illumina' "+params.reference+referenceBWA+" "+params.BWAAligned_aln+carryOverList_new[pos+len(fileArraySE)]+" "+params.BWAAligned_aln+carryOverList_new[pos+1+len(fileArraySE)]+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1]+" > "+params.BWAAligned_aln+IDPE[pos]+"_"+referenceBWA_shortName+"_"+"trim_bwa.sam")
                f2.write(params.bwa+" sampe -r "+readGroup+" "+params.reference+referenceBWA+" "+params.BWAAligned_aln+carryOverList_new[pos+len(fileArraySE)]+" "+params.BWAAligned_aln+carryOverList_new[pos+1+len(fileArraySE)]+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1]+" > "+params.BWAAligned_aln+IDPE[pos]+"_bwa.sam")           
                f2.write('\n')
                f3.write("rm "+params.BWAAligned_aln+IDPE[pos]+"_bwa.sam\n")
                pos +=2

    f2.close()
    f3.close()
    #print "combine list for 'bwa sampe' creates as: ",combineReads
    return


       
#############################################################################
# NOVO ALIGNMENT
# 

'''This program collects the names of all the trimemd fastq files and creates a
new .sh file to automate NOVO alignment of all files '''


def NOVOAlign(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #change dirX to params.trimmedFastQ
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) 
    '''
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE
    
    if params.reads == "singleEnd":
        #fileArray , trimArray , ID, SM  = GenerateCleanFileNamesSEMode(params.trimmedFastQ)
        fileArray = trimmedFilesSE
##        trimArray = trimmedFilesPE
        ID = IDSE
        SM = SMSE
    if params.reads == "pairedEnd":
        #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)
        fileArray = trimmedFilesPE
##        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    if params.reads == "mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
##        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE

    #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)

    os.chdir(params.scripts_NOVO)
    NOVO = "1_1_NOVOAlign.sh"
    NOVO_Cleanup = "1_1_NOVOAlign_cleanup.sh"

    pos = 0

    f = open(NOVO,'w')
    f2 = open(NOVO_Cleanup,'w')
    if fileArray == []:
        print "the were no fastq files found in ", params.trimmedFastQ," fix path and run again"
        raw_input()
        return
    if params.reads == "singleEnd":
        for referenceNOVO in params.fastaList:
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            for pos in range(len(fileArraySE)):
##                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArraySE[pos]+" -o SAM '@RG\tID:"+IDSE[pos]+"\tSM:"+SMSE[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim"+"_"+trimArraySE[pos]+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDSE[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                readGroup = "'@RG\tID:"+IDSE[pos]+"\tSM:"+SMSE[pos]+"\tLB:"+LBSE[pos]+"\tPL:Illumina'"
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArraySE[pos]+" > "+params.trimmedFastQ+fileArraySE[pos][:-3]+" && "+params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArraySE[pos][:-3]+" -o SAM "+readGroup+" 2> "+params.NOVOAligned_aln+IDSE[pos]+"_"+trimArraySE[pos]+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim_novo.sam")
                f.write(" && rm "+params.trimmedFastQ+fileArraySE[pos][:-3]+"\n")
                f2.write("rm "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim_novo.sam\n")
    
    if params.reads == "pairedEnd":
        for referenceNOVO in params.fastaList:
            pos = 0
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            while pos <= len(fileArray)-2:
##                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArray[pos]+" "+params.trimmedFastQ+fileArray[pos+1]+" -o SAM '@RG\tID:"+ID[pos]+"\tSM:"+SM[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+ID[pos]+"_"+"trim_novo_stats.novodist > "+params.NOVOAligned_aln+ID[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                readGroup = "'@RG\tID:"+IDPE[pos]+"\tSM:"+SMPE[pos]+"\tLB:"+LBPE[pos]+"\tPL:Illumina'"
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArrayPE[pos]+" > "+params.trimmedFastQ+fileArrayPE[pos][:-3]+" && ")
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArrayPE[pos+1]+" > "+params.trimmedFastQ+fileArrayPE[pos+1][:-3]+" && ")
                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArray[pos][:-3]+" "+params.trimmedFastQ+fileArray[pos+1][:-3]+" -o SAM "+readGroup+"+ 2> "+params.NOVOAligned_aln+ID[pos]+"_"+"trim_novo_stats.novodist > "+params.NOVOAligned_aln+ID[pos]+"_"+"trim_novo.sam")
                f.write(" && rm "+params.trimmedFastQ+fileArrayPE[pos][:-3])
                f.write(" && rm "+params.trimmedFastQ+fileArrayPE[pos+1][:-3]+"\n")
                f.write('\n')
                f2.write("rm "+params.NOVOAligned_aln+ID[pos]+"_"+"trim_novo.sam\n")
                pos += 2
                
    if params.reads == "mixed":
        for referenceNOVO in params.fastaList:
            pos = 0
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            for pos in range(len(fileArraySE)):
                readGroup = "'@RG\tID:"+IDSE[pos]+"\tSM:"+SMSE[pos]+"\tLB:"+LBSE[pos]+"\tPL:Illumina'"
##                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArraySE[pos]+" -o SAM '@RG\tID:"+IDSE[pos]+"\tSM:"+SMSE[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim"+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDSE[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArraySE[pos]+" > "+params.trimmedFastQ+fileArraySE[pos][:-3]+" && ")
                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArraySE[pos][:-3]+" -o SAM "+readGroup+" 2> "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim"+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim_novo.sam")
                f.write(" && rm "+params.trimmedFastQ+fileArraySE[pos][:-3]+"\n")
                f2.write("rm "+params.NOVOAligned_aln+IDSE[pos]+"_"+"trim_novo.sam\n")
        for referenceNOVO in params.fastaList:
            referenceNOVO_shortName = getFastaName(referenceNOVO)    
            pos = 0
            while pos <= len(fileArrayPE)-2:
                readGroup = "'@RG\tID:"+IDPE[pos]+"\tSM:"+SMPE[pos]+"\tLB:"+LBPE[pos]+"\tPL:Illumina'"
                #f.write(params.novoalign+" -d "+params.refNovo+referenceNOVO[0:-6]+".ndx"+" -f "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1]+" -o SAM '@RG\tID:"+IDPE[pos]+"\tSM:"+SMPE[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim"+"_"+trimArrayPE[pos]+"and"+trimArrayPE[pos+1]+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim_novo.sam")
##                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1]+" -o SAM '@RG\tID:"+IDPE[pos]+"\tSM:"+SMPE[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim"+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDPE[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArrayPE[pos]+" > "+params.trimmedFastQ+fileArrayPE[pos][:-3]+" && ")
                f.write("gunzip -f -c "+params.trimmedFastQ+fileArrayPE[pos+1]+" > "+params.trimmedFastQ+fileArrayPE[pos+1][:-3]+" && ")
                f.write(params.novoalign+" -d "+params.reference+referenceNOVO_shortName+".ndx"+" -f "+params.trimmedFastQ+fileArrayPE[pos][:-3]+" "+params.trimmedFastQ+fileArrayPE[pos+1][:-3]+" -o SAM "+readGroup+" 2> "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim"+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim_novo.sam")
                f.write(" && rm "+params.trimmedFastQ+fileArrayPE[pos][:-3])
                f.write(" && rm "+params.trimmedFastQ+fileArrayPE[pos+1][:-3]+"\n")
                f2.write("rm "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim_novo.sam\n")
                pos += 2
                
    #print "novo alignment .sh list file created as: ",params.scripts_NOVO+NOVO
    f.close()
    f2.close()
    return

def NOVOAlignMulti():
    #splits the sh file from novoalign into several files
    #since the new novo align does not support parralelizing anymore by specifying the amount of threads, instead you need to run more instances at the same time.
    #thus if you have 4 cores, run 4 novoalgns.

    os.chdir(params.scripts_NOVO)
    NOVO = open("1_1_NOVOAlign.sh",'r')
    data = []
    pos = 0
    flag = False
    for line in NOVO:
        line = line.replace("\n","")
        if pos == int(params.cores)-1:
            pos = 0
            data.append(line+" &\n")
            data.append("wait\n")
            flag = True
        else:
            data.append(line+" &\n")
        pos+=1
    if not flag:
        data.append("wait\n")
    NOVO.close()

    NOVO = open("1_2_NOVOAlign_multi.sh",'w')
    for x in data:
        NOVO.write(x)
    NOVO.close()
    
##    for x in range(int(params.cores)):
##        if splitList[x] <> []:
##            NOVO.write("sh ./Scripts/NOVO/1_3_NOVOAlign"+str(x+1)+".sh &\n")
##    NOVO.write("wait\n")
##    NOVO.close()
##    
##    for x in range(int(params.coreSplit[1])):
##        if splitList[x] == []:
##            break
##        NOVO = open("NOVOAlign"+str(x+1)+".sh",'w')
##        for line in splitList[x]:
##            NOVO.write(line)
##        NOVO.close()
    return
        
##############################################################################
# SMALT ALIGNMENT
# 

'''This program collects the names of all the trimemd fastq files and creates a
new .sh file to automate SMALT alignment of all files '''

def SMALTAlign(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #change dirX to params.trimmedFastQ
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) 
    '''
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE
    
    if params.reads == "singleEnd":
        #fileArray , trimArray , ID, SM  = GenerateCleanFileNamesSEMode(params.trimmedFastQ)
        fileArray = trimmedFilesSE
##        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
        LB = LBSE
    if params.reads == "pairedEnd":
        #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)
        fileArray = trimmedFilesPE
##        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
        LB = LBPE
    if params.reads =="mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
##        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE
        LB = LBSE + LBPE

    os.chdir(params.scripts_SMALT)
    SMALT = "1_SMALTAlign.sh"
    SMALT_cleanup = "1_SMALTAlign_cleanup.sh"
    carryOverList_old = []
    pos = 0
    f = open(SMALT,'w')
    f2 = open(SMALT_cleanup,'w')

    if fileArray == []:
        print "there were no fastq files found in ", params.trimmedFastQ," fix path and run again"
        raw_input()
        return
    if params.reads == "singleEnd":
        for referenceSMALT in params.fastaList:
            if referenceSMALT.endswith(".fasta"):
                referenceSMALT = referenceSMALT[:-6]
            if referenceSMALT.endswith(".fa"):
                referenceSMALT = referenceSMALT[:-3]  
            referenceSMALT_shortName = getFastaName(referenceSMALT)
            for pos in range(len(fileArraySE)):
##                f.write(params.smaltBinary+" map -f sam -o "+params.SMALTAligned_aln+IDSE[pos]+"_"+referenceSMALT_shortName+"_"+"trim_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArraySE[pos])
                f.write(params.smaltBinary+" map -x -f sam -n "+str(params.coreSplit[2])+" -O -o "+params.SMALTAligned_aln+IDSE[pos]+"_"+"trim_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArraySE[pos])
                carryOverList_old.append(IDSE[pos]+"_"+"trim_smalt.sam")
                f.write('\n')
                f2.write("rm "+params.SMALTAligned_aln+IDSE[pos]+"_"+"trim_smalt.sam\n")
    
    if params.reads == "pairedEnd":
        for referenceSMALT in params.fastaList:
            if referenceSMALT.endswith(".fasta"):
                referenceSMALT = referenceSMALT[:-6]
            if referenceSMALT.endswith(".fa"):
                referenceSMALT = referenceSMALT[:-3] 
            pos = 0
            referenceSMALT_shortName = getFastaName(referenceSMALT)
            while pos <= len(fileArray)-2:
##                f.write(params.smaltBinary+" map -i "+str(params.insertmax)+" -j "+params.insertmin+" -f sam -n "+str(params.coreSplit[2])+" -O -o "+params.SMALTAligned_aln+IDPE[pos]+"_"+referenceSMALT_shortName+"_"+"trim"+"_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1])
                f.write(params.smaltBinary+" map -x -i "+str(params.insertmax)+" -j "+params.insertmin+" -f sam -n "+str(params.coreSplit[2])+" -O -o "+params.SMALTAligned_aln+IDPE[pos]+"_"+"trim"+"_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1])
                carryOverList_old.append(IDPE[pos]+"_"+"trim_smalt.sam")
                f.write('\n')
                f2.write("rm "+params.SMALTAligned_aln+IDPE[pos]+"_"+"trim"+"_smalt.sam\n")
                pos +=2
                
    
    if params.reads == "mixed":
        for referenceSMALT in params.fastaList:
            if referenceSMALT.endswith(".fasta"):
                referenceSMALT = referenceSMALT[:-6]
            if referenceSMALT.endswith(".fa"):
                referenceSMALT = referenceSMALT[:-3] 
            pos = 0
            referenceSMALT_shortName = getFastaName(referenceSMALT)
            for pos in range(len(fileArraySE)):
##                f.write(params.smaltBinary+" map -f sam -o "+params.SMALTAligned_aln+IDSE[pos]+"_"+referenceSMALT_shortName+"_"+"trim_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArraySE[pos])
                f.write(params.smaltBinary+" map -x -f sam -o "+params.SMALTAligned_aln+IDSE[pos]+"_"+"trim_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArraySE[pos])
                carryOverList_old.append(IDSE[pos]+"_"+"trim_smalt.sam")
                f.write('\n')
                f2.write("rm "+params.SMALTAligned_aln+IDSE[pos]+"_"+"trim_smalt.sam\n")
        for referenceSMALT in params.fastaList:
            if referenceSMALT.endswith(".fasta"):
                referenceSMALT = referenceSMALT[:-6]
            if referenceSMALT.endswith(".fa"):
                referenceSMALT = referenceSMALT[:-3] 
            pos = 0
            referenceSMALT_shortName = getFastaName(referenceSMALT) 
            while pos <= len(fileArrayPE)-2:
                #f.write(params.novoalign+" -d "+params.refNovo+referenceNOVO[0:-6]+".ndx"+" -f "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1]+" -o SAM '@RG\tID:"+IDPE[pos]+"\tSM:"+SMPE[pos]+"\tPL:Illumina' 2> "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim"+"_"+trimArrayPE[pos]+"and"+trimArrayPE[pos+1]+"_novo_stats.novodist > "+params.NOVOAligned_aln+IDPE[pos]+"_"+"trim_novo.sam")
##                f.write(params.smaltBinary+" map -i "+str(params.insertmax)+" -j "+str(params.insertmin)+" -f sam -n "+str(params.coreSplit[2])+" -O -o "+params.SMALTAligned_aln+IDPE[pos]+"_"+referenceSMALT_shortName+"_"+"trim"+"_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1])
                f.write(params.smaltBinary+" map -x -i "+str(params.insertmax)+" -j "+str(params.insertmin)+" -f sam -n "+str(params.coreSplit[2])+" -O -o "+params.SMALTAligned_aln+IDPE[pos]+"_"+"trim"+"_smalt.sam "+params.reference+referenceSMALT+" "+params.trimmedFastQ+fileArrayPE[pos]+" "+params.trimmedFastQ+fileArrayPE[pos+1])
                carryOverList_old.append(IDPE[pos]+"_"+"trim_smalt.sam")
                f.write('\n')
                f2.write("rm "+params.SMALTAligned_aln+IDPE[pos]+"_"+"trim"+"_smalt.sam\n")
                pos += 2
    f.close()
    f2.close()
    ########################3
    #This creates the FIRST picard sort sh file to sort the sam file

    os.chdir(params.scripts_SMALT)
    picardSort = "2_sortSmaltSam.sh"
    picardSort_cleanup = "2_sortSmaltSam_cleanup.sh"
    carryOverList_new = []
    f = open(picardSort,'w')
    f2 = open(picardSort_cleanup,'w')
    for x in carryOverList_old: #SAMFileList:            
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.SortSamDir+" I="+params.SMALTAligned_aln+x+" O="
        +params.SMALTAligned_aln+x[:(len(x)-4)]+"_sort.sam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT")
        carryOverList_new.append(x[:(len(x)-4)]+"_sort.sam")                           
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sort.sam\n")
    #print "first picard sort sh file created as sortSmaltSam.sh"
    f.close()
    f2.close()

    ###########################
    #This adds read groups to the alignend and sorted sam files
    os.chdir(params.scripts_SMALT)
    addReadGroups = "3_addReadGroupsToSortedSam.sh"
    addReadGroups_cleanup = "3_addReadGroupsToSortedSam_cleanup.sh"
    pos = 0
    carryOverList_old = carryOverList_new
    carryOverList_new = []                             
    f = open(addReadGroups,'w')
    f2 = open(addReadGroups_cleanup,'w')

    for x in carryOverList_old:  #SAMFileList:
        readGroup = " RGID="+ID[pos]+" RGSM="+SM[pos]+" RGPL=Illumina RGPU=run RGLB="+LB[pos]
        f.write(params.java7+" -jar "+params.picardAddReadGroup+" INPUT="+params.SMALTAligned_aln+x+" OUTPUT="+params.SMALTAligned_aln+x[:-4]+"_RG.sam"+readGroup)
        carryOverList_new.append(x[:-4]+"_RG.sam")
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x[:-4]+"_RG.sam\n")
        pos += 1
    f.close()
    f2.close()
    return

#############################################-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#scripts creation
def variantScriptsBWA(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) 
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) 
    '''
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE
    if params.reads == "singleEnd":
        #fileArray , trimArray , ID, SM  = GenerateCleanFileNamesSEMode(params.trimmedFastQ)
        fileArray = trimmedFilesSE
##        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
    if params.reads == "pairedEnd":
        #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)
        fileArray = trimmedFilesPE
##        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    if params.reads == "mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
##        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE

##    fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ) #change dirX to params.trimmedFastQ
    carryOverList_old = ID
    carryOverList_new = []
##########################################
    #this part creates the picard .sh file 
    os.chdir(params.BWAAligned_aln)
    #samFileList = []
    if params.reads == "singleEnds":
        for referenceBWA in params.fastaList:
            referenceBWA_shortName = getFastaName(referenceBWA)
            for pos in range(len(fileArraySE)): #Add all
##                carryOverList_new.append(carryOverList_old[pos]+"_"+referenceBWA_shortName+"_"+"trim_bwa.sam")
                carryOverList_new.append(carryOverList_old[pos]+"_"+"bwa.sam")
        
    if params.reads == "pairedEnd":
        for referenceBWA in params.fastaList:
            referenceBWA_shortName = getFastaName(referenceBWA)
            for pos in range(len(fileArrayPE)): # add every 2nd one
                if pos % 2 <> 0:
                    #samFileList.append(carryOverList_old[pos]+"_"+"trim_bwa.sam")
##                    carryOverList_new.append(carryOverList_old[pos]+"_"+referenceBWA_shortName+"_"+"trim_bwa.sam")
                    carryOverList_new.append(carryOverList_old[pos]+"_"+"bwa.sam")
     
    if params.reads == "mixed": # add both
        for referenceBWA in params.fastaList:
            referenceBWA_shortName = getFastaName(referenceBWA)
            for pos in range(len(fileArraySE)):
##                carryOverList_new.append(carryOverList_old[pos]+"_"+referenceBWA_shortName+"_"+"trim_bwa.sam")
                carryOverList_new.append(carryOverList_old[pos]+"_"+"bwa.sam")
            for pos in range(len(fileArrayPE)):
                if pos % 2 <> 0:
##                    carryOverList_new.append(carryOverList_old[pos+len(fileArraySE)]+"_"+referenceBWA_shortName+"_"+"trim_bwa.sam")
                    carryOverList_new.append(carryOverList_old[pos+len(fileArraySE)]+"_"+"bwa.sam")


    os.chdir(params.scripts_BWA)
    picard = "3_picardValidate.sh"
##    picard_Cleanup = "3_picardValidate_cleanup.sh"
    f = open(picard,'w')
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    for x in carryOverList_old:
        f.write(params.java7+" -jar "+params.picardDirOnPc+" I="+params.BWAAligned_aln+x+" O="+params.BWAAligned+picardReport+x[0:len(x)-4]+"_validateReport.txt")
        f.write('\n')
    #print "picard validation sh file created as picardValidate.sh"
    f.close()
    ############################################3
    
    #This part creates the sam to bam .sh file
         
    os.chdir(params.scripts_BWA)
    samToBam = "4_createSamToBam.sh"
    samToBam_cleanup = "4_createSamToBam_cleanup.sh"
    carryOverList_new = []
    f = open(samToBam,'w')
    f2 = open(samToBam_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        f.write(params.samtools+" view -Sb "+params.BWAAligned_aln+x+" | "+params.samtools+" sort - --threads "+str(params.coreSplit[0])+" -o "+params.BWAAligned_aln+x[:(len(x)-4)]+"_sorted.bam")
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+"_sorted.bam\n")
                 
        carryOverList_new.append(x[:(len(x)-4)]+"_sorted.bam")
    #print "sam to bam .sh file created as createSamToBam.sh"
    f.close()
    f2.close()

    #This part creates the indexing of the bam .sh file
    carryOverList_new = []    
    os.chdir(params.scripts_BWA)
    index = "5_indexBam.sh"
    index_cleanup = "5_indexBam_cleanup.sh"
    f = open(index,'w')
    f2 = open(index_cleanup,'w')
    for x in carryOverList_old:    #samFileList:
        f.write(params.samtools+" index "+params.BWAAligned_aln+x[:(len(x)-4)]+"_sorted.bam")
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+"_sorted.bam.bai\n")
        carryOverList_new.append(x[:(len(x)-4)]+"_sorted"+".bam")
    #print "bam indexing sh file created as indexBam.sh"
    f.close()


    #getMappedReads
    os.chdir(params.scripts_BWA)
    getMappedReads = "13_getMappedReads.sh"

    f = open(getMappedReads,'w')
    for x in carryOverList_new:    #samFileList:
        #print x[:(len(x)-11)]+"_realigned_resorted_dedup.bam"
        f.write(params.samtools+" flagstat "+params.BWAAligned_aln+x[:(len(x)-11)]+"_realigned_resorted_dedup.bam > "+params.BWAAligned_aln+x[:(len(x)-11)]+"_realigned_resorted_dedup_samtools_stats.txt")
        f.write('\n')
    #print "samtools flagstat .sh file created as getMappedReads.sh "
    f.close()

 #########################
    #This creates the GATK sh files
    
    GATK = "6_1_GATK.sh"
    GATK2 = "6_2_GATK.sh"

    GATK_cleanup = "6_1_GATK_cleanup.sh"
    GATK2_cleanup = "6_2_GATK_cleanup.sh"                 

    carryOverList_old = carryOverList_new
    carryOverList_new = []

    #ADD THIS FEATURE: Note - if there is a problem then the program can also run with the extra parameter "-fixMisencodedQuals" which subtracts 31 from the qualities
    # Thus run the program below, if the output file is not generated, then run with this additional parameter.
##    referenceBWA = loadReferenceFasta(params.bwaRef)
    referenceBWA = ""
    os.chdir(params.scripts_BWA)           
    f = open(GATK,'w')
    f2 = open(GATK2,'w')
    f3 = open(GATK_cleanup,'w')
    f4 = open(GATK2_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break
            referenceBWA = ref
        if referenceBWA == "":
            print "FATAL ERROR, could not match any reference to the filename!"
            raw_input("press enter to exit")
            exit(0)
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T RealignerTargetCreator -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned_aln+x[:(len(x)-4)]+".intervals")
        f.write('\n')
        f3.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+".intervals\n")
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T RealignerTargetCreator -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned_aln+x[:(len(x)-4)]+".intervals")
##        f2.write('\n')
        f4.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+".intervals"+"\n")
                 
        carryOverList_new.append(x[:(len(x)-4)]+".intervals") #This is the interval file, not the main bam file, so keep both old and new lists
    #print "GATK intervals sh file created as GATK.sh"
    f.close()
    f2.close()
    f3.close()
    f4.close()
    '''
    if samArray == []:
        if params.recal == True: 
            os.chdir(params.BWAAligned_aln)
            baseRecalArray = []   
            for fileX in glob.glob("*_bwa_sorted_realigned_recal.bam"):
                baseRecalArray.append(fileX)
            os.chdir(params.scripts_BWA)           
            f = open(GATK,'w')
            for x in baseRecalArray:
                f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T RealignerTargetCreator -R "+params.bwaRef+referenceNOVO+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned_aln+x[:(len(x)-4)]+"_sorted.intervals")
                f.write('\n')
            f.close()
     '''       

    ########################3
    #This creates the realignment sh file
    os.chdir(params.scripts_BWA)
    Realignment = "7_1_Realignment.sh"
    Realignment2 = "7_2_Realignment.sh"

    Realignment_cleanup = "7_1_Realignment_cleanup.sh"
    Realignment2_cleanup = "7_2_Realignment_cleanup.sh"
    temp = []     
    f = open(Realignment,'w')
    f2 = open(Realignment2,'w')
    f3 = open(Realignment_cleanup,'w')
    f4 =  open(Realignment2_cleanup,'w')
    for pos in range(len(carryOverList_old)): #samFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in carryOverList_old[pos]:
                referenceBWA = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T IndelRealigner -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+carryOverList_old[pos]+" -o "+params.BWAAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam -targetIntervals "+params.BWAAligned_aln+carryOverList_new[pos])
        f.write('\n')
        f3.write("rm "+params.BWAAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam\n")
        f3.write("rm "+params.BWAAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bai\n")
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T IndelRealigner -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+carryOverList_old[pos]+" -o "+params.BWAAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam -targetIntervals "+params.BWAAligned_aln+carryOverList_new[pos])
##        f2.write('\n')
        f4.write("rm "+params.BWAAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam\n")
        temp.append(carryOverList_old[pos][:len(carryOverList_old[pos])-4]+"_realigned.bam")        
    #print "GATK realignment sh file created as Realignment.sh"
    f.close()
    f2.close()
    f3.close()
    f4.close()
    carryOverList_new = temp
    
    ########################3
    #This creates the base quality recalibration table
    #AND creates the base qualitry recal step script, this 2 steps in one script
    #creating temp bam array to save on space:
    if params.BQSRPossible:
        os.chdir(params.scripts_BWA)
        carryOverList_old = carryOverList_new
        carryOverList_new = []
        f1 = open("8.1_baseQualRecalBWA.sh",'w')
        f2 = open("8.2_baseQualRecalBWA.sh",'w')
        f3 = open("8.1_baseQualRecalBWA_cleanup.sh",'w')
        f4 = open("8.2_baseQualRecalBWA_cleanup.sh",'w')
        for x in carryOverList_old: #bAmFileList:
            for ref in params.fastaList:
                referenceBWA_shortName = getFastaName(ref)
                if referenceBWA_shortName in x:
                    referenceBWA = ref
                    break
                referenceBWA = ref
            f1.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T BaseRecalibrator -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -knownSites "+params.dbSNP+"dbSNP.vcf -o "+params.BWAAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T PrintReads -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -BQSR "+params.BWAAligned_aln+x[:len(x)-20]+"recal_data.table -o "+params.BWAAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            f3.write("rm "+params.BWAAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f4.write("rm "+params.BWAAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            f4.write("rm "+params.BWAAligned_aln+x[:len(x)-20]+"realigned_recal.bai\n")
            carryOverList_new.append(x[:(len(x)-20)]+"realigned_recal.bam")
        #print "picard sort sh file created as picardSort.sh"
        f1.close()
        f2.close()
        f3.close()
        f4.close()        
    else:
        print "Skipping Base quality score recalibration due to missing dbSNP file"

    ########################
    #This creates the picard sort sh file
    #depends on sam array
    # creating temp bam array to save on space:
    os.chdir(params.scripts_BWA)
    picardSort = "9_picardSort.sh"
    picardSort_cleanup = "9_picardSort_cleanup.sh"
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    
    f = open(picardSort,'w')
    f2 = open(picardSort_cleanup,'w')
    if params.BQSRPossible:
        amount = 20
    else:
        amount = 21
    for x in carryOverList_old: #samFileList:          
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.SortSamDir+" I="+params.BWAAligned_aln+x+" O="
        +params.BWAAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT")
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam\n")
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bai\n")
        carryOverList_new.append(x[:(len(x)-amount)]+"_realigned_resorted.bam")
    #print "picard sort sh file created as picardSort.sh"
    f.close()
    f2.close()


    ########################3
    #This creates the RE-indexing of the bam files sh file
    os.chdir(params.scripts_BWA)
    reIndexBamFiles = "10_reIndexBamFiles.sh"
    reIndexBamFiles_cleanup = "10_reIndexBamFiles_cleanup.sh"
    carryOverList_old = carryOverList_new
    carryOverList_new = []
     
    f = open(reIndexBamFiles,'w')
    f2 = open(reIndexBamFiles_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        f.write(params.samtools+" index "+params.BWAAligned_aln+x)               
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x+".bai\n")
    #print "re-Index of bam files sh writen to reIndexBamFiles.sh"
    f.close()
    f2.close()

    ########################3
    #This creates the remove PCR duplicates sh file
    os.chdir(params.scripts_BWA)
    removePCRDuplicates = "11_removePCRDuplicates.sh"
    removePCRDuplicates_cleanup = "11_removePCRDuplicates_cleanup.sh" 
    f = open(removePCRDuplicates,'w')
    f2 = open(removePCRDuplicates_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        f.write(params.java7+" -jar "+params.markDuplicates+" I="+params.BWAAligned_aln+x+" O="+params.BWAAligned_aln+x[:(len(x)-4)]+"_dedup.bam VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE M=duplicate_metrics TMP_DIR=tmp ASSUME_SORTED=true > "+params.BWAAligned_aln+x[:(len(x)-4)]+"_rmdup.log")
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+"_dedup.bam\n")
    #print "picard remove pcr duplicates sh writen to removePCRDuplicates.sh"
    f.close()
    f2.close()
    
    ########################3
    #This creates the RE-indexing of the bam files sh file a 1nd time after the removal of pcr duplicates as in previous step
    os.chdir(params.scripts_BWA)
    reIndexBamFiles2 = "12_reIndexBamFiles2.sh"
    reIndexBamFiles2_cleanup = "12_reIndexBamFiles2_cleanup.sh"
    carryOverList_new = []     
    f = open(reIndexBamFiles2,'w')
    f2 = open(reIndexBamFiles2_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        f.write(params.samtools+" index "+params.BWAAligned_aln+x[:(len(x)-4)]+"_dedup.bam")              
        f.write('\n')
        f2.write("rm "+params.BWAAligned_aln+x[:(len(x)-4)]+"_dedup.bam\n")
        carryOverList_new.append(x[:(len(x)-4)]+"_dedup.bam")
    #print "re-Index (FOR SECOND TIME) of bam files sh writen to reIndexBamFiles2.sh"
    f.close()
    f2.close()

    ########################3
    #This creates the UNIFIED GENOTYPER SNP calling sh file using GATK
    
    os.chdir(params.scripts_BWA)
    snpCalling = "14_SNPCallingGATK.sh"
    carryOverList_old = carryOverList_new
     
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned+snpDir+x[:-38]+"_gatk_snps.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.BWAAligned+snpDir+x[:-38]+"_Genotype.log")  
        f.write('\n')
##    print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    ########################3
    #This creates the UNIFIED GENOTYPER INDEL calling sh file using GATK
    '''
    os.chdir(params.scripts_BWA)
    indelCalling = "INDELCallingGATK.sh"
     
    f = open(indelCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO --genotype_likelihoods_model INDEL -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned+indelDir+x[:-38]+"_gatk_indels.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.BWAAligned+indelDir+x[:-38]+"_Indel_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to INDELCallingGATK.sh"
    f.close()
    '''
    ########################3
    #This creates the SNP CALLER sh file using SAMTOOLS

    os.chdir(params.scripts_BWA)
    snpCalling = "14_2_VARIANT_CALLING_SAMTOOLS.sh"
     
    f = open(snpCalling,'w')
    coreCount = 0
    waitFlag = False
    for x in carryOverList_old: #bamFileList:
        coreCount += 1
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break        
        if coreCount < max(params.coreSplit):
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceBWA+" "+params.BWAAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.BWAAligned+snpDir+x[:-33]+"_VARIANTS_SAMTOOLS.vcf &\n")
            waitFlag = False        
        else:
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceBWA+" "+params.BWAAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.BWAAligned+snpDir+x[:-33]+"_VARIANTS_SAMTOOLS.vcf &\n")
            f.write("wait\n")
            waitFlag = True
            coreCount =  0
    if not waitFlag:
        f.write("wait\n")
    f.close()
    
    ########################3
    #This creates the SNP HAPLOTYPE CALLER sh file using GATK


    os.chdir(params.scripts_BWA)
    snpCalling = "14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh"
     
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T HaplotypeCaller -R "+params.reference+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned+snpDir+x[:-33]+"_gatk_HC_snps.vcf -stand_call_conf 30 -stand_emit_conf 10.0 > "+params.BWAAligned+snpDir+x[:-33]+"_gatk_HC_snps.log")  
        #f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T HaplotypeCaller -nct "+str(coreSplit[0])+" -R "+params.bwaRef+referenceBWA+" -I "+params.BWAAligned_aln+x+" -o "+params.BWAAligned_aln+snpDir+x[:-38]+"_gatk_HC_snps.vcf -stand_call_conf 30 -stand_emit_conf 10.0 > "+params.BWAAligned+snpDir+x[:-38]+"_SNPHC_Genotype.log")  
        f.write('\n')
##    print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    #########################3
    ##This creates the genome coverage gatk sh file
    #os.chdir(params.scripts_BWA)
    #GenomeCoverage = "15_GenomeCoverage.sh"
    #GenomeCoverage_cleanup = "15_GenomeCoverage_cleanup.sh"
    #f = open(GenomeCoverage,'w')
    #f2 = open(GenomeCoverage_cleanup,'w')
    #for x in carryOverList_old: #bamFileList:
    #    for ref in params.fastaList:
    #        referenceBWA_shortName = getFastaName(ref)
    #        if referenceBWA_shortName in x:
    #            referenceBWA = ref
    #            break
    #    f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T DepthOfCoverage -R "+params.reference+referenceBWA+" -o "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt -I "+params.BWAAligned_aln+x)#+" -nt"+str(coreSplit[0]))
    #    f.write('\n')
    #    f2.write("rm "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt\n")
    ##print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    #f.close()
    #f2.close()
    
    ########################3
    #This creates the genome coverage bedtools sh file
    os.chdir(params.scripts_BWA)
    GenomeCoverage = "15_2_GenomeCoverage.sh"
    GenomeCoverage_cleanup = "15_2_GenomeCoverage_cleanup.sh"
    f = open(GenomeCoverage,'w')
    f2 = open(GenomeCoverage_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceBWA_shortName = getFastaName(ref)
            if referenceBWA_shortName in x:
                referenceBWA = ref
                break
        f.write(params.bedtools+" -bga -ibam "+params.BWAAligned_aln+x+" -g "+params.reference+referenceBWA+" > "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt\n") 
        f2.write("rm "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt\n")
    #print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    f.close()
    f2.close()

 ########################3
    #This creates the regions with zero coverage sh file
    os.chdir(params.scripts_BWA)
    ZeroCov = "16_ZeroCov.sh"
    ZeroCov_cleanup = "16_ZeroCov_cleanup.sh"
     
    f = open(ZeroCov,'w')
    f2 = open(ZeroCov_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        f.write("awk 'NF && $4<2' "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt > "+params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt")
##        f.write("grep -w 0$ "+params.BWAAligned+genomeCovDir+x[:(len(x)-38)]+"_genomecov.txt > "+params.BWAAligned+genomeCovDir+x[:(len(x)-38)]+"_genomecov=0.txt")
##        f.write("grep -w 0$ "+fileX[:-4]+"_gen_cov.txt > "+fileX[:-4]+"_gen_0-cov.txt\n")               
        f.write('\n')
        f2.write(params.BWAAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt\n")
    #print "zero coverage sh file written as ZeroCov.sh"
    f.close()
    f2.close()
    return

#############################################-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#scripts creation
def variantScriptsNOVO(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE)
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) 
    '''
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE
    if params.reads == "singleEnd":
        #fileArray , trimArray , ID, SM  = GenerateCleanFileNamesSEMode(params.trimmedFastQ)
        fileArray = trimmedFilesSE
##        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
    if params.reads == "pairedEnd":
        #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)
        fileArray = trimmedFilesPE
##        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    if params.reads == "mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
##        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE

    carryOverList_old = ID
    carryOverList_new = []
##########################################
    #this part creates the picard .sh file 

    os.chdir(params.NOVOAligned_aln)
    if params.reads == "singleEnd":
        for referenceNOVO in params.fastaList:
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            for pos in range(len(fileArraySE)): #Add all
##                carryOverList_new.append(carryOverList_old[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_novo.sam")
            
    if params.reads == "pairedEnds":
        for referenceNOVO in params.fastaList:
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            for pos in range(len(fileArrayPE)): # add every 2nd one
                if pos % 2 <> 0:
                    #samFileList.append(carryOverList_old[pos]+"_"+"trim_bwa.sam")
##                    carryOverList_new.append(carryOverList_old[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                    carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_novo.sam")
         
    if params.reads == "mixed": # add both
        for referenceNOVO in params.fastaList:
            referenceNOVO_shortName = getFastaName(referenceNOVO)
            for pos in range(len(fileArraySE)):
##                carryOverList_new.append(carryOverList_old[pos]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_novo.sam")
            for pos in range(len(fileArrayPE)):
                if pos % 2 <> 0:
##                    carryOverList_new.append(carryOverList_old[pos+len(fileArraySE)]+"_"+referenceNOVO_shortName+"_"+"trim_novo.sam")
                    carryOverList_new.append(carryOverList_old[pos+len(fileArraySE)]+"_"+"trim_novo.sam")
                
    os.chdir(params.scripts_NOVO)
    picard = "2_picardValidate.sh"
##    picard_cleanup = "2_picardValidate_cleanup.sh"
    f = open(picard,'w')
##    f2 = open(picard_cleanup,'w')
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    pos = 0
    for x in carryOverList_old: #while pos <= len(carryOverList_old)-1:
        f.write(params.java7+" -jar "+params.picardDirOnPc+" I="+params.NOVOAligned_aln+x+" O="+params.NOVOAligned+picardReport+x[0:len(x)-4]+"_validateReport.txt")
        f.write('\n')
##        f2.write()
        pos += 1
    #print "picard validation sh file created as picardValidate.sh"
    f.close()
    ############################################3
    
    #This part creates the sam to bam .sh file
       
    os.chdir(params.scripts_NOVO)
    samToBam = "3_createSamToBam.sh"
    samToBam_cleanup = "3_createSamToBam_cleanup.sh"
    f = open(samToBam,'w')
    f2 = open(samToBam_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        f.write(params.samtools+" view -Sb "+params.NOVOAligned_aln+x+" | "+params.samtools+" sort - --threads "+str(params.coreSplit[1])+" -o "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_sorted.bam")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_sorted.bam\n")
    #print "sam to bam .sh file created as createSamToBam.sh"
    f.close()

    #This part creates the indexing of the bam .sh file
        
    os.chdir(params.scripts_NOVO)
    index = "4_indexBam.sh"
    index_cleanup = "4_indexBam_cleanup.sh"
    f = open(index,'w')
    f2 = open(index_cleanup,'w')
    for x in carryOverList_old:    #samFileList:
        f.write(params.samtools+" index "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_sorted"+".bam")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_sorted"+".bam.bai")
        carryOverList_new.append(x[:(len(x)-4)]+"_sorted.bam")
    #print "bam indexing sh file created as indexBam.sh"
    f.close()
    f2.close()


    #getMappedReads
    #depends on samArray created above
    os.chdir(params.scripts_NOVO)
    getMappedReads = "12_getMappedReads.sh"
    f = open(getMappedReads,'w')
    for x in carryOverList_old:    #samFileList:
        f.write(params.samtools+" flagstat "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_realigned_resorted_dedup.bam > "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_realigned_resorted_dedup_samtools_stats.txt")
        f.write('\n')
    #print "samtools flagstat .sh file created as getMappedReads.sh "
    f.close()

 #########################
    #This creates the GATK sh files
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    GATK = "5_1_GATK.sh"
    GATK2 = "5_2_GATK.sh"
    GATK_cleanup = "5_1_GATK_cleanup.sh"
##    GATK2_cleanup = "5_2_GATK_cleanup.sh"
    
##    referenceNOVO = loadReferenceFasta(params.refNovo)
    os.chdir(params.scripts_NOVO)
    f = open(GATK,'w')
    f2 = open(GATK2,'w')

    f3 = open(GATK_cleanup,'w')
##    f4 = open(GATK2_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T RealignerTargetCreator -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -o "+params.NOVOAligned_aln+x[:(len(x)-4)]+".intervals")
        f.write('\n')
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T RealignerTargetCreator -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -o "+params.NOVOAligned_aln+x[:(len(x)-4)]+".intervals")
##        f2.write('\n')
        carryOverList_new.append(x[:(len(x)-4)]+".intervals") #This is the interval file, not the main bam file, so keep both old and new lists

        f3.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+".intervals\n")
##        f4.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+".intervals\n")
    #print "GATK intervals sh file created as GATK.sh"
    
    f.close()
    f2.close()
    f3.close()
    
    ########################3
    #This creates the realignment sh file
    temp = []  
    os.chdir(params.scripts_NOVO)
    Realignment = "6_1_Realignment.sh"
    Realignment2 = "6_2_Realignment.sh"
    Realignment_cleanup = "6_x_Realignment_cleanup.sh"
    f = open(Realignment,'w')
    f2 = open(Realignment2,'w')
    f3 = open(Realignment_cleanup,'w')
    for pos in range(len(carryOverList_old)): #samFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in carryOverList_old[pos]:
                referenceNOVO = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T IndelRealigner -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+carryOverList_old[pos]+" -o "+params.NOVOAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam"+" -targetIntervals "+params.NOVOAligned_aln+carryOverList_new[pos])
        f.write('\n')
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T IndelRealigner -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+carryOverList_old[pos]+" -o "+params.NOVOAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam"+" -targetIntervals "+params.NOVOAligned_aln+carryOverList_new[pos])
##        f2.write('\n')
        f3.write("rm "+params.NOVOAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam\n")
        f3.write("rm "+params.NOVOAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bai\n")
        temp.append(carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam")
    #print "GATK realignment sh file created as Realignment.sh"
    f.close()
    f2.close()
    f3.close()
    carryOverList_new = temp
    
    ########################3
    #This creates the base quality recalibration sh file
    #creating temp bam array to save on space:
    if params.BQSRPossible:
        os.chdir(params.scripts_NOVO)
        carryOverList_old = carryOverList_new
        carryOverList_new = []
        f1 = open("7.1_baseQualRecalNOVO.sh",'w')
        f2 = open("7.2_baseQualRecalNOVO.sh",'w')
        f3 = open("7.1_baseQualRecalNOVO_cleanup.sh",'w')
        f4 = open("7.2_baseQualRecalNOVO_cleanup.sh",'w')
        for x in carryOverList_old: 
            for ref in params.fastaList:
                referenceNOVO_shortName = getFastaName(ref)
                if referenceNOVO_shortName in x:
                    referenceNOVO = ref
                    break
                referenceNOVO = ref
            f1.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T BaseRecalibrator -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -knownSites "+params.dbSNP+"dbSNP.vcf -o "+params.NOVOAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T PrintReads -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -BQSR "+params.NOVOAligned_aln+x[:len(x)-20]+"recal_data.table -o "+params.NOVOAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            carryOverList_new.append(x[:(len(x)-20)]+"realigned_recal.bam")
            f3.write("rm "+params.NOVOAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f4.write("rm "+params.NOVOAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            f4.write("rm "+params.NOVOAligned_aln+x[:len(x)-20]+"realigned_recal.bai\n")
        #print "picard sort sh file created as picardSort.sh"
        f1.close()
        f2.close()
        f3.close()
        f4.close()
    else:
        print "Skipping Base quality score recalibration due to missing dbSNP file"

    ########################3
    #This creates the picard sort sh file
    #depends on sam array
    # creating temp bam array to save on space:

    os.chdir(params.scripts_NOVO)
    picardSort = "8_picardSort.sh"
    picardSort_cleanup = "8_picardSort_cleanup.sh"
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    
    if BQSRPossible:
        amount = 20
    else:
        amount = 21
    f = open(picardSort,'w')
    f2 = open(picardSort_cleanup,'w')
    for x in carryOverList_old: #samFileList:            
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.SortSamDir+" I="+params.NOVOAligned_aln+x+" O="
        +params.NOVOAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam\n")
##        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-20)]+"_realigned_resorted.bam.bai\n")
        carryOverList_new.append(x[:(len(x)-amount)]+"_realigned_resorted.bam")
    #print "picard sort sh file created as picardSort.sh"
    f.close()
    f2.close()


    ########################3
    #This creates the RE-indexing of the bam files sh file
    os.chdir(params.scripts_NOVO)
    reIndexBamFiles = "9_reIndexBamFiles.sh"
    reIndexBamFiles_cleanup = "9_reIndexBamFiles_cleanup.sh"
    carryOverList_old = carryOverList_new
    carryOverList_new = []  
    f = open(reIndexBamFiles,'w')
    f2= open(reIndexBamFiles_cleanup,'w')

    for x in carryOverList_old: #bamFileList:
        f.write(params.samtools+" index "+params.NOVOAligned_aln+x)               
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x+".bai\n")
    #print "re-Index of bam files sh writen to reIndexBamFiles.sh"
    f.close()
    f2.close()

    ########################3
    #This creates the remove PCR duplicates sh file
    os.chdir(params.scripts_NOVO)
    removePCRDuplicates = "10_removePCRDuplicates.sh"
    removePCRDuplicates_cleanup = "10_removePCRDuplicates_cleanup.sh"
     
    f = open(removePCRDuplicates,'w')
    f2 = open(removePCRDuplicates_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        f.write(params.java7+" -jar "+params.markDuplicates+" I="+params.NOVOAligned_aln+x+" O="+params.NOVOAligned_aln+x[:(len(x)-4)]+"_dedup.bam VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE M=duplicate_metrics TMP_DIR=tmp ASSUME_SORTED=true > "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_rmdup.log")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_dedup.bam\n")
    #print "picard remove pcr duplicates sh writen to removePCRDuplicates.sh"
    f.close()
    f2.close()
  
    ########################3
    #This creates the RE-indexing of the bam files sh file a 1nd time after the removal of pcr duplicates as in previous step
    os.chdir(params.scripts_NOVO)
    reIndexBamFiles2 = "11_reIndexBamFiles2.sh"
    reIndexBamFiles2_cleanup = "11_reIndexBamFiles2_cleanup.sh"
    carryOverList_new = [] 
    f = open(reIndexBamFiles2,'w')
    f2 = open(reIndexBamFiles2_cleanup,'w')
    
    for x in carryOverList_old: #bamFileList:
        f.write(params.samtools+" index "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_dedup.bam")              
        f.write('\n')
        f2.write("rm "+params.NOVOAligned_aln+x[:(len(x)-4)]+"_dedup.bai\n")
        carryOverList_new.append(x[:(len(x)-4)]+"_dedup.bam")
    #print "re-Index (FOR SECOND TIME) of bam files sh writen to reIndexBamFiles2.sh"
    f.close()
    f2.close()

    ########################3
    #This creates the SNP calling sh file using GATK
    os.chdir(params.scripts_NOVO)
    snpCalling = "SNPCallingGATK.sh"
    carryOverList_old = carryOverList_new
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -o "+params.NOVOAligned+snpDir+x[:-39]+"_gatk_snps.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.NOVOAligned+snpDir+x[:-39]+"_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    ########################3
    #This creates the INDEL calling sh file using GATK
    '''
    os.chdir(params.scripts_NOVO)
    indelCalling = "INDELCallingGATK.sh"
     
    f = open(indelCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO --genotype_likelihoods_model INDEL -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -o "+params.NOVOAligned+indelDir+x[:-39]+"_gatk_indels.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.NOVOAligned+indelDir+x[:-39]+"_Indel_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to INDELCallingGATK.sh"
    f.close()
    '''
    
    
    ########################3
    #This creates the SNP HAPLOTYPE CALLER sh file using GATK
    os.chdir(params.scripts_NOVO)
    snpCalling = "13_2_VARIANT_CALLING_SAMTOOLS.sh"
     
    f = open(snpCalling,'w')
    coreCount = 0
    waitFlag = False
    for x in carryOverList_old: #bamFileList:
        coreCount += 1
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break   
        if coreCount < max(params.coreSplit):         
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceNOVO+" "+params.NOVOAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.NOVOAligned+snpDir+x[:-4]+"_VARIANTS_SAMTOOLS.vcf &\n")
            waitFlag = False
        else:   
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceNOVO+" "+params.NOVOAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.NOVOAligned+snpDir+x[:-4]+"_VARIANTS_SAMTOOLS.vcf &\n")
            f.write("wait\n")
            waitFlag = True
            coreCount =  0
    if not waitFlag:
        f.write("wait\n")
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()
        
    ########################3
    #This creates the SNP HAPLOTYPE CALLER sh file using GATK
    os.chdir(params.scripts_NOVO)
    snpCalling = "13_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh"
     
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T HaplotypeCaller -nct "+str(params.coreSplit[1])+" -R "+params.reference+referenceNOVO+" -I "+params.NOVOAligned_aln+x+" -o "+params.NOVOAligned+snpDir+x[:-4]+"_gatk_HC_snps.vcf -stand_call_conf 30 -stand_emit_conf 10.0 > "+params.NOVOAligned+snpDir+x[:-4]+"_SNPHC_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    #########################3
    ##This creates the genome coverage bed tools sh file
    #os.chdir(params.scripts_NOVO)
    #GenomeCoverage = "14_GenomeCoverage.sh"
    #GenomeCoverage_cleanup = "14_GenomeCoverage_cleanup.sh"
    # 
    #f = open(GenomeCoverage,'w')
    #f2 = open(GenomeCoverage_cleanup,'w')
    #for x in carryOverList_old: #bamFileList:
    #    for ref in params.fastaList:
    #        referenceNOVO_shortName = getFastaName(ref)
    #        if referenceNOVO_shortName in x:
    #            referenceNOVO = ref
    #            break
    #    f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T DepthOfCoverage -R "+params.reference+referenceNOVO+" -o "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt -I "+params.NOVOAligned_aln+x) #+" -nt "+str(coreSplit[0]))
    #    f.write('\n')
    #    f2.write("rm "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt\n")
    ##print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    #f.close()
    #f2.close()
    
    ########################3
    #This creates the genome coverage bed tools sh file
    
    os.chdir(params.scripts_NOVO)
    GenomeCoverage = "14_2_GenomeCoverage.sh"
    GenomeCoverage_cleanup = "14_2_GenomeCoverage_cleanup.sh"
     
    f = open(GenomeCoverage,'w')
    f2 = open(GenomeCoverage_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceNOVO_shortName = getFastaName(ref)
            if referenceNOVO_shortName in x:
                referenceNOVO = ref
                break
        f.write(params.bedtools+" -bga -ibam "+params.NOVOAligned_aln+x+" -g "+params.reference+referenceNOVO+" > "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt\n")
    #print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    f.close()
    f2.close()
    

 ########################3
    #This creates the regions with zero coverage sh file
    os.chdir(params.scripts_NOVO)
    ZeroCov = "15_ZeroCov.sh"
    ZeroCov_cleanup = "15_ZeroCov_cleanup.sh"
     
    f = open(ZeroCov,'w')
    f2 = open(ZeroCov_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        #f.write("grep -w 0$ "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt > "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt") 
        f.write("awk 'NF && $4<2' "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt > "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt")
        f.write('\n')
        f2.write("rm "+params.NOVOAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt\n")
    #print "zero coverage sh file written as ZeroCov.sh"
    f.close()
    f2.close()
    return

#############################################-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#scripts creation
def variantScriptsSMALT(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE):
    '''
    cleanedUpFileData = partitionFastQList(params.trimmedFastQ)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #change dirX to params.trimmedFastQ
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE) 
    '''
    fileArraySE = trimmedFilesSE
    fileArrayPE = trimmedFilesPE
    if params.reads == "singleEnd":
        #fileArray , trimArray , ID, SM  = GenerateCleanFileNamesSEMode(params.trimmedFastQ)
        fileArray = trimmedFilesSE
##        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
    if params.reads == "pairedEnd":
        #fileArray , trimArray , ID, SM = GenerateCleanFileNames(params.trimmedFastQ)
        fileArray = trimmedFilesPE
##        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    if params.reads == "mixed":
        fileArray = trimmedFilesSE+trimmedFilesPE
##        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE

    carryOverList_old = ID
    carryOverList_new = []
##########################################
    #this part creates the picard .sh file 

    os.chdir(params.SMALTAligned_aln)
    
    if params.reads == "singleEnd":
        for pos in range(len(fileArraySE)): #Add all
            carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_smalt_sort_RG.sam")
        
    if params.reads == "pairedEnd":
        for pos in range(len(fileArrayPE)): # add every 2nd one
            if pos % 2 <> 0:
                #samFileList.append(carryOverList_old[pos]+"_"+"trim_bwa.sam")
                carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_smalt_sort_RG.sam")
     
    if params.reads == "mixed": # add both
        for pos in range(len(fileArraySE)):
            carryOverList_new.append(carryOverList_old[pos]+"_"+"trim_smalt_sort_RG.sam")
        for pos in range(len(fileArrayPE)):
            if pos % 2 <> 0:
                carryOverList_new.append(carryOverList_old[pos+len(fileArraySE)]+"_"+"trim_smalt_sort_RG.sam")
                
    os.chdir(params.scripts_SMALT)
    picard = "4_picardValidate.sh"
##    picard_cleanup = "4_picardValidate_cleanup.sh"
    f = open(picard,'w')
##    f2 = open(picard_cleanup,'w')
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    pos = 0
    for x in carryOverList_old:#while pos <= len(carryOverList_old)-1:
        #f.write("java -jar "+params.picardDirOnPc+" I="+params.SMALTAligned_aln+samFileList[pos]+" O="+params.SMALTAligned+picardReport+samFileList[pos][0:len(samFileList[pos])-4]+"_validateReport.txt")
        f.write(params.java7+" -jar "+params.picardDirOnPc+" I="+params.SMALTAligned_aln+x+" O="+params.SMALTAligned+picardReport+x[0:len(x)-4]+"_validateReport.txt")
        #carryOverList_new.append(#Nothing because this is just a report which is not used again in pipeline)
        f.write('\n')
##        f2.write()
        pos +=1
    #print "picard validation sh file created as picardValidate.sh"
    f.close()
    ############################################3
    
    #This part creates the sam to bam .sh file
##    samArray = samFileList
         
    os.chdir(params.scripts_SMALT)
    samToBam = "5_createSamToBam.sh"
    samToBam_cleanup = "5_createSamToBam_cleanup.sh"
    f = open(samToBam,'w')
    f2 = open(samToBam_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        f.write(params.samtools+" view -Sb "+params.SMALTAligned_aln+x+" | "+params.samtools+" sort - --threads "+str(params.coreSplit[2])+" -o "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.bam")
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.bam\n")
        
    #print "sam to bam .sh file created as createSamToBam.sh"
    f.close()
    f2.close()

    #This part creates the indexing of the bam .sh file       
    os.chdir(params.scripts_SMALT)
    index = "6_indexBam.sh"
    index_cleanup = "6_indexBam_cleanup.sh"
    f = open(index,'w')
    f2 = open(index_cleanup,'w')
    for x in carryOverList_old:    #samFileList:
        f.write(params.samtools+" index "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.bam")
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.bam.bai\n")
        carryOverList_new.append(x[:(len(x)-4)]+"_sorted.bam")
    #print "bam indexing sh file created as indexBam.sh"
    f.close()
    f2.close()

    #getMappedReads
    #depends on samArray created above
    carryOverList_old = carryOverList_new
    #carryOverList_new = []
    os.chdir(params.scripts_SMALT)
    getMappedReads = "14_getMappedReads.sh"
    f = open(getMappedReads,'w')
##    getMappedReads_cleanup = "14_getMappedReads_cleanup .sh"
##    f2 = open(getMappedReads_cleanup ,'w')
    for x in carryOverList_old:    #samFileList:
        #f.write("samtools flagstat "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.bam > "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_samtools_stats.txt")
        f.write(params.samtools+" flagstat "+params.SMALTAligned_aln+x[:(len(x)-11)]+"_realigned_resorted_dedup.bam > "+params.SMALTAligned_aln+x[:(len(x)-11)]+"_realigned_resorted_dedup_samtools_stats.txt")
        f.write('\n')

        #Dont append to new list, only output is report file
    #print "samtools flagstat .sh file created as getMappedReads.sh "
    f.close()

 #########################
    #This creates the GATK sh files
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    GATK = "7_1_GATK.sh"
    GATK2 = "7_2_GATK.sh"
    GATK_cleanup = "7_x_GATK_cleanup.sh"
##    referenceNOVO = loadReferenceFasta(params.smaltRef)
    os.chdir(params.scripts_SMALT)           
    f = open(GATK,'w')
    f2 = open(GATK2,'w')
    f3 = open(GATK_cleanup,'w')
    for x in carryOverList_old:   #samFileList:
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in x:
                referenceSMALT = ref
                break
            referenceSMALT = ref
##        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T RealignerTargetCreator -R "+params.smaltRef+referenceNOVO+" -I "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted"+".bam -o "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_sorted.intervals")
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T RealignerTargetCreator -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -o "+params.SMALTAligned_aln+x[:(len(x)-4)]+".intervals")
        f.write('\n')
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T RealignerTargetCreator -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -o "+params.SMALTAligned_aln+x[:(len(x)-4)]+".intervals")
##        f2.write('\n')
        f3.write("rm "+params.SMALTAligned_aln+x[:(len(x)-4)]+".intervals\n")
        carryOverList_new.append(x[:(len(x)-4)]+".intervals") #This is the interval file, not the main bam file, so keep both old and new lists
    #print "GATK intervals sh file created as GATK.sh"

    f.close()
    f2.close()
    f3.close()
    ########################3
    #This creates the realignment sh file
    os.chdir(params.SMALTAligned_aln) #~!~~~~~~~~~~~~~~~~~~~NOOOO use previous samFileList
    #samFileList = []

    '''
    carryOverList_new is the intervals file
    carryOverList_old is the bam file list.
    '''
    
##    for fileX in glob.glob('*_smaltSrtRG_sorted.bam'): 
##        samFileList.append(fileX)

    os.chdir(params.scripts_SMALT)
    Realignment = "8_1_Realignment.sh"
    Realignment2 = "8_2_Realignment.sh"
    Realignment_cleanup = "8_x_Realignment_cleanup.sh"
    temp = []     
    f = open(Realignment,'w')
    f2 = open(Realignment2,'w')
    f3 = open(Realignment_cleanup,'w')
    for pos in range(len(carryOverList_old)): #samFileList:
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in carryOverList_old[pos]:
                referenceSMALT = ref
                break
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T IndelRealigner -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+carryOverList_old[pos]+" -o "+params.SMALTAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam"+" -targetIntervals "+params.SMALTAligned_aln+carryOverList_new[pos])
        f.write('\n')
##        f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -fixMisencodedQuals -T IndelRealigner -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+carryOverList_old[pos]+" -o "+params.SMALTAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam"+" -targetIntervals "+params.SMALTAligned_aln+carryOverList_new[pos])
##        f2.write('\n')
        f3.write("rm "+params.SMALTAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bam\n")
        f3.write("rm "+params.SMALTAligned_aln+carryOverList_old[pos][:(len(carryOverList_old[pos])-4)]+"_realigned.bai\n")
        temp.append(carryOverList_old[pos][:len(carryOverList_old[pos])-4]+"_realigned.bam")
    #print "GATK realignment sh file created as Realignment.sh"
    f.close()
    f2.close()
    f3.close()
    carryOverList_new = temp

    ########################3
    #This creates the base quality recalibration sh file
    #creating temp bam array to save on space:
    if params.BQSRPossible:
        os.chdir(params.scripts_SMALT)
        carryOverList_old = carryOverList_new
        carryOverList_new = []
        f1 = open("9.1_baseQualRecalSMALT.sh",'w')
        f2 = open("9.2_baseQualRecalSMALT.sh",'w')
        f3 = open("9.1_baseQualRecalSMALT_cleanup.sh",'w')
        f4 = open("9.2_baseQualRecalSMALT_cleanup.sh",'w')
        for x in carryOverList_old: 
            for ref in params.fastaList:
                referenceSMALT_shortName = getFastaName(ref)
                if referenceSMALT_shortName in x:
                    referenceSMALT = ref
                    break
                referenceSMALT = ref
            f1.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T BaseRecalibrator -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -knownSites "+params.dbSNP+"dbSNP.vcf -o "+params.SMALTAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f2.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T PrintReads -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -BQSR "+params.SMALTAligned_aln+x[:len(x)-20]+"recal_data.table -o "+params.SMALTAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            carryOverList_new.append(x[:(len(x)-20)]+"realigned_recal.bam")
            f3.write("rm "+params.SMALTAligned_aln+x[:len(x)-20]+"recal_data.table\n")
            f4.write("rm "+params.SMALTAligned_aln+x[:len(x)-20]+"realigned_recal.bam\n")
            f4.write("rm "+params.SMALTAligned_aln+x[:len(x)-20]+"realigned_recal.bai\n")
            #print "picard sort sh file created as picardSort.sh"
        f1.close()
        f2.close()
        f3.close()
        f4.close()
    else:
        print "Skipping Base quality score recalibration due to missing dbSNP file"

    ########################3
    #This creates the picard sort sh file
    #depends on sam array
    # creating temp bam array to save on space:

    #os.chdir(params.SMALTAligned_aln)
    os.chdir(params.scripts_SMALT)
    if BQSRPossible:
        amount = 20
    else:
        amount = 21
    
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    picardSort = "10_picardSort.sh"
    f = open(picardSort,'w')
    picardSort_cleanup = "10_picardSort_cleanup.sh"
    f2 = open(picardSort_cleanup,'w')
    for x in carryOverList_old: #samFileList:
##        f.write("java -jar "+params.SortSamDir+" I="+params.SMALTAligned_aln+x[:-4]+"_sorted_realigned.bam"+" O="
##        +params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT")       
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.SortSamDir+" I="+params.SMALTAligned_aln+x+" O="
        +params.SMALTAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT")
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam\n")
        f2.write("rm "+params.SMALTAligned_aln+x[:(len(x)-amount)]+"_realigned_resorted.bam.bai\n")
        carryOverList_new.append(x[:(len(x)-amount)]+"_realigned_resorted.bam")
    #print "picard sort sh file created as picardSort.sh"
    f.close()
    f2.close()

    
    ########################3
    #This creates the RE-indexing of the bam files sh file
    os.chdir(params.scripts_SMALT)
    carryOverList_old = carryOverList_new
    carryOverList_new = []
    reIndexBamFiles = "11_reIndexBamFiles.sh"
    f = open(reIndexBamFiles,'w')
    reIndexBamFiles_cleanup = "11_reIndexBamFiles_cleanup.sh"
    f2 = open(reIndexBamFiles_cleanup,'w')
    
    for x in carryOverList_old: #bamFileList:
##        print [carryOverList_old]
##        raw_input()
##        f.write("samtools index "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted.bam")               
        f.write(params.samtools+" index "+params.SMALTAligned_aln+x)               
        f.write('\n')
        f2.write("rm "+params.SMALTAligned_aln+x+".bai\n")
    #print "re-Index of bam files sh writen to reIndexBamFiles.sh"
    f.close()
    f2.close()


    ########################3
    #This creates the remove PCR duplicates sh file
    os.chdir(params.scripts_SMALT)
    removePCRDuplicates = "12_removePCRDuplicates.sh"
    f = open(removePCRDuplicates,'w')
    removePCRDuplicates_cleanup = "12_removePCRDuplicates_cleanup.sh"
    f2 = open(removePCRDuplicates_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
##        f.write(params.java7+" -jar "+params.markDuplicates+" I="+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted.bam"+" O="+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_dedup.bam VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE M=duplicate_metrics TMP_DIR=tmp ASSUME_SORTED=true > "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_rmdup.log")
        f.write(params.java7+" -jar "+params.markDuplicates+" I="+params.SMALTAligned_aln+x+" O="+params.SMALTAligned_aln+x[:(len(x)-4)]+"_dedup.bam VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE M=duplicate_metrics TMP_DIR=tmp ASSUME_SORTED=true > "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_rmdup.log")
        f.write('\n')
##        f2.write(params.SMALTAligned_aln+x[:(len(x)-4)]+"_dedup.bam")
        f2.write(params.SMALTAligned_aln+x[:(len(x)-4)]+"_rmdup.log")
    #print "picard remove pcr duplicates sh writen to removePCRDuplicates.sh"
    f.close()
    f2.close()
    

    ########################3
    #This creates the RE-indexing of the bam files sh file a 1nd time after the removal of pcr duplicates as in previous step
    os.chdir(params.scripts_SMALT)
    carryOverList_new = []
    reIndexBamFiles2 = "13_reIndexBamFiles2.sh"
    f = open(reIndexBamFiles2,'w')
    for x in carryOverList_old: #bamFileList:
##        f.write("samtools index "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_dedup.bam")              
        
        f.write(params.samtools+" index "+params.SMALTAligned_aln+x[:(len(x)-4)]+"_dedup.bam")              
        f.write('\n')
        carryOverList_new.append(x[:(len(x)-4)]+"_dedup.bam")
    #print "re-Index (FOR SECOND TIME) of bam files sh writen to reIndexBamFiles2.sh"
    f.close()

    ########################3
    #This creates the SNP calling sh file using GATK

    os.chdir(params.scripts_SMALT)
    snpCalling = "15_SNPCallingGATK.sh"
    carryOverList_old = carryOverList_new
##    carryOverList_new = []
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in carryOverList_old[pos]:
                referenceSMALT = ref
                break
##        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO -R "+params.smaltRef+referenceNOVO+" -I "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_dedup.bam -o "+params.SMALTAligned+snpDir+x[:-32]+"_gatk_snps.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.SMALTAligned+snpDir+x[:-32]+"_SNP_Genotype.log")  
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -o "+params.SMALTAligned+snpDir+x[:-46]+"_gatk_snps.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.SMALTAligned+snpDir+x[:-46]+"_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    ########################3
    #This creates the INDEL calling sh file using GATK
    #os.chdir(params.scripts_SMALT)
    #indelCalling = "15_INDELCallingGATK.sh"
    # 
    #f = open(indelCalling,'w')
    #for x in carryOverList_old: #bamFileList:
    #    for ref in params.fastaList:
    #        referenceSMALT_shortName = getFastaName(ref)
    #        if referenceSMALT_shortName in x:
    #            referenceSMALT = ref
    #            break
    #    #f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO --genotype_likelihoods_model INDEL -R "+params.smaltRef+referenceNOVO+" -I "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_dedup.bam -o "+params.SMALTAligned+indelDir+x[:-32]+"_gatk_indels.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.SMALTAligned+indelDir+x[:-32]+"_Genotype.log")  
    #    f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T UnifiedGenotyper -l INFO --genotype_likelihoods_model INDEL -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -o "+params.SMALTAligned+indelDir+x[:-46]+"_gatk_indels.vcf -stand_call_conf 50 -stand_emit_conf 10.0 -dcov 2000 > "+params.SMALTAligned+indelDir+x[:-46]+"_Indel_Genotype.log")  
    #    f.write('\n')
    ##print "SNP calling using GATK sh writen to INDELCallingGATK.sh"
    #f.close()
    
    
    ########################3
    #This creates the SAMTOOLS SNP CALLER sh file 
    os.chdir(params.scripts_SMALT)
    snpCalling = "15_2_VARIANT_CALLING_SAMTOOLS.sh"
     
    f = open(snpCalling,'w')
    coreCount = 0
    waitFlag = False
    for x in carryOverList_old: #bamFileList:
        coreCount += 1
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in x:
                referenceSMALT = ref
                break
        if coreCount < max(params.coreSplit):
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceSMALT+" "+params.SMALTAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.SMALTAligned+snpDir+x[:-4]+"_VARIANTS_SAMTOOLS.vcf &\n")
            waitFlag = False 
        else:
            f.write(params.samtools+" mpileup -t AD -ugf "+params.reference+referenceSMALT+" "+params.SMALTAligned_aln+x+" | "+params.bcftools+" call -vmO v -o "+params.SMALTAligned+snpDir+x[:-4]+"_VARIANTS_SAMTOOLS.vcf &\n")
            f.write("wait\n")
            waitFlag = True
            coreCount =  0
    if not waitFlag:
        f.write("wait\n")
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()
       
    ########################3
    #This creates the SNP HAPLOTYPE CALLER sh file using GATK
    os.chdir(params.scripts_SMALT)
    snpCalling = "15_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh"
     
    f = open(snpCalling,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in x:
                referenceSMALT = ref
                break
##        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T HaplotypeCaller -nct "+str(coreSplit[1])+" -R "+params.smaltRef+referenceNOVO+" -I "+params.SMALTAligned_aln+x[:(len(x)-20)]+"realigned_resorted_dedup.bam -o "+params.SMALTAligned+snpDir+x[:-32]+"_gatk_HC_snps.vcf -stand_call_conf 30 -stand_emit_conf 10.0 > "+params.SMALTAligned+snpDir+x[:-32]+"_Genotype.log")  
        f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T HaplotypeCaller -nct "+str(params.coreSplit[2])+" -R "+params.reference+referenceSMALT+" -I "+params.SMALTAligned_aln+x+" -o "+params.SMALTAligned+snpDir+x[:-4]+"_gatk_HC_snps.vcf -stand_call_conf 30 -stand_emit_conf 10.0 > "+params.SMALTAligned+snpDir+x[:-4]+"_SNP_HC_Genotype.log")  
        f.write('\n')
    #print "SNP calling using GATK sh writen to SNPCallingGATK.sh"
    f.close()

    ################################
    ## GATK GEN COVERAGE
    ################################
    #os.chdir(params.scripts_SMALT)
    #GenomeCoverage = "16_GenomeCoverage.sh"
    #f = open(GenomeCoverage,'w')
    #GenomeCoverage_cleanup = "16_GenomeCoverage_cleanup.sh"
    #f2 = open(GenomeCoverage_cleanup,'w')
    #for x in carryOverList_old: #bamFileList:
    #    for ref in params.fastaList:
    #        referenceSMALT_shortName = getFastaName(ref)
    #        if referenceSMALT_shortName in x:
    #            referenceSMALT = ref
    #            break
    #    f.write(params.java7+" -Xmx"+params.mem+"g -jar "+params.gatkHomeDir+" -T DepthOfCoverage -R "+params.reference+referenceSMALT+" -o "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt -I "+params.SMALTAligned_aln+x) #+" -nt"+str(coreSplit[0]))
    #    f.write('\n')
    #    f2.write("rm "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov.txt\n")
    ##print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    #f.close()
    #f2.close()
    
    ###############################
    # BED TOOL GEN COVERAGE
    ###############################
    os.chdir(params.scripts_SMALT)
    GenomeCoverage = "16_2_GenomeCoverage.sh"
    f = open(GenomeCoverage,'w')
    GenomeCoverage_cleanup = "16_2_GenomeCoverage_cleanup.sh"
    f2 = open(GenomeCoverage_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        for ref in params.fastaList:
            referenceSMALT_shortName = getFastaName(ref)
            if referenceSMALT_shortName in x:
                referenceSMALT = ref
                break

        f.write(params.bedtools+" -bga -ibam "+params.SMALTAligned_aln+x+" -g "+params.reference+referenceSMALT+" > "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt")
        f.write('\n')
        f2.write("rm "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt\n")
    #print "genome coverage bed tools sh file created as GenomeCoverage.sh"
    f.close()
    f2.close()
    
 ########################3
    #This creates the regions with zero coverage sh file
    os.chdir(params.scripts_SMALT)
    ZeroCov = "17_ZeroCov.sh"
    f = open(ZeroCov,'w')
    ZeroCov_cleanup = "17_ZeroCov_cleanup.sh"
    f2 = open(ZeroCov_cleanup,'w')
    for x in carryOverList_old: #bamFileList:
        #f.write("grep -w 0$ "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt > "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt") 
        f.write("awk 'NF && $4<2' "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov_bed.txt > "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt") 
        f.write('\n')
        f2.write("rm "+params.SMALTAligned+genomeCovDir+x[:(len(x)-4)]+"_genomecov=0.txt\n")

    #print "zero coverage sh file written as ZeroCov.sh"
    f.close()
    f2.close()
    return


def referenceSH():
    os.chdir(params.scripts_SMALT)
    f = open("indexSMALTRef.sh",'w')
    f.write(params.smaltBinary+" index -k 20 -s 1 "+params.smaltRef+"h37smaltrefk20s1 "+params.smaltRef+"H37Rv_4411532_fixed.fasta")
    f.close()

def load_seq_lengths(dirX, fileArray):
    fileSeqLengths = {} 
    for tempDir in os.listdir(dirX):
        if ".zip" in tempDir:
            continue
        try:
            os.chdir(dirX+tempDir)
            f = open("fastqc_data.txt",'r')
        except:
            continue 
        for line in f:
            if "Sequence length" not in line:
                continue
            else:
                if "-" in line.split()[-1]:
                    fileSeqLengths[tempDir.replace("_fastqc",".fastq.gz")] = line.split()[-1].split("-")[-1]
                    fileSeqLengths[tempDir.replace("_fastqc",".fastq")] = line.split()[-1].split("-")[-1]
                else:                        
                    fileSeqLengths[tempDir.replace("_fastqc",".fastq.gz")] = line.split()[-1]
                    fileSeqLengths[tempDir.replace("_fastqc",".fastq")] = line.split()[-1]
                break
    return fileSeqLengths

def spolpred(params,trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE,debugMode):
    seqLengthsPE = load_seq_lengths(params.fastQCStatsDir1,fileArrayPE)
    seqLengthsSE = load_seq_lengths(params.fastQCStatsDir1,fileArraySE)
##    print seqLengths
##    raw_input()
    
    if debugMode:
        print fileArraySE
        print fileArrayPE
        raw_input("testing spolpred, must run on uncompressed fastq - non trimmed")    
        
    os.chdir(params.scripts_StrainIdentification)
    f = open("spolpred.sh",'w')
    pos = 0
    count = 0
    while pos <= len(fileArrayPE)-2:
        if fileArrayPE[pos].endswith(".gz"):
            seqLength = "100"
            if fileArrayPE[pos] in seqLengthsPE:
                seqLength = seqLengthsPE[fileArrayPE[pos]]
            else:
                print "error no fastqc info found for:", fileArrayPE[pos]
                if debugMode:
                    raw_input("press enter to see full list of avail fastqc files to query")
                    print seqLengthsPE
                    raw_input("press enter to continue")
            if debugMode:
                print fileArrayPE[pos], seqLength
            f.write("gunzip -f "+params.fastQ+fileArrayPE[pos]+"\n")
            f.write(params.spolpred+" "+params.fastQ+fileArrayPE[pos][:-3]+" -l "+seqLength+" -o "+params.mapperOut+spolPredOut+str(fileArrayPE[pos][:-9])+"_spolPredOut.txt\n")                
            f.write("gzip "+params.fastQ+fileArrayPE[pos][:-3]+" &\n")
        else:
            seqLength = "100"
            if fileArrayPE[pos] in seqLengthsPE:
                seqLength = seqLengthsPE[fileArrayPE[pos]]
            else:
                print "error no fastqc info found for:", fileArrayPE[pos]
                if debugMode:
                    raw_input("2 press enter to see full list of avail fastqc files to query")
                    print seqLengthsPE
                    raw_input("2 press enter to continue")
            f.write(params.spolpred+" "+params.fastQ+fileArrayPE[pos]+" -l "+seqLength+" -o "+params.mapperOut+spolPredOut+str(fileArrayPE[pos][:-9])+"_spolPredOut.txt\n")                
            f.write("gzip "+params.fastQ+fileArrayPE[pos]+" &\n")
            #f.write(params.spolpred+" "+params.mapperOut+spolPredOut+str(fileArrayPE[pos])+" -l 100 -o "+params.mapperOut+spolPredOut+str(fileArrayPE[pos][:-8])+"_spolPredOut.txt -d off &\n")
        count += 1
        if count >= 2: #int(params.cores):
            count = 0
            #f.write("wait\n")
        pos += 2       
    pos = 0
    threadCount = 0
    for pos in range(len(fileArraySE)):
        if fileArraySE[pos].endswith(".gz"):
            seqLength = "100"
            if fileArraySE[pos] in seqLengthsSE:
                seqLength = seqLengthsSE[fileArraySE[pos]]
            else:
                print "error no fastqc info found for:", fileArraySE[pos]
            f.write("gunzip -f "+params.fastQ+fileArraySE[pos]+"\n")
            f.write(params.spolpred+" "+params.fastQ+fileArraySE[pos][:-3]+" -l "+seqLength+" -o "+params.mapperOut+spolPredOut+str(fileArraySE[pos])[:-9]+"_spolPredOut.txt\n")
            f.write("gzip "+params.fastQ+fileArraySE[pos][:-3]+" &\n")
        else:
            seqLength = "100"
            if fileArraySE[pos] in seqLengthsSE:
                seqLength = seqLengthsSE[fileArraySE[pos]]
            else:
                print "error no fastqc info found for:", fileArraySE[pos]
            f.write(params.spolpred+" "+params.fastQ+fileArraySE[pos]+" -l "+seqLength+" -o "+params.mapperOut+spolPredOut+str(fileArraySE[pos])[:-9]+"_spolPredOut.txt\n")
            f.write("gzip "+params.fastQ+fileArraySE[pos]+" &\n")
        if threadCount >= 2: #int(params.cores):
            #f.write("wait\n")
            threadCount = 0
        threadCount +=1
    #if not flag:
    #    print
        #f.write("wait\n")
    f.close()
    return

def spolpred_custom(inputDir,outputDir):

    cleanedUpFileData = partitionFastQList(inputDir)
    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]

    fileArraySE , trimArraySE , IDSE, SMSE = GenerateCleanFileNamesX(fileArraySE) #change dirX to params.trimmedFastQ
    fileArrayPE , trimArrayPE , IDPE, SMPE = GenerateCleanFileNamesX(fileArrayPE) #change dirX to params.trimmedFastQ

    fileArray = fileArraySE+fileArrayPE
    trimArray = trimArraySE+trimArrayPE
    ID = IDSE + IDPE
    SM = SMSE + SMPE
   
    os.chdir(params.scripts_StrainIdentification)
    f = open("spolpred1.sh",'w')

    pos = 0
    count = 0
    while pos <= len(fileArrayPE)-2:
        f.write("perl "+params.shuffle+" "+inputDir+str(fileArrayPE[pos])+" "+inputDir+str(fileArrayPE[pos+1])+" "+outputDir+str(fileArrayPE[pos+1])[:-6]+"_combined.fastq &\n")    
        count += 1
        if count == params.cores:
            count = 0
            f.write("wait\n")
        pos += 2    
    f.close()
    #return

    f = open("spolpred2.sh",'w')
    pos = 0
    threadCount = 0

    #NOTE these come from trimmed fastq, and are all single ends, did not perform combine reads on these so doing spolpred on SE
    flag = False
    for pos in range(len(fileArraySE)):
        flag = False
        f.write(params.spolpred+" "+inputDir+str(fileArraySE[pos])+" -l 100 -o "+outputDir+str(fileArraySE[pos])[:-6]+"_spolPredOut.txt -d off&\n")
        if threadCount == params.cores:
            f.write("wait\n")
            flag= True
            threadCount = 0
        threadCount +=1
    if not flag:
        f.write("wait\n")

    #NOTE these come from RESULTS/SpolPredOut/*combined files, these are PE files condenced into one file, this gives spolpred more reads
    #to work with and thus more accuracy hopefully. 
    pos = 0
    flag = False
    while pos <= len(fileArrayPE)-2:
        flag = False
        if IDPE[pos] <> IDPE[pos+1]:
            print "error - the two files are not matching - cannot proceed - please manually quit and fix the error"
            print ID[pos],'and',ID[pos+1]
            raw_input("error - the two files are not matching - cannot proceed - please manually quit and fix the error")
            exit
        if outputDir[-1] == "/" and outputDir[-2] == "/":
            params.mapperOut = params.mapperOut[:-1]
        f.write(params.spolpred+" "+outputDir+str(fileArrayPE[pos+1])[:-6]+"_combined.fastq"+" -l 100 -o "+outputDir+spolPredOut+str(fileArrayPE[pos+1])[:-6]+"_spolPredOut.txt -d off& > spolpred_log.txt\n")
        pos += 2

        if threadCount == params.cores:
            flag = True
            f.write("wait\n")
            threadCount = 0
        threadCount +=1
    if not flag:
        f.write("wait\n")
    f.close()

    print "spolpred sh written"
    f.close()
    return

###############################################################################
#END mapper scripts
###############################################################################


###############################################################################
#### TRIMMING
###############################################################################

def partitionFastQList(fastQDir):
    def sampleName(fileX):
        return fileX.split("_")[0]
    data = []
    os.chdir(fastQDir)
    for fileX in os.listdir(fastQDir):
        if fileX.endswith(".fastq") or fileX.endswith("fastq.gz"):
            data.append(fileX)
    data.sort()
    singleData = []
    pairedData = []
    previous = ''
    firstEntry = True
    pos = 0
    flag = True
    while pos <= len(data)-1:
        if pos == 0 or flag:
            previous = data[pos]
            if pos == len(data)-1:
                singleData.append(previous.replace("\n",""))
            pos+=1
            flag = False
            continue

        current = data[pos]
        if sampleName(current) == sampleName(previous):
            pairedData.append(previous.replace("\n",''))
            pairedData.append(current.replace("\n",''))
            pos+=1
            flag=True
            continue
        else:
            if pos == len(data) -1:
                singleData.append(previous.replace("\n",''))
                singleData.append(current.replace("\n",''))
                pos+=2
                continue
            else:
                singleData.append(previous.replace("\n",''))
                flag=True
                continue
    return [singleData, pairedData]

def noTrimmingFileNamePartition(): 

    outputTrimmedFilesSE = []
    outputTrimmedFilesPE = []
    cleanedUpFileData = partitionFastQList(params.fastQ)

    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]
    
    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #ID,SM,LB,barcodes,trimArray 
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE)  #ID,SM,LB,barcodes,trimArray

    if fileArraySE <> []:
        print "files detected as SE "
        print fileArraySE
    if fileArrayPE <> []:
        print "files detected as PE:"
        print fileArrayPE
    
    if params.reads == "singleEnd": 
        fileArray = fileArraySE
        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
    elif params.reads == "pairedEnd":
        fileArray = fileArrayPE
        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    elif params.reads == "mixed":
        fileArray = fileArraySE+fileArrayPE
        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE
    pos = 0
    for fileNameX in fileArraySE:
        if fileNameX.lower().endswith(".fastq.gz"):
            outputName = fileNameX #fileNameX[:-9]+"_trimSE.fastq"
        elif fileNameX.lower().endswith(".fastq"):
            outputName = fileNameX #fileNameX[:-6]+"_trimSE.fastq"
        outputTrimmedFilesSE.append(outputName) #+".gz")
    fileArray = fileArrayPE
    ID = IDPE
    while pos <= len(fileArray)-2:
        if ID[pos] <> ID[pos+1]:
            print "filename matching error - the two files are not matching - cannot proceed - please manually quit and fix the error"
            raw_input()
            exit
        if fileArray[pos].lower().endswith("fastq.gz"):
            outputName1 = fileArray[pos] #fileArray[pos][:-9]+"_trimPE.fastq"
        elif fileArray[pos].lower().endswith("fastq"):
            outputName1 = fileArray[pos] #fileArray[pos][:-6]+"_trimPE.fastq"
        if fileArray[pos+1].lower().endswith("fastq.gz"):
            outputName2 = fileArray[pos+1] #fileArray[pos+1][:-9]+"_trimPE.fastq"
        elif fileArray[pos+1].lower().endswith("fastq"):
            outputName2 = fileArray[pos+1] #fileArray[pos+1][:-6]+"_trimPE.fastq"
        outputTrimmedFilesPE.append(outputName1) #+".gz")
        outputTrimmedFilesPE.append(outputName2) #+".gz")
        pos +=2
    print "no-trimming filename partition complete"
    return outputTrimmedFilesSE, outputTrimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE


def trimmomaticMulti(): 
    outputTrimmedFilesSE = []
    outputTrimmedFilesPE = []
    cleanedUpFileData = partitionFastQList(params.fastQ)

    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]
    
    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #ID,SM,LB,barcodes,trimArray 
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE = extractFileNameData(fileArrayPE)  #ID,SM,LB,barcodes,trimArray
    if fileArraySE <> []:
        print "files detected as SE "
        print fileArraySE
    if fileArrayPE <> []:
        print "files detected as PE:"
        print fileArrayPE
    
    if params.reads == "singleEnd": 
        fileArray = fileArraySE
        trimArray = trimArraySE
        ID = IDSE
        SM = SMSE
    elif params.reads == "pairedEnd":
        fileArray = fileArrayPE
        trimArray = trimArrayPE
        ID = IDPE
        SM = SMPE
    elif params.reads == "mixed":
        fileArray = fileArraySE+fileArrayPE
        trimArray = trimArraySE+trimArrayPE
        ID = IDSE + IDPE
        SM = SMSE + SMPE

    os.chdir(params.main)

    try:
        os.makedirs(params.scripts_trimming)
    except:
        print "Using previously existing temporary trimming script directory"
    try:
        os.makedirs(params.trimmedFastQ)
    except:
        print "Using previously existing output folder for trimmed FASTQ files" 
        
    os.chdir(params.trimmedFastQ)
    try:
        #os.makedirs("log/")
        os.makedirs("unpaired/")
    except:
        print "The log and unpaired trimming directories already exists, proceeding"       
    trimmomaticSH = "autoTrim.sh"
    os.chdir(params.scripts_trimming)
    f = open(trimmomaticSH,'w') 
    pos = -1

    for fileNameX in fileArraySE:
        pos += 1
        if fileNameX.lower().endswith("fastq.gz"):
            outputName = fileNameX[:-9]+"_trimSE.fastq"
        elif fileNameX.lower().endswith("fastq"):
            outputName = fileNameX[:-6]+"_trimSE.fastq"
        outputTrimmedFilesSE.append(outputName+".gz")
        f.write(params.java7+" -jar "+params.trimOMatic+" SE -threads "+str(params.cores)+" -phred33 "+params.fastQ+str(fileNameX)+" "+params.trimmedFastQ+outputName+" ILLUMINACLIP:"+params.tools+"illumina_adapters.fna.fasta:"+params.trimOMaticParams+"\n")
        if pos == len(fileArraySE)-1:
            f.write("gzip "+params.trimmedFastQ+outputName+" \n")
        else:
            f.write("gzip "+params.trimmedFastQ+outputName+" &\n")
    if fileArraySE <> []:
        f.write("wait\n")
        #f.write("rm "+params.trimmedFastQ+outputName+"\n")                                                                                                                                                                                                       
    fileArray = fileArrayPE
    ID = IDPE
    pos = 0
    while pos <= len(fileArray)-2:
        if ID[pos] <> ID[pos+1]:
            print "trimmomaticSH error - the two files are not matching - cannot proceed - please manually quit and fix the error"
            raw_input()
            exit
        if fileArray[pos].lower().endswith("fastq.gz"):
            outputName1 = fileArray[pos][:-9]+"_trimPE.fastq"
        elif fileArray[pos].lower().endswith("fastq"):
            outputName1 = fileArray[pos][:-6]+"_trimPE.fastq"
        if fileArray[pos+1].lower().endswith("fastq.gz"):
            outputName2 = fileArray[pos+1][:-9]+"_trimPE.fastq"
        elif fileArray[pos+1].lower().endswith("fastq"):
            outputName2 = fileArray[pos+1][:-6]+"_trimPE.fastq"
        outputTrimmedFilesPE.append(outputName1+".gz")
        outputTrimmedFilesPE.append(outputName2+".gz")
        f.write(params.java7+" -jar "+params.trimOMatic+" PE -threads "+str(params.cores)+" -phred33 "+params.fastQ+str(fileArray[pos])+" "+params.fastQ+str(fileArray[pos+1])+" "+params.trimmedFastQ+outputName1+" "+params.trimmedFastQ+"unpaired/"+outputName1+" "+params.trimmedFastQ+outputName2+" "+params.trimmedFastQ+"unpaired/"+outputName2+" ILLUMINACLIP:"+params.tools+"illumina_adapters.fna.fasta:"+params.trimOMaticParams+"\n") #params are usually: 2:30:10 LEADING:20 TRAILING:20 SLIDINGWINDOW:4:20 MINLEN:36
        f.write("gzip -f "+params.trimmedFastQ+outputName1+" &\n")
        if pos >= len(fileArray)-2:
            f.write("gzip -f "+params.trimmedFastQ+outputName2+" \n")
        else:
            f.write("gzip -f "+params.trimmedFastQ+outputName2+" &\n")   
        #f.write("rm "+params.trimmedFastQ+outputName1+ " &\n")
        #f.write("rm "+params.trimmedFastQ+outputName2+" &\n")                
        pos +=2
    f.write("wait\n")
    f.close()

    #print "trimmomatic mixed-mode list created as: ",trimmomaticSH
    f.close()
    return outputTrimmedFilesSE, outputTrimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE
    
############################################    

def fastXToolKitTrim():
    outputTrimmedFilesSE = []
    outputTrimmedFilesPE = []
    cleanedUpFileData = partitionFastQList(params.fastQ)

    fileArraySE = cleanedUpFileData[0]
    fileArrayPE = cleanedUpFileData[1]
    
    IDSE, SMSE, LBSE, barcodesSE, trimArraySE = extractFileNameData(fileArraySE) #ID,SM,LB,barcodes,trimArray 
    IDPE, SMPE, LBPE, barcodesPE, trimArrayPE= extractFileNameData(fileArrayPE)  #ID,SM,LB,barcodes,trimArray

    print "files detected as SE "
    print fileArraySE
    print "files detected as PE:"
    print fileArrayPE
    
    def calculateTrim(strList,cutOffList):
        trimValueList = []
        pos = 0      
        valueList = []
        for stringX in strList:
            valueList.append(stringX)

        pos = 0
        for x in valueList:
            print int(cutOffList[pos]), "and ", int(x), " trim ", (int(cutOffList[pos]) - int(x))
            trimValueList.append(int(cutOffList[pos]) - int(x))
            pos+=1
        return trimValueList
    ################################################################

    fileArray = []
    values = []
    totalLoaded = 0
    roots = []
    readLength =0
    readLenArray = []

    lookFor = "fastqc_data.txt"
    print "Working directory: ",params.fastQCStatsDir1

    for root, directories,files in os.walk(params.fastQCStatsDir1):
        for f in files:     
            if f == lookFor:
                totalLoaded +=1
                with open(os.path.join(root, f), 'r') as tempFile:
                    cutOff = None
                    lineNum = 0
                    
                    for line in tempFile:
                        lineNum += 1
                    
                        if lineNum>15 and ">>END_MODULE" in line:
                            break                   
                        wordList = line.strip()
                        if lineNum == 9:
                            s = wordList.split()
                            readLenArray.append(int(s[2]))                                        
                    
                        if lineNum == 4:
                            fileName = wordList[9:]
                            fileArray.append(fileName)
                        if lineNum >= 14 and wordList <> ">>END_MODULE":
                            s = wordList.split()
   
##                            if trimmingMethod == "Strict":
##                                if float(s[3]) >= 20.0 and float(s[2]) >=  20.0 and float(s[1]) >=  20.0: #1 is the mean, 2 is the median and 3 is my previous yellow box cutoff
##                                    cutOff = (s[0])
##                                else:
##                                    break                               
                            if params.trimMethod == "Fixed_Amount_Trim": 
                                if float(s[2]) >=  20.0 and float(s[1]) >=  20.0: #1 is the mean, 2 is the median and 3 is my previous yellow box cutoff
                                    cutOff = (s[0])
                                else:
                                    break
                    values.append(cutOff)
                tempFile.close()

    print "Loading FastQC summary statistics, a total of ",totalLoaded,"files were loaded"
    trimList = calculateTrim(values,readLenArray) 
    #print trimList

    autoTrim = "autoTrim.sh"
    os.chdir(params.scripts_trimming)
    f = open(autoTrim,'w')
    pos = 0

    for x in trimList:
        outputName = ""
        if fileArray[pos] in fileArraySE:
            if fileArray[pos].lower().endswith("fastq.gz"):
                outputName = fileArray[pos][:-9]+"_trimSE"+str(x)+".fastq"
                outputTrimmedFilesSE.append(outputName+".gz")
            elif fileArray[pos].lower().endswith("fastq"):
                outputName = fileArray[pos][:-6]+"_trimSE"+str(x)+".fastq"
                outputTrimmedFilesSE.append(outputName+".gz")

        elif fileArray[pos] in fileArrayPE:
            if fileArray[pos].lower().endswith("fastq.gz"):
                outputName = fileArray[pos][:-9]+"_trimPE"+str(x)+".fastq"
                outputTrimmedFilesPE.append(outputName+".gz")
                    
            elif fileArray[pos].lower().endswith("fastq"):
                outputName = fileArray[pos][:-6]+"_trimPE"+str(x)+".fastq"
                outputTrimmedFilesPE.append(outputName+".gz")
        else:
            raw_input("File could not be matched to either PE or SE: "+fileArray[pos]+" please rename file according to suggested naming convention listed in manual")
            exit(0)

        if int(x) == 0: #if you dont have to trim, then just copy file over 
            writeThis = "cp "+params.fastQ+str(fileArray[pos])+' '+params.trimmedFastQ+outputName
        else:
            writeThis = params.fastXTrimmer+ ' -t '+ str(x)+' -Q 33 -i '+ params.fastQ+str(fileArray[pos])+' -o '+params.trimmedFastQ+outputName
        f.write(writeThis+"\n")
        f.write("gzip "+params.trimmedFastQ+outputName+" &\n")
                    
        f.write() 
        pos +=1
        
    print "Trimming script file created as",autoTrim
    f.write("wait\n")
    f.close()
    return outputTrimmedFilesSE, outputTrimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArraySE

##########################################################
#END TRIMMING
##########################################################


##########################################################
#Check if EMBL and FASTA files match to support annotation
##########################################################
def validateRefFiles(refDir,userRef):
    if debugMode or True:
        print "validating reference folder for required files, current reference folder is:", userRef
       # raw_input("Remove checkpoint -66-66-66")
    '''
    each fasta file requires a matching embl file
    Assumption using only one reference fasta file
    May use multiple embl files for annotation 
    '''
    BQSRPossible = False
    os.chdir(refDir)
    fastaList = []
    emblList = []
    try:
        for fileX in os.listdir(refDir+"/"+userRef+"/dbSNP"):
            fileName = fileX.lower()
            if fileName.lower() == "dbsnp.vcf":
                BQSRPossible = True
    except:
        BQSRPossible = False
  
    for fileX in os.listdir(refDir+"/"+userRef+"/FASTA"):
        fileName = fileX.lower()
        if fileName.endswith(".gz"):
            print "Error, the input fasta file is in compressed format:",fileX
            print "Please ensure the reference fasta and embl files are uncompressed"
            raw_input("Press enter to exit the program")
            exit(0)
        if fileName.endswith(".fasta") or fileName.endswith(".fa"):
            print "Evaluating", fileX
            fileExt = fileX.split(".")[-1]
##            print fileExt
            tempFasta = fileX[:len(fileX)-len(fileExt)-1]
##            print "adding", [tempFasta]
            fastaList.append(tempFasta)
    fastaList.sort()
    if not os.path.isdir(refDir+"/"+userRef+"/EMBL"):
        emblList = []
    else:
        for fileX in os.listdir(refDir+"/"+userRef+"/EMBL"):
            print "Evaluating", fileX
            fileName = fileX.lower()
            if fileName.endswith(".gz"):
                print "Error, the input fasta file is in compressed format:",fileX
                print "Please ensure the reference fasta and embl files are uncompressed"
                raw_input("Press enter to exit the program")
                exit(0)
            if fileName.endswith(".embl") or fileName.endswith(".dat"):
                fileExt = fileX.split(".")[-1]
    ##            print fileExt
                tempEmbl = fileX[:len(fileX)-len(fileExt)-1]
    ##            print "adding", [tempEmbl]
                emblList.append(tempEmbl)
        emblList.sort()
            
    if len(fastaList) == 0:
        print "Error, no fasta files found in", refDir+"/"+userRef+"/FASTA"
        raw_input("Press enter to exit the program")
        exit(0)
        return False , BQSRPossible, ""
    if len(emblList) == 0:
        print "No embl files found in", refDir+"/"+userRef+"/EMBL"
        print "This will not allow annotation of variants..."
        #raw_input("Press enter to continue.")
        #exit()
        return False , BQSRPossible, ""
    flag = True
    for fileX in fastaList:
        if fileX not in emblList:
            print "Error matching FASTA file to EMBL file"
            print "The fasta file '",fileX,"' does not have a matching EMBL file"
            #raw_input("Press enter to exit the program")
            flag = False

    for fileX in emblList:
        if fileX not in fastaList:
            print "Error matching EMBL file to FASTA file"
            print "The EMBL file '",fileX,"' does not have a matching FASTA file"
            #raw_input("Press enter to exit the program")
            flag = False
    if flag:
        print "All FASTA files matched to corresponding EMBL files"
    return flag, BQSRPossible, emblList[0]

def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    #http://code.google.com/p/psutil/
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass
    print "Error auto-detecting system CPU thread count."
    return "2"
    
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except:
        pass


def available_memory():
    temp =""
    try:
        p = Popen(['free', '-m'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate("input data that is passed to subprocess' stdin")
        
        temp = ""
        prev = " "
        for char in output:
            if char == prev and prev == " ":
                continue
            else:
                temp += char
                prev = char

        ##print temp
        temp = temp.split("\n")[1]
        temp = temp.split(" ")
        temp = temp[1]
    except:
        print "error detecting free memory, re-attempting"
    if temp == "":
        try:
            p = Popen(['free', '-m'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate("input data that is passed to subprocess' stdin")

##            raw_input()
            rc = p.returncode
            temp = output.split("\n")
##            print temp
            temp = temp[2]
##            print temp
            temp=temp.replace(" ","*")
##            print temp
            temp=temp.split("*")
            print temp
            temp = temp[-1]
##            raw_input("error is here")
        except:
            print "Error auto-detecting system memory."
            return "4000"
    if temp == "":
        print "Error auto-detecting system memory"
        return "4000" #default
    return temp





#################################################################################################################

def checkFileNames(fastQDir,readsType):
    print "------------------------------------"
    print "checking validity of file names in these given directories:"
    print "INPUT DIR:", fastQDir
    print "reads type", readsType
##    print "OUTPUTDIR:",settingsList[3]
##    print "SETTINGS:", settingsList
    print "------------------------------------"
    count = 0
    #settingsList=['4', '2954', '/home/pagit/MASTER', 'Illumina', 'pairedEnd']
    fileList = []
    for tempFile in os.listdir(fastQDir):
        if tempFile.endswith(".fastq") or tempFile.endswith("fastq.gz"):
            fileList.append(tempFile)
            count += 1
    if count == 0:
        return False
    print "a total of ",len(fileList),"files were found in ",fastQDir
    try:
        for x in fileList:
            f = open(x,'r')
            print "checking read access to:",f.name
            f.close()
    except:
        print "error opening fastQ files in",fastQDir,"ensure file permissions allow read access"
        return False

    if readsType == 'pairedEnd':
        print "now matching paired-end file mathcing..."
        fileList.sort()
        pos = -2
        while True: 
            pos += 2
            if ("R1" in fileList[pos] or "read1" in str.lower(fileList[pos])) and ("R2" in fileList[pos+1] or "read2" in str.lower(fileList[pos+1])):
                print fileList[pos],"matched to ",fileList[pos+1]
            else:
                print "error matching paired end files, please rename files to use unique identifier followed by '_' and R1 or R2 in case of "
                print "paired-end files or simply unique identifier in case of single end files."
                print "example: Single end filename --> R1234.fastq or R1234.fastq.gz"
                print "example: Paired end files --> R1234_R1.fastq.gz and R1234_R2.fastq.gz" 
                print "The problematic files were:",fileList[pos],"and",fileList[pos+1]
                print "make sure to select mixed mode when running paired end and single end files together."
                return False
            if pos+2 == len(fileList):
                break
        print "If the fastQ files do not appear to correctly match, you should exit the program and rename the files as described in the manual"
    return True
   
#####################################################################################################
def loadSettingsFile(cpu_count,memory):
    globalDir = os.getcwd()
    if "/BIN" in globalDir:
        globalDir = globalDir[:-4]
    refDir = globalDir+"/Reference"
    outputDir = globalDir+"/Output" #"\home\user\NGS-DATA\Output"
    binDir = globalDir+"/BIN"
    os.chdir(globalDir)

    try:
        f = open('userSettings.txt','r') 
    except:
        print "No user settings file found, creating new config file..."
        f=open('userSettings.txt','w')
        f.write("CPU_CORES\t"+str(cpu_count)+"\n") #1
        f.write("SYSTEM_MEMORY\t"+str(memory)+"\n") #2
        f.write("FASTQ_DIRECTORY\t"+outputDir[:-6]+"FASTQ\n") #3
        f.write("OUTPUT_DIRECTORY\t"+outputDir+"\n") #4
        f.write("READS_TYPE\tmixedReads\n") #5
        f.write("reference\tMycobacteriumTuberculosis_H37Rv\n") #6
        f.write("trimmingMode\tQuality_Trim\n") #7
        f.write("----------------------------------------------------\n") #8
        f.write("Mapper settings:\n") #9
        f.write("Mapper BWA:\tTrue\n") #10
        f.write("Mapper NOVOAlign:\tTrue\n") #11
        f.write("Mapper SMALT:\tTrue\n") #12
        f.write("----------------------------------------------------\n") #13
        f.write("Variant detection settings:\n") #14
        f.write("Variant Detection tools GATK:\tTrue\n") #15
        f.write("Variant Detection tools SAMTools (mpileup):\tTrue\n") #16
        f.write("----------------------------------------------------\n") # 17
        f.write("Variant Filtering Settings:\n") # 18
        f.write("mapperCount_GATK =\t3\n") # 19
        f.write("mapperCount_SAMTOOLS =\t0\n") #20
        f.write("qualityCutOff_GATK =\t100\n") #21
        f.write("qualityCutOff_SAMTOOLS =\t100\n") #22
        f.write("minCoverage_GATK =\t10\n") #23
        f.write("minCoverage_SAMTOOLS =\t10\n") #24
        f.write("readFreqCutoff_GATK =\t0.3\n") #25
        f.write("readFreqCutoff_SAMTOOLS =\t0.3\n") #26
        f.write("filterMappabilityPositions =\tFalse\n") #27
        f.write("filterCustomPositions =\tFalse\n") #28
        f.write("filterOnKeywords =\tFalse\n") #29
        f.write("----------------------------------------------------\n") # 30
        f.write("Minimum_Genome_Coverage =\t50\n") #31
        f.write("Minimum_percentage_mapped_reads =\t90\n") #32
        f.close()
    print "loading userSettings.txt..."
    f = open('userSettings.txt','r')
    print "Current user settings from previous run:"
    print ("----------------------------------------------------")
    count = 0
    tempDir1 = ""
    tempDir2 = ""
    #DEFUALT SETTINGS ARE:
    bwa = False
    novo = False
    smalt = False
    gatk = False
    samtools = False
    mapperCount_GATK = 3
    mapperCount_SAMTOOLS = 0
    qualityCutOff_GATK = 10
    qualityCutOff_SAMTOOLS = 10
    minCoverage_GATK = 10
    minCoverage_SAMTOOLS = 10
    readFreqCutoff_GATK = 0.3
    readFreqCutoff_SAMTOOLS = 0.3
    filterMappabilityPositions = False
    filterCustomPositions = False
    filterOnKeywords = False
    minCov = 50
    minMappedReads = 90.0    
    for x in f: #load settings from userSettings.txt
        count+=1
        x = x.replace("\n","")
        print x
        if count == 1:
            temp = x.split("\t")[1]
            temp = temp.replace("\n","")
            prev_cpu_count = temp    
        if count == 2:
            temp = x.split("\t")[1]
            temp = temp.replace("\n","")
            prev_memory = int(temp)      
        if count == 3:
            tempDir1 = x.split("\t")[-1].strip()
            if tempDir1[-1] <> "/":
                tempDir1+="/"
            inputDir = tempDir1
        if count == 4:
            tempDir2 = x.split("\t")[-1].strip()
            if tempDir2[-1] <> "/":
                tempDir2+="/"
            outputDir = tempDir2
        if count == 5:
            temp = x.split("\t")[1]
            temp = temp.replace("\n","")
            reads_type = temp
            
        if count == 6:
            temp = x.split("\t")[1]
            temp = temp.replace("\n","")
            userRef = temp
            
        if count == 7:
            temp = x.split("\t")[1]
            temp = temp.replace("\n","")
            trimmingMode = temp
        #----MAPPERS--------------------------
        
        
        if count == 10:
            temp = x.split("\t")[1]
            if temp == "True":
                bwa = True
            else:
                bwa = False
        if count == 11:
            temp = x.split("\t")[1]
            if temp == "True":
                novo = True
            else:
                novo = False
        if count == 12:
            temp = x.split("\t")[1]
            if temp == "True":
                smalt = True
            else:
                smalt = False
        #----Variant detection tools----------
        if count == 15:
            temp = x.split("\t")[1]
            if temp == "True":
                gatk = True
            else:
                gatk = False
        if count == 16:
            temp = x.split("\t")[1]
            if temp == "True":
                samtools = True
            else:
                samtools = False
    
        ##################################
        #load previous filtering settings:
        if count == 19:
            valX = x.split("\t")[1]
            try:
                mapperCount_GATK = int(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 20:
            valX = x.split("\t")[1]
            try:
                mapperCount_SAMTOOLS = int(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 21:
            valX = x.split("\t")[1]
            try:
                qualityCutOff_GATK = float(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 22:
            valX = x.split("\t")[1]
            try:
                qualityCutOff_SAMTOOLS = float(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 23:
            valX = x.split("\t")[1]
            try:
                minCoverage_GATK = int(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 24:
            valX = x.split("\t")[1]
            try:
                minCoverage_SAMTOOLS = int(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 25:
            valX = x.split("\t")[1]
            try:
                readFreqCutoff_GATK = float(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 26:
            valX = x.split("\t")[1]
            try:
                readFreqCutoff_SAMTOOLS = float(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 27:
            valX = x.split("\t")[1]
            if valX.lower() == "true":
                filterMappabilityPositions = True
            elif valX.lower() == "false":
                filterMappabilityPositions = False 
            else:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a 'True' or 'False' value, got",[valX],"...now loading default setting..."
        if count == 28:
            valX = x.split("\t")[1]
            if valX.lower() == "true":
                filterCustomPositions = True
            elif valX.lower() == "false":
                filterCustomPositions = False 
            else:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a 'True' or 'False' value, got",[valX],"...now loading default setting..."
        if count == 29:
            valX = x.split("\t")[1]
            if valX.lower() == "true":
                filterOnKeywords = True
            elif valX.lower() == "false":
                filterOnKeywords = False 
            else:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a 'True' or 'False' value, got",[valX],"...now loading default setting..."
        ######################
        #Values for use in summary file for QC fail or pass
        if count == 31:
            valX = x.split("\t")[1]
            try:
                minCov = int(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
        if count == 32:
            valX = x.split("\t")[1]
            try:
                minMappedReads = float(valX)
            except:
                print "error loading value in line "+str(count)+" of userSettings.txt, was expecting a number, got",[valX],"...now loading default setting..."
    ##########################################################################
    f.close()
    mappers = [["BWA",bwa],["NOVOAlign",novo],["SMALT",smalt]]
    variantTools = [["GATK",gatk],["SAMTOOLS",samtools]]
    
    if ["GATK",True] in variantTools:
        gatkFlag = True
    else:
        gatkFlag = False
    if ["SAMTOOLS",True] in variantTools:
        samtoolsFlag = True
    else:
        samtoolsFlag = False
    if ["BWA",True] in mappers:
        useBWA = True
    else:
        useBWA = False
    if ["NOVOAlign",True] in mappers:
        useNOVO = True
    else:
        useNOVO = False
    if ["SMALT",True] in mappers:
        useSMALT = True
    else:
        useSMALT = False

    return reads_type, refDir, binDir, globalDir, prev_cpu_count,prev_memory,inputDir, outputDir, userRef, trimmingMode, useBWA, useNOVO,  useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK, readFreqCutoff_SAMTOOLS,    filterMappabilityPositions, filterCustomPositions,    filterOnKeywords , tempDir1, tempDir2, mappers, variantTools, minCov, minMappedReads


def setup(cpu_count, memory, skipSetup):
    '''
    create a usersettings file or read an existing one.
    Store info for input fastq, hardware, output folder, selected reference, mappers, var tools, filter settings
    '''
    #########################################################################################
    #EXTRACT PREVIOUS SETTINGS:
    reads_type, refDir, binDir, globalDir, prev_cpu_count,prev_memory,inputDir, outputDir, userRef, trimmingMode, useBWA, useNOVO,  useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK, readFreqCutoff_SAMTOOLS,    filterMappabilityPositions, filterCustomPositions,    filterOnKeywords , tempDir1, tempDir2, mappers, variantTools, minCov, minMappedReads = loadSettingsFile(cpu_count,memory)
    #binDir, globalDir, userPrefcpu , userPrefmem,  inputDir, outputDir, readsType, userRef, trimMethod, BQSRPossible, emblFile, variantTools, prev_cpu_count,prev_memory, outputDir, userRef, trimmingMode, useBWA,    useNOVO, useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK,    mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS,    minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK,    readFreqCutoff_SAMTOOLS,  ,    filterCustomPositions,    filterOnKeywords ,  tempDir1, tempDir2 = loadSettingsFile(cpu_count,memory)
    #########################################################################################
##    print "-"*70
##    print "Input Folder containing FASTQ files: ",[tempDir1]
##    print "Output Folder: ",[tempDir2]
##    print "-"*70
    skip = "?"
    try:
        os.chdir(tempDir1)
    except:
        print "could not access FASTQ directory:",tempDir1,"user will be prompted to provide valid path..."
        skip = "N"  
    try:
        os.chdir(tempDir2)
    except:
        print "could not access valid output directory",tempDir2,"user will be prompted to provide valid path..."
        skip = "N"

    if skip == "?": #if the user has a choice since the input and outpur paths exist
        while True and not skipSetup:
            skip = raw_input("are these the correct settings to use?  Y/N,  Q = quit:")
            if skip not in ["Y","y","N","n","Q","q"]:
                continue
            else:
                break
    if skip == "Q" or skip == "q":
        print "exiting program"
        exit(0)
    
    ############################################################################################################################################################################
    if skip == "Y" or skip == "y" or skipSetup:
        print "Not altering current settings, exiting setup"
        annotationAllowed, BQSRPossible, emblFile = validateRefFiles(refDir,userRef)
        if not annotationAllowed:
            print "Please refer to the manual for providing a suitable reference folder."
            print "Variant annotation will NOT be supported if you deceide to continue..."
            while True:
                ans = raw_input("press Q to quit or C to continue without annotation support: ")
                if ans == "Q" or ans == "q":
                    exit(0)
                elif ans =="C" or ans == "c":
                    break    
        junkterms = []
        if filterOnKeywords:
            #if True:
            try:
                os.chdir(globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/")
                for fileZ in os.listdir(globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/"):
                    if fileZ.endswith(".txt"):
                        fjunk = open(fileZ,'r')
                        for line in fjunk:
                            junkterms.append(line.replace("\n",""))
                        fjunk.close()
                        break
            except:
                print [filterOnKeywords]
                raw_input("Error loading keywords to exclude from: "+globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/"+"\tPress enter to contiune")
                
        filterSettings = [useBWA, useNOVO,   useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK,    readFreqCutoff_SAMTOOLS,    filterMappabilityPositions,filterCustomPositions,    filterOnKeywords, junkterms, minCov, minMappedReads]
        return binDir, globalDir, prev_cpu_count , prev_memory,  inputDir, outputDir, reads_type, userRef, trimmingMode, annotationAllowed, BQSRPossible, emblFile, mappers, variantTools, filterSettings
    ############################################################################################################################################################################
    #User wants to modify settings / enter new settings
    print "Settings require update, entering setup"
    print cpu_count,'CPU cores and',
    print memory,'mb free memory detected.'
  
    flag = False
    ans = False

    refOptions = [name for name in os.listdir(refDir) if os.path.isdir(os.path.join(refDir, name))]
    refOptions.sort()
    
    while not flag:
        counter = 0
        print "--------------------------------------------"
        print "Please select a reference from the selection below:"
        for ref in refOptions:
            counter += 1
            print str(counter)+":\t",ref
        print "Q: quit\n"
        
        selectedRef = raw_input("Enter the corresponding number for the reference (1,2,3 etc): ")
        if selectedRef =="q" or selectedRef =="Q":
            quit()
        try:
            selectedRef = int(selectedRef)
        except:
            selectedRef = "N/A"
        if selectedRef not in range(1,len(refOptions)+1): 
            continue
        else:
            print "Reference selected:", refOptions[selectedRef-1]
            userRef = refOptions[selectedRef-1]
            #Changes all user_ref to userRef 
            break
    annotationAllowed, BQSRPossible, emblFile = validateRefFiles(refDir,userRef)
    
    if not annotationAllowed:
        print "Please refer to the manual to create a reference folder"
        print "Annotation will NOT be supported if you deceide to continue"
        while True:
            ans = raw_input("press enter Q to quit or C to continue without annotation support")
            if ans == "Q" or ans == "q":
                exit(0)
            elif ans =="C" or ans == "c":
                annotationAllowed = False
                break
  
    while not flag:
        print
        #raw_input("debuggin override")
        #userPrefcpu = "2"
        userPrefcpu = raw_input("How many CPU cores would you like to use (recommended amount: "+str(cpu_count)+" cores):")
        try:
            userPrefcpu = int(userPrefcpu)
        except:
            print "not a valid input"
            continue
        
        if userPrefcpu > int(cpu_count):
            ans = raw_input("Your system does not appear to have",userPrefcpu,"cores, continue anyway? Y/N:")
        elif int(userPrefcpu) <= 0:
            print "not a valid input"
            continue
        if ans == "N" or ans == "n":
            continue
        #raw_input("debugging override mem")
        #userPrefmem = "10000"
        userPrefmem = raw_input("How much memory (in Mb) would you like to allocate to this process? (recommended "+str(int(memory))+"):")
        try:
            userPrefmem = int(userPrefmem)
        except:
            print "not a valid input"
            continue
        
        if int(userPrefmem) > int(memory):
            ans = raw_input("Your system does not appear to have "+userPrefmem+" memory, continue anyway? Y/N:")
        if ans == "N" or ans == "n":
            continue
        if int(userPrefmem <= 100):
            print "Invalid amount, try again"
            continue
        flag = True

    flag = False
    while not flag:
        print ("Is your data Paired-end, Single-end reads or both (mixed)? ")
        #raw_input("read type override")
        #reads = "1"
        reads = raw_input("1 = paired-end 2 = single end, 3 = both (mixed): Q = quit:")
        if reads == 'Q' or reads == 'q':
            print "exiting program"
            exit(0)
        elif reads == "1" or reads == "2" or reads == "3":
            flag = True
    if reads =="1":
        reads = "pairedEnd"
    elif reads == "2":
        reads = "singleEnd"
    elif reads == "3":
        reads = "mixed"
    #params.reads = reads
    validDir = False
    workingDir = ""
    while not validDir:
        print
        #raw_input("debugging override here, remove this")
        #workingDir = "/home/pagit/USAP/demo_data/"
        workingDir = raw_input("Enter directory containing your FASTQ files to be processed, for example /home/user/USAP/FASTQ, enter Q to quit:")
        if workingDir == 'Q' or workingDir == 'q':
            print "halting program"
            exit(0)
##        print workingDir    
        if workingDir[0] <> "/":
            workingDir = "/"+workingDir
        if workingDir[-1] <> "/":
            workingDir += "/"
##        print workingDir
##        raw_input("matching?")
            
        try:  #Check if working dir exists
            os.chdir(workingDir)
            print "directory accepted"
            if not checkFileNames(workingDir,reads): #check if there are suitable fastQ files and read access
                print "No suitable FASTQ files could be found in the provided input folder"
                print "Will now prompt user to re-enter input folder containing suitable input files"
                validDir = False
                continue
            else:
                validDir = True
        except:         
            validDir = False
            print "there is no such directory found: ",workingDir
            print 
            if "\\" in workingDir:
                print "make sure to use '/' and not '\\'"
                continue

    validDir = False
    while not validDir:
        print
        #raw_input("debugging override here, remove this 2")
        #outputDir = "/media/sf_VBOXSHARE/ttt/" #home/pagit/USAP/demo_data/"
        outputDir = raw_input("Enter your output directory to which you have write access (example: /home/user/NGS-DATA-OUT) or enter Q to quit:")
        if outputDir == 'Q' or outputDir == 'q':
            print "halting program"
            exit(0)

        if outputDir[0] <> "/":
            outputDir ="/"+outputDir 
        if outputDir[-1] <> "/":
            outputDir += "/"
        try:                        #Check if working dir exists
            os.chdir(outputDir)
            validDir=True
            print "directory accepted"
            break
        except:       
            if "\\" in outputDir:
                print "make sure to use '/' and not '\\'"           
                continue
            print "no such directory exists, would you like to create it? Y/N, Quit= Q"
            ans = raw_input()
            if ans =="q" or ans =="Q":
                exit(0)
        
            if ans =="n" or ans =="N":
                continue #retry entering the dir
                
            if ans == "Y" or ans == "y":
                try:
                    if outputDir[-1] <> "/":
                        outputDir+="/"
                    os.mkdir(outputDir)
                    os.chdir(outputDir)
                    validDir = True
                    print outputDir,"directory created"
                except:
                    print "could not create ",outputDir,"make sure file permissions are set correct to allow write access."
                    continue

    flag = False
    while not flag:
        print "Select read trimming method:"
        #raw_input("override trim")
        #trimMethod = "1"
        trimMethod = raw_input("1 = Quality Trimming (recommended method), 2 = fixed amount, 3 = no trimming (not recommended), Q = quit:")
        if trimMethod == 'Q' or trimMethod == 'q':
            print "halting program"
            exit(0)

        elif trimMethod == "1" or trimMethod == "2" or trimMethod == "3":
            flag = True

    if trimMethod =="1":
        trimMethod = "Quality_Trim"
    elif trimMethod == "2":
        trimMethod ="Fixed_Amount_Trim"
    elif trimMethod == "3":
        raw_input("Please note that using this setting requires all fastq files to be Gzipped and thus to end with .gz, press enter to continue")
        trimMethod ="No_Trim"
        #print "Warning: To use this option all input fastq files must be in compressed format."
        #raw_input("Please ensure all input fastQ files are uncompressed before continuing, press enter to continue")

    #get mapper settings and variant calling algorithms
    ans_temp = None
    while ans_temp not in ["Y","y","n","N"]:
        print "-------------------------------------------------------"
        print "Previous mapper settings were:"
        
        for x in mappers:
            #print [x]
            print x[0]+" = "+str(x[1])
        print "-------------------------------------------------------"
        print "Previous variant detection tools used were:"
        
        for x in variantTools:
            #print [x]
            print x[0]+" = "+str(x[1])
        ans_temp = raw_input("would you like to change these settings? [Y/N]:")
    if ans_temp in ["y","Y"]:
        flag = True 
        while flag:
            print "Please toggle the mappers to use by entering the corresponding number (enter 'Y' to accept current settings)"
            print "Mapping algorithms:"
            pos = 0
            for x in mappers:
                pos += 1
                print str(pos)+"\t"+x[0],":",x[1]
            print "Enter the corresponding digit to toggle the use of specific mappers and variant callers, press 'Y' to accept current settings"
            ans = raw_input("Selection: ")
            if ans == "Y" or ans == "y":
                numMappers = 0
                for mapper in mappers:
                    if mapper[1] == True:
                        numMappers +=1
                if numMappers > 0:
                    flag = False
                    print numMappers, "mappers selected."
                    print
                else:
                    print "error, must select at least one mapper"
                continue
            if ans not in ["0","1","2","3","4","5","6","7","8","9"]:
                continue
            if int(ans) > len(mappers):
                print "Error,invalid selection"
                continue
            mappers[int(ans)-1][1] = not(mappers[int(ans)-1][1])

        flag = True 
        while flag:
            print "Please toggle the variant callers to use by entering the corresponding number (enter 'Y' to accept current settings)"
            print "Variant detection tools:"
            pos = 0
            for x in variantTools:
                pos += 1
                print str(pos)+"\t"+x[0],":",x[1]   
            #for x in filterSettings:
            #    print x[0],":",x[1]
            print "Enter the corresponding digit to toggle the use of specific mappers and variant callers, press 'Y' to accept current settings"
            ans = raw_input("Selection: ")
            if ans == "Y" or ans == "y":
                numMappers = 0
                for mapper in mappers:
                    if mapper[1] == True:
                        numMappers +=1
                if numMappers > 0:
                    flag = False
                    print numMappers, "mappers selected."
                    print
                else:
                    print "error, must select at least one mapper"
                continue
            if ans not in ["0","1","2","3","4","5","6","7","8","9"]:
                continue
            if int(ans) > len(variantTools):
                print "Error,invalid selection"
                continue
            variantTools[int(ans)-1][1] = not(variantTools[int(ans)-1][1])
                
            
    if ["GATK",True] in variantTools:
        gatkFlag = True
    else:
        gatkFlag = False
    if ["SAMTOOLS",True] in variantTools:
        samtoolsFlag = True
    else:
        samtoolsFlag = False
    if ["BWA",True] in mappers:
        useBWA = True
    else:
        useBWA = False
    if ["NOVOAlign",True] in mappers:
        useNOVO = True
    else:
        useNOVO = False
    if ["SMALT",True] in mappers:
        useSMALT = True
    else:
        useSMALT = False
        
    extraSettingsAns = None    
    while extraSettingsAns not in ["Y","y","n","N"]:
        print "The previous variant filtering settings were:"
        print "mapperCount_GATK:",mapperCount_GATK 
        print "mapperCount_SAMTOOLS:",mapperCount_SAMTOOLS 
        print "qualityCutOff_GATK:",qualityCutOff_GATK 
        print "qualityCutOff_SAMTOOLS:",qualityCutOff_SAMTOOLS
        print "minCoverage_GATK:",minCoverage_GATK
        print "minCoverage_SAMTOOLS",minCoverage_SAMTOOLS
        print "readFreqCutoff_GATK:",readFreqCutoff_GATK
        print "readFreqCutoff_SAMTOOLS:",readFreqCutoff_SAMTOOLS
        print "filterMappabilityPositions:",filterMappabilityPositions
        print "filterCustomPositions:",filterCustomPositions
        print "filterOnKeywords:",filterOnKeywords #junkterms - reads from folder FilterKeyWords
        print "minimum reference genome coverage to pass QC:",minCov #for summary QC pass/fail
        print "minimum percentage mapped reads to pass QC:",minMappedReads #junkterms - reads from folder FilterKeyWords
        extraSettingsAns = raw_input("Would you like to change these settings? [Y/N]:")
        print
        
    if extraSettingsAns in ["Y","y"]: 
        if gatkFlag:
            mapperCount_GATK = None
            while mapperCount_GATK not in ["0","1","2","3"]:    
                mapperCount_GATK = raw_input("Number of mappers that must agree on a variant using GATK variant detection tool? (defualt = 3)")
            mapperCount_GATK= int(mapperCount_GATK)
        else:
            mapperCount_GATK = 0
        
        if samtoolsFlag:
            mapperCount_SAMTOOLS = None
            while mapperCount_SAMTOOLS not in ["0","1","2","3"]:    
                mapperCount_SAMTOOLS = raw_input("Number of mappers that must agree on a variant using samtools mpileup variant detection tool? (defualt = 3)")
            mapperCount_SAMTOOLS= int(mapperCount_SAMTOOLS)
        else:
            mapperCount_GATK = 0
            
        if gatkFlag:
            flag = False
            while not flag:
                qualityCutOff_GATK = raw_input("qualityCutOFF for GATK detected variants? (default = 0)")
                try:
                    qualityCutOff_GATK = int(qualityCutOff_GATK)
                    flag = True
                except:
                    print "Invalid input."
                    flag = False
        if samtoolsFlag:
            flag = False
            while not flag:
                qualityCutOff_SAMTOOLS = raw_input("qualityCutOFF for samtools mpileup detected variants? (default = 0)")
                try:
                    qualityCutOff_SAMTOOLS = int(qualityCutOff_SAMTOOLS)
                    flag = True
                except:
                    print "Invalid input."
                    flag = False
        if gatkFlag:        
            flag = False
            while not flag:
                print "Mutant read frequency (proportion of 'mutant' to 'Wild-Type' reads to use for filtering cutoff."
                readFreqCutoff_GATK = raw_input("GATK variant read frequency cutoff: enter a value between 0 and 1 (default = 0.5) :")
                try:
                    readFreqCutoff_GATK = float(readFreqCutoff_GATK)
                    flag = True
                    if readFreqCutoff_GATK > 1 or readFreqCutoff_GATK < 0:
                        print "invalid input"
                        flag = False
                except:
                    print "Invalid input."
                    flag = False
                
        if samtoolsFlag:        
            flag = False
            while not flag:
                print "Read frequency: The proportion of mutant:Wild-Type reads to use for filtering cutoff."
                readFreqCutoff_SAMTOOLS = raw_input("Samtools variant read frequency cutoff: enter a value between 0 and 1 (default = 0.5) :")
                try:
                    readFreqCutoff_SAMTOOLS = float(readFreqCutoff_SAMTOOLS)
                    flag = True
                except:
                    print "Invalid input."
                    flag = False      
        if gatkFlag:     
            flag = False
            while not flag:
                print ""
                minCoverage_GATK = raw_input("Please enter the minimum coverage cutoff for GATK variants: ")
                try:
                    minCoverage_GATK = int(minCoverage_GATK)
                    flag = True
                except:
                    print "Invalid input."
                    flag = False
        if samtoolsFlag:     
            flag = False
            while not flag:
                print ""
                minCoverage_SAMTOOLS = raw_input("Please enter the minimum coverage cutoff for samtools variants: ")
                try:
                    minCoverage_SAMTOOLS = int(minCoverage_SAMTOOLS)
                    flag = True
                except:
                    print "Invalid input."
                    flag = False
        
        filterMappabilityPositions = False
        flag = False
        while not flag:
            print ""
            filterMappabilityPositions = raw_input("Would you like to filter out regions of low mappabaility ? (Note: You will need to have run the Genome mappability score analyzer wrapper script first, located under USAP extra features) [Y/N]: ")
            if filterMappabilityPositions in ["Y","y"]:
                filterMappabilityPositions = True
                flag = True
                try:
                    os.chdir(refDir+"/"+userRef+"/Mappability/") #test to see if this was run 
                except:
                    raw_input("It does not appear as though the Genome Mappability Script has been run for your reference yet, no folder was found called:"+refDir+"/"+userRef+"/Mappability/\tPress enter to continue")
                    filterMappabilityPositions = False
                    flag = True
            elif filterMappabilityPositions in ["N","n"]:
                filterMappabilityPositions = False
                flag = True
            else:
                flag = False
        print
        filterSpecificPositions = False
        while filterSpecificPositions not in ["y","Y","N","n"]:
            filterSpecificPositions = raw_input("Would you like to exclude custom variants detected in the exclustion folder under "+globalDir+"/Reference/"+userRef+"/EXCLUDE/"+" ? [Y/N]:")
        if filterSpecificPositions in ["Y","y"]:
            filterSpecificPositions = True
            try:
                os.chdir(globalDir+"/Reference/"+userRef+"/EXCLUDE/")
            except:
                filterSpecificPositions = False
                raw_input("It does not appear as though the Genome Mappability Script has been run for your reference yet, no folder was found called:"+refDir+"/"+userRef+"/EXCLUDE/\tPress enter to continue")
        else:
            filterSpecificPositions = False
        print    
        filterOnKeywords = False
        junkterms = []
        while filterOnKeywords not in ["y","Y","N","n"]:
            filterOnKeywords = raw_input("Would you like to filter variants corresponding specific annotation keywords detected in the 'KEYWORDSTOREMOVE' folder under "+globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/"+" ? [Y/N]:")
        if filterOnKeywords in ["Y","y"]:
            try:
            #if True:
                os.chdir(refDir+"/"+userRef+"/KEYWORDSTOEXCLUDE/")
                for fileZ in os.listdir(refDir+"/"+userRef+"/KEYWORDSTOEXCLUDE/"):
                    if fileZ.endswith(".txt"):
                        junkterms = []
                        fjunk = open(fileZ,'r')
                        for line in fjunk:
                            junkterms.append(line.replace("\n",""))
                        fjunk.close()
                        break
                filterOnKeywords = True
            except:
                raw_input("It does not appear as though the folder 'KEYWORDSEXCLUDE' exists. No folder was found called:"+refDir+"/"+userRef+"/KEYWORDSTOEXCLUDE/\tPress enter to continue")
                filterOnKeywords = False
        else:
            filterOnKeywords = False
            
        changeSummaryQCCutoffs = False
        tempAns = ""
        while tempAns.upper() not in ["Y","N"]:
            tempAns = raw_input("Would you like to specify the minimum genome coverage and minimum percentage mapped reads to pass QC?  Y/N: ")
        if tempAns.upper() in ["Y","y"]:
            while True:
                minCov = raw_input("Please enter the minimum genome coverage cutoff (defualt=50):")
                try:
                    minCov = int(minCov)
                    if minCov >= 0: 
                        break
                    else:
                        continue
                except:
                    continue
            while True:
                minMappedReads = raw_input("Please enter the minimum percentage mapped reads cutoff to pass QC (defualt=90):")
                try:
                    minMappedReads = float(minMappedReads)
                    if minMappedReads >= 0 and minMappedReads <= 100:
                        break
                    else:
                        continue
                except:
                    continue
                
    else: #user does not want to alter filtering settings, only need to load junkterms then.
        junkterms = []
        if filterOnKeywords:
            try:
                os.chdir(globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/")
                for fileZ in os.listdir(globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/"):
                    if fileZ.endswith(".txt"):
                        fjunk = open(fileZ,'r')
                        for line in fjunk:
                            junkterms.append(line.replace("\n",""))
                        fjunk.close()
                        break
            except:
                print [filterOnKeywords]
                raw_input("Error loading keywords to exclude from: "+globalDir+"/Reference/"+userRef+"/KEYWORDSTOEXCLUDE/"+"\tPress enter to contiune")
                

    print "-"*40
    print "Updated Settings:"
    print "Detected CPU cores: ",str(cpu_count)+", cores selected:",userPrefcpu
    print "Detected memory (mb):",str(memory)+", memory allocated:",userPrefmem
    print "FastQ directory", workingDir
    print "Output directory", outputDir
    print "reads type:", reads
    print "Refrence Strain selection:", userRef
    print "Trimming method:",trimMethod
    print str(mappers)
    print str(variantTools)
    print "mapperCount_GATK:",mapperCount_GATK 
    print "mapperCount_SAMTOOLS:",mapperCount_SAMTOOLS 
    print "qualityCutOff_GATK:",qualityCutOff_GATK 
    print "qualityCutOff_SAMTOOLS:",qualityCutOff_SAMTOOLS
    print "minCoverage_GATK:",minCoverage_GATK
    print "minCoverage_SAMTOOLS",minCoverage_SAMTOOLS
    print "readFreqCutoff_GATK:",readFreqCutoff_GATK
    print "readFreqCutoff_SAMTOOLS:",readFreqCutoff_SAMTOOLS
    print "filterMappabilityPositions:",filterMappabilityPositions
    print "filterCustomPositions:",filterCustomPositions
    print "filterOnKeywords:",filterOnKeywords #junkterms - reads from folder FilterKeyWords
    print "minimum reference genome coverage to pass QC:",minCov #for summary QC pass/fail
    print "minimum percentage mapped reads to pass QC:",minMappedReads #junkterms - reads from folder FilterKeyWords
    print "-"*40
   
    os.chdir(globalDir)
    
    f=open('userSettings.txt','w')
    f.write("CPU_CORES\t"+str(userPrefcpu)+"\n")
    f.write("SYSTEM_MEMORY\t"+str(userPrefmem)+"\n")
    tempWorkingDir = workingDir
    if tempWorkingDir[-1] == "/":
        tempWorkingDir = tempWorkingDir[:-1]
    f.write("FASTQ_DIRECTORY\t"+tempWorkingDir+"\n")
    outputDirTemp = outputDir
    if outputDirTemp[-1] == "/":
        outputDirTemp = outputDirTemp[:-1]
    f.write("OUTPUT_DIRECTORY\t"+outputDirTemp+"\n")
    f.write("READS_TYPE\t"+reads+"\n")
    f.write("reference\t"+userRef+"\n")
    f.write("trimmingMode\t"+trimMethod+"\n")
    ####################################################
    f.write("----------------------------------------------------\n") #8
    f.write("Mapper settings:\n") #9
    f.write("Mapper BWA:\t"+str(useBWA)+"\n") #10
    f.write("Mapper NOVOAlign:\t"+str(useNOVO)+"\n") #11
    f.write("Mapper SMALT:\t"+str(useSMALT)+"\n") #12
    f.write("----------------------------------------------------\n") #13
    f.write("Variant detection settings:\n") #14
    f.write("Variant Detection tools GATK:\t"+str(gatkFlag)+"\n") #15
    f.write("Variant Detection tools SAMTools (mpileup):\t"+str(samtoolsFlag)+"\n") #16
    f.write("----------------------------------------------------\n") # 17
    f.write("Variant Filtering Settings:\n") # 18
    f.write("mapperCount_GATK =\t"+str(mapperCount_GATK)+"\n") # 19
    f.write("mapperCount_SAMTOOLS =\t"+str(mapperCount_SAMTOOLS)+"\n") #20
    f.write("qualityCutOff_GATK =\t"+str(qualityCutOff_GATK)+"\n") #21
    f.write("qualityCutOff_SAMTOOLS =\t"+str(qualityCutOff_SAMTOOLS)+"\n") #22
    f.write("minCoverage_GATK =\t"+str(minCoverage_GATK)+"\n") #23
    f.write("minCoverage_SAMTOOLS =\t"+str(minCoverage_SAMTOOLS)+"\n") #24
    f.write("readFreqCutoff_GATK =\t"+str(readFreqCutoff_GATK)+"\n") #25
    f.write("readFreqCutoff_SAMTOOLS =\t"+str(readFreqCutoff_SAMTOOLS)+"\n") #26
    f.write("filterMappabilityPositions =\t"+str(filterMappabilityPositions)+"\n") #27
    f.write("filterCustomPositions =\t"+str(filterCustomPositions)+"\n") #28
    f.write("filterOnKeywords =\t"+str(filterOnKeywords)+"\n") #29 junkterms - reads from folder FilterKeyWords
    f.write("----------------------------------------------------\n") # 30
    f.write("Minimum_Genome_Coverage =\t"+str(minCov)+"\n") #31
    f.write("Minimum_percentage_mapped_reads =\t"+str(minMappedReads)+"\n") #32
    f.close()
    print "setup completed."
    filterSettings = [useBWA, useNOVO,   useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK,    readFreqCutoff_SAMTOOLS,    filterMappabilityPositions,filterCustomPositions, filterOnKeywords, junkterms, minCov, minMappedReads]
    return binDir, globalDir, userPrefcpu , userPrefmem,  workingDir, outputDir, reads, userRef, trimMethod, annotationAllowed, BQSRPossible, emblFile, mappers, variantTools, filterSettings
    
#################################################################

##########################33
def indexReferences():
    try:
        os.makedirs(params.scripts_BWA)
    except:
        print "overriding existing temporary BWA pipeline scripts"
            
    allRefFiles = []
    fastaList = []
    nessisaryExtBWA = ["dict","amb","ann","bwt","fai","pac","sa"]
    nessisaryExtNOVO = ["ndx"]
    nessisaryExtSMALT =["sma","smi"]
    already_indexed = True
    bwa_indexed = True
    novo_indexed = True
    smalt_indexed = True
    allRefFiles = []

    os.chdir(params.reference)     
    for ref_fasta_file in os.listdir(params.reference):  # fasta each fasta file in ref fasta dir
        allRefFiles.append(ref_fasta_file)

    for fastaFile in allRefFiles:
        if not fastaFile.lower().endswith(".fasta") or fastaFile.lower().endswith(".fa"):
            continue
        fastaList.append(fastaFile)
        already_indexed = True

        print "determining if index nessisary for:",fastaFile
        for ext in nessisaryExtBWA:
            #print ext
            if not fastaFile+"."+ext in allRefFiles:
                
                if ext == "dict":
                    fileExt = fastaFile.split(".")[-1]
                    fastaDictName = fastaFile[:len(fastaFile)-len(fileExt)-1]+".dict"
                    if fastaDictName in allRefFiles:
                        continue
                already_indexed = False
                print fastaFile+" has not been previously indexed -> required file extention is:"+"."+ext,
                print "indexing for BWA:", fastaFile
##                raw_input()
                #bwa index step
                print "Command:",params.bwa,"index",params.reference+fastaFile
                subprocess.call([params.bwa,"index",params.reference+fastaFile])
                os.chdir(params.scripts_BWA)
##                f = open("indexBWAREF.sh",'w')
                #--> subprocess.call("samtools faidx "+params.reference+fastaFile) #replaced with method below due to samtools path issues
                print "creating .fai file:", fastaFile
                #raw_input("ready?")
                path = params.reference
                fileX = fastaFile
                cmd = [params.samtools,'faidx',path+fileX]
                pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out,err = pipe.communicate()
                result = out.decode()
                
                print out
                print err
                #raw_input("press enter, checking ref")
                #if debugMode:
                    
##                subprocess.call("sh "+params.scripts_BWA+"indexBWAREF.sh",shell=True)
                fileExt = fastaFile.split(".")[-1]
                fastaDictName = fastaFile[:len(fastaFile)-len(fileExt)-1]+".dict"            
                subprocess.call(params.java7+ " -jar "+params.picardCreateSequenceDictionary+" REFERENCE="+params.reference+fastaFile+" OUTPUT="+params.reference+fastaDictName, shell=True)
                for ref_fasta_file in os.listdir(params.reference):  # fasta each fasta file in ref fasta dir
                    if ref_fasta_file not in allRefFiles:
                        allRefFiles.append(ref_fasta_file)
##            break #--> continue to index with next mapper


        ###Indexing for novoalign --> ."ndx"
        fileExt = fastaFile.split(".")[-1]
        NOVORefName = fastaFile[:len(fastaFile)-len(fileExt)-1]+".ndx"
        if not NOVORefName in allRefFiles:
            already_indexed = False
            print "indexing for NOVOAlign:", fastaFile
##                print "debugging12345"
##                print "1",params.novoIndex
##                print "2",params.reference+NOVORefName
##                print "3",params.reference+fastaFile
##                print "and"
##                print [params.novoIndex,params.reference+NOVORefName,params.reference+fastaFile]
##                raw_input("ok?")
            os.chdir(params.reference)
            ftemp = open(params.reference+fastaFile,'r')
            ftemp.close()
            
            os.chdir(params.reference)
##                subprocess.call([params.novoIndex,params.reference+NOVORefName,params.reference+fastaFile])
            
            cmd = [params.novoIndex,params.reference+NOVORefName,params.reference+fastaFile]
            pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
            print "Result : ", [result]
            print "novoindex complete"

        ###Indexing for smalt --> .sma and .smi"
        fileExt = fastaFile.split(".")[-1]
        SMALTRefName = fastaFile[:len(fastaFile)-len(fileExt)-1]
        for ext in nessisaryExtSMALT:
            if not SMALTRefName+"."+ext in allRefFiles:
                already_indexed = False
                print "indexing for SMALT:", fastaFile
                os.chdir(params.reference)
                statinfo = os.stat(fastaFile) #(33188, 422511L, 769L, 1, 1032, 100, 926L, 1105022698,1105022732, 1105022732)
                byteSize = statinfo.st_size
                #  4411540 bacteria 
                #100000000 large
                if byteSize < 100000000:
                    print "using stepsize 1 for smalt index"
                    subprocess.call([params.smaltBinary,"index","-k","13","-s","1",params.reference+SMALTRefName,params.reference+fastaFile])
                else:
                    print "using stepsize 6 for smalt index"
                    subprocess.call([params.smaltBinary,"index","-k","13","-s","6",params.reference+SMALTRefName,params.reference+fastaFile])
            break

    if already_indexed:
        print "All reference files previously indexed"
    return fastaList
##################################################################################
def calculate_coverage_bed(inputFolder):      
    os.chdir(inputFolder)
    resultFile = open("Genome_Coverage_Results_Summary.txt",'w')
    resultFile.write("Sample\tCoverage\n")

    for fileX in os.listdir(inputFolder):
        if not fileX.endswith("genomecov_bed.txt"):
            continue
        print "Processing deletion data for:",fileX
        f = open(fileX,"r")
        #f.readline()
        cov = 0
        genome = 0
        #prevLine = "begin"
        for line in f:
            temp = line.split()
            if not line or temp == [] or temp == "":
                continue
            start = temp[1]
            end = temp[2]
            for x in range(int(start),int(end)):
                try:
                    genome += 1 #int(temp[3])
                    cov += float(int(temp[3]))
                except:
                    print "error calculating genome coverage"
                    continue
        f.close()

        if "_" in f.name:
            tempName = f.name.split("_")[0]
            try:
                resultFile.write(tempName+"\t"+str(int(round(float(cov)/genome,2)))+"\n")
            except:
                print "Error calculating genome coverage"
                resultFile.write(tempName+"\tERROR\n")
                
        else:
            try:
                resultFile.write(f.name+"\t"+str(int(round(float(cov)/genome,2)))+"\n")
            except:
                print "Error calculating genome coverage"
                resultFile.write(tempName+"\tERROR\n")
                
##        print "coverage calculation"
##        print "total reads", str(cov)
##        print "total bp", str(genome)
##        print "ave coverage", float(cov) / genome
    resultFile.close()
    return
######################################################################

##################################################################################
def calculate_coverage(inputFolder):      
    os.chdir(inputFolder)
    resultFile = open("Genome_Coverage_Results_Summary.txt",'w')
    resultFile.write("Sample\tCoverage\n")

    for fileX in os.listdir(inputFolder):
        if not fileX.endswith("genomecov.txt"):
            continue
        f = open(fileX,"r")
        f.readline()
        cov = 0
        genome = 0
        #prevLine = "begin"
        for line in f:
            temp = line.split()
            if not line or temp == [] or temp == "":
                continue
            genome += 1
            try:
                cov += float(temp[-1])
            except:
                print "error processing genome coverage line:", line
        f.close()

        if "_" in f.name:
            tempName = f.name.split("_")[0]
            try:
                resultFile.write(tempName+"\t"+str(int(round(float(cov)/genome,2)))+"\n")
            except:
                print "Error calculating genome coverage"
                resultFile.write(tempName+"\tERROR\n")
                
        else:
            try:
                resultFile.write(f.name+"\t"+str(int(round(float(cov)/genome,2)))+"\n")
            except:
                print "Error calculating genome coverage"
                resultFile.write(tempName+"\tERROR\n")
                
##        print "coverage calculation"
##        print "total reads", str(cov)
##        print "total bp", str(genome)
##        print "ave coverage", float(cov) / genome
    resultFile.close()
    return
######################################################################
def loadPostitionsToRemove(exclustionListFolder):
    positions = {}
    try:
        os.chdir(exclustionListFolder)
    except:
        print "Error, no mappability folder found"
        return positions
    for fileX in os.listdir(exclustionListFolder):
        if not fileX.endswith(".txt"):
            continue
        f = open(fileX,'r')
        for line in f:
            temp = line.split("\t")
            pos = temp[0]
            try:
                pos = int(pos)
            except:
                continue
            if pos not in positions:
                positions[pos] = True 
        f.close()
    if positions == {}:
        print "No positions to exclude could be found in folder: ", exclustionListFolder
    return positions
##########################################################   
def RemoveJunkFromVCF5(annotatedDir,outputDir,junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutOff_GATK,readFreqCutOff_SAMTOOLS,exclude_list,filterSpecificPositions, gatkFlag, samtoolsFlag):
    '''
    This is the main filter step to remove:
    snps not called by at least n mappers
    snps which dont have qual above cutoff 
    snps with annotation data containing key words for filtering :pe ppe pgrs repeat etc
    snps with coverage below min cov cutoff
    snps which are present in less than X% of reads, so only those above X% are kept, the rest is heterogenous / seq error.

    It looks for the x, x, x rows for the bwa/novo/smalt quality values and requires that the amount of mappers that you specifify...
    ...be above the quality value that you specificy
    '''
    def extractKeyPositionsFromHeader(header):
        #Here keyWordList contains names of the columns we want to filter based on the column value
        keyWordDict = {}
        keyWordDict["pos"] = None
        
        keyWordDict["qual_BWA_GATK"] = None
        keyWordDict["hetero_freq_BWA_GATK"] = None
        keyWordDict["num_Reads_BWA_GATK"] = None
        
        keyWordDict["qual_BWA_SAMTOOLS"] = None
        keyWordDict["hetero_freq_BWA_SAMTOOLS"] = None
        keyWordDict["num_Reads_BWA_SAMTOOLS"] = None

        keyWordDict["qual_NOVO_GATK"] = None
        keyWordDict["hetero_freq_NOVO_GATK"] = None
        keyWordDict["num_Reads_NOVO_GATK"] = None

        keyWordDict["qual_NOVO_SAMTOOLS"] = None
        keyWordDict["hetero_freq_NOVO_SAMTOOLS"] = None
        keyWordDict["num_Reads_NOVO_SAMTOOLS"] = None
        
        keyWordDict["qual_SMALT_GATK"] = None
        keyWordDict["hetero_freq_SMALT_GATK"] = None
        keyWordDict["num_Reads_SMALT_GATK"] = None
        
        keyWordDict["qual_SMALT_SAMTOOLS"] = None
        keyWordDict["hetero_freq_SMALT_SAMTOOLS"] = None
        keyWordDict["num_Reads_SMALT_SAMTOOLS"] = None

        keyWordPositionDict = {}

        temp = header.split("\t")
        pos = -1
        #print temp
        #raw_input("enter1")
        #print keyWordDict
        #raw_input("enter2")
        for element in temp:
            #print [element], element in keyWordDict
            #print "-"*10
            pos += 1
            if element in keyWordDict:
                keyWordDict[element] = True
                keyWordPositionDict[element] = pos #Dictionary of positions in the annofile that need to extract values from for filtering
        for key in keyWordDict:
            if keyWordDict[key] == None:
                keyWordPositionDict[key] = None
        #print "-------------->", keyWordPositionDict
        return keyWordPositionDict
        ################################################################################################3
            
    def extractDataFromAnnoFileLine(line,keyWordPositionDict):
        dataForFilter = {}
        line = line.split("\t")
        for keyWord in keyWordPositionDict:
            colPos = keyWordPositionDict[keyWord]
            if colPos <> None:
                dataForFilter[keyWord] = line[colPos]
        return dataForFilter
        
    ##########################################################
    def containJunkRegion(stringX,junkTerms):
        for x in junkTerms:
            if x in stringX:
                #print "junk ",x,"in ", stringX
                #raw_input()
                return True #it contains JUNK!
        return False
    ###########################################################
    def checkIfQualFilterPass(m1,m2,m3,qualityCutOFF, mapperCount):
        #here if value is == False (no value) then will convert to 0.0
        if m1 == "":
            m1 = 0.0
        else:
            m1 = float(m1)                
        if m2 == "":
            m2 = 0.0
        else:
            m2 = float(m2)
        if m3 == "":
            m3 = 0.0
        else:
            m3= float(m3)
        count = 0
        if m1 > float(qualityCutOFF):
            count += 1
        if m2 > float(qualityCutOFF):
            count += 1
        if m3 > float(qualityCutOFF):
            count += 1
        if count < mapperCount: 
            return False
        else:
            return True
    ################################################
    def checkIfNumReadsFilterPass(m1,m2,m3, minCoverage, mapperCount):
        #here if value is == False (no value) then will convert to 0.0
        if m1 == "" or m1 == "Calculation error":
            m1 = 0
        else:
            m1 = int(m1)                
        if m2 == "" or m2 == "Calculation error":
            m2 = 0
        else:
            m2 = int(m2)
        if m3 == "" or m3 == "Calculation error":
            m3 = 0
        else:
            m3= int(m3)
        minCovNum = 0
        if m1 > minCoverage:
            minCovNum += 1
        if m2 > minCoverage:
            minCovNum += 1
        if m3 > minCoverage:
            minCovNum += 1
        if minCovNum < mapperCount: #at least mapperCount amount of mapper must pass the coverage cutoff 
            return False
        else:
            return True
    ################################################
    def checkIfMutFreqFilterPass(m1,m2,m3, readFreqCutoff, mapperCount):
        #here if value is == False (no value) then will convert to 0.0
        if m1 == "" or m1 == "Calculation error":
            m1 = 0.0
        else:
            m1 = float(m1)                
        if m2 == "" or m2 == "Calculation error":
            m2 = 0.0
        else:
            m2 = float(m2)
        if m3 == "" or m3 == "Calculation error":
            m3 = 0.0
        else:
            m3= float(m3)
        mutFreqNum = 0
        if m1 > float(readFreqCutoff):
            mutFreqNum += 1
        if m2 > float(readFreqCutoff):
            mutFreqNum += 1
        if m3 > float(readFreqCutoff):
            mutFreqNum += 1
        if mutFreqNum < mapperCount: #at least mapperCount amount of mapper must pass the coverage cutoff 
            return False
        else:
            return True
    ################################################
                                
    totalLoaded = 0
    os.chdir(annotatedDir)
    for fileX in os.listdir(annotatedDir):
        if fileX.endswith(".vcf"):
            totalLoaded +=1
            print "filtering variants for file: ",fileX
            os.chdir(annotatedDir)
            inFile = open(fileX, 'r')
            fileData = []
            header = inFile.readline()
            keyWordPositionDict = extractKeyPositionsFromHeader(header)
            fileData.append(header)
            for line in inFile:
                dataForFilter = extractDataFromAnnoFileLine(line,keyWordPositionDict)
                #print keyWordPositionDict
                #print dataForFilter
                #raw_input("1111111111112222222222222")
##                print line
##                print [line]
                SNPPosition = dataForFilter["pos"]
                if filterSpecificPositions:
                    if int(SNPPosition) in exclude_list:
##                        print "Removing known variant provided by user: ", SNPPosition
##                        raw_input("55555555555555555")
                        continue
                if containJunkRegion(str.lower(line),junkTerms):
##                    print "Skipping due to junk"
##                    raw_input("999999999999")
                    continue
                #Check if qual value acceptable
                #GATK
                if gatkFlag:
                    if not checkIfQualFilterPass(dataForFilter["qual_BWA_GATK"],dataForFilter["qual_NOVO_GATK"], dataForFilter["qual_SMALT_GATK"], qualityCutOff_GATK, mapperCount_GATK):
##                        print "Skipping due to faul qual filter GATK", [dataForFilter["qual_BWA_GATK"], dataForFilter["qual_NOVO_GATK"], dataForFilter["qual_SMALT_GATK"]]
##                        raw_input("999999999999")
                        continue
                #SAMTOOLS
                if samtoolsFlag:
                    if not checkIfQualFilterPass(dataForFilter["qual_BWA_SAMTOOLS"],dataForFilter["qual_NOVO_SAMTOOLS"], dataForFilter["qual_SMALT_SAMTOOLS"], qualityCutOff_SAMTOOLS, mapperCount_SAMTOOLS):
##                        print "Skipping due to faul qual filter SAMTOOLS"
##                        raw_input("999999999999")
                        continue

                #Check if numReads value acceptable
                #GATK
                if gatkFlag:
                    if not checkIfNumReadsFilterPass(dataForFilter["num_Reads_BWA_GATK"], dataForFilter["num_Reads_NOVO_GATK"] , dataForFilter["num_Reads_SMALT_GATK"], minCoverage_GATK, mapperCount_GATK):
##                        print "Skipping due to fail checkIfNumReadsFilterPass GATK"
##                        raw_input("999999999999")
                        continue
                if samtoolsFlag:
                    if not checkIfNumReadsFilterPass(dataForFilter["num_Reads_BWA_SAMTOOLS"] , dataForFilter["num_Reads_NOVO_SAMTOOLS"] , dataForFilter["num_Reads_SMALT_SAMTOOLS"], minCoverage_SAMTOOLS, mapperCount_SAMTOOLS):
##                        print "Skipping due to fail checkIfNumReadsFilterPass SAMTOOLS"
##                        raw_input("999999999999")
                        continue
                #Mut freq cutoff
                if gatkFlag:
                    if not checkIfMutFreqFilterPass(dataForFilter["hetero_freq_BWA_GATK"], dataForFilter["hetero_freq_NOVO_GATK"] , dataForFilter["hetero_freq_SMALT_GATK"], readFreqCutOff_GATK, mapperCount_GATK):
##                        print "Skipping due to fail checkIfMutFreqFilterPass GATK"
##                        raw_input("999999999999")
                        continue
                if samtoolsFlag:
                    if not checkIfMutFreqFilterPass(dataForFilter["hetero_freq_BWA_SAMTOOLS"] , dataForFilter["hetero_freq_NOVO_SAMTOOLS"] , dataForFilter["hetero_freq_SMALT_SAMTOOLS"], readFreqCutOff_SAMTOOLS, mapperCount_SAMTOOLS):
##                        print "Skipping due to fail checkIfMutFreqFilterPass SAMTOOLS"
##                        raw_input("999999999999")
                        continue
                #print "Accepted"
                    
                fileData.append(line)
            inFile.close()

            try:
                os.chdir(outputDir)
            except:
                os.mkdir(outputDir)
                os.chdir(outputDir)
            newVCFFile = open(fileX.replace("ANNO","FILTERED"),'w')
            for x in fileData:            
                newVCFFile.write(x)
            newVCFFile.close()
    print totalLoaded,"files Filtered"
    return 
###############################################################################################
def test_SNP_INDEL_Path(path,variantType):
    try:
        os.chdir(path)
        os.chdir(path+"BWA/"+variantType)
        os.chdir(path+"NOVO/"+variantType)
        os.chdir(path+"SMALT/"+variantType)
        return True
    except:
        print "could not find variant directory for", variantType
        return False
    return None
#######################################################################
def compressDeletionData_bedtools(genCovDir):    
    os.chdir(genCovDir)
    for fileX in os.listdir(genCovDir):
        if "_genomecov=0.txt" not in fileX:
            continue
        f = open(fileX,'r')
        print "extracting deletion data from file:",fileX
        outputData = []
        line = f.readline()

        temp = line.split()
        if temp == []:
            continue
        start = int(float(temp[1])) 
        end = int(float(temp[2]))
        outputData.append((start,end))
        for line in f:
            temp = line.split()
            if temp == []:
                continue
            prevStart = outputData[-1][0]
            prevEnd = outputData[-1][1]
            start = int(float(temp[1])) 
            end = int(float(temp[2]))
            if prevEnd == start: #join data and update
                outputData[-1] = (prevStart,end)
                continue
            else: # add new data range
                outputData.append((start,end))
        f.close()
        f=open(fileX[:-4]+"_collapsed.txt",'w')
        for x in outputData:
            f.write(str(x[0]+1)+"\t"+str(x[1]+1)+"\n")
        f.close()
###############################################        
def compressDeletionData(genCovDir):
    def process_line(line):
        dataCurr = line.split()
        dataCurr = int(dataCurr[0].split(":")[1])
        return dataCurr

    def add_element(element,dataList):
        dataList.append(element)
        return dataList
        
    def update_element(outputData,element):
        previous_element = outputData[-1]
        if type(previous_element) == int: #then its just one element, add one more
    ##        print "adding1"
            previous_element = (previous_element,element)
        elif type(previous_element) == tuple:
    ##        print "adding2"
            previous_element = (previous_element[0],element)
        else:
            print "type error"
            print type(previous_element)
            print previous_element
            raw_input()
        outputData[-1] = previous_element
        return outputData
    
    os.chdir(genCovDir)
    print genCovDir
    for fileX in os.listdir(genCovDir):
        if "_genomecov=0.txt" not in fileX:
            continue
        f = open(fileX,'r')
        print fileX
        outputData = []
        dataCurr = -1
        dataPrev = -1

        #add first element
        line = f.readline()
        dataCurr = line.split()
        if dataCurr == []:
            #print "fatal error, no data found for:",fileX
            #print "in DIR:",genCovDir
            #print [line]
            continue
        dataCurr = int(dataCurr[0].split(":")[1])
        outputData.append(dataCurr)
         
        #check if remaining elements must be collapesed or added individually
        pos = 0
        for line in f:
            pos += 1
            dataPrev = outputData[-1]
            if type(dataPrev) == tuple: #its already a range
                dataPrev = dataPrev[1] #just concider last element (1,1003)
            dataCurr = process_line(line)
            if dataPrev + 1 == dataCurr:
                #update previous to include this number in the number range
                outputData = update_element(outputData,dataCurr)
            else: # add previsous to list
                outputData = add_element(dataCurr,outputData)
        f.close()
        f=open(fileX[:-4]+"_collapsed.txt",'w')
        for x in outputData:
            if type(x) == tuple:
                f.write(str(x[0])+"\t"+str(x[1])+"\n")
            else:
                f.write(str(x)+"\t\n")
        f.close()
#######################################################################################
def loadAnnotationData(dirX):
    #LOADS THE ENTIRE Annotation DATA file into memory
    os.chdir(dirX)
    f = open("ANNO_TABLE_UPDATE_2014.txt","r")
    f = open("AnnotationTable.txt","r") 
    header = f.readline() #skip header
    header = f.readline()
    data = []
    for line in f:
        data.append(line)
    f.close()
    return header,data
#######################################################################################
def lookup(del_startPos,del_endPos,data):
    '''
    This function simply checks if the deletion is inside the start and end
    or spanning the start and end sites
    '''
    matches = []
    del_startPos = int(del_startPos)
    del_endPos = int(del_endPos)

    for line in data:
        tempLine = line.split()
        rvStart = int(tempLine[3])
        rvEnd = int(tempLine[4])
        if (rvStart >= del_startPos) and (rvStart <= del_endPos):
            #The the gene start location falls in the deletion
            matches.append(line)
        elif (rvEnd >= del_startPos) and (rvEnd <= del_endPos):
            #The the gene end location falls in the deletion
            matches.append(line)
        elif (del_startPos > rvStart) and (del_endPos < rvEnd): 
            #The deletion falls inside the gene
            matches.append(line)
        if rvStart > del_endPos:
            return matches
    return matches
######################################################################
def loadDeletionData(inputDir,fileX):
    os.chdir(inputDir)
    data = []
    for tempFile in os.listdir(inputDir):
        if tempFile.split("_")[0] == fileX and "0_collapsed.txt" in tempFile:
            try:
                print "loading", tempFile, "from", inputDir
                f=open(tempFile,'r')
            except:
                print "error, no deletion data found for ,",fileX
                return []
            data=[]
            for x in f:
                temp = x.replace("\n",'')
                data.append(temp.split("\t"))
            f.close()
    return data
########################################################################
def getDeletionStatus(rvStart,rvEnd,deletionData):
    #Screen the entire list of deletions to see if any fall inside
    #the rv start and rv end range
    #rvStart 100
    #rvEnd   150
    #deletionData [[142, ""],[1244,1245], 1500,1600]]
    '''
    takes as input the start and end of each rv number in the annotation data table
    for each it looks in the deletion data to see of the rv number is affeceted by any deletions
    appends deletion status and range, this allows for multiple deletions in a gene
    returns a list: [[1bp del, 100,200],[partial_deletion(right flank), 200,300]]
    '''
    rvStart = int(rvStart)
    rvEnd = int(rvEnd)
    deletion = [] #"none"
    pos = -1
    for x in deletionData: #For each deleion in the list, see if it affects this rvNumber (affects area from rvstart to rvend)
        if rvEnd < int(x[0]): #then all further deletions would also be way to far to the right, no need to continue
            return deletion    #     ====Start=============End===Del=====
        if x[1] == "":
            if int(x[0]) >= rvStart and int(x[0]) <= rvEnd:
                deletion.append(["1bp_deletion",x[0],"-"]) #====Start=====Del========End=====
                continue
            else:
                continue
        #The code below handles deletions which are of a range X to Y (not 1 bp) 
        delStart = int(x[0])
        delEnd = int(x[1])
          
        #case 1 rvnumber falls inside deletion thus rvnumber fully deleted   #=del_S======Start=====End===del_end==
        if delStart <= rvStart and delEnd >= rvEnd: #entire rvnumber deleted
##            print "full deletion found"
##            raw_input()
            deletion.append(["entire_gene_deleted",x[0],x[1]])  
        #case 2 rvnumber spans the left start site of rvnum  #=del_S======Start===del_end======End=====
        elif delStart <= rvStart and delEnd < rvEnd and delEnd > rvStart: #deletion on left part of rvnumber
##            print "partial del found1"
##            raw_input()
            deletion.append(["gene_left_flank_deleted",x[0],x[1]])
        #case 3 rvnumber spans the right start site of rvnum  #===Start===del_start======End==del_end======
        elif delStart > rvStart and delStart < rvEnd and delEnd > rvEnd: 
##            print "partial del found1"
##            raw_input()
            deletion.append(["gene_right_flank_deleted",x[0],x[1]])
        #case 4 deletion falls in central part of rvnum  #===Start===del_start==DEL_ENd====End==== 
        elif delStart > rvStart and delEnd < rvEnd: 
##            print "CENTRAL DELETION found1"
##            raw_input()
            deletion.append(["internal_deletion",x[0],x[1]])

##    print "this is the deletion"
##    print deletion
##    raw_input()
    return deletion

######################################################################
def addAnnoDataToDeletions(outputDir,pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties,mapperOrderList):
    allZeroCovFiles = []
    print "Pooling deletion data..."
    anno_del_dir = outputDir+"ANNOTATED_DELETIONS/"
    try:
        os.mkdir(anno_del_dir)
    except:
        print "could not create ",anno_del_dir,"directory might already exist" 
    os.chdir(anno_del_dir) #The output directory

    #os.chdir(params.globalDir)
    #header, annoData = loadAnnotationData(params.globalDir)
    
    #inputDirBWA = mainPath+"BWA/GenomeCoverage/"
    #inputDirNOVO = mainPath+"NOVO/GenomeCoverage/"
    #inputDirSMALT = mainPath+"SMALT/GenomeCoverage/"
    
    #first load a comprehensive list of 0-cov files, may not have run all mappers
    
    for mapperName in mapperOrderList:
        for fileX in os.listdir(outputDir+mapperName+"/GenomeCoverage/"):
            if fileX.split("_")[0] not in allZeroCovFiles and "genomecov=0_collapsed.txt" in fileX:
                allZeroCovFiles.append(fileX.split("_")[0])
        
    for fileX in allZeroCovFiles: #This is the file abbpreviation
        tempZeroCovFileData = []
        
        print "loading deletion data from:",fileX
        zeroCovDataLists = []
        for mapperName in mapperOrderList:
            print mapperName
            zeroCovDataLists.append(loadDeletionData(outputDir+mapperName+"/GenomeCoverage/",fileX))
        #bwaData = loadDeletionData(inputDirBWA,fileX)
        #novoData = loadDeletionData(inputDirNOVO,fileX)
        #smaltData = loadDeletionData(inputDirSMALT,fileX)
        #Now have 3 lists which contain all the deletions from bwa novo and smalt for this file
        
        os.chdir(anno_del_dir)
        '''
        for each feature number:
            check if affected in each mappper
            if affected store data
            if not skip
        store in list
        sort list
        write data
        '''
        #for line in annoData: changing to make use of the new annotation data format 
        for featureNum in featureNum_to_Anno_DataDict:  
            temp = featureNum_to_Anno_DataDict[featureNum]        #[ranges,feature_type,orientation,temp_features]
            ranges = temp[0]
            for rangeX in ranges:
                tempString = ""
                start = rangeX[0]
                end = rangeX[1]
                deletionSum = 0
                deletionDataNOVO = getDeletionStatus(start,end,zeroCovDataLists[1])
                if deletionDataNOVO <> []:
                    deletionSum = 1
                deletionDataBWA = getDeletionStatus(start,end,zeroCovDataLists[0])
                if deletionDataBWA <> []:
                    deletionSum += 1
                deletionDataSMALT = getDeletionStatus(start,end,zeroCovDataLists[2])
                if deletionDataSMALT <> []:
                    deletionSum += 1
                if deletionSum == 0:
                    continue

                numDels = len(deletionDataBWA) # 1 or 2 typically
                pos = 0
                for x in deletionDataBWA:
                    pos+=1
                    tempString+=(str(x))
##                    delFile.write(str(x))
                    if pos < numDels:
##                        delFile.write(",")
                        tempString+=(",")
                        
##                delFile.write("\t")
                tempString+=("\t")

                numDels = len(deletionDataNOVO) # 1 or 2 typically
                pos = 0
                for x in deletionDataNOVO:
                    pos+=1
##                    delFile.write(str(x))
                    tempString += str(x)
                    if pos < numDels:
##                        delFile.write(",")
                        tempString += ","
##                delFile.write("\t")
                tempString += "\t"

                numDels = len(deletionDataSMALT) # 1 or 2 typically
                pos = 0
                for x in deletionDataSMALT:
                    pos+=1
##                    delFile.write(str(x))
                    tempString += str(x)
                    if pos < numDels:
##                        delFile.write(",")
                        tempString += ","
##                delFile.write("\t"+"del_Sum="+str(deletionSum))
                tempString += "\t"+"del_Sum="+str(deletionSum)+"\t"
                #delFile.write(ranges[0]+"\t"+temp[1]+"\t"+temp[2]+"\t")
##                print temp
##                print "-----------------------------------"
                tempString+=temp[0][0][0]+"\t"
                tempString+=temp[0][0][1]+"\t"
                tempString+=temp[1]+"\t"
                tempString+="'"+temp[2]+"'\t"
                tempDict = {}
##                print temp[3]
                for element in temp[3]:
                    tempDict[element[0]] = element[1]
                for known_feature in known_feature_properties:
##                    print known_feature, known_feature in tempDict
##                    raw_input("ok1!1")
                    if known_feature in tempDict:
                        tempString += tempDict[known_feature]+"\t"
                    else:
                        tempString += " \t"
##                tempString+= "\n"
##                print "this should be written"
##                print tempString
##                raw_input()
                tempData = tempString.split("\t")
                tempZeroCovFileData.append(tempData)
##                print tempZeroCovFileData
##                raw_input("ok which element to sort on?")
        tempZeroCovFileData = sorted(tempZeroCovFileData,key=lambda x: int(x[4]))
        tempString = ""
        delFile = open(str(fileX)+".txt",'w')
        for mapperName in mapperOrderList:
            tempString+=mapperName+"_del_status\t"
        tempString+="Del_sum\t"
        tempString+="GeneStart\tGeneEnd\t"
        tempString+="Feature_type\tOrientation\t"
        header = ""
        for x in known_feature_properties:
            header += x+"\t" 
        header += "\n"
        delFile.write(tempString+header)
        for line_element in tempZeroCovFileData:
##            print [line_element]
##            raw_input()
            for part in line_element:
                #print [part]
                #raw_input()
                delFile.write(part.replace("\n",'').replace("\r","")+"\t")
            delFile.write("\n")
        delFile.close()
        #delFile2.close()
    return
######################################################################
def getFilterSettings(MTB,params, gatkFlag, samtoolsFlag):
    junkTerms = []
    try:
        f = open(params.reference+"filter_settings.txt",'r')
        for line in f:
            temp = line.strip().replace("\n","")
            if temp not in junkTerms:
                junkTerms.append(temp)
        f.close()
    except:
        if MTB:
            f = open(params.reference+"filter_settings.txt",'w')
            junkTerms = ["ppe ","PE/PPE","repeat","PE_PGRS","PE-PGRS","pe family","PGRS family","insertion seqs and phages","Possible transposase"] #,"LowQual","lowqual",'not a real mutation']
            for term in junkTerms:
                f.write(term+"\n")
            f.close()
        else:
            f = open(params.reference+"filter_settings.txt",'w')
            f.close()
##    if autoMode and MTB: #Created for debugging
##        fix the check for auto here 
##        these settings should also be stored in the user settings file
##        there will no longer be an auto mode, use only previouls settings or customize settings
##        or use defualt settings
##        mapperCount_GATK = 3
##        mapperCount_SAMTOOLS = 0
##        qualityCutOff_GATK = 10
##        qualityCutOff_SAMTOOLS = 10
##        minCoverage_GATK = 10
##        minCoverage_SAMTOOLS = 10
##        readFreqCutoff_GATK = 0.5
##        readFreqCutoff_SAMTOOLS = 0.5
##        filterSpecificPositions = False
##        return junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutoff_GATK,readFreqCutoff_SAMTOOLS, filterSpecificPositions


    filterFlag = None
    while filterFlag not in ["y","Y","n","N"]:
        filterFlag = raw_input("Would you like to customize your variant filtering?  Y/N: ")

    if filterFlag.upper() == "Y":        
        print "These are the default filter terms:"
        print junkTerms 
        
        print "Variants containing these keywords in their annotation data will be filtered"
        print "press Y to agree to filter these from all your samples, press N to customize your filter keywords"
        ans = raw_input("Y/N")
        while ans.upper() not in ["Y","N"]:
            ans = raw_input("Y/N")
        if ans.upper() == "N":
            print "You can now manually enter keywords you would like to filter for"
            print "if this keyword appears in any of your annotated variants, then these variants will be exclused from your downstream analysis"
            print "enter each term followed by the return key, enter 'quit' terminate the process"
            print "suggested terms are", junkTerms
            ans2 = []
            count = 0
            while "quit" not in ans2:
                count +=1
                temp = raw_input("filter Term"+str(count)+":")
                if temp.lower() =="quit":
                    break
                else:
                    ans2.append(temp)
            junkTerms = ans2
            print "your new filter terms are:",junkTerms
                            
        if gatkFlag:
            mapperCount_GATK = None
            while mapperCount_GATK not in ["1","2","3"]:    
                mapperCount_GATK = raw_input("mapperCount for GATK variants ? (defualt = 3)")
            mapperCount_GATK= int(mapperCount_GATK)
        else:
            mapperCount_GATK = 0

        if samtoolsFlag:
            mapperCount_SAMTOOLS = None
            while mapperCount_SAMTOOLS not in ["1","2","3"]:    
                mapperCount_SAMTOOLS = raw_input("mapperCount for SAMTOOLS variants ? (defualt = 1)")
            mapperCount_SAMTOOLS= int(mapperCount_SAMTOOLS)
        else:
            mapperCount_SAMTOOLS = 0

        if gatkFlag:
            flag = False
            while not flag:
                qualityCutOff_GATK = raw_input("qualityCutOFF ? (default = 0)")
                try:
                    qualityCutOff_GATK = int(qualityCutOff_GATK)
                    flag = True
                except:
                    flag = False
        if samtoolsFlag:
            flag = False
            while not flag:
                qualityCutOff_SAMTOOLS = raw_input("qualityCutOFF ? (default = 0)")
                try:
                    qualityCutOff_SAMTOOLS = int(qualityCutOff_SAMTOOLS)
                    flag = True
                except:
                    flag = False
        if gatkFlag:        
            flag = False
            while not flag:
                print "Read frequency: The proportion of mutant:Wild-Type reads to use for filtering cutoff."
                readFreqCutoff_GATK = raw_input("Read frequency cutoff: enter a value between 0 and 1 (default = 0.5) :")
                try:
                    readFreqCutoff_GATK = float(readFreqCutoff_GATK)
                    flag = True
                except:
                    flag = False
        if samtoolsFlag:        
            flag = False
            while not flag:
                print "Read frequency: The proportion of mutant:Wild-Type reads to use for filtering cutoff."
                readFreqCutoff_SAMTOOLS = raw_input("Read frequency cutoff: enter a value between 0 and 1 (default = 0.5) :")
                try:
                    readFreqCutoff_SAMTOOLS = float(readFreqCutoff_SAMTOOLS)
                    flag = True
                except:
                    flag = False
                    
        if gatkFlag:     
            flag = False
            while not flag:
                print ""
                minCoverage_GATK = raw_input("Please enter the minimum coverage cutoff: ")
                try:
                    minCoverage_GATK = int(minCoverage_GATK)
                    flag = True
                except:
                    flag = False
        if samtoolsFlag:     
            flag = False
            while not flag:
                print ""
                minCoverage_SAMTOOLS = raw_input("Please enter the minimum coverage cutoff: ")
                try:
                    minCoverage_SAMTOOLS = int(minCoverage_SAMTOOLS)
                    flag = True
                except:
                    flag = False
        filterSpecificPositions = False
        while filterSpecificPositions not in ["y","Y","N","n"]:
            filterSpecificPositions = raw_input("Would you like to exclude custom variants detected in the exclustion folder under "+exclusionListFolder+" ? [Y/N]:")
        if filterSpecificPositions in ["Y","y"]:
            filterSpecificPositions = True
        else:
            filterSpecificPositions = False
    else:
        #Default settings:
        #junkTerms = [] # ["ppe ","PE/PPE","repeat","pe-pgrs","pe_pgrs","pe family","insertion seqs and phages","Possible transposase"]#,"LowQual","lowqual",'not a real mutation']   
        mapperCount_GATK = 3
        mapperCount_SAMTOOLS = 0
        qualityCutOff_GATK = 10
        qualityCutOff_SAMTOOLS = 10
        minCoverage_GATK = 10
        minCoverage_SAMTOOLS = 10
        readFreqCutoff_GATK = 0.5
        readFreqCutoff_SAMTOOLS = 0.5
        filterSpecificPositions = False
        
    return junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutoff_GATK,readFreqCutoff_SAMTOOLS, filterSpecificPositions

def filterDeletions(inputDir,outputDir,mapperCount_GATK,mapperCount_SAMTOOLS,junkTerms):
    mapperCount = max(mapperCount_GATK , mapperCount_SAMTOOLS)
    for fileX in os.listdir(inputDir):
        print "Filtering deletions from file:", fileX
        if not fileX.endswith(".txt"):
            continue
        os.chdir(inputDir)
        f = open(fileX,'r')
        data = []
        data.append(f.readline())
        
        for line in f:
            filterLine = False
            temp = line.split("\t")
            delSum = int(temp[3].split("=")[1])
            if delSum < mapperCount:
                continue
            for term in junkTerms:
                if term in line:
##                    print "filtering this line:", line
                    filterLine = True
                    break
            if not filterLine:
                data.append(line)
        f.close()
        os.chdir(outputDir)
        f=open(fileX[:-4]+"_FILTERED_DEL.txt",'w')
        for x in data:
            f.write(x)
        f.close()
    return    
    

############# START DETERMINE LINEAGES ################
def loadDataLineageDatabase(fileX):

##    os.chdir("C:/Users/rvdm/Dropbox/Ruben Custom Tools/")
    f= open(fileX,'r')
    headerInfo = f.readline().split("\t")
    #load the data into a dictionary
    data = {}
    knownLineages = []
    knownLineagesCounts = {}
    for line in f:
        temp = line.split("\t")
        pos = temp[1]
        lineage = temp[0]
        if lineage not in knownLineagesCounts:
            knownLineagesCounts[lineage] = 1
        else:
            knownLineagesCounts[lineage] += 1
        if lineage not in knownLineages:
            knownLineages.append(lineage)
        change = temp[3]
        if pos not in data:
            data[pos] = [[change,lineage]]
        else:
            data[pos].append([change,lineage])
    f.close()
    knownLineages.sort()
    return data, headerInfo,knownLineages,knownLineagesCounts

def matchVCF_to_Lineage_DB(dirX,fileX,DB,lineageOrder):
##    print dirX,fileX
##    raw_input("__999___")
    os.chdir(dirX)
    f = open(fileX,'r')
    header = f.readline()
    temp = header.split("\t")
    posLookup = {}
    pos = 0
    for x in temp:
        posLookup[x] = pos
        pos += 1
    refOrder = ["ref_NOVO_GATK","ref_BWA_GATK","ref_SMALT_GATK","ref_NOVO_SAMTOOLS","ref_BWA_SAMTOOLS","ref_SMALT_SAMTOOLS"]
    mutOrder = ["mut_NOVO_GATK","mut_BWA_GATK","mut_SMALT_GATK","mut_NOVO_SAMTOOLS","mut_BWA_SAMTOOLS","mut_SMALT_SAMTOOLS"]
    lineage = "NONE"
    lineage_scores = {}
    ref = ""
    mut = ""
    for line in f:
        temp = line.split("\t")
        pos = temp[0]
        if pos in DB: #Then it is a lineage marker
            for comboX in refOrder:
                ref = temp[posLookup[comboX]]
                if ref <> "":
                    break
            for comboX in mutOrder:
                mut = temp[posLookup[comboX]]
                if mut <> "":
                    break
            if len(ref) > 1 or len(mut) >1: # skip indels
                continue                
            for DB_element in DB[pos]: #could be marker for more than one lineage, these are ["A/T","lineage2.2"],[],[]
                #unpack data
                temp_lineage = DB_element[1]
                temp_ref = DB_element[0][0]
                temp_mut = DB_element[0][2]
                if temp_ref not in ["A","T","G","C"] or temp_mut not in ["A","T","G","C"]:
                    print DB_element
                    raw_input("database format error")
                if ref <> temp_ref:
                    print "error, references do not match"
                    print line
                    print DB_element
                    raw_input()
                if ref == temp_ref and mut == temp_mut:
                    #print line
                    #print DB_element
                    #print "found a lineage specific marker"
                    #raw_input()
                    #NOW STORE THE SCORE TOWARDS EACH LINEAGE IN THE SCORE DICTIONARY
                    if temp_lineage not in lineage_scores:
                        lineage_scores[temp_lineage] = 1
                    else:
                        lineage_scores[temp_lineage] += 1
    #print "done loading data for", fileX
    best_lineage_score = 0
    best_lineage_name = "No matches: Either not enough reads or sample is same as reference."
    for lineageName in lineage_scores:
        if int(lineage_scores[lineageName]) > int(best_lineage_score):
            best_lineage_score = lineage_scores[lineageName]
            best_lineage_name = lineageName
        #print best_lineage_name, best_lineage_score
        #raw_input()
    allDataPerLineage = []
    
    for lineage in lineageOrder:
        if lineage not in lineage_scores: #then this lineage had no matches
            allDataPerLineage.append(0)
        else:
            allDataPerLineage.append(lineage_scores[lineage])
##    print best_lineage_name
##    print best_lineage_score
##    print allDataPerLineage
##    raw_input()
    return best_lineage_name, best_lineage_score, allDataPerLineage

def determine_lineages(filteredVariantsDir,lineageFile):
    DB, headerInfo, knownLineages, knownLineageCounts  = loadDataLineageDatabase(lineageFile)
    percentage_results = open(params.mapperOut+"/percentage_lineageData.txt",'w')
    fullResults = open(params.mapperOut+"/full_lineageData.txt",'w')
    fullResults.write("Sample\tClosest_Matching_Lineage\tBest_Score")
#here i want the lineage score for ALL known lineages, the summary file will deceide which to report
    percentage_results.write("Sample\tClosest_Matching_Lineage\tBest_Score")
    for lineage in knownLineages:
        fullResults.write("\t"+lineage)
        percentage_results.write("\t"+lineage)
    fullResults.write("\n")
    percentage_results.write("\n")
        
    for fileX in os.listdir(filteredVariantsDir):
        if not fileX.endswith(".vcf"):
            continue
        print "Detecting known lineage markers in file:", fileX
        lineageName, score, allData = matchVCF_to_Lineage_DB(filteredVariantsDir,fileX,DB,knownLineages)
##        print fileX, [lineageName], [score]
##        print allData
##        raw_input("check if lineage matches here...")
        fullResults.write(fileX+"\t"+lineageName+"\t"+str(score))
        if lineageName not in knownLineageCounts: #Then there was no mathces to lineage DB, could be this is very similar to the refenrece used.
            percentage_results.write(fileX+"\t"+lineageName+"\t"+"NO_MATCHES")
            
        else:
            percentage_results.write(fileX+"\t"+lineageName+"\t"+str(round( 100.0*score / knownLineageCounts[lineageName],2)))
        pos = -1
        for x in allData:
            pos += 1
            #tempLineage = knownLineages[pos]
            fullResults.write("\t"+str(x))
            if lineageName not in knownLineageCounts: #Then there was no mathces to lineage DB, could be this is very similar to the refenrece used.
                percentage_results.write("\t"+"NO_MATCHES")
            else:
                percentage_results.write("\t"+str(round(100.0*x / knownLineageCounts[lineageName],2)))
        fullResults.write("\n")
        percentage_results.write("\n")
##    results.close()
    percentage_results.close()
    fullResults.close()
    return
#########   End determine lineages  ##################################
def hardWareInit(debugMode):
    if params.multiMode:
        params.coreSplit = [0,0,0]
        corePos = 0
        if debugMode:
            print params.cores
        for x in range(int(params.cores)):
            corePos = corePos % 3
            corePos +=1
            params.coreSplit[corePos-1] += 1

        for x in params.coreSplit: #Failsafe 
            if x == 0:
                params.coreSplit = [1,1,1]
                break
            
        params.mem = str(int(params.mem)/ 3000)
        if params.mem == "0":
            params.mem = str(int(params.mem) / 1000)
        if params.mem == "0":
            params.mem = "1"
    else: 
        params.mem = str(int(params.mem) / 1000)
        if params.mem == "0": #Failsafe
            params.mem = "1"
        params.coreSplit = [str(params.cores),str(params.cores),str(params.cores)]
        if params.cores == 0:
            params.coreSplit = ["1","1","1"]  #Failsafe
    return 

######################
def lookupSpoligotypes(spolPredOut,debugMode, mapperOut, binDir):
    dirX = mapperOut+spolPredOut
    os.chdir(dirX)

    count = 0
    #data = []
    names = {}
    for fileX in os.listdir(dirX):
        if not fileX.endswith("spolPredOut.txt"):
            continue
        f = open(fileX,'r')
        line = f.readline()

        temp = line.split()[0]
        octal = line.split()[1]
        while temp.find("/") <> -1:
            temp = temp[temp.find("/")+1:]
        temp = temp.split("_")[0]
        name = temp
        if name not in names:
            names[name] = octal
        else:
            print fileX, name, "already have from", names[name]
    ##        print name,octal
    ##        raw_input()
        f.close()
        count += 1
    f = open("concat_spoligo_all.txt",'w')
    for x in names:
        f.write(x+"\t"+names[x]+"\n")
    f.close()

    print count, "SpolPred files loaded"

    os.chdir(binDir)
    
    lookupDict = {}
    f = open("spolpred_lookup_table.txt",'r')
    for line in f:
        temp= line.replace("\n",'')
        temp= temp.split("\t")
        name = temp[2]
        octal = temp[1]
        #code = temp[0]
    ##    print name
    ##    print octal
    ##    raw_input()
        lookupDict[octal] = name
    f.close()
        
    os.chdir(dirX)
    results = []
    f = open("concat_spoligo_all.txt",'r')
    for line in f:
        temp= line.split()
        name = temp[0]
        octal = temp[1]
        if octal in lookupDict:
            spoligo = lookupDict[octal]
            print "found",spoligo
        else:
            spoligo = "no_match"
        results.append(name+"\t"+octal+"\t"+spoligo+"\n")
    f.close()

    os.chdir(mapperOut) #the main results folder
    
    f=open("SpolPred_Results_Summary.txt",'w')
    f.write("Sample\toctalCode\tStrain_Name\n")
    for x in results:
        if debugMode:
            print x
        f.write(x)
    f.close()
    return
    
###########################################################################################################################################################
def snpDistanceMatrix(dir1,outputDir, outputDir_for_indiv_files,write_all_results,output_File_Name):
    def write_individual_results(file1, file2 ,unique1, unique2,outputDir):
        os.chdir(outputDir)
        f=open(file1.split("_")[0]+"_"+file2.split("_")[0]+".vcf",'w')
        for x in unique1:
            f.write(x)
        f.close()
        
    def merge(left,right,compare):
        result = []
        i,j = 0, 0
        while i < len(left) and j < len(right):
            if compare(int(left[i][0]),int(right[j][0])):
                result.append(left[i])
                i+=1
            else:
                result.append(right[j])
                j+=1
        while (i < len(left)):
            result.append(left[i])
            i+=1
        while (j < len(right)):
            result.append(right[j])
            j+=1
        return result


    def mergeSort(L, compare = operator.lt):
        if len(L) < 2:
            return L[:]
        else:
            middle = int(len(L)/2)
            left = mergeSort(L[:middle], compare)
            right = mergeSort(L[middle:], compare)
            return merge(left, right, compare)

    def getOverlap(a,b):
        #takes two dictionaries, returns the common variants between B and A, (sorted)
        overlapList = []
        match = 0
        for x in a:
            if x in b:
                overlapList.append(a[x]) #[x,a[x]])
        mergeSortedList = mergeSort(overlapList)
        return mergeSortedList

    def subtract(a,b):
        '''
        Snps at same pos can have syn or non-syn- thuse NOT  the same
        ie this function should return 2 lists, one list of all the snps that are at the same position
        and a second list of snps that a exactly the same mutation
        '''
        
        #takes two dictionaries, subtracts all info in B from A,
        #ie only the unique elements in A remain and are returned (sorted).
        exactMatches = []
        positionMatches = [] # - these will be split into the 4 possibilities - A,T,G or C  =  [0,0,2,1]
        #total = the sum of these two above
        uniqueList = []
        match = 0
        for x in a:
            if x not in b: #then the bp pos match, but do the mutations match - fix this later
                uniqueList.append(a[x]) #[x, a[x]])
        return uniqueList


    def loadAllRefereceSNPS_singleFile(dirX,fileX):
        '''
        this creates a dictionary of all the bp position snp info...problem is what about diff mut at same bp pos - use poolData2List instead
        '''
        genome = {} # {100:"b",200:"c"}
        totalLoaded = 0
        totalSNPS = 0
        fileArray = []
        os.chdir(dirX)

        print "reading file: ",fileX
        inFile = open(fileX, 'r')
        for x in range(1): #there is only a one line header
            header = inFile.readline()
        for x in inFile:
            line = x.split('\t')
            if "INTERGENIC" in line.upper():
                extra = '' #\t\t\t\t\t\t\t\t\t\t\t\t\t'
            else:
                extra = ""
            if line[0] not in genome: #this bp pos is already in genome
                genome[line[0]] = x.replace("\n","\t")+extra+str(file)+"\talt="+line[2]+"\n"  #the 1 means one file had this mutation
            else:
                fileCountPostition = len(x)+len(extra)
                genome[line[0]] = genome[line[0]].replace("\n","\t")+str(file)+"\talt="+line[2]+"\n"      
        inFile.close()
        totalSNPS += len(genome)
        #print "A total of ",totalLoaded,"files were loaded which contains a total of",totalSNPS,"SNPS."
        return genome,header

    def compareALL_VS_ALL(dir1,outputdir,outputDir_for_indiv_files,write_all_results,output_File_Name): #strict - must be in all of a all of b
        allFiles = [] # list of all files in the comparison folder
        os.chdir(outputdir)
        for fileX in os.listdir(dir1):
            if fileX.endswith(".vcf"):
                allFiles.append(fileX)
        allFiles.sort()
        
        inFile = open(output_File_Name,'w')
        for x in allFiles:
            inFile.write("\t"+x.split("_")[0])
        inFile.write("\n")
        
        for x in range(len(allFiles)): #x each file from beginning of all files:
            inFile.write(allFiles[x].split("_")[0])
            for y in range(len(allFiles)): # fileY in allFiles y each file from here to the right:
                #print [x,y],
                #load snps for x
                #load snps for y
                #subtract 
                #write output (unique to a, unique to b, overlap, total)
                pooledSNP1,header = loadAllRefereceSNPS_singleFile(dir1,allFiles[x]) 
                pooledSNP2,header = loadAllRefereceSNPS_singleFile(dir1,allFiles[y])         
                unique1 = subtract(pooledSNP1,pooledSNP2)
                unique2 = subtract(pooledSNP2,pooledSNP1)
                numberUniqueA = len(unique1)
                numberUniqueB = len(unique2)
                overlap = getOverlap(pooledSNP1,pooledSNP2) #a list
                lenOverlap = len(overlap)

                ALLUniqueSNPSFROMDIR1= unique1 # = subtract(pooledSNP1,{})
                ALLUniqueSNPSFROMDIR1 = sorted(ALLUniqueSNPSFROMDIR1, key=lambda x: int(x.split("\t")[0]))
                unique2 = sorted(unique2, key=lambda x: int(x.split("\t")[0]))
                overLapList = sorted(overlap, key=lambda x: int(x.split("\t")[0]))
        
                os.chdir(outputdir)
                inFile.write("\t"+str(len(unique1)+len(unique2)))
                if write_all_results:
                    write_individual_results(allFiles[x],allFiles[y],unique1, unique2,outputDir_for_indiv_files)
            inFile.write("\n")
        print "closing "
        inFile.close()
    compareALL_VS_ALL(dir1,outputDir,outputDir_for_indiv_files,write_all_results,output_File_Name)
###############################
def GMA_wrapper(gmaDir, gma_BWA, mapResultsDir, refPath, refName, outputScript):
    try:
        from shutil import copyfile
    except:
        pass  
    def rewrite_fasta_header(fileX):
        os.chdir(mapResultsDir)
        f = open(fileX,'r')
        f.readline()
        rest = f.read()
        f.close()
        f = open(fileX,'w')
        f.write(">"+refName.split(".")[0]+"\n")
        f.write(rest)
        f.close()
    #################################
    #mapResultsDir = refPath+"Mappability/"
    #try:
    #    os.mkdir(mapResultsDir)
    #except:
    #    pass
    ppdDir = mapResultsDir #"/home/pagit/USAP/Reference/MycobacteriumTuberculosis_H37Rv/ppd/"
    
    ref = mapResultsDir+refName #"/home/pagit/USAP/Reference/MycobacteriumTuberculosis_H37Rv/FASTA/"+refName
    original = refPath+"/"+refName #"/home/pagit/USAP/Reference/MycobacteriumTuberculosis_H37Rv/FASTA/"+refName
    #try:
    #print original
    #print mapResultsDir+refName
    print "Copying reference file..."
    copyfile(original,mapResultsDir+refName)
    #except:
    #    pass
    rewrite_fasta_header(mapResultsDir+refName)
    print "indexing reference..."
    cmd = [gma_BWA,'index',ref]
    pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = pipe.communicate()
    result = out.decode()
    print out
    print err
    #raw_input(" this was gma bwa indexing ")

    refName2 = refName.lower().replace(".fasta",'')
    refName2 = refName2.lower().replace(".fa",'')
    s = "#!/bin/bash\n"
    ##s += gmaDir+"\n"
    ##s += "PREPRO=$GMA_DIR/bin/prepro.chr.py\n"
    s += "cd "+ppdDir+"\n"
    s += "python "+gmaDir+"bin/prepro.chr.py "+ref+"\n"

    MAPPER= gmaDir+"bin/mapper"
    REDUCER= gmaDir+"bin/reducer"
    PPD=ppdDir+refName+".ppd" 

    s += "cd "+mapResultsDir 
    s += '''
    for l in 100; do
      for o in 0; do
        for s in 0.02; do
          for i in 0; do
            for d in 0; do
            '''
    s+= "  mkdir "+refName2+".l$l.o$o.qA.s$s.i$i.d$d;\n"
    s+= "          cd "+refName2+".l$l.o$o.qA.s$s.i$i.d$d;\n"
    s += '''
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
    '''
    s+="          cat "+PPD+" | "+MAPPER+" runall -l $l -q A -s $s -i $i -d $d -o $o -t 20 -f ref.fa -b 70 -x "+ref+" -p "+gmaDir+"bin 1> map.txt\n"
    s+= '''
              echo "sorting..."
              cat map.txt | sort > mapsort.txt

              echo "complete"
              echo "====================================="

              echo "analyzing..."
              '''
              #cat mapsort.txt | $REDUCER analyzer -l $l -t 20 -o $o 1> mapred.txt
    s+= "cat mapsort.txt | "+REDUCER+" analyzer -l $l -t 20 -o $o 1> mapred.txt 2> log\n"
              #cat mapsort.txt | $REDUCER analyzer -l $l -t 20 -o $o &> log
              
    s+= '''

              echo "====================================="
              echo "reducer is done"
              echo "====================================="

            done; 
          done;
        done;
      done;
    done;
    '''

    f = open(outputScript,'w')
    f.write(s)
    f.close()
    return
####################
############################################################################################################################################
##############################################################################################
def fixFastq(fileX):
    if fileX.endswith(".fastq.gz"): #gunzip first
        print "uncompressing",fileX
        cmd = ["gunzip",fileX]
        pipe = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = pipe.communicate()
        result = out.decode()
        if "unexpected" in result or "unexpected" in err:
            print result
            print err
    fileX = fileX.replace(".gz",'')
    try:
        f = open(fileX,'r')
    except:
        print "error fixing broken fastq file:",fileX
        return False
    
    #print "fixing", fileX
    newFileName = fileX.replace(".fastq","_fixed.fastq")
    newFile = open(newFileName,'w')
    haveNewHeader = False
    nextHeader = ""
    while True:
        if haveNewHeader:
            header = nextHeader
        else:
            header = f.readline()
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        if not header:
            break
                  
        #if len(line3) == len(line1)+1: #crop last char from line3 probably = "!"
        #    haveNewHeader = False
        #    newFile.write(header)
        #    newFile.write(line1)
        #    newFile.write(line2)
        #    newFile.write(line3[:-2]+"\n")
        #    
        #elif len(line3) <> len(line1)+1 and "!@SL" in line3:
        #    nextHeader = line3[len(line1):]
        #    haveNewHeader = True
        #    newFile.write(header)
        #    newFile.write(line1)
        #    newFile.write(line2)
        #    newFile.write(line3[:len(line1)-2]+"\n")
        #    print "sit1"
        #    print [line1]
        #    print [(line3[:len(line1)-2]+"\n")]
        #    raw_input()
        elif len(line1) <> len(line3): #crop last char from line3 probably = "!"
            #if "@SL" in line3:
            #nextHeader = line3[len(line1):]
            #haveNewHeader = True
            newFile.write(header)
            newFile.write(line1)
            newFile.write(line2)
            newFile.write(line3[:len(line1)-1]+"\n")
            
            #print "sit3"
            #print [line1]
            #print [line3[:len(line1)-2]+"\n"]
            #raw_input()
                          
        else:
            haveNewHeader = False
            newFile.write(header)
            newFile.write(line1)
            newFile.write(line2)
            newFile.write(line3) 

    f.close()
    newFile.close()
    return newFileName
##############################################################################################    
    
def createDirStructure():
    if True:
        os.chdir(params.main)
        print params.main
        try:
            os.makedirs(params.scripts_BWA) #Scripts
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.scripts_NOVO)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.scripts_SMALT)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.scripts_StrainIdentification)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.mapperOut) #Results
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.BWAAligned)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.NOVOAligned)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.SMALTAligned)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.BWAAligned_aln) #Alignment_Files
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.NOVOAligned_aln)
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.SMALTAligned_aln)
        except: "The directory already exists, proceeding"
        picardReport = "picardReport/"   
        try:
            os.makedirs(params.BWAAligned+picardReport) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.NOVOAligned+picardReport) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.SMALTAligned+picardReport) 
        except: "The directory already exists, proceeding"
        genomeCovDir = "GenomeCoverage/"
        try:
            os.makedirs(params.BWAAligned+genomeCovDir) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.NOVOAligned+genomeCovDir) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.SMALTAligned+genomeCovDir) 
        except: "The directory already exists, proceeding"
        snpDir = os.path.join("VARIANTS/") 
        try:
            os.makedirs(params.BWAAligned+snpDir) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.NOVOAligned+snpDir) 
        except: "The directory already exists, proceeding"
        try:
            os.makedirs(params.SMALTAligned+snpDir) 
        except: "The directory already exists, proceeding"
    ##    indelDir = os.path.join("INDELS/") 
    ##    try:
    ##        os.makedirs(params.BWAAligned+indelDir) 
    ##    except: "The directory already exists, proceeding"
    ##    try:
    ##        os.makedirs(params.NOVOAligned+indelDir) 
    ##    except: "The directory already exists, proceeding"
    ##    try:
    ##        os.makedirs(params.SMALTAligned+indelDir) 
    ##    except: "The directory already exists, proceeding"
        spolPredOut = "SpolPredOut/"
        try:
            os.makedirs(params.mapperOut+spolPredOut)
        except:
            "The directory already exists, proceeding"
        return picardReport, genomeCovDir, snpDir, spolPredOut
        
def compareTwoDirectories2_main(dir1,dir2,outputDir):
    class ComparisonVariant(object):
        def __init__(self, pos, mutRefCombo,presentInA,presentInB,filesA,filesB,anno):
            self.pos = int(pos)
            self.mutRefCombo = mutRefCombo
            self.presentInA = presentInA
            self.presentInB = presentInB
            self.filesA = filesA
            self.filesB = filesB
            self.anno = anno
        def addFilesA(self,newFile):
            self.filesA.append(newFile)
            self.presentInA = True
            return
        def addFilesB(self,newFile):
            self.filesB.append(newFile)
            self.presentInB = True
            return

    
    def getRef(line,gatk_bwaRefPos,gatk_novoRefPos,gatk_smaltRefPos,samtools_bwaRefPos,samtools_novoRefPos,samtools_smaltRefPos):
        ref = ""
        for x in [gatk_novoRefPos, gatk_bwaRefPos,gatk_smaltRefPos,samtools_novoRefPos,samtools_bwaRefPos,samtools_smaltRefPos]:
            if line[int(x)] <> "":
                ref = line[int(x)]
                break
        return ref
    def getMut(line,gatk_bwaRefPos,gatk_novoRefPos,gatk_smaltRefPos,samtools_bwaRefPos,samtools_novoRefPos,samtools_smaltRefPos):
        mut = ""
        for x in [gatk_novoRefPos, gatk_bwaRefPos,gatk_smaltRefPos,samtools_novoRefPos,samtools_bwaRefPos,samtools_smaltRefPos]:
            if line[int(x)] <> "":
                mut = line[int(x)]
                break
        return mut
        
    def loadAllSNPS (dir1,dir2,onlySNPS):
        #Takes diff mutation at same pos into account, stores as list inside pos dict.
        mutDict = {}  #dictionary of pos: variant object
        totalLoaded = 0
        os.chdir(dir1)
        for fileX in os.listdir(dir1):
            if not fileX.endswith(".vcf"):
                print "skipping", fileX
                continue
            else:
                totalLoaded +=1
                headerPositions = {}

                print "reading file: ",fileX
                inFile = open(fileX, 'r')
                header = inFile.readline()
                pos = 0
                for htemp in header.split("\t"):
                    headerPositions[htemp] = pos
                    pos += 1
                mut_gatk_bwaRefPos = headerPositions["mut_BWA_GATK"]
                mut_gatk_novoRefPos = headerPositions["mut_NOVO_GATK"]
                mut_gatk_smaltRefPos = headerPositions["mut_SMALT_GATK"] 
                mut_samtools_bwaRefPos = headerPositions["mut_BWA_SAMTOOLS"]
                mut_samtools_novoRefPos = headerPositions["mut_NOVO_SAMTOOLS"]
                mut_samtools_smaltRefPos = headerPositions["mut_SMALT_SAMTOOLS"]      
                
                ref_gatk_bwaRefPos = headerPositions["ref_BWA_GATK"]
                ref_gatk_novoRefPos = headerPositions["ref_NOVO_GATK"]
                ref_gatk_smaltRefPos = headerPositions["ref_SMALT_GATK"] 
                ref_samtools_bwaRefPos = headerPositions["ref_BWA_SAMTOOLS"]
                ref_samtools_novoRefPos = headerPositions["ref_NOVO_SAMTOOLS"]
                ref_samtools_smaltRefPos = headerPositions["ref_SMALT_SAMTOOLS"]                                         
                
                '''
                3 scenarios which can be at same position:
                SNP
                ref = C
                mut = G
                
                INS
                ref = C
                mut = ATGS

                DEL
                ref = CATG
                mut = G
                
                thus must store entry as dictionary using pos:[[ref,alt,fileName],[ref,alt,fileName],[ref,alt,fileName],[ref,alt,fileName]]
                also need {pos:anno} for each position
                '''
                
                for x in inFile:
                    if onlySNPS and "\tINDEL\t" in x:
                        continue
                    line = x.split('\t')
                    pos = line[0]
                    if pos == "":
                        continue
                    ref = getRef(line,ref_gatk_bwaRefPos,ref_gatk_novoRefPos,ref_gatk_smaltRefPos,ref_samtools_bwaRefPos,ref_samtools_novoRefPos,ref_samtools_smaltRefPos)
                    mut = getMut(line,mut_gatk_bwaRefPos,mut_gatk_novoRefPos,mut_gatk_smaltRefPos,mut_samtools_bwaRefPos,mut_samtools_novoRefPos,mut_samtools_smaltRefPos)
                    if pos not in mutDict: #then also not in annoDict
                        mutRefCombo = ref+"/"+mut
                        mutDict[pos] = {}
                        presentInA = True
                        presentInB = False
                        filesA = [fileX]
                        filesB = []
                        annoData = x
                        newVar = ComparisonVariant(pos,mutRefCombo,presentInA,presentInB,filesA,filesB,annoData)
                        mutDict[pos][mutRefCombo] = newVar #can have many files, from a and b
                        #annoDict[pos] = anno
                    else:
                        mutRefCombo = ref+"/"+mut
                        if  mutRefCombo in mutDict[pos]:
                            mutDict[pos][mutRefCombo].addFilesA(fileX)
                        else:
                            presentInA = True
                            presentInB = False
                            filesA = [fileX]
                            filesB = []
                            annoData = x
                            newVar = ComparisonVariant(pos,mutRefCombo,presentInA,presentInB,filesA,filesB,annoData)
                            mutDict[pos][mutRefCombo] = newVar
                inFile.close()
        #now dir2 #####################################################################################  
        os.chdir(dir2)     
        for fileX in os.listdir(dir2):
            if not fileX.endswith(".vcf"):
                print "skipping", fileX
                continue
            else:
                totalLoaded +=1
                headerPositions = {}

                print "reading file: ",fileX
                inFile = open(fileX, 'r')
                header = inFile.readline()
                pos = 0
                for htemp in header.split("\t"):
                    headerPositions[htemp] = pos
                    pos += 1
                mut_gatk_bwaRefPos = headerPositions["mut_BWA_GATK"]
                mut_gatk_novoRefPos = headerPositions["mut_NOVO_GATK"]
                mut_gatk_smaltRefPos = headerPositions["mut_SMALT_GATK"] 
                mut_samtools_bwaRefPos = headerPositions["mut_BWA_SAMTOOLS"]
                mut_samtools_novoRefPos = headerPositions["mut_NOVO_SAMTOOLS"]
                mut_samtools_smaltRefPos = headerPositions["mut_SMALT_SAMTOOLS"]      
                
                ref_gatk_bwaRefPos = headerPositions["ref_BWA_GATK"]
                ref_gatk_novoRefPos = headerPositions["ref_NOVO_GATK"]
                ref_gatk_smaltRefPos = headerPositions["ref_SMALT_GATK"] 
                ref_samtools_bwaRefPos = headerPositions["ref_BWA_SAMTOOLS"]
                ref_samtools_novoRefPos = headerPositions["ref_NOVO_SAMTOOLS"]
                ref_samtools_smaltRefPos = headerPositions["ref_SMALT_SAMTOOLS"]                                         
                
                for x in inFile:
                    if onlySNPS and "\tINDEL\t" in x:
                        continue
                    line = x.split('\t')
                    pos = line[0]
                    if pos == "":
                        continue
                    ref = getRef(line,ref_gatk_bwaRefPos,ref_gatk_novoRefPos,ref_gatk_smaltRefPos,ref_samtools_bwaRefPos,ref_samtools_novoRefPos,ref_samtools_smaltRefPos)
                    mut = getMut(line,mut_gatk_bwaRefPos,mut_gatk_novoRefPos,mut_gatk_smaltRefPos,mut_samtools_bwaRefPos,mut_samtools_novoRefPos,mut_samtools_smaltRefPos)
                    if pos not in mutDict: #then also not in annoDict
                        mutRefCombo = ref+"/"+mut
                        mutDict[pos] = {}
                        presentInA = False
                        presentInB = True
                        filesA = []
                        filesB = [fileX]
                        annoData = x
                        newVar = ComparisonVariant(pos,mutRefCombo,presentInA,presentInB,filesA,filesB,annoData)
                        mutDict[pos][mutRefCombo] = newVar #can have many files, from a and b
                        #annoDict[pos] = anno
                    else:
                        mutRefCombo = ref+"/"+mut
                        if  mutRefCombo in mutDict[pos]:
                            mutDict[pos][mutRefCombo].addFilesB(fileX)
                        else:
                            presentInA = False
                            presentInB = True
                            filesA = []
                            filesB = [fileX]
                            annoData = x
                            newVar = ComparisonVariant(pos,mutRefCombo,presentInA,presentInB,filesA,filesB,annoData)
                            mutDict[pos][mutRefCombo] = newVar
                inFile.close()
        print "Files loaded...",totalLoaded 
        return mutDict, header
#############################################################################
def compareTwoDirectories2(dir1,dir2,outputdir,printFileNames, onlySNPS):
    allSNPS, header =  loadAllSNPS(dir1,dir2,onlySNPS)
    unique1 = []
    unique2 = []
    overlap = []        
    for pos in allSNPS:
        for combo in allSNPS[pos]:
            var = allSNPS[pos][combo] #one varinat, possible many files from a and from b
            if var.presentInA and not var.presentInB: #unique to A
                unique1.append([pos,var])
            elif var.presentInB and not var.presentInA:
                unique2.append([pos,var])
            elif var.presentInA and var.presentInB:
                 overlap.append([pos,var])
            else:
                print "Fatal error"
                print pos, var.presentInA, var.presentInB
                raw_input("Press enter, !!??")
        
        
    unique1 =  sorted(unique1, key=lambda x: int(x[0]))
    unique2 =  sorted(unique2, key=lambda x: int(x[0]))
    overlap =  sorted(overlap, key=lambda x: int(x[0]))

    print "---------------------------------------------------------------------------------------"
    print "Directory comparison results are: "
    print "dir A = ", dir1, " and dir B = ", dir2, " output directory = ", outputdir
    print "Unique SNVs present only in dir A: ", len(unique1) 
    print "Unique SNVs present only in dir B: ", len(unique2) 
    print "Total number of overlapping SNVs present in both dirA and dirB:", len(overlap) 
    print "---------------------------------------------------------------------------------------"

    os.chdir(outputdir)
    f = open("dirA_unique.txt",'w')
    f.write("pos\tref\tmut\tfileCount\tfilesA\tfilesB\t"+header)
    for x in unique1:
        f.write(str(x[1].pos)+"\t") #pos
        f.write(x[1].mutRefCombo.split("/")[0]+"\t")  #ref
        f.write(x[1].mutRefCombo.split("/")[1]+"\t")  #mut
        f.write(str(len(x[1].filesA)+len(x[1].filesB))+"\t")  #total files
        f.write(str(x[1].filesA)+"\t")  #filesA
        f.write(str(x[1].filesB)+"\t")  #filesB
        f.write(x[1].anno)
    f.close()

    f = open("dirB_unique.txt",'w')
    f.write("pos\tref\tmut\tfileCount\tfilesA\tfilesB\t"+header)
    #infile.write("FileCount\tPOS\tREF\tMUTATIONS(BWA/NOVO/SMALT)\tBWA_QUAL\tBWA_INFO\tBWA_EXTRA_INFO\tNOVO_QUAL\tNOVO_INFO\tNOVO_EXTRA_INFO\tSMALT_QUAL\tSMALT_INFO\tSMALT_EXTRA_INFO\tMAPPER_COUNT\tTYPE\tSYN/nonSyn\tAACHANGE\tAACODON\tNAME\tREGION\tLENGTH\tSTART\tEND\tORIENTATION\tPRODUCT\tFUNCTIONALCATAGORY\tFUNCTION\tDR\tPFAM\tGO\tMOLECULARMASS(Dalton)\t\tFILES AND MUTATIONS\n")
    for x in unique2:
        f.write(str(x[1].pos)+"\t") #pos
        f.write(x[1].mutRefCombo.split("/")[0]+"\t")  #ref
        f.write(x[1].mutRefCombo.split("/")[1]+"\t")  #mut
        f.write(str(len(x[1].filesA)+len(x[1].filesB))+"\t")  #total files
        f.write(str(x[1].filesA)+"\t")  #filesA
        f.write(str(x[1].filesB)+"\t")  #filesB
        f.write(x[1].anno)
    f.close()

    f = open("overlap.txt",'w')
    f.write("pos\tref\tmut\tfileCount\tfilesA\tfilesB\t"+header)
    #infile.write("FileCount\tPOS\tREF\tMUTATIONS(BWA/NOVO/SMALT)\tBWA_QUAL\tBWA_INFO\tBWA_EXTRA_INFO\tNOVO_QUAL\tNOVO_INFO\tNOVO_EXTRA_INFO\tSMALT_QUAL\tSMALT_INFO\tSMALT_EXTRA_INFO\tMAPPER_COUNT\tTYPE\tSYN/nonSyn\tAACHANGE\tAACODON\tNAME\tREGION\tLENGTH\tSTART\tEND\tORIENTATION\tPRODUCT\tFUNCTIONALCATAGORY\tFUNCTION\tDR\tPFAM\tGO\tMOLECULARMASS(Dalton)\t\tFILES AND MUTATIONS\n")
    for x in overlap:
        f.write(str(x[1].pos)+"\t") #pos
        f.write(x[1].mutRefCombo.split("/")[0]+"\t")  #ref
        f.write(x[1].mutRefCombo.split("/")[1]+"\t")  #mut
        f.write(str(len(x[1].filesA)+len(x[1].filesB))+"\t")  #total files
        f.write(str(x[1].filesA)+"\t")  #filesA
        f.write(str(x[1].filesB)+"\t")  #filesB
        f.write(x[1].anno)
    f.close()

    print "writing results to :", outputDir
    print "done."
    return
    
    ans = ""
    while ans.upper() not in ["1","2","Q"]:
        print "Select which comparison to make: 1 = SNVS and INDELS, 2 = only SNVS, Q = Quit"
        ans = raw_input("Selection :") 
    if ans in ["Q","q"]:
        return
    if ans == "1":
        onlySNPS = False
    elif ans == "2":
        onlySNPS = True

    compareTwoDirectories2(dir1,dir2,outputDir,True,onlySNPS)
    #############################################################################
    
def setPermissions(globalDir,params):
    def testTool(tool):
        out = "error"
        result = "error"
        err = "error"
        if debugMode:
            print "Testing tool:", tool
        result = ""
        if "fastqc" in tool or "fastx_" in tool:
            cmd = [tool,"-h"]
        elif ".jar" in tool:
            cmd = [params.java7,"-jar",tool]
        else:
            cmd = [tool]
        try:
            pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
##            if debugMode:
##                print "out is", [out]
##                print "err is", [err]
##                print "result is", result
##                print "and here with brackets"
            #    print [result]
            #    raw_input("allowing user to view report, press enter to continue")
        except:
            #permission denied
            print "error testing: ", tool," Will now attempt to fix this error..."
        return out,err,result
    ######################################################################
    def setToolPermission(tool):
        try:
        #change execution permissions
            fix_cmd = ["chmod","770",tool]
            pipe = subprocess.Popen(fix_cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
            print result
            return True
        except:
            return False
    #################################################################################
    def runMake(globalDir,tool):
        try:
            f = open(params.globalDir+"/install.sh",'w')
            f.write("cd "+tool.split("/")[0]+"\n")
            f.write("make\n")
            f.close()
            cmd = ["sh",params.globalDir+"/install.sh"]
            pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
            #if debugMode:
                #print [err]
                #print [result]
        except:
            return False
        return True
    #################################################################################
    print "Testing file permissions of required tools..."
    for tool in params.inits:   
        #raw_input("press enter, now gonna run new tool...")
        out,err,result = testTool(tool)
        if "spolpred" in tool and "Incorrect number of arguments" in err:
            print tool, "--> tested OK."
            continue
        elif "spolpred" in tool:
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "spolpred" in tool and "Incorrect number of arguments" in err:
                print tool, "--> tested OK."
                continue
            elif "spolpred" in tool: #Error not resolved
                print "Error testing: ", tool," attempting to fix this error..."
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        if "smalt" in tool and "Sequence Mapping and Alignment Tool" in result:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "smalt" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "smalt" in tool and "Sequence Mapping and Alignment Tool" in result:
                print tool, "--> tested OK."
                continue
            if "Sequence Mapping and Alignment Tool" not in result: #Error not resolved
                runMake(globalDir,tool[:-4]) #removes the "/src", make is one dir back
                setToolPermission(tool)
                out,err,result = testTool(tool)
            if "smalt" in tool and "Sequence Mapping and Alignment Tool" in result:
                print tool, "--> tested OK."
                continue
            if "Sequence Mapping and Alignment Tool" not in result: #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        
        #####################################################       
        if "bwa" in tool and "alignment via Burrows-Wheeler transformation" in err:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "bwa" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "bwa" in tool and "alignment via Burrows-Wheeler transformation" in err:
                print tool, "--> tested OK."
                toolWorks = True
            if "alignment via Burrows-Wheeler transformation" not in err: #Error not resolved
                runMake(globalDir,tool) 
                setToolPermission(tool)
                out,err,result = testTool(tool)
            if "bwa" in tool and "alignment via Burrows-Wheeler transformation" in err:
                print tool, "--> tested OK."
                toolWorks = True
            if "alignment via Burrows-Wheeler transformation" not in err:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################       
        if "novoalign" in tool and "Novoalign" in result:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "novoalign" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "novoalign" in tool and "Novoalign" in result:
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "Novoalign" not in result:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "IF this tool is no located in the correct folder path it not be accesible to USAP. If you would like to use it, make sure that this tool located in the USAP/Tools/novocraft folder. If this problem persists, check that file permissions are set to allow execution or refer to the user manual.")
                raw_input("press enter to continue without this tool.")
                #exit(0)
                continue
        #####################################################  
        if "novoindex" in tool and "novoindex" in result:
             print tool, "--> tested OK."
             toolWorks = True
             continue
        elif "novoalign" in tool:
             print "Error testing: ", tool," attempting to fix this error..."
             setToolPermission(tool)
             out,err,result = testTool(tool)
             if "novoindex" in tool and "novoindex" in result:
                 print tool, "--> tested OK."
                 toolWorks = True
                 continue
             elif "novoindex" not in result:  #Error not resolved
                 raw_input("Error, could not test-run tool:", tool, "IF this tool is no located in the correct folder path it not be accesible to USAP. If you would like to use it, make sure that this tool located in the USAP/Tools/novocraft folder. If this problem persists, check that file permissions are set to allow execution or refer to the user manual.") 
                 raw_input("press enter to continue without this tool.")
                 #exit(0)
        #####################################################  
        if "picard-tools" in tool and "Option '" in err:
             print tool, "--> tested OK."
             toolWorks = True
             continue
        elif "picard-tools" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
##            raw_input("extra check here fixing 6666666666")
##            print "out", out
##            print "err", err
##            print "result", result
            if "picard-tools" in tool and "Option '" in err:
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "picard-tools" in tool and not ("Option '" in err):  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "GenomeAnalysisTK" in tool and "A USER ERROR has occurred" in err:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "GenomeAnalysisTK" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "GenomeAnalysisTK" in tool and "A USER ERROR has occurred" in err:
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "GenomeAnalysisTK" in tool and "A USER ERROR has occurred" not in err:  #Error not resolved
                print out
                print err
                print result
                raw_input("Error, could not test-run tool:", tool, "IF this tool is no located in the correct folder path it not be accesible to USAP. If you would like to use it, make sure that this tool located in the USAP/Tools/GATK folder. If this problem persists, check that file permissions are set to allow execution or refer to the user manual.") 
                #print "Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set"
                raw_input("press enter to continue without this tool.")
                #exit(0)
                continue
        #####################################################  
        if "fastqc" in tool and "FastQC" in result: 
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "fastqc" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "fastqc" in tool and "FastQC" in result: 
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "fastqc" in tool and "FastQC" not in result:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "java" in tool and "Usage" in err: 
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "java" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "java" in tool and "Usage" in err: 
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "java" in tool and "Usage" not in err:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "genomeCoverageBed" in tool and "genomeCoverageBed" in err: 
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "genomeCoverageBed" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "genomeCoverageBed" in tool and "genomeCoverageBed" in err: 
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "genomeCoverageBed" in tool and "genomeCoverageBed" not in result:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "fastx_" in tool and "usage: " in err or "usage:" in result: 
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "fastx_" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "fastx_" in tool and "usage: " not in err: 
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "fastx_" in tool and not ("usage: " in err):  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "trimmomatic" in tool  and "Usage:" in err: 
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "trimmomatic" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "fastx_" in tool and "Usage:" in err: 
                print tool, "--> tested OK."
                toolWorks = True
                continue
            elif "trimmomatic" in tool and "Usage:" not in err:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        #####################################################  
        if "bcftools" in tool and "Tools for variant calling and manipulating" in err:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "bcftools" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "bcftools" in tool and "Tools for variant calling and manipulating" in err:
                print tool, "--> tested OK."
                toolWorks = True
            if "Tools for variant calling and manipulating" not in err: #Error not resolved
                runMake(globalDir,tool) 
                setToolPermission(tool)
                out,err,result = testTool(tool)
            if "bcftools" in tool and "Tools for variant calling and manipulating" in err:
                print tool, "--> tested OK."
                toolWorks = True
            elif "Tools for variant calling and manipulating" not in err:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)

        #####################################################       
        if "samtools" in tool and "Program: samtools" in err:
            print tool, "--> tested OK."
            toolWorks = True
            continue
        elif "samtools" in tool:
            print "Error testing: ", tool," attempting to fix this error..."
            setToolPermission(tool)
            out,err,result = testTool(tool)
            if "samtools" in tool and "Program: samtools" in err:
                print tool, "--> tested OK."
                toolWorks = True
            if "Program: samtools" not in err: #Error not resolved
                runMake(globalDir,tool) 
                setToolPermission(tool)
                out,err,result = testTool(tool)
            if "samtools" in tool and "Program: samtools" in err:
                print tool, "--> tested OK."
                toolWorks = True
            if "Program: samtools" not in err:  #Error not resolved
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
    print "All tools tested OK"        
    return
    
#####################################################################################################           
                  
def init_GMA(tools): 
    def testTool_gma(tool):
        out = "error"
        result = "error"
        err = "error"
        if debugMode:
            print "Testing tool:", tool
        result = ""
        if "fastqc" in tool or "fastx_" in tool:
            cmd = [tool,"-h"]
        elif ".jar" in tool:
            cmd = [params.java7,"-jar",tool]
        else:
            cmd = [tool]
        try:
            pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
        except:
            #permission denied
            print "error testing: ", tool," Will now attempt to fix this error..."
        return out,err,result
        
    def setToolPermission_gma(tool):
        try:
        #change execution permissions
            fix_cmd = ["chmod","770",tool]
            pipe = subprocess.Popen(fix_cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
            print result
            return True
        except:
            return False
    #################################################################################
    def runMake(globalDir,tool):
        try:
            f = open(params.globalDir+"/install.sh",'w')
            f.write("cd "+tool.split("/")[0]+"\n")
            f.write("make\n")
            f.close()
            cmd = ["sh",params.globalDir+"/install.sh"]
            pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = pipe.communicate()
            result = out.decode()
        except:
            return False
        return True
    #################################################################################
    gma_BWA = tools+"gma-0.1.5/bin/bwa"
    gmaDir = tools+"gma-0.1.5/"        
    MAPPER= gmaDir+"bin/mapper"
    REDUCER= gmaDir+"bin/reducer"            
    gma_tools = [gma_BWA,MAPPER,REDUCER]
    print "Testing file permissions of required tools..."
    for tool in gma_tools: 
        out,err,result = testTool_gma(tool)
        if "bwa" in tool and "Program" in err:
            print tool, "--> tested OK."
            continue
        elif "bwa" in tool:
            setToolPermission_gma(tool)
            out,err,result = testTool_gma(tool)
            if "bwa" in tool and "Program" in err:
                print tool, "--> tested OK."
                continue
            elif "bwa" in tool: #Error not resolved
                print "Error testing: ", tool," attempting to fix this error..."
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
        if "mapper" in tool and "Program" in err:
            print tool, "--> tested OK."
            continue
        elif "mapper" in tool:
            setToolPermission_gma(tool)
            out,err,result = testTool_gma(tool)
            if "mapper" in tool and "Program" in err:
                print tool, "--> tested OK."
                continue
            elif "mapper" in tool: #Error not resolved
                print "Error testing: ", tool," attempting to fix this error..."
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
                   
        if "reducer" in tool and "Hadoop" in err:
            print tool, "--> tested OK."
            continue
        elif "reducer" in tool:
            setToolPermission_gma(tool)
            out,err,result = testTool_gma(tool)
            if "reducer" in tool and "Hadoop" in err:
                print tool, "--> tested OK."
                continue
            elif "reducer" in tool: #Error not resolved
                print "Error testing: ", tool," attempting to fix this error..."
                raw_input("Error, could not test-run tool:", tool, "Make sure that this tool located in the USAP/Tools/toolname is functional and that the folder permissions are set")
                raw_input("press enter to quit")
                exit(0)
    print "All tools required for GMA tested OK."
    return  
    
def convert_USAP_to_VCF(inputDir,outputDir):
    vcf_header = '''##fileformat=VCFv4.1
##FILTER=<ID=LowQual,Description="Low quality">
##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=PL,Number=G,Type=Integer,Description="Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification">
##GATKCommandLine.HaplotypeCaller=<ID=HaplotypeCaller,Version=3.4-46-gbc02625,Date="Sun Jan 17 21:37:24 SAST 2016",Epoch=1453059444846,CommandLineOptions="analysis_type=HaplotypeCaller input_file=[/home/rvdm/PHYRESSE_OUT/Results/BWA/Alignment_Files/420-04-lib935-miseq-r0062-251bp_bwa_realigned_resorted_dedup.bam] showFullBamList=false read_buffer_size=null phone_home=AWS gatk_key=null tag=NA read_filter=[] disable_read_filter=[] intervals=null excludeIntervals=null interval_set_rule=UNION interval_merging=ALL interval_padding=0 reference_sequence=/home/rvdm/USAP_DEC/Reference/MycobacteriumTuberculosis_H37Rv/FASTA/H37Rv_4411532_updated_13_jun_2013.fasta nonDeterministicRandomSeed=false disableDithering=false maxRuntime=-1 maxRuntimeUnits=MINUTES downsampling_type=BY_SAMPLE downsample_to_fraction=null downsample_to_coverage=500 baq=OFF baqGapOpenPenalty=40.0 refactor_NDN_cigar_string=false fix_misencoded_quality_scores=false allow_potentially_misencoded_quality_scores=false useOriginalQualities=false defaultBaseQualities=-1 performanceLog=null BQSR=null quantize_quals=0 disable_indel_quals=false emit_original_quals=false preserve_qscores_less_than=6 globalQScorePrior=-1.0 validation_strictness=SILENT remove_program_records=false keep_program_records=false sample_rename_mapping_file=null unsafe=null disable_auto_index_creation_and_locking_when_reading_rods=false no_cmdline_in_header=false sites_only=false never_trim_vcf_format_field=false bcf=false bam_compression=null simplifyBAM=false disable_bam_indexing=false generate_md5=false num_threads=1 num_cpu_threads_per_data_thread=1 num_io_threads=0 monitorThreadEfficiency=false num_bam_file_handles=null read_group_black_list=null pedigree=[] pedigreeString=[] pedigreeValidationType=STRICT allow_intervals_with_unindexed_bam=false generateShadowBCF=false variant_index_type=DYNAMIC_SEEK variant_index_parameter=-1 logging_level=INFO log_to_file=null help=false version=false out=/home/rvdm/PHYRESSE_OUT/Results/BWA/VARIANTS/420-04-lib935-miseq-r0062-251bp_gatk_HC_snps.vcf likelihoodCalculationEngine=PairHMM heterogeneousKmerSizeResolution=COMBO_MIN dbsnp=(RodBinding name= source=UNBOUND) dontTrimActiveRegions=false maxDiscARExtension=25 maxGGAARExtension=300 paddingAroundIndels=150 paddingAroundSNPs=20 comp=[] annotation=[ClippingRankSumTest, DepthPerSampleHC] excludeAnnotation=[] debug=false useFilteredReadsForAnnotations=false emitRefConfidence=NONE bamOutput=null bamWriterType=CALLED_HAPLOTYPES disableOptimizations=false annotateNDA=false heterozygosity=0.001 indel_heterozygosity=1.25E-4 standard_min_confidence_threshold_for_calling=30.0 standard_min_confidence_threshold_for_emitting=10.0 max_alternate_alleles=6 input_prior=[] sample_ploidy=2 genotyping_mode=DISCOVERY alleles=(RodBinding name= source=UNBOUND) contamination_fraction_to_filter=0.0 contamination_fraction_per_sample_file=null p_nonref_model=null exactcallslog=null output_mode=EMIT_VARIANTS_ONLY allSitePLs=false gcpHMM=10 pair_hmm_implementation=VECTOR_LOGLESS_CACHING pair_hmm_sub_implementation=ENABLE_ALL always_load_vector_logless_PairHMM_lib=false phredScaledGlobalReadMismappingRate=45 noFpga=false sample_name=null kmerSize=[10, 25] dontIncreaseKmerSizesForCycles=false allowNonUniqueKmersInRef=false numPruningSamples=1 recoverDanglingHeads=false doNotRecoverDanglingBranches=false minDanglingBranchLength=4 consensus=false maxNumHaplotypesInPopulation=128 errorCorrectKmers=false minPruning=2 debugGraphTransformations=false allowCyclesInKmerGraphToGeneratePaths=false graphOutput=null kmerLengthForReadErrorCorrection=25 minObservationsForKmerToBeSolid=20 GVCFGQBands=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99] indelSizeToEliminateInRefModel=10 min_base_quality_score=10 includeUmappedReads=false useAllelesTrigger=false doNotRunPhysicalPhasing=true keepRG=null justDetermineActiveRegions=false dontGenotype=false dontUseSoftClippedBases=false captureAssemblyFailureBAM=false errorCorrectReads=false pcr_indel_model=CONSERVATIVE maxReadsInRegionPerSample=10000 minReadsPerAlignmentStart=10 mergeVariantsViaLD=false activityProfileOut=null activeRegionOut=null activeRegionIn=null activeRegionExtension=null forceActive=false activeRegionMaxSize=null bandPassSigma=null maxProbPropagationDistance=50 activeProbabilityThreshold=0.002 min_mapping_quality_score=20 filter_reads_with_N_cigar=false filter_mismatching_base_and_quals=false filter_bases_not_stored=false">
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes, for each ALT allele, in the same order as listed">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency, for each ALT allele, in the same order as listed">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles in called genotypes">
##INFO=<ID=BaseQRankSum,Number=1,Type=Float,Description="Z-score from Wilcoxon rank sum test of Alt Vs. Ref base qualities">
##INFO=<ID=ClippingRankSum,Number=1,Type=Float,Description="Z-score From Wilcoxon rank sum test of Alt vs. Ref number of hard clipped bases">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth; some reads may have been filtered">
##INFO=<ID=DS,Number=0,Type=Flag,Description="Were any of the samples downsampled?">
##INFO=<ID=FS,Number=1,Type=Float,Description="Phred-scaled p-value using Fisher's exact test to detect strand bias">
##INFO=<ID=HaplotypeScore,Number=1,Type=Float,Description="Consistency of the site with at most two segregating haplotypes">
##INFO=<ID=InbreedingCoeff,Number=1,Type=Float,Description="Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation">
##INFO=<ID=MLEAC,Number=A,Type=Integer,Description="Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC), for each ALT allele, in the same order as listed">
##INFO=<ID=MLEAF,Number=A,Type=Float,Description="Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed">
##INFO=<ID=MQ,Number=1,Type=Float,Description="RMS Mapping Quality">
##INFO=<ID=MQRankSum,Number=1,Type=Float,Description="Z-score From Wilcoxon rank sum test of Alt vs. Ref read mapping qualities">
##INFO=<ID=QD,Number=1,Type=Float,Description="Variant Confidence/Quality by Depth">
##INFO=<ID=ReadPosRankSum,Number=1,Type=Float,Description="Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias">
##INFO=<ID=SOR,Number=1,Type=Float,Description="Symmetric Odds Ratio of 2x2 contingency table to detect strand bias">
##contig=<ID=gi|444893469|emb|AL123456.3|,length=4411532>
##reference=file:H37Rv_4411532_updated_13_jun_2013.fasta
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	12345
'''
    #######################
    def convertLine(line):
        '''
        CHROM = 1
        POS = 0
        ID = "."
        REF = 2
        ALT = 3
        QUAL = 4
        FILTER = "."
        INFO = "N/A"
        FORMAT = "GT:AD:DP:GQ:PL"
        last = 5
        '''
        temp = line.split("\t")
        if temp[38] <> "3":
            return False
        try:
            newLine = ""
            if len(temp[2]) > 1 or len(temp[3]) >1:
                return False #skip indels for now
            newLine += temp[1]+"\t"+temp[0]+"\t"+"."+"\t"+temp[2]+"\t"+temp[3]+"\t"+temp[4]+"\t"+"."+"\t"+"N/A"+"\t"+"GT:AD:DP:GQ:PL"+"\t"+temp[5]+"\n"
        except:
            print "Error converting USAP VCF to normal VCF for line:", line
            return False
        return newLine
    #################################
    try:
        os.mkdir(outputDir)
    except:
        pass
        
    for fileX in os.listdir(inputDir):
        fileData = []
        if not fileX.endswith(".vcf"):
            continue
        os.chdir(inputDir)
        f = open(fileX,'r')
        f.readline()
        for line in f:
            fileData.append(convertLine(line))
        f.close()
        os.chdir(outputDir)
        f=open(fileX,'w')
        f.write(vcf_header)
        for x in fileData:
            if x == False:
                continue
            f.write(x)
        f.close()
    print "conversion complete, files written to folder ",outputDir
    return
    
    
    
def create_consensus(globalDir,variantsDir,outputDir,tools,ref):
    os.chdir(variantsDir)
    files = []
    for fileX in os.listdir(variantsDir):
        if not fileX.endswith(".vcf"):
            continue
        files.append(fileX)
    f = open(globalDir+"/Scripts/createConsensus.sh",'w')
    
    globalDir
    gatk = tools+"GATK/GenomeAnalysisTK.jar"
    java = tools+"jre1.7.0_51/bin/java" 
    for fName in files:
        f.write(java+" -jar "+gatk+" -T FastaAlternateReferenceMaker -R "+ref+" -o "+outputDir+fName.replace(".vcf","_consensus.FASTA")+" --variant "+variantsDir+fName+"\n")        
    f.close()
    print "create consensus script written to", globalDir+"/Scripts/createConsensus.sh"
    cmd = ["sh",globalDir+"/Scripts/createConsensus.sh"]
    pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = pipe.communicate()
    result = out.decode()
    print err
    print result
    return
         
#######################################################################
#def runScript(path,scriptName):
#    '''
#    Many of the steps in the pipelines do not support multi-threading
#    this does not optimally make use of multi-core CPUs.
#    Program running structure is thus to run all pipelines simultanously with equal split of resources
#    this presents a problem for large references - solultion is to taper alignment steps
#    For now will run all at same time 
#    '''
#    print "Running script:", "sh "+path+scriptName
#    startTime = time.time()
#    cmd = ['sh',path+scriptName]
#    pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
###    if wait_flag:
#    out,err = pipe.communicate()
#    result = out.decode()
#    print "Result : ", [result]
#    print "Error : ", [err]
#    print "COMPLETED:", scriptName
#    print time.time() - startTime
#######################################################################
def makeSummaryFile(mainOrExtraToolsMode, debugMode, globalDir, fastQFolder, mapperOrderList, mapperOut, MTB, spolPredOut, BWAAligned_aln, NOVOAligned_aln, SMALTAligned_aln, minCov, minMappedReads, phenoAllowed):
    print "creating detailed report file." 
    #Here the summary file needs to report all data available, does not matter if annotation was possible
    if debugMode:
        raw_input("press enter to create report file")
    #startTime = time.time()
    try:
        if mainOrExtraToolsMode == "extraTools":
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','a')
            timeLogFile.write("summary started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
    except:
        raw_input("Error, could not create timelog, press enter to continue")
    orderedFiles = []
    fileData = {}
    for fileX in os.listdir(fastQFolder):
        if fileX.lower().endswith(".fastq.gz") or fileX.lower().endswith(".fastq"):
            if "_" not in fileX:
                temp = fileX.replace(".gz","")
                temp = temp.replace(".fastq",'')
            else:    
                temp = fileX.split("_")[0]
            if temp not in fileData:
                fileData[temp] = {} #a dictionary of dictionaries
                orderedFiles.append(temp)
    orderedFiles.sort()
    #print "Summarizing results for :",fileData
    #{File} : {coverage_BWA,coverage_NOVO,coverage_SMALT,DR,lineage,spolpred...etc}

    #loading genome coverage data
    #################################################
    mapperListFileNameToCovDict = []
    for mapper in mapperOrderList:
        tempDict = {}
        tempData = []
        try:
            f = open(mapperOut+mapper+"/GenomeCoverage/Genome_Coverage_Results_Summary.txt",'r')
            f.readline()
            for line in f:
                temp = line.split("\t")
                name = temp[0]
                cov = temp[1].replace("\n","")
                tempDict[name] = cov
            f.close()
        except:
            print "Error loading genome coverage data, file not found:", mapperOut+mapper+"/GenomeCoverage/Genome_Coverage_Results_Summary.txt"
        mapperListFileNameToCovDict.append(tempDict) #a list of 3 dictionaries
    #now have [{bwa_file:cov},{novo_file:cov},{smalt_file:cov{]
    #STORE the data in the main summary dictionary
    pos = -1
    for mapper in mapperOrderList:
        pos += 1
        covData = mapperListFileNameToCovDict[pos]
        for fileName in orderedFiles:
            if fileName in covData:
                if "AVR_COVERAGE" in fileData[fileName]:
                    fileData[fileName]["AVR_COVERAGE"].append(covData[fileName])
                else:
                    fileData[fileName]["AVR_COVERAGE"] = [covData[fileName]] #slightly complicated...

                    #this ends up as fileName : [10,10,4] for bwa cov novo cov and smalt cov
    ###########################################
    #Loading lineage data
    if MTB:
		lineageAllowed = True
            
    if lineageAllowed:
        try:
            f = open(mapperOut+"full_lineageData.txt",'r')
            f.readline()
        except:
            raw_input("no lineage data detected")
        for line in f:
            temp = line.split("\t")
            name = temp[0].split("_")[0]
            if ".fastq" in name:
                name = name.replace(".gz","")
                name = name.replace(".fastq","")
            lineage = temp[1]
            score = temp[2]
            if name in fileData:
                fileData[name]["LINEAGE"] = lineage+"\t"+score
            else:
                print "this is fileData names", fileData.keys()
                print "error #4454, file with no output results detected, possible reason: Non-Unique identifier left of '_' sign OR a Corrupt FASTQ. File affected is :",name
                raw_input("Press enter to continue") 
    ############################################################    
    if MTB:
        lookupSpoligotypes(spolPredOut,debugMode, mapperOut, globalDir+"/BIN")
        f = open(mapperOut+"SpolPred_Results_Summary.txt",'r')
        temp = f.readline()
        for line in f:
            temp = line.split("\t")
            name = temp[0]
            if ".gz" in name:
                name = name.replace(".gz","")
            if ".fastq" in name:
                name = name.replace(".fastq","")
            code = temp[1]
            commonName = temp[2].replace("\n","")
            commonName = commonName.replace("\r","")
            if name in fileData:
                fileData[name]["SPOLPRED"] = code+"\t"+commonName
            else:
                print "this is fileData",fileData.keys()
                print "error #4454, file with no output results detected, possible error: Corrupt FASTQ. File affected is :",name
                raw_input("Press enter to continue") 
        f.close()

    #######################################
    #get % mapped reads
    mappedReadsList = []
    for folderName in [BWAAligned_aln, NOVOAligned_aln, SMALTAligned_aln]:
        os.chdir(folderName)
        mappedReadsDict = {}
        for fileX in os.listdir(folderName):
            if "samtools_stats.txt" not in fileX or "samtools_stats.txt~" in fileX :
                continue
            tempFile = open(fileX,'r')
            numReads = tempFile.readline()
            if numReads == "":
                print "no mapped reads data found for file", fileX
                numReads = ""
                percentageMapped = ""
            else:
                numReads=numReads.split()[0]
                tempFile.readline()
        ##        percentageMapped = tempFile.readline().split("(")[1].split(":")[0]
                percentageMapped = tempFile.readline()
                if "duplicates" in percentageMapped or "supplementary" in percentageMapped:
                    percentageMapped = tempFile.readline()
                if "duplicates" in percentageMapped or "supplementary" in percentageMapped:
                    percentageMapped = tempFile.readline()
        ##        print [percentageMapped]
                percentageMapped = percentageMapped.split("(")[1]
        ##        print percentageMapped
                percentageMapped = percentageMapped.split(":")[0]
        ##        print percentageMapped
        ##        raw_input()
            if "_" in fileX:
                mappedReadsDict[fileX.split("_")[0]] = [percentageMapped,"of total",numReads]
            else:
                mappedReadsDict[fileX] = [percentageMapped,"of total",numReads]
            tempFile.close()
        mappedReadsList.append(mappedReadsDict)

    #now have [{bwa_file:[percentageMapped,numReads]},{novo_file:[percentageMapped,numReads]},{smalt_file:[percentageMapped,numReads]}]
    #STORE the data in the main summary dictionary
    pos = -1
    for mapper in mapperOrderList:
        pos += 1
        mappedReadsData = mappedReadsList[pos]
        for fileName in orderedFiles:
            if fileName in mappedReadsData:
                if "MAPPED_READS" in fileData[fileName]:
                    fileData[fileName]["MAPPED_READS"].append(mappedReadsData[fileName])
                else:
                    fileData[fileName]["MAPPED_READS"] = [mappedReadsData[fileName]] #slightly complicated...
    #NOW have file : [% mappedreads, numreads] for bwa,  [% mappedreads, numreads] for novo,  [% mappedreads, numreads] for smalt

    ########################################
    #########LOAD DR DATA
    try:
        f = open(mapperOut+"PHENO_RESULTS.txt",'r')
        DRflag = True
    except:
        print "NO phenotype file found"
        DRflag = False
    if DRflag:    
        DR_header = f.readline()
        for line in f:
            temp = line.split("\t")
            name = temp[0]
            nameLen = len(name)
            if "_" in name:
                name = name.split("_")[0]
            DRdata = line[nameLen+1:] 
            if name in fileData:
                if "PHENO" in fileData[name]:
                    
                    print "have the same DR data element for more than one file:", name
                    raw_input("FATAL ERROR, fix file name error")
                else:
                    fileData[name]["PHENO"] = DRdata
            else:
                raw_input("error have dr for a file not in main list! Press enter to continue")

    #################################################
    #write data to file
    if debugMode:
        phenoAns = raw_input("is pheno allowed here?")
        if phenoAns not in ["n","N"]:
            phenoAllowed = True
        raw_input("now writing to one big happy file, press enter")
    else:
        print "Writing summarized results to file"
    os.chdir(mapperOut)
    f = open("SUMMARY.txt",'w')
    if phenoAllowed:
        if MTB:
            keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","SPOLPRED","PHENO"]
        else:
            keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","PHENO"]
    else:
        if MTB:
            keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","SPOLPRED"]
        else:
            keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE"]
     
    f.write("SAMPLE_NAME")
    f.write("\tQC\tQC_Average_Coverage_Comment\tQC_Percentage_Mapped_Reads_Comment") #New June    
    for key in keys[:-1]:
        if MTB and key == "SPOLPRED":
            f.write("\tSPOLPRED_OCTAL_CODE\tCOMMON_NAME")
        elif key == "LINEAGE":
            f.write("\tLINEAGE\tNUM_LINEAGE_SNP_MATCHES")
        else:
            f.write("\t"+key)
    flagX = True
    if phenoAllowed and DRflag:
        for x in DR_header.split("\t"):
            if flagX:
                flagX = False # to skip sample_name
                continue
            f.write("\t"+x)
        if not "\n" in x:
            f.write("\n")
    else:
        f.write("\n")
    #header is done, now write the data for each sample
    for fileName in orderedFiles:
        f.write(fileName)
        #if True:
        try:
            key = "AVR_COVERAGE"  
            covData = str(fileData[fileName][key])
            covData = covData.replace("'","").replace("[","").replace("]","") #Using all the converage info available 
            covData = covData.split(",") 
        except: 
            covData = ""
        #if True:
        try:
            key = "MAPPED_READS"
            mapData = str(fileData[fileName][key])
            mapData = mapData.replace("'","").replace("[","").replace("]","")
            mapData=mapData.replace(" of total, ","")
            mapData=mapData.split(",")
            mapDataList = [] 
            for tempString in mapData:
                if "%" in tempString:
                    mapDataList.append(tempString.replace("%",""))
        except:
            mapDataList = []
        QCString = ""
        QC_MAIN = "PASS"
        flag = False
        for element in covData:
            if element == "" or "ERROR" in element:
                continue
            elif int(element) < int(minCov):
                flag = True
        if flag:
            QC_MAIN = "FAIL"
            QCString= "Low_Coverage, <"+str(minCov)+"\t"
        if not flag:
            QCString = "\t"
        flag = False
        for element in mapDataList:
            if float(element) < float(minMappedReads): 
                flag = True
        if flag:
            QC_MAIN = "FAIL"
            QCString += "Low_%_Mapped_Reads, <"+str(minMappedReads)#+"\t"
        #now write the QC, comment1, comment2
        f.write("\t"+QC_MAIN+"\t"+QCString)

        for key in keys:
            if key not in fileData[fileName]:
                if debugMode:
                    print fileName, "does not have info for", key
                if MTB and key == "SPOLPRED":
                    f.write("\tN/A\t")
                elif not MTB and key == "SPOLPRED":
                    f.write("\t")
                else:
                    f.write("\tN/A")
                lastString = "A"
            else:
                print "writing:", ["\t"+str(fileData[fileName][key])]
                f.write("\t"+str(fileData[fileName][key]))
                lastString = str(fileData[fileName][key])[-1]
        if lastString <> "\n":
            f.write("\n")
    f.close()

    if mainOrExtraToolsMode == "extraTools":
        try:
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','a')
            timeLogFile.write("summary ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
        except:
            raw_input("Error, could not create timelog, press enter to continue")
    print "Summary complete, proceed to additional tool menu for further built-in analysis tools"
    os.chdir(globalDir)
    f = open("exitSignal.txt",'w')
    f.write("complete") #here write to file complete - this stops the monitoring tool
    f.close()
    
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#       USAP MAIN CONTROL   ###########################################
#123456789#

try:
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete)
except:
    print "Error loading completer module..."
runFastQC = True # remove all traces of this variable later
raw_input("remove this forced non-fastc variable here")
runFastQC = False
if True:         
    ans, skipSetup, controlPoint, spaceSavingMode, debugMode = interface()
    mapperOrderList = ["BWA","NOVO","SMALT"]
    if ans == "1":
        print "Running USAP..."        
        #obtain system settings to optimize performace
        cpu_count = available_cpu_count() #int or None
        memory = available_memory() #int or None
##        if debugMode:
##            print [cpu_count]
##            print [memory]
##            raw_input("These are detected")        
        #Obtain user preferences
                
        binDir, globalDir, userPrefcpu , userPrefmem,  inputDir, outputDir, readsType, userRef, trimMethod, annotationAllowed, BQSRPossible, emblFile, mappers, variantTools, filterSettings = setup(cpu_count,memory,skipSetup)
        params = paramaters(binDir, globalDir, userPrefcpu , userPrefmem,  inputDir, outputDir, readsType, userRef, trimMethod, BQSRPossible, emblFile, variantTools , filterSettings)
        refPath = params.reference
        refFastaName  = ""
        print 
        for fileX in os.listdir(refPath):
            if fileX.endswith(".FASTA"):
                print "ERROR, the input fasta file must have extention .fasta, not .FASTA, please rename this file in folder: ", refPath
                raw_input("Press enter to exit")
                exit()
        if debugMode:
            print mappers
            print variantTools
            raw_input("does this reflect what i want?")
        os.chdir(globalDir)
        f = open("exitSignal.txt",'w')
        f.close()
        try:
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','w')
            timeLogFile.write("Initialize_tools started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
        except:
            raw_input("Error, could not create timelog, press enter to continue")
        #if not debugMode:
        #setPermissions(globalDir,params)
        
        #if debugMode:
        #    print "Selected user reference and output folder:"
        #    print userRef
        #    print params.reference
        #    print outputDir
        #    raw_input("ref and output settings are shown")

        if "MycobacteriumTuberculosis_H37Rv" in params.reference: 
            MTB = True
        else:
            MTB = False
        #junkTerms, mapperCount_GATK, mapperCount_SAMTOOLS ,qualityCutOFF, minCoverage, readFreqCutoff = getFilterSettings(MTB,autoMode,params)
        #junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutoff_GATK,readFreqCutoff_SAMTOOLS, filterSpecificPositions = getFilterSettings(MTB,autoMode,params, params.gatkFlag, params.samtoolsFlag)
        
        try:
            os.chdir(outputDir)
        except:
            try:
                os.mkdir(outputDir)
            except:
                print "output directory already exists"
        print "Setup and parameter initialization complete."

        shutDownWhenDone = False 
        #sAns = raw_input("shutdown PC when done? (Note: Root access required) Y/N :")
        #if sAns in ["y","Y"]:
        #    raw_input("The system will now shutdown when USAP fully complete...press enter")
        #    shutDownWhenDone = True
        
        #raw_input("special case sleep for 48h line 7965")
        #print "now roaming in nightmares for 48 hours..."
        #time.sleep(60*60*48)
        #print "AWAKE!"
       
        #step 1
        #Determine running mode
        ################################################
        #startTime = time.time()
                    
        params.multiMode = True 
        if userPrefmem < 2000:
            params.multiMode = False
            print "Less than 2gig RAM allocated, this wil not allow simultanious execution due to resource requirements..."
        elif int(userPrefcpu) < 3:
            params.multiMode = False
            print "Detected 2 or less CPU cores, this wil not allow simultanious execution due to resource requirements..."
        hardWareInit(debugMode) # determine the coresplit and mem allocation
        #duration = time.time() - startTime
        try:
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','a')
            timeLogFile.write("Initialize_tools ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
        except:
            raw_input("Error, could not create timelog, press enter to continue")
        
        ###############################################
        #Step 2: check if nessisary to index reference, if so index for each mapper
        #startTime = time.time()
        try:
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','a')
            timeLogFile.write("indexReferences started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
        except:
            raw_input("Error, could not create timelog, press enter to continue")
        params.fastaList = indexReferences()
        #duration = time.time() - startTime
        try:
            os.chdir(globalDir)
            timeLogFile = open('timeLog.txt','a')
            timeLogFile.write("indexReferences ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            timeLogFile.close()
        except:
            raw_input("Error, could not create timelog, press enter to continue")
        
        ####################################################################################################################
        #Step 3: FASTQC, Trim reads + adapter removal:
        print "preparing to run FastQC"
        try:
            os.makedirs(params.scripts_trimming)
        except:
            print "Using previously existing trimming script directory"
        try:
            os.chdir(params.scripts_trimming)
            f=open('FastQC.sh','w')
            f.close()
            f=open('autoTrim.sh','w')
            f.close()
        except:
            print "Error creating QC scripts."
            raw_input()
            exit(0)
        
        ###################################
        #Setup output directory structure:
        picardReport, genomeCovDir, snpDir, spolPredOut = createDirStructure()
        ###################################
        flag = False
        flag = fastQCSH(False) 
        if not flag:
            exit(0)
        ###########################################################################
        #note: trimMethod can be "Quality_Trim", "Fixed_Amount_Trim", or "No_Trim"
        if params.trimMethod == "No_Trim":
            print "No trimming selected."
            trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE  = noTrimmingFileNamePartition()
            #print trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE
            #raw_input("1111111111111111111111111")
        else:
            os.chdir(params.scripts_trimming)
            try:    
                os.makedirs(params.trimmedFastQ)
            except:
                print "Using previously existing trimmed-FastQ folder"
                
            #print "Trimming method selected:", params.trimMethod
            if params.trimMethod == "Quality_Trim":
                print "creating trimmomatic script..."
                trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE  = trimmomaticMulti() 
            elif params.trimMethod == "Fixed_Amount_Trim":
                trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE  = fastXToolKitTrim()
            else:
                print [params.trimMethod]
                raw_input("user settings file corrupt")
                exit(0)
        
        if controlPoint <= 2 and runFastQC:
            if debugMode:
                raw_input("control point 1: FASTQC")
            print "Running FastQC..."
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("FASTQC1 started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
    ##        subprocess.call("sh "+params.scripts_trimming+"FastQC.sh &",shell = True)
            subprocess.call(["sh",params.scripts_trimming+"FastQC1.sh"])
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("FASTQC1 ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            print "FastQC complete."
    
        if controlPoint <= 3:
            #raw_input("remove this extra stop before trimming")
            if debugMode:
                raw_input("control point reached: Trimming")
            print "Trimming reads..."
            startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Trimming started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            ###################################NEW FEB 2016####################
            ##############################
            '''os.chdir(params.scripts_trimming)
            path = params.scripts_trimming
            scriptName = "autoTrim.sh"
            print "Running Trimming script:", "sh "+params.scripts_trimming+scriptName
            cmd = ['sh',path+scriptName]
            trimLog1 = open(params.scripts_trimming+"Trim_LOG1.log",'a')
            trimLog2= open(params.scripts_trimming+"Trim_LOG2.log",'a')
            pipe1 = subprocess.Popen(cmd, shell = False, stdout=trimLog1, stderr=trimLog2)
            '''
            ###############################
            
            os.chdir(params.scripts_trimming)
            f = open("autoTrim.sh",'r')
            
            for line in f:
                temp = line.split()
                if temp == []:
                    continue
                print temp
                if temp == "wait":
                    cmd = [temp]
                else:
                    cmd = temp
                if debugMode:
                    print "running", cmd
                try:
                    pipe = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                    out,err = pipe.communicate()
                    result = out.decode()
                except:
                    if "wait" in cmd:
                        continue 
                    else:
                        print "Error processing command:", cmd
                    continue
                if "Sequence and quality length don't match" in err:
                    #get the filename of the broken file / files
                    #case 1 - it is SE
                    if cmd[3] == "SE":
                        print "SE FASTQ found with mismatching sequence and quality lengths, attempting to fix broken file...", cmd[7]
                        newFileName = fixFastq(cmd[7])
                        if not newFileName:
                            continue
                        cmd[7] = newFileName
                    elif cmd[3] == "PE":
                        print "PE FASTQ found with mismatching sequence and quality lengths, attempting to fix broken file...", cmd[7],"and",cmd[8]
                        newFileNameR1 = fixFastq(cmd[7])
                        if not newFileNameR1:
                            continue
                        cmd[7] = newFileNameR1
                        newFileNameR2 = fixFastq(cmd[8])
                        if not newFileNameR2:
                            continue
                        cmd[8] = newFileNameR2
                
                    print "Attempting to use fixed fastq file(s) for trimming..." 
                    #if debugMode:
                    print "running", cmd
                    pipe = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                    out,err = pipe.communicate()
                    result = out.decode()
                    print "remove this extra check dubky111:"
                    if "Sequence and quality length don't match" in err:
                        print "Fatal error, attempt to fix FASTQ file failed for 2nd time, is this file corruput? Check the file format matches input types:"
                        raw_input("press enter to contiune to next file(s)")
            ################################### END NEW FEB 2016####################
              
            #subprocess.call("sh "+params.scripts_trimming+"autoTrim.sh",shell = True)
            #subprocess.call(["sh ",params.scripts_trimming,"autoTrim.sh"])
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Trimming ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            print "Trimming complete."
            
        if controlPoint <= 4 and runFastQC:
            if debugMode:
                raw_input("Control Point 4 - 2nd FASTQC on trimmed reads")
            flag = True
            if params.trimMethod <> "No_Trim":
                flag = fastQCSH(True)     
            if not flag:
                print "Error in running 2nd FASTQC!"
            if flag and params.trimMethod <> "No_Trim":
                print "Running FastQC 2nd run..."
                try:
                    os.chdir(globalDir)
                    timeLogFile = open('timeLog.txt','a')
                    timeLogFile.write("FASTQC2 started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                    timeLogFile.close()
                except:
                    raw_input("Error, could not create timelog, press enter to continue")
                #startTime = time.time()
                subprocess.call(["sh",params.scripts_trimming+"FastQC2.sh"])
                #duration = time.time() - startTime
                try:
                    os.chdir(globalDir)
                    timeLogFile = open('timeLog.txt','a')
                    timeLogFile.write("FASTQC2 ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                    timeLogFile.close()
                except:
                    raw_input("Error, could not create timelog, press enter to continue")
                print "FastQC 2nd run complete."
                

        if controlPoint <= 5:
            ####################################################################################################################
            #Step4 Alignment using 3 mappers 
            #Here the program maximize performance by divising the resources between the 3 mappers
            #so if there is not enough resources, the programs must run one at a time, two at a time or all 3 at the same time
            ####################################################################################################################
            #CREATE TRI-PARTATE-SCRIPTS
            print "creating variant detection scripts"
            if params.BQSRPossible:
                print "BASE QUALITY SCORE RECALIBRATION IS ENABLED"
            else:
                print "BASE QUALITY SCORE RECALIBRATION IS NOT POSSIBLE DUE TO MISSING DATABASE FILE"
            #if debugMode:
                #raw_input("is this correct BQSR info?")
            if debugMode:
                print "Mappers are:", mappers
                print "selected variant callers are:",variantTools
                raw_input("press enter to continue")
            #BWA:
            for mapper in mappers:
                if mapper[0] == "BWA" and mapper[1] == True:
                    BWAAlign_combine(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE) 
                    variantScriptsBWA(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE)
            #NOVO:
            for mapper in mappers:
                if mapper[0] == "NOVOAlign" and mapper[1] == True:
                    NOVOAlign(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE)
                    NOVOAlignMulti()
                    variantScriptsNOVO(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE)
            #SMALT:
            for mapper in mappers:
                if mapper[0] == "SMALT" and mapper[1] == True:
                    SMALTAlign(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE) 
                    variantScriptsSMALT(trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE)
            #######################################################################################################################
            #Run serially
            commandListBWA = []
            commandListNOVO = []
            commandListSMALT = []
            ##BWA
            for mapper in mappers:
                if mapper[0] == "BWA" and mapper[1] == True:
                    
                    commandListBWA.append("1_BWAAlign.sh") #"Combining reads from sai files..." Step 1
                    commandListBWA.append("2_combineReads.sh") #Step 2
                    commandListBWA.append("3_picardValidate.sh") #echo "Validating reads..." #Step 3
                    commandListBWA.append("4_createSamToBam.sh") #echo "Converting Sam file to BAM file..." #Step 4
                    commandListBWA.append("1_BWAAlign_cleanup.sh") #for step 3 CLEANUP
                    commandListBWA.append("2_combineReads_Cleanup.sh") #for step 5 CLEANUP
                    commandListBWA.append("5_indexBam.sh") #echo "Indexing BAM file..." #Step 5
                    commandListBWA.append("6_1_GATK.sh") #echo "Creating intervals file to allow realignment..." #Step 6    
                    commandListBWA.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.BWAAligned_aln+" "+params.scripts_BWA+" "+"6_2_GATK.sh") #This script updates 6_2_GATK.sh if any files did not complete
                    commandListBWA.append("6_2_GATK.sh") #echo "Creating intervals file to allow realignment..." --> fix misencoded_quality_scores #Step 7
                    commandListBWA.append("7_1_Realignment.sh") #echo "Realigning reads..." #Step 8
                    commandListBWA.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.BWAAligned_aln+" "+params.scripts_BWA+" "+"7_2_Realignment.sh") #This script updates 7_1_GATK.sh if any files did not complete
                    commandListBWA.append("7_2_Realignment.sh") #echo "Realigning reads..." #Step 9
                    commandListBWA.append("4_createSamToBam_cleanup.sh") #for step 12 CLEANUP
                    commandListBWA.append("5_indexBam_cleanup.sh") #for step 12
                    if params.BQSRPossible: 
                        commandListBWA.append("8.1_baseQualRecalBWA.sh") # Base quality recalibration #Step 10
                        commandListBWA.append("8.2_baseQualRecalBWA.sh") # Base quality recalibration #Step 11
                    commandListBWA.append("6_1_GATK_cleanup.sh") #for step 12
                    commandListBWA.append("6_2_GATK_cleanup.sh") #for step 12
                    commandListBWA.append("9_picardSort.sh") #echo "Sorting reads..." 12
                    commandListBWA.append("7_1_Realignment_cleanup.sh") #for step 12
                    commandListBWA.append("7_2_Realignment_cleanup.sh")
                    commandListBWA.append("10_reIndexBamFiles.sh") #echo "Re-indexing..."
                    commandListBWA.append("8.1_baseQualRecalBWA_cleanup.sh") #for step 12 CLEANUP"
                    commandListBWA.append("8.2_baseQualRecalBWA_cleanup.sh") #for step 12 CLEANUP"
                    commandListBWA.append("11_removePCRDuplicates.sh") #echo "Removing PCR duplicates..." 13
                    commandListBWA.append("12_reIndexBamFiles2.sh") #echo "Re-indexing..." 14
                    commandListBWA.append("9_picardSort_cleanup.sh") #for step 15 CLEANUP"
                    commandListBWA.append("13_getMappedReads.sh") #echo "Calculating mapped reads..." 15
                    commandListBWA.append("10_reIndexBamFiles_cleanup.sh") #for step 15 CLEANUP"
                    #here make use of the list variantTools which is [callername:True/False,callername:True/False] to toggle between gatk,samtools or gatk+samtools
                    for caller in variantTools:
                        if caller[0] == "GATK" and caller[1] == True:
                            commandListBWA.append("14_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh") #echo "SNP calling using GATK..." 16
                        elif caller[0] == "GATK" and caller[1] == False:
                                commandListBWA.append('echo "Skipping GATK based variant calling due to user customization"')   #Default is True
                    #commandListBWA.append("15_GenomeCoverage.sh") #echo "Calculating genome coverage..." 18
                    commandListBWA.append("15_2_GenomeCoverage.sh") #echo "Calculating genome coverage..." 18
                    commandListBWA.append("16_ZeroCov.sh")  #echo "Calculating areas with no coverage..." 19
                    for caller in variantTools:
                        if caller[0] == "SAMTOOLS" and caller[1] == True:
                            commandListBWA.append("14_2_VARIANT_CALLING_SAMTOOLS.sh") #echo running samtools based variant calling
                        elif caller[0] == "SAMTOOLS" and caller[1] == False:
                            commandListBWA.append('echo "Skipping Samtools based variant calling due to user customization"')   #Default is True
        ##            commandListBWA.append("15_GenomeCoverage_cleanup.sh")
        ##            commandListBWA.append("16_ZeroCov_cleanup.sh")
                ########################
                #NOVO
                if mapper[0] == "NOVOAlign" and mapper[1] == True:
                ##    commandListNOVO.append("1_1_NOVOAlign.sh")
                    commandListNOVO.append("1_2_NOVOAlign_multi.sh")
                ##    commandListNOVO.append("1_2_NOVOAlign_multi.sh")# > ./Scripts/NOVO/NovoAlign.out")  #echo "Aligning Reads to reference using NOVOAlign..." 1
                    commandListNOVO.append("2_picardValidate.sh") #echo "Validating reads..." 2
                    commandListNOVO.append("3_createSamToBam.sh") # echo "Converting Sam file to BAM file..." 3
                    commandListNOVO.append("1_1_NOVOAlign_cleanup.sh") 
                    commandListNOVO.append("4_indexBam.sh") #echo "Indexing BAM file..." 4
                    commandListNOVO.append("5_1_GATK.sh") #echo "Creating intervals file to allow realignment..." 5
                    commandListNOVO.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.NOVOAligned_aln+" "+params.scripts_NOVO+" "+"5_2_GATK.sh") #This script updates 6_2_GATK.sh if any files did not complete
                    commandListNOVO.append("5_2_GATK.sh") #echo "Creating intervals file to allow realignment..." 6
        
                    commandListNOVO.append("6_1_Realignment.sh") #echo "Realigning reads..." 7
                    commandListNOVO.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.NOVOAligned_aln+" "+params.scripts_NOVO+" "+"6_2_Realignment.sh") #This script updates 6_2_GATK.sh if any files did not complete
                    commandListNOVO.append("6_2_Realignment.sh") #echo "Realigning reads..." 8
                    commandListNOVO.append("3_createSamToBam_cleanup.sh")
                    commandListNOVO.append("4_indexBam_cleanup.sh")
                    if params.BQSRPossible:
                        commandListNOVO.append("7.1_baseQualRecalNOVO.sh") # Base quality recalibration 9
                        commandListNOVO.append("7.2_baseQualRecalNOVO.sh") # Base quality recalibration 10
                    commandListNOVO.append("5_1_GATK_cleanup.sh")
                    commandListNOVO.append("8_picardSort.sh")  #echo "Sorting reads..." 11   
                    commandListNOVO.append("6_x_Realignment_cleanup.sh")     
                    commandListNOVO.append("7.1_baseQualRecalNOVO_cleanup.sh")
                    commandListNOVO.append("7.2_baseQualRecalNOVO_cleanup.sh") 
                    
                    commandListNOVO.append("9_reIndexBamFiles.sh") #echo "Re-indexing..." 12
                    commandListNOVO.append("10_removePCRDuplicates.sh") #echo "Removing PCR duplicates..." 13
                    commandListNOVO.append("11_reIndexBamFiles2.sh") #echo "Re-indexing..." 14        
                    commandListNOVO.append("8_picardSort_cleanup.sh")
                    commandListNOVO.append("12_getMappedReads.sh") #echo "Calculating mapped reads..." 15
                    commandListNOVO.append("9_reIndexBamFiles_cleanup.sh")
                ##    commandListNOVO.append("13_SNPCallingGATK.sh") #echo "SNP calling using GATK..." 
                ##    commandListNOVO.append("13_INDELCallingGATK.sh") # echo "INDEL calling using GATK..."
                    for caller in variantTools:
                        if caller[0] == "GATK" and caller[1] == True:
                            commandListNOVO.append("13_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh") #echo "SNP calling using GATK..." 16
                        elif caller[0] == "GATK" and caller[1] == False:
                            commandListNOVO.append('echo "Skipping GATK based variant calling due to user customization"')   #Default is True
                    
                    #commandListNOVO.append("14_GenomeCoverage.sh") #echo "Calculating genome coverage..." 17
                    commandListNOVO.append("14_2_GenomeCoverage.sh") #echo "Calculating genome coverage..." 17
                    commandListNOVO.append("15_ZeroCov.sh") #echo "Calculating areas with no coverage..." 18
                    for caller in variantTools:
                        if caller[0] == "SAMTOOLS" and caller[1] == True:
                            commandListNOVO.append("13_2_VARIANT_CALLING_SAMTOOLS.sh") #echo "Calculating areas with no coverage..." 18
                        elif caller[0] == "SAMTOOLS" and caller[1] == False:
                            commandListNOVO.append('echo "Skipping Samtools based variant calling due to user customization"')   #Default is True 
        ##            commandListNOVO.append("14_GenomeCoverage_cleanup.sh")
                    #commandListNOVO.append("15_ZeroCov_cleanup.sh")

                ########################
                #SMALT
                if mapper[0] == "SMALT" and mapper[1] == True:
                    commandListSMALT.append("1_SMALTAlign.sh") #echo "Aligning Reads to reference using SMALT...Output is <SampleName>_trim_smalt.sam" 1
                    commandListSMALT.append("2_sortSmaltSam.sh") #echo "Sorting reads...Output is <SampleName>_trim_smalt_sort.sam" 2
                    commandListSMALT.append("1_SMALTAlign_cleanup.sh")
                    commandListSMALT.append("3_addReadGroupsToSortedSam.sh")#echo "Adding readgroups...Output is <SampleName>_trim_smalt_SrtRG.sam" 3
                    commandListSMALT.append("2_sortSmaltSam_cleanup.sh")
                    commandListSMALT.append("4_picardValidate.sh")  #echo "Validating reads...Output is <SampleName>_trim_smalt_SrtRG_validateReport" 4
                    commandListSMALT.append("5_createSamToBam.sh") #echo "Converting Sam file to BAM file and sorting...Output is <SampleName>_trim_smalt_SrtRG.sam" 5
                    commandListSMALT.append("6_indexBam.sh") #echo "Indexing BAM file...Output is <SampleName>_trim_smalt_SrtRG_sorted.bam.bai" 6
                    commandListSMALT.append("3_addReadGroupsToSortedSam_cleanup.sh")
                    commandListSMALT.append("7_1_GATK.sh")#echo "Creating intervals file to allow realignment...Output is <SampleName>_trim_smalt_SrtRG_sorted.intervals" 7
        
                    commandListSMALT.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.SMALTAligned_aln+" "+params.scripts_SMALT+" "+"7_2_GATK.sh") #This script updates 6_2_GATK.sh if any files did not complete
                    commandListSMALT.append("7_2_GATK.sh")#echo "Creating intervals file to allow realignment...Output is <SampleName>_trim_smalt_SrtRG_sorted.intervals" 8
                    commandListSMALT.append("8_1_Realignment.sh") #echo "Realigning reads...Output is <SampleName>_trim_smalt_SrtRG_sorted_realigned.bam" 9
                    commandListSMALT.append("python "+params.binDir+"/fixMisEncodedQuals.py "+params.SMALTAligned_aln+" "+params.scripts_SMALT+" "+"8_2_Realignment.sh") #This script updates 6_2_GATK.sh if any files did not complete
                    commandListSMALT.append("8_2_Realignment.sh") #echo "Realigning reads...Output is <SampleName>_trim_smalt_SrtRG_sorted_realigned.bam" 10
                    commandListSMALT.append("5_createSamToBam_cleanup.sh")
                    commandListSMALT.append("6_indexBam_cleanup.sh")
                    if params.BQSRPossible: 
                        commandListSMALT.append("9.1_baseQualRecalSMALT.sh") # Base quality recalibration 11
                        commandListSMALT.append("9.2_baseQualRecalSMALT.sh") # Base quality recalibration 12
                    commandListSMALT.append("7_x_GATK_cleanup.sh")
                    
                    commandListSMALT.append("10_picardSort.sh")#echo "Sorting reads...Output is <SampleName>_trim_smalt_SrtRG_realigned_resorted.bam" 13
                    commandListSMALT.append("8_x_Realignment_cleanup.sh")
                    commandListSMALT.append("9.1_baseQualRecalSMALT_cleanup.sh")
                    commandListSMALT.append("9.2_baseQualRecalSMALT_cleanup.sh")
                    commandListSMALT.append("11_reIndexBamFiles.sh") #echo "Re-indexing...Output is <SampleName>_trim_smalt_SrtRG_realigned_resorted.bam.bai" 14
                    commandListSMALT.append("12_removePCRDuplicates.sh")  #echo "Removing PCR duplicates...Output is <SampleName>_trim_smalt_SrtRG_realigned_resorted_dedup.bam" 15
                    commandListSMALT.append("13_reIndexBamFiles2.sh")  #echo "Re-indexing...Output is <SampleName>_trim_smalt_SrtRG_realigned_resorted_dedup.bam.bai" 16
                    commandListSMALT.append("10_picardSort_cleanup.sh")
                    #commandListSMALT.append("11_reIndexBamFiles_cleanup.sh")
                    commandListSMALT.append("14_getMappedReads.sh")  #echo "Calculating mapped reads...Output is <SampleName>_trim_smalt_SrtRG_sorted_samtools_stats.txt" 17
                    commandListSMALT.append("12_removePCRDuplicates_cleanup.sh")
                    commandListSMALT.append("11_reIndexBamFiles_cleanup.sh") 
                    #commandListSMALT.append("15_SNPCallingGATK.sh")   #echo "SNP calling using GATK...Output is in /SNP directory, <SampleName>_gatk_snps.vcf and <SampleName>_Genotype.log" 18
                ##    commandListSMALT.append("15_INDELCallingGATK.sh")  #echo "INDEL calling using GATK...Output is in INDEL directory, <SampleName>_gatk_indels.vcf" 
            
                    for caller in variantTools:
                        if caller[0] == "GATK" and caller[1] == True:
                            commandListSMALT.append("15_SNP_INDEL_Calling_GATK_HAPLOTYPECALLER.sh") #echo "SNP calling using GATK..." 19
                        elif caller[0] == "GATK" and caller[1] == False:
                            commandListSMALT.append('echo "Skipping GATK based variant calling due to user customization"')   #Default is True
                    
                    #commandListSMALT.append("16_GenomeCoverage.sh") #echo "Calculating genome coverage...Output is in GenomeCoverage directory ,<sampleName>_genomecov.txt" 20 
                    commandListSMALT.append("16_2_GenomeCoverage.sh") #echo "Calculating genome coverage...Output is in GenomeCoverage directory ,<sampleName>_genomecov.txt" 20 
                    commandListSMALT.append("17_ZeroCov.sh") #echo "Calculating areas with no coverage...Output is in GenomeCoverage directory, <sampleName>_genomecov=0.txt" 21
                    
                    for caller in variantTools:
                        if caller[0] == "SAMTOOLS" and caller[1] == True:
                            commandListSMALT.append("15_2_VARIANT_CALLING_SAMTOOLS.sh") #echo "Calculating areas with no coverage...Output is in GenomeCoverage directory, <sampleName>_genomecov=0.txt" 21
                        elif caller[0] == "SAMTOOLS" and caller[1] == False:
                            commandListSMALT.append('echo "Skipping Samtools based variant calling due to user customization"')   #Default is True
                    
                    ##commandListSMALT.append("16_GenomeCoverage_cleanup.sh")
                    #SMALT_cleanups["FINAL"] = ["18_ZeroCov_cleanup.sh"]
                #################################################################################################################    
            if debugMode:
                raw_input("control point reached: MapperScipts")
            print "Running BWA/NOVO/SMALT scripts"
            '''
            if not multimode:
                one at a time
            elif multimode:
                all 3 same time
            if one pipeline complete, increase the cpu and memory allocation to others
            wait till done, print output to screen
            print "done"
            '''
            if debugMode:
                print commandListBWA
                print
                print commandListNOVO
                print
                print commandListSMALT
                print
            
            os.chdir(params.scripts_BWA)
            f = open("BWA_pipeline.sh",'w')
            #Write the timestamp for each command to a log file
            try:
                os.chdir(globalDir)
                timeLog_BWA = open('timeLog_BWA.txt','w') 
                timeLog_BWA.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            try:
                os.chdir(globalDir)
                timeLog_NOVO = open('timeLog_NOVO.txt','w') 
                timeLog_NOVO.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            try:
                os.chdir(globalDir)
                timeLog_SMALT = open('timeLog_SMALT.txt','w') 
                timeLog_SMALT.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            for command in commandListBWA:
                f.write('echo "'+command+' started: " >> '+globalDir+"/timeLog_BWA.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_BWA.txt\n")
                if "python" not in command and "echo" not in command:
                    f.write("sh "+command+"\n")
                else:
                    f.write(command+"\n")
                f.write('echo "'+command+' ended: " >> '+globalDir+"/timeLog_BWA.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_BWA.txt\n")
            f.close()
            
            os.chdir(params.scripts_NOVO)
            f = open("NOVOAlign_pipeline.sh",'w')
            for command in commandListNOVO:
                f.write('echo "'+command+' started: " >> '+globalDir+"/timeLog_NOVO.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_NOVO.txt\n")
                if "python" not in command:
                    f.write("sh "+command+"\n")
                else:
                    f.write(command+"\n")
                f.write('echo "'+command+' ended: " >> '+globalDir+"/timeLog_NOVO.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_NOVO.txt\n")
            f.close()
            
            os.chdir(params.scripts_SMALT)
            f = open("SMALT_pipeline.sh",'w')
            for command in commandListSMALT:
                f.write('echo "'+command+' started: " >> '+globalDir+"/timeLog_SMALT.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_SMALT.txt\n")
                if "python" not in command:
                    f.write("sh "+command+"\n")
                else:
                    f.write(command+"\n")
                f.write('echo "'+command+' ended: " >> '+globalDir+"/timeLog_SMALT.txt\n")
                f.write("date +%Y-%m-%d%t%T >> "+globalDir+"/timeLog_SMALT.txt\n")
            f.close()
            if debugMode:
                raw_input("HALT! press enter to start running scripts!")
            #raw_input("Extra stop introduced")
            #if MTB and debugMode:
            #    raw_input("creating spolpred scripts here")
            picardReport, genomeCovDir, snpDir, spolPredOut = createDirStructure()
            runSpolpredOrSkip = True
            if debugMode and MTB:
                runSpolpredOrSkip = raw_input("run spolpred or skip? y=run n=skip")
            if MTB and runSpolpredOrSkip <> "n":
                spolpred(params, trimmedFilesSE, trimmedFilesPE, IDSE, SMSE, LBSE, IDPE, SMPE, LBPE, fileArraySE, fileArrayPE,debugMode)
                if debugMode:
                    raw_input("press enter to start running spolpred and mapping scripts...")
                os.chdir(params.scripts_StrainIdentification)
                path = params.scripts_StrainIdentification
                scriptName = "spolpred.sh"
                print "Running spolpred scrript:", "sh "+params.scripts_StrainIdentification+scriptName
                #startTime = time.time()
                try:
                    os.chdir(globalDir)
                    timeLogFile = open('timeLog.txt','a')
                    timeLogFile.write("Spolpred started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                    timeLogFile.close()
                except:
                    raw_input("Error, could not create timelog, press enter to continue")
                cmd = ['sh',path+scriptName]
                strainLogFile1 = open(params.scripts_StrainIdentification+"spolpred_LOG1.log",'w')
                strainLogFile2 = open(params.scripts_StrainIdentification+"spolpred_LOG2.log",'w')
                strainLogFile1.close()
                strainLogFile2.close()
                strainLogFile1 = open(params.scripts_StrainIdentification+"spolpred_LOG1.log",'a')
                strainLogFile2 = open(params.scripts_StrainIdentification+"spolpred_LOG2.log",'a')
                pipe_strainIdent = subprocess.Popen(cmd, shell = False, stdout=strainLogFile1, stderr=strainLogFile2)
                areadyDoneSpolpred = False
                if debugMode:
                    exit_codes = [p.wait() for p in [pipe_strainIdent]]
                    out4,err4 = pipe_strainIdent.communicate()
                    areadyDoneSpolpred = True
                    try:
                        result4 = out4.decode()
                    except:
                        print "could not decode pipe for spolpred in debug mode"
                    print "Spolpred Completed"
                    raw_input("press enter to continue")
                else:
                    print "Spolpred Completed"
                #duration = time.time() - startTime
                try:
                    os.chdir(globalDir)
                    timeLogFile = open('timeLog.txt','a')
                    timeLogFile.write("Spolpred ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                    timeLogFile.close()
                except:
                    raw_input("Error, could not create timelog, press enter to continue")

            if not spaceSavingMode:
                scriptLocations = [params.scripts_BWA,params.scripts_NOVO,params.scripts_SMALT]
                for scriptLocation in scriptLocations:
                    for scriptName in os.listdir(scriptLocation):
                        if "cleanup" in scriptName:
                            os.chdir(scriptLocation)
                            os.remove(scriptName) 
                #raw_input("check if cleanup scripts are removed or kept")                     
            ###########################################################################################################
            #BWA
            ###########################################################################################################
            if debugMode:
                raw_input("this is the final check before mapping starts")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("MainPipeline started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            os.chdir(params.scripts_BWA)
            path = params.scripts_BWA
            scriptName = "BWA_pipeline.sh"
            for mapper in mappers:
                if mapper[0] == "BWA" and mapper[1] == True:
                    print "Running BWA script:", "sh "+params.scripts_BWA+scriptName
            path = params.scripts_BWA
            cmd = ['sh',path+scriptName]
    ##        pipe1 = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            bwaLogFile1 = open(params.scripts_BWA+"BWA_LOG1.log",'a')
            bwaLogFile2 = open(params.scripts_BWA+"BWA_LOG2.log",'a')
            pipe1 = subprocess.Popen(cmd, shell = False, stdout=bwaLogFile1, stderr=bwaLogFile2)
    
    ##        out,err = pipe1.communicate()
    ##        result = out.decode()
    ##        print "Result : ", [result]
    ##        if err <> "":
    ##            print "Error : ", err
    ##        print "BWA mapper scripts completed"
            ###########################################################################################################
            #BWA END
            ###########################################################################################################
            ###########################################################################################################
            #NOVO BEGIN
            ###########################################################################################################
            os.chdir(params.scripts_NOVO)
            path = params.scripts_NOVO
            scriptName = "NOVOAlign_pipeline.sh"
            for mapper in mappers:
                if mapper[0] == "NOVOAlign" and mapper[1] == True:
                    print "Running NOVOAlign script:", "sh "+params.scripts_NOVO+scriptName
            path = params.scripts_NOVO
            cmd = ['sh',path+scriptName]
    ##        cmd = ["echo","hello"]
    ##        pipe2 = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            novoLogFile1 = open(params.scripts_NOVO+"NOVO_LOG1.log",'a')
            novoLogFile2 = open(params.scripts_NOVO+"NOVO_LOG2.log",'a')
            pipe2 = subprocess.Popen(cmd, shell = False, stdout=novoLogFile1, stderr=novoLogFile2)
    
    ##        out,err = pipe2.communicate()
    ##        result = out.decode()
    ##        print "Result : ", [result]
    ##        if err <> "":
    ##            print "Error : ", err
    ##        print "NOVOAlign mapper scripts completed"
            ######################################################################
            #NOVO END
            ######################################################################
            ###########################################################################################################
            #SMALT BEGIN
            ###########################################################################################################
            os.chdir(params.scripts_SMALT)
            path = params.scripts_SMALT
            scriptName = "SMALT_pipeline.sh"
            for mapper in mappers:
                if mapper[0] == "SMALT" and mapper[1] == True:
                    print "Running SMALT script:", "sh "+params.scripts_SMALT+scriptName
            path = params.scripts_SMALT
            cmd = ['sh',path+scriptName]
    ##        pipe3 = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            smaltLogFile1 = open(params.scripts_SMALT+"SMALT_LOG1.log",'a')
            smaltLogFile2 = open(params.scripts_SMALT+"SMALT_LOG2.log",'a')
            pipe3 = subprocess.Popen(cmd, shell = False, stdout=smaltLogFile1, stderr=smaltLogFile2)
    ##        out,err = pipe3.communicate()
    ##        result = out.decode()
    ##        print "Result : ", [result]
    ##        if err <> "":
    ##            print "Error : ", err
    ##        print "SMALT mapper scripts completed"
            ######################################################################
            #SMALT END
            ######################################################################
            areadyDoneSpolpred = False
            if MTB:
                if not areadyDoneSpolpred and runSpolpredOrSkip <> "n":
                    exit_codes = [p.wait() for p in pipe1,pipe2,pipe3,pipe_strainIdent]
                    out4,err4 = pipe_strainIdent.communicate()
                else:
                    exit_codes = [p.wait() for p in pipe1,pipe2,pipe3]
                    
            else:
                exit_codes = [p.wait() for p in pipe1,pipe2,pipe3]
            out1,err1 = pipe1.communicate()
            out2,err2 = pipe2.communicate()
            out3,err3 = pipe3.communicate()
            
            try:
                result1 = out1.decode()
                result2 = out2.decode()
                result3 = out3.decode()
                if MTB:
                    result4 = out4.decode()
            except:
                print "variant detection complete"
            
    ##        print "Result : ", [result3]
    ##        if err3 <> "":
    ##            print "Error : ", err3
    ##        print "Mapper scripts completed"
    ##        print params.scripts_SMALT
    ##        raw_input("ok to proceed?")
            
            bwaLogFile1.close
            bwaLogFile2.close
            novoLogFile1.close
            novoLogFile2.close
            smaltLogFile1.close
            smaltLogFile2.close
            if MTB:
                try:
                    strainLogFile1.close 
                except:
                    pass
                try:
                    strainLogFile2.close 
                except:
                    pass
                    
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("MainPipeline ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            
        if controlPoint <= 6:
            if debugMode:
                print "Creating genome coverage bed files"
                print "control point ", [controlPoint]
                raw_input("press enter")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("GenomeCov started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            BWAGenCov = params.BWAAligned+"GenomeCoverage/" #NOVO Results dir
            NOVOGenCov = params.NOVOAligned+"GenomeCoverage/" #NOVO Results dir
            SMALTGenCov = params.SMALTAligned+"GenomeCoverage/" #NOVO Results dir
            calculate_coverage_bed(BWAGenCov) #outputs results into inputfolder
            calculate_coverage_bed(NOVOGenCov) #outputs results into inputfolder
            calculate_coverage_bed(SMALTGenCov) #outputs results into inputfolder
            ####################
            '''
            if spaceSavingMode:
                for covDir in [BWAGenCov,NOVOGenCov,SMALTGenCov]:
                    os.chdir(covDir)
                    for fileX in os.listdir(covDir):
                        if "_dedup_genomecov.txt" in fileX:
                            #raw_input("will now remove file"+str(fileX))
                            os.remove(fileX)
            '''
            print "genome coverage calculation complete"
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("GenomeCov ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            ####################
        if controlPoint <= 7:
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("genCovCalc started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            if debugMode:
                print "control point 6"
                raw_input("gen cov calc, press enter")
            #Compress deletion data before annotation
    ##        mainDir = "C:/Ruben/[ALL_RESULTS]/[ANNO_TEST]/Results/"      
            #mainDir = params.mapperOut
            BWAGenCov = params.BWAAligned+"GenomeCoverage/" #NOVO Results dir
            NOVOGenCov = params.NOVOAligned+"GenomeCoverage/" #NOVO Results dir
            SMALTGenCov = params.SMALTAligned+"GenomeCoverage/" #NOVO Results dir
            for covDir in [BWAGenCov,NOVOGenCov,SMALTGenCov]:
                print "Compressing deletion data in :",covDir 
                compressDeletionData_bedtools(covDir)#---------------------------------------------------------control point--------------------------------------------------------------------------------------
                #compressDeletionData(covDir)#---------------------------------------------------------control point--------------------------------------------------------------------------------------
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("genCovCalc ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
                
        if controlPoint <= 8:
            print "Summarizing and / or annotating detected variants"
            if debugMode:
                raw_input("press enter")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("annotation started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            VCF_Location_List = [params.BWAAligned+snpDir, params.NOVOAligned+snpDir,params.SMALTAligned+snpDir]
            emblDir = params.EMBL
            annotationFile = params.emblFile
            outputDir = params.mapperOut+"ANNOTATED_VARIANTS/"
            try:
                os.mkdir(outputDir)
            except:
                "already exists"        
            pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties = autoAnnotateEMBL(emblDir, annotationFile, outputDir, VCF_Location_List, mapperOrderList, annotationAllowed)
            print "Variant annotation completed"
            print "Annotating putative deletions"
            outputDir = params.mapperOut
            if annotationAllowed:
                addAnnoDataToDeletions(outputDir,pos_to_feature_num_dict, featureNum_to_Anno_DataDict, known_feature_properties,mapperOrderList)
            print "Annotation complete"
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("annotation ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            
        if controlPoint <= 9:
            print "Preparing to filter variants."
            if debugMode:
                raw_input("press enter")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Filtering started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            ##########################################################################
            #Variant filtering 
            ##########################################################################
            
            annotatedDir = params.mapperOut+"ANNOTATED_VARIANTS/"
            outputDir =  params.mapperOut+"FILTERED_VARIANTS/"

            try:
                os.mkdir(outputDir) 
            except: "already exists"
            
            print "Applying filtering settings:"
            if debugMode:
                print "Variants containing these keywords will be filtered:", params.junkTerms
            if params.gatkFlag:
                print "filtering settings specific to variants detected by GATK:"
                print "mapper count: ", params.mapperCount_GATK
                print "Quality cutoff: ", params.qualityCutOff_GATK
                print "readFreqCutoff cutoff: ", params.readFreqCutoff_GATK
                print "minCoverage cutoff: ", params.minCoverage_GATK

            if params.samtoolsFlag:
                print "filtering settings specific to variants detected by SAMTOOLS:"
                print "mapper count: ", params.mapperCount_SAMTOOLS
                print "Quality cutoff: ", params.qualityCutOff_SAMTOOLS
                print "readFreqCutoff cutoff: ", params.readFreqCutoff_SAMTOOLS
                print "minCoverage cutoff: ", params.minCoverage_SAMTOOLS

            #junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutoff_GATK,readFreqCutoff_SAMTOOLS
            
            #junkTerms = ["ppe ","PE/PPE","repeat","pe-pgrs","pe_pgrs","pe family","insertion seqs and phages","Possible transposase"] 

            if params.filterCustomPositions:
                exclusionListFolder = params.exclusionListFolder 
                exclude_list = loadPostitionsToRemove(exclusionListFolder)
            else:
                exclude_list = []
            #print params.gatkFlag
            #print params.samtoolsFlag
            exclude_list2 = []
            if params.filterMappabilityPositions:
                exclude_list2 = loadPostitionsToRemove(params.mappabilityDir) #refDir+"/"+userRef+"/Mappability/")
                if exclude_list2 == []:
                    print "Error, no positions could be loaded from any .txt file in the folder: "+ params.mappabilityDir # refDir+"/"+userRef+"/Mappability/"
                    raw_input("press enter to continue")
                    pass
            exclude_list += exclude_list2
            exclude_list.sort()


                
            RemoveJunkFromVCF5(annotatedDir,outputDir,params.junkTerms,params.mapperCount_GATK,params.mapperCount_SAMTOOLS,params.qualityCutOff_GATK,params.qualityCutOff_SAMTOOLS,params.minCoverage_GATK,params.minCoverage_SAMTOOLS,params.readFreqCutoff_GATK,params.readFreqCutoff_SAMTOOLS,exclude_list, params.filterCustomPositions, params.gatkFlag, params.samtoolsFlag)
            print "Variant filtering completed" 
            inputDir = params.mapperOut+"ANNOTATED_DELETIONS/"
            outputDir = params.mapperOut+"FILTERED_DELETIONS/"
            try:
                os.mkdir(outputDir)
            except:
                print "Filtered deletion directory already exists..."
            if annotationAllowed:
                filterDeletions(inputDir,outputDir,params.mapperCount_GATK,params.mapperCount_SAMTOOLS,params.junkTerms)
            print "Deletion filtering completed"
            #duration =  time.time()- startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Filtering ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
        #############################################################################################################
    
        if controlPoint <= 10: #phenotype prediction
            phenoAllowed = True
            print "Matching known variants to phenotype database"
            if debugMode:
                raw_input("press enter to continue")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Pheno started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            try:
                os.chdir(params.pheno)
            except:
                print "No database of known molecular markers found (For disease/phenotype/drug resistance determination)."
                phenoAllowed = False
            if phenoAllowed:
                phenoFileList = []
                phenoAllowed = True
                for fileX in os.listdir(params.pheno):
                    if fileX.endswith(".txt"):
                        phenoFileList.append(fileX)
                if len(phenoFileList) == 0:
                    print "No phenotype database was detected in: ", params.pheno
                    print "This wil not allow matching of detected variants to known phenotypes."
                    print "Refer to user manual on creating an appropriate phenotype database for your selected reference."
                    phenoAllowed = False 
    
                if len(phenoFileList) > 1:
                    print "Error, more than one .txt file found in:", params.pheno
                    print "Please ensure that only one phenotype databse file is present in this folder." 
                    phenoAllowed = False
            if phenoAllowed:
                print "Matching detected variants to known phenotype"
                if "MycobacteriumTuberculosis_H37Rv" in params.reference: 
                    MTB = True
                    print "Matching to M. tuberculosis"
                resultsFolder = params.mapperOut 
                FILTERED_VARIANTS = params.mapperOut+"FILTERED_VARIANTS/"  
                FILTERED_DELETIONS = params.mapperOut+"FILTERED_DELETIONS/"
                outputFolder = params.mapperOut
                variantListName = params.pheno+fileX             
                MATCH_PHENO_TO_VARIANTS(variantListName,FILTERED_VARIANTS,FILTERED_DELETIONS,outputFolder,MTB,debugMode, annotationAllowed)
                print "Phenotype matching to detected variants complete."
                if debugMode:
                    print FILTERED_VARIANTS
                    print FILTERED_DELETIONS
                    print outputFolder
                    print MTB
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Pheno ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
        ###################################################################################################################################
        lineageAllowed = False        
        if controlPoint <= 11:
            print "Starting Lineage Detection"
            if debugMode:
                raw_input("press enter")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("Lineage started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            #Determine sample lineage based on list of known snps
            try:
                os.chdir(params.lineage)
                lineageFileList = []
                lineageAllowed = True
                for fileX in os.listdir(params.lineage):
                    if fileX.endswith(".txt"):
                        lineageFileList.append(fileX)
                if len(lineageFileList) == 0:
                    print "No lineage was detected in: ", params.lineage
                    print "This wil not allow matching of detected variants to known lineages."
                    print "Refer to user manual on creating an appropriate lineage database for your selected reference."
                    lineageAllowed = False 
        
                if len(lineageFileList) > 1:
                    print "Error, more than one .txt file found in:", params.pheno
                    print "Please ensure that only one phenotype databse file is present in this folder." 
                    lineageAllowed = False
            except:
                print "No list of lineage markers found, skipping lineage matching"
                lineageAllowed =  False
            
            if lineageAllowed:
                f = open(params.lineage+fileX)
                header = f.readline()
                f.close()
                temp = header.split("\t")
                assumeHeader = ["lineage","coordinate","gene_coordinate","allele_change","codon_number","codon_change","amino_acid_change","locus_Id","gene_name","mutation_type","essential"]
                pos = -1
                for element in assumeHeader:
                    pos+=1
                    if element <> temp[pos].strip(): #replace("\n","").replace("\r",""):
                        print "Format error in lineage database file,"
                        print "The col num:",pos,"does not match to ",element
                        print [temp[pos]],"vs",[element]
                        print "Please refer to the user manual for correctly formatting the lineage database."
                        lineageAllowed = False
                        break
            if lineageAllowed:
                FILTERED_VARIANTS = params.mapperOut+"FILTERED_VARIANTS/"
                determine_lineages(params.mapperOut+"FILTERED_VARIANTS/",params.lineage+fileX)
                print "Lineage determination completed"
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("lineage ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
    
        #################################################################################################
        if controlPoint <= 12: #Create Per sample Summary File
            print "creating detailed report file." #- currintly missing spolpred data
            #Here the summary file needs to report all data available, does not matter if annotation was possible
            if debugMode:
                raw_input("press enter to create report file")
            #startTime = time.time()
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("summary started\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            orderedFiles = []
            fileData = {}
            for fileX in os.listdir(params.fastQ):
                if fileX.lower().endswith(".fastq.gz") or fileX.lower().endswith(".fastq"):
                    if "_" not in fileX:
                        temp = fileX.replace(".gz","")
                        temp = temp.replace(".fastq",'')
                    else:    
                        temp = fileX.split("_")[0]
                    if temp not in fileData:
                        fileData[temp] = {} #a dictionary of dictionaries
                        orderedFiles.append(temp)
            orderedFiles.sort()
            #print "Summarizing results for :",fileData
            #{File} : {coverage_BWA,coverage_NOVO,coverage_SMALT,DR,lineage,spolpred...etc}
    
            #loading genome coverage data
            #################################################
            mapperListFileNameToCovDict = []
            for mapper in mapperOrderList:
                tempDict = {}
                tempData = []
                try:
                    f = open(params.mapperOut+mapper+"/GenomeCoverage/Genome_Coverage_Results_Summary.txt",'r')
                    f.readline()
                    for line in f:
                        temp = line.split("\t")
                        name = temp[0]
                        cov = temp[1].replace("\n","")
                        tempDict[name] = cov
                    f.close()
                except:
                    print "Error loading genome coverage data, file not found:", params.mapperOut+mapper+"/GenomeCoverage/Genome_Coverage_Results_Summary.txt"
                mapperListFileNameToCovDict.append(tempDict) #a list of 3 dictionaries
            #now have [{bwa_file:cov},{novo_file:cov},{smalt_file:cov{]
            #STORE the data in the main summary dictionary
            pos = -1
            for mapper in mapperOrderList:
                pos += 1
                covData = mapperListFileNameToCovDict[pos]
                for fileName in orderedFiles:
                    if fileName in covData:
                        if "AVR_COVERAGE" in fileData[fileName]:
                            fileData[fileName]["AVR_COVERAGE"].append(covData[fileName])
                        else:
                            fileData[fileName]["AVR_COVERAGE"] = [covData[fileName]] #slightly complicated...

                            #this ends up as fileName : [10,10,4] for bwa cov novo cov and smalt cov
            ###########################################
            #Loading lineage data
            if debugMode and MTB:
                linAns = raw_input("Forcing lineage allowed here?")
                if linAns == "n" or linAns == "n":
                    lineageAllowed = False
                else:
                    lineageAllowed = True
                    
            if lineageAllowed:
                try:
                    f = open(params.mapperOut+"full_lineageData.txt",'r')
                    f.readline()
                except:
                    raw_input("no lineage data detected")
                for line in f:
                    temp = line.split("\t")
                    name = temp[0].split("_")[0]
                    if ".fastq" in name:
                        name = name.replace(".gz","")
                        name = name.replace(".fastq","")
                    lineage = temp[1]
                    score = temp[2]
                    if name in fileData:
                        fileData[name]["LINEAGE"] = lineage+"\t"+score
                    else:
                        print "this is fileData names", fileData.keys()
                        print "error #4454, file with no output results detected, possible reason: Non-Unique identifier left of '_' sign OR a Corrupt FASTQ. File affected is :",name
                        raw_input("Press enter to continue") 
            ############################################################    
            if MTB:
                lookupSpoligotypes(spolPredOut,debugMode, params.mapperOut, params.binDir)
                f = open(params.mapperOut+"SpolPred_Results_Summary.txt",'r')
                temp = f.readline()
                for line in f:
                    temp = line.split("\t")
                    name = temp[0]
                    if ".gz" in name:
                        name = name.replace(".gz","")
                    if ".fastq" in name:
                        name = name.replace(".fastq","")
                    code = temp[1]
                    commonName = temp[2].replace("\n","")
                    commonName = commonName.replace("\r","")
                    if name in fileData:
                        fileData[name]["SPOLPRED"] = code+"\t"+commonName
                    else:
                        print "this is fileData",fileData.keys()
                        print "error #4454, file with no output results detected, possible error: Corrupt FASTQ. File affected is :",name
                        raw_input("Press enter to continue") 
                f.close()

            #######################################
            #get % mapped reads
            mappedReadsList = []
            for folderName in [params.BWAAligned_aln,params.NOVOAligned_aln,params.SMALTAligned_aln]:
                os.chdir(folderName)
                mappedReadsDict = {}
                for fileX in os.listdir(folderName):
                    if "samtools_stats.txt" not in fileX or "samtools_stats.txt~" in fileX :
                        continue
                    tempFile = open(fileX,'r')
                    numReads = tempFile.readline()
                    if numReads == "":
                        print "no mapped reads data found for file", fileX
                        numReads = ""
                        percentageMapped = ""
                    else:
                        numReads=numReads.split()[0]
                        tempFile.readline()
                ##        percentageMapped = tempFile.readline().split("(")[1].split(":")[0]
                        percentageMapped = tempFile.readline()
                        if "duplicates" in percentageMapped or "supplementary" in percentageMapped:
                            percentageMapped = tempFile.readline()
                        if "duplicates" in percentageMapped or "supplementary" in percentageMapped:
                            percentageMapped = tempFile.readline()
                ##        print [percentageMapped]
                        percentageMapped = percentageMapped.split("(")[1]
                ##        print percentageMapped
                        percentageMapped = percentageMapped.split(":")[0]
                ##        print percentageMapped
                ##        raw_input()
                    if "_" in fileX:
                        mappedReadsDict[fileX.split("_")[0]] = [percentageMapped,"of total",numReads]
                    else:
                        mappedReadsDict[fileX] = [percentageMapped,"of total",numReads]
                    tempFile.close()
                mappedReadsList.append(mappedReadsDict)

            #now have [{bwa_file:[percentageMapped,numReads]},{novo_file:[percentageMapped,numReads]},{smalt_file:[percentageMapped,numReads]}]
            #STORE the data in the main summary dictionary
            pos = -1
            for mapper in mapperOrderList:
                pos += 1
                mappedReadsData = mappedReadsList[pos]
                for fileName in orderedFiles:
                    if fileName in mappedReadsData:
                        if "MAPPED_READS" in fileData[fileName]:
                            fileData[fileName]["MAPPED_READS"].append(mappedReadsData[fileName])
                        else:
                            fileData[fileName]["MAPPED_READS"] = [mappedReadsData[fileName]] #slightly complicated...
            #NOW have file : [% mappedreads, numreads] for bwa,  [% mappedreads, numreads] for novo,  [% mappedreads, numreads] for smalt

            ########################################
            #########LOAD DR DATA
            try:
                f = open(params.mapperOut+"PHENO_RESULTS.txt",'r')
                DRflag = True
            except:
                print "NO phenotype file found"
                DRflag = False
            if DRflag:    
                DR_header = f.readline()
                for line in f:
                    temp = line.split("\t")
                    name = temp[0]
                    nameLen = len(name)
                    if "_" in name:
                        name = name.split("_")[0]
                    DRdata = line[nameLen+1:] 
                    if name in fileData:
                        if "PHENO" in fileData[name]:
                            
                            print "have the same DR data element for more than one file:", name
                            raw_input("FATAL ERROR, fix file name error")
                        else:
                            fileData[name]["PHENO"] = DRdata
                    else:
                        raw_input("error have dr for a file not in main list! Press enter to continue")

            #################################################
            #write data to file
            if debugMode:
                phenoAns = raw_input("is pheno allowed here?")
                if phenoAns not in ["n","N"]:
                    phenoAllowed = True
                raw_input("now writing to one big happy file, press enter")
            else:
                print "Writing summarized results to file"
            os.chdir(params.mapperOut)
            f = open("SUMMARY.txt",'w')
            if phenoAllowed:
                if MTB:
                    keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","SPOLPRED","PHENO"]
                else:
                    keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","PHENO"]
            else:
                if MTB:
                    keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE","SPOLPRED"]
                else:
                    keys = ["AVR_COVERAGE","MAPPED_READS","LINEAGE"]
             
            f.write("SAMPLE_NAME")
            f.write("\tQC\tQC_Average_Coverage_Comment\tQC_Percentage_Mapped_Reads_Comment") #New June    
            for key in keys[:-1]:
                if MTB and key == "SPOLPRED":
                    f.write("\tSPOLPRED_OCTAL_CODE\tCOMMON_NAME")
                elif key == "LINEAGE":
                    f.write("\tLINEAGE\tNUM_LINEAGE_SNP_MATCHES")
                else:
                    f.write("\t"+key)
            flagX = True
            if phenoAllowed and DRflag:
                for x in DR_header.split("\t"):
                    if flagX:
                        flagX = False # to skip sample_name
                        continue
                    f.write("\t"+x)
                if not "\n" in x:
                    f.write("\n")
            else:
                f.write("\n")
            #header is done, now write the data for each sample
            for fileName in orderedFiles:
                f.write(fileName)
                #if True:
                try:
                    key = "AVR_COVERAGE"  
                    covData = str(fileData[fileName][key])
                    covData = covData.replace("'","").replace("[","").replace("]","") #Using all the converage info available 
                    covData = covData.split(",") 
                except: 
                    covData = ""
                #if True:
                try:
                    key = "MAPPED_READS"
                    mapData = str(fileData[fileName][key])
                    mapData = mapData.replace("'","").replace("[","").replace("]","")
                    mapData=mapData.replace(" of total, ","")
                    mapData=mapData.split(",")
                    mapDataList = [] 
                    for tempString in mapData:
                        if "%" in tempString:
                            mapDataList.append(tempString.replace("%",""))
                except:
                    mapDataList = []
                QCString = ""
                QC_MAIN = "PASS"
                flag = False
                for element in covData:
                    if element == "" or "ERROR" in element:
                        continue
                    elif int(element) < int(params.minCov):
                        flag = True
                if flag:
                    QC_MAIN = "FAIL"
                    QCString= "Low_Coverage, <"+str(params.minCov)+"\t"
                if not flag:
                    QCString = "\t"
                flag = False
                for element in mapDataList:
                    if float(element) < float(params.minMappedReads): 
                        flag = True
                if flag:
                    QC_MAIN = "FAIL"
                    QCString += "Low_%_Mapped_Reads, <"+str(params.minMappedReads)#+"\t"
                #now write the QC, comment1, comment2
                f.write("\t"+QC_MAIN+"\t"+QCString)

                for key in keys:
                    if key not in fileData[fileName]:
                        if debugMode:
                            print fileName, "does not have info for", key
                        if MTB and key == "SPOLPRED":
                            f.write("\tN/A\t")
                        elif not MTB and key == "SPOLPRED":
                            f.write("\t")
                        else:
                            f.write("\tN/A")
                        lastString = "A"
                    else:
                        print "writing:", ["\t"+str(fileData[fileName][key])]
                        f.write("\t"+str(fileData[fileName][key]))
                        lastString = str(fileData[fileName][key])[-1]
                if lastString <> "\n":
                    f.write("\n")
            f.close()
            #duration = time.time() - startTime
            try:
                os.chdir(globalDir)
                timeLogFile = open('timeLog.txt','a')
                timeLogFile.write("summary ended\n"+strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
                timeLogFile.close()
            except:
                raw_input("Error, could not create timelog, press enter to continue")
            print "USAP complete, proceed to additional tool menu for further built-in analysis tools"
            os.chdir(globalDir)
            f = open("exitSignal.txt",'w')
            f.write("complete") #here write to file complete - this stops the monitoring tool
            f.close()
    #######################################################################################################################################################  

    #######################################################################################################################################################

    #######################################################################################################################################################

    #######################################################################################################################################################

    #######################################################################################################################################################  

    #######################################################################################################################################################

    #######################################################################################################################################################  

    #######################################################################################################################################################
    elif ans == "2": #USAP extra tools
        for x in range(10):
            print
        disclaimer = '''
        USAP V1.0
        Copyright 2016 Ruben van der Merwe
        This program is distributed under the terms of the GNA General Public Licence (GPL).
        
        This file is part of USAP.

        USAP is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        USAP is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with USAP. If not, see <http://www.gnu.org/licenses/>.'''
        print disclaimer
        print
        print "_____________________________________________________________________________________________"
        print "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
        print "USAP - Universal sequence analysis pipeline for whole genome sequence data                   "
        print "V1.0, Created by Ruben G. van der Merwe, 1 August 2016, email: rubengvdm@hotmail.com           "
        print "Copyright Ruben G. van der Merwe 2016                                                        "
        print "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
        print "_____________________________________________________________________________________________"
        print ""
        #####################################################################################################
        
        globalDir = os.getcwd()
        if "/BIN" in globalDir:
            globalDir = globalDir[:-4]
        tools = globalDir+"/Tools/"
        refDir = globalDir+"/Reference"
        ans = "?"
        while ans not in ["Q","q"]:   #Keep menu alive until user selects quit.
            print
            while ans not in ["1","2","3","4","5","6","7","8","9","10","Q","q"]:
                ###############################################################################################################################################
                print "USAP tools:"
                print "1: Reference mappability calculation using GMA (Only run this once per reference)"
                print "2: Custom variant filtering" # (such as to remove homoplasy, variants in regions with low mappability or user specified regions)" 
                print "3: Generate whole genome SNV multi-Fasta file for phylogeny"
                print "4: Variant comparison between samples or groups of samples"
                print "5: Generate SNP distance matrix for two or more samples"
                print "6: Find variants in specific gene(s) / positions"
                print "7: Convert USAP filtered variants to VCF"
                print "8: Create consensus sequence FASTA file for each file (Requires step 7)" 
                print "9: Decompose heterogeneous SNVs and indels"
                print "10: Reannotate decomposed variants and attempt matching to known mol markers"
                print "Q: Quit"
                ###############################################################################################################################################
                ans = raw_input("Please select the tool you would like to run from the list above: ")
                continue
            if ans == "Q" or ans == "q":
                print "Thank you for using USAP, goodbye."
                exit(0)
            if ans == "1":
            ####################################################################
            # Mappability
            ####################################################################
                print "Genome mappability score analyzer wrapper script. The paper describing the Genome Mappability Score Analyzer is described is: 'Bioinformatics Aug 2012 15;28(16):2097-105. doi: 10. 1093/bioinformatics/bts330. Epub 2012 Jun4. Authors: Lee H and Schatz MC.'. Also see https://sourceforge.net/projects/mga-bio for further details." 
                init_GMA(tools)
                
                gma_BWA = tools+"gma-0.1.5/bin/bwa"
                gmaDir = tools+"gma-0.1.5/"
                scripts_mappability = globalDir+"/Scripts/Mappability/"

                refOptions = [name for name in os.listdir(refDir) if os.path.isdir(os.path.join(refDir, name))]
                refOptions.sort()
                flag = False
                while not flag:
                    counter = 0
                    print "--------------------------------------------"
                    print "Please select a reference from the selection below:"
                    for ref in refOptions:
                        counter += 1
                        print str(counter)+":\t",ref
                    print "Q: quit\n"
                    
                    selectedRef = raw_input("Enter the corresponding number for the reference (1,2,3 etc): ")
                    if selectedRef =="q" or selectedRef =="Q":
                        quit()
                    try:
                        selectedRef = int(selectedRef)
                    except:
                        selectedRef = "N/A"
                    if selectedRef not in range(1,len(refOptions)+1): 
                        continue
                    else:
                        print "Reference selected:", refOptions[selectedRef-1]
                        userRef = refOptions[selectedRef-1]
                        break
                
                for fileX in os.listdir(refDir+"/"+userRef+"/FASTA"):
                    if fileX.lower().endswith(".fasta"):
                        ref = fileX
                        break
                print "The detected fasta file for use in mappability determination is:",fileX
                ans = 'z'
                while ans.upper() not in ["Y","N"]:
                    ans = raw_input("Press 'Y' to continue calculating mappability (generates a report file of poor mapping regions), enter 'N' to quit:\t")
                if ans.upper() == "N":
                    exit(0)
                elif ans.upper() == "Y":
                    if debugMode:
                        raw_input("running mappability determination on file"+ fileX)
                    mapResultsDir = refDir+"/"+userRef+"/Mappability/"
                    try:
                        os.mkdir(mapResultsDir)
                    except:
                        pass
                    try:
                        os.mkdir(scripts_mappability)
                    except:
                        pass

                    refPath = refDir+"/"+userRef+"/FASTA" 
                    outputScript = scripts_mappability+"map.sh"
                    os.chdir(refPath)     
                    
                    refName = fileX #"H37Rv_4411532_updated_13_jun_2013.fasta"
                    GMA_wrapper(gmaDir, gma_BWA, mapResultsDir, refPath, refName, outputScript)
                    print "Running GMA, this will take some time..."
                    cmd = ['sh',outputScript]
                    pipe = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out,err = pipe.communicate()
                    result = out.decode()
                    print out
                    print err
                    print "GMA complete"

                    #Find the obscure dir name from GMA
                    gmaOutputDir = "NONE_FOUND"
                    for x in os.listdir(mapResultsDir):
                        if os.path.isdir(mapResultsDir+x) and not os.path.isfile(mapResultsDir+x):
                            gmaOutputDir = mapResultsDir+x+"/"
                            break 
                    print "Creating list of low mappability for use in custom filtering..."
                    results = []
                    f = open(gmaOutputDir+"mapred.txt",'r')
                    f.readline()
                    for line in f:
                        temp = line.split("\t")
                        pos = temp[1]
                        val = float(temp[-1])
                        if val == 0.0:
                            results.append(str(pos)+"\t"+str(val)+"\n")
                            results.append(pos)
                    f.close()
                    f = open(mapResultsDir+"low_mappability.txt",'w')
                    for x in results:
                        f.write(str(x)+"\n")
                    f.close()
                    
                    try:
                        timeLogFile.close()
                    except:
                        pass
                    #raw_input("press enter to remove files...")
                    os.chdir(gmaOutputDir)
                    for fileX in os.listdir(gmaOutputDir):
                        if "mapred" not in fileX and "low_mappability" not in fileX and os.path.isfile(fileX):
                            print "removing", fileX
                            os.remove(fileX)
                    os.chdir(mapResultsDir)
                    for fileX in os.listdir(mapResultsDir):
                        if "mapred" not in fileX and "low_mappability" not in fileX and os.path.isfile(fileX):
                            print "removing", fileX
                            os.remove(fileX)
                print "Mappability analysis using GMA complete, now proceed to custom variant filtering tool"
                ans = "?" #reset user selection
            #####################################################################
            if ans == "2": #Custom variant filtering
            #####################################################################
                #Load filtering settings from file
##                gatkFlag = True
##                samtoolsFlag = True

                reads_type, refDir, binDir, globalDir, prev_cpu_count,prev_memory,fastQDir, outputDir, userRef, trimmingMode, useBWA, useNOVO,  useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK, readFreqCutOff_SAMTOOLS,    filterMappabilityPositions, filterCustomPositions,    filterOnKeywords , tempDir1, tempDir2, mappers, variantTools, minCov, minMappedReads = loadSettingsFile(2,2000)
                #print [reads_type, refDir, binDir, globalDir, prev_cpu_count,prev_memory,fastQDir, outputDir, userRef, trimmingMode, useBWA, useNOVO,  useSMALT,    gatkFlag,    samtoolsFlag,    mapperCount_GATK, mapperCount_SAMTOOLS,    qualityCutOff_GATK,    qualityCutOff_SAMTOOLS, minCoverage_GATK,    minCoverage_SAMTOOLS,    readFreqCutoff_GATK, readFreqCutOff_SAMTOOLS,    filterMappabilityPositions, filterCustomPositions,    filterOnKeywords , tempDir1, tempDir2, mappers, variantTools, minCov, minMappedReads]

                raw_input("todo: make sure low mapp removal works")
                ##GET the reference - create a separate function for this will need it in several sections
                refOptions = [name for name in os.listdir(refDir) if os.path.isdir(os.path.join(refDir, name))]
                refOptions.sort()
                flag = False
                while not flag:
                    counter = 0
                    print "--------------------------------------------"
                    print "Please select a reference from the selection below:"
                    for ref in refOptions:
                        counter += 1
                        print str(counter)+":\t",ref
                    print "Q: quit\n"
                    
                    selectedRef = raw_input("Enter the corresponding number for the reference (1,2,3 etc): ")
                    if selectedRef =="q" or selectedRef =="Q":
                        quit()
                    try:
                        selectedRef = int(selectedRef)
                    except:
                        selectedRef = "N/A"
                    if selectedRef not in range(1,len(refOptions)+1): 
                        continue
                    else:
                        print "Reference selected:", refOptions[selectedRef-1]
                        userRef = refOptions[selectedRef-1]
                        break
                #################################################################
                    
                os.chdir(globalDir)
                detectedMainOutput = ""
                try:
                    f = open("userSettings.txt",'r')
                    for line in f:
                        temp = line.split("\t")
                        if temp[0] == "OUTPUT_DIRECTORY":
                            detectedMainOutput = temp[1].replace("\n","")
                        if temp[0] == "reference":
                            detected_ref = temp[1].replace("\n","")     
                except:
                    print "Error, the userSettings.txt file is missing from the expected location:", globalDir
                    raw_input("press enter to exit")
                    exit(0)
                annotatedDir = detectedMainOutput+"/Results/ANNOTATED_VARIANTS/"
                accept = ""
                while accept not in ["Y","y","n","N"]:
                    accept = raw_input("Would you like to use the following folder as input: "+annotatedDir+" ? [Y/N]:")
                if accept in ["n","N"]:
                    flag = False
                    while not flag:
                        inputDir = raw_input("Please provide the location of the input folder: ")
                        try:
                            os.chdir(inputDir)
                            annotatedDir = inputDir
                            flag = True
                        except:
                            tempFlag = False
                            while not tempFlag:
                                ans = raw_input("error, this folder does not exist, would you like to create it? [Y/N]")
                                if ans in ["n","N"]:
                                    break
                                if ans in ["y","Y"]:
                                    try:
                                        os.mkdir(annotatedDir)
                                        tempFlag = True
                                        flag = True
                                    except:
                                        print "error creating folder", annotatedDir
                                        break
                elif accept in ["Y","y"]:
                    pass
                outputDir = detectedMainOutput+"/Results/FILTERED_VARIANTS/"
                accept = ""
                while accept not in ["Y","y","n","N"]:
                    accept = raw_input("Would you like to use the following folder as output: "+outputDir+" ? [Y/N]:")
                if accept in ["n","N"]:
                    flag = False
                    while not flag:
                        outputDir = raw_input("Please provide the location of the input folder: ")
                        try:
                            os.chdir(outputDir)
                            flag = True
                        except:
                            tempFlag = False
                            while not tempFlag:
                                ans = raw_input("error, this folder does not exist, would you like to create it? [Y/N]")
                                if ans in ["n","N"]:
                                    break
                                if ans in ["y","Y"]:
                                    try:
                                        os.mkdir(outputDir)
                                        tempFlag = True
                                        flag = True
                                    except:
                                        print "error creating folder", outputDir
                                        break
                refDir = globalDir+"/Reference/"
                junkTerms = []
                #try:
                print [detected_ref]
                #below should try to open KEYWORDSTOEXCLUDE / any text file inside it.

                print "Attempting to load keywords for variant filteting from file:", refDir+detected_ref+"/FASTA/filter_settings.txt"

                try:
                    f = open(refDir+detected_ref+"/FASTA/filter_settings.txt",'r')
                    for line in f:
                        temp = line.strip().replace("\n","")
                        if temp not in junkTerms:
                            junkTerms.append(temp)
                    f.close()
                except:
                    print "Could not load reference filter settings, assuming this file does not exist" 

                if junkTerms <> []:
                    print "These are the previous filter terms:"
                    print junkTerms 
                    print "Would you like to add or modify keywords to use for variant filtering ?"
                    print "Press Y to agree to filter these from all your samples, press C to customize your filter keywords or N to continue without filtering for keywords"
                    ans = raw_input("Y/N/C")
                    while ans.upper() not in ["Y","N","C"]:
                        ans = raw_input("Y/N/C")
                    if ans.upper() == "C":
                        junkTerms = []
                else:
                    ans = ""
                    while ans.upper() not in ["Y","N"]:
                        ans = raw_input("Would you like to manually enter keywords for use in filtering variants ? Y/N:")
                    
                if ans.upper() == "Y":
                    print "You can now manually enter keywords you would like to filter for"
                    print "if this keyword appears in any of your annotated variants, then these variants will be exclused from your downstream analysis"
                    print "enter each term followed by the return key, enter 'quit' terminate the process"
                    print "suggested terms are", junkTerms
                    ans2 = []
                    count = 0
                    while "quit" not in ans2:
                        count +=1
                        temp = raw_input("Please enter filter Term number "+str(count)+":")
                        print "(enter 'quit' to stop adding terms)"
                        if temp.lower() =="quit":
                            break
                        else:
                            ans2.append(temp)
                    junkTerms = ans2
                    print "your new filter terms are:",junkTerms
                
                #Have These:###########################
                #annotatedDir #the input dir
                #outputDir
                #junkTerms
                #######################################

                #Get filtering settings
                ans = ""
                while ans.upper() not in ["Y","N"]:
                    ans = raw_input("Would you like to use the filtering settings specified in the userSettings.txt file? Y/N: ")
                if ans.upper() == "N":
                    

                    mapperCount_GATK = "" 
                    while mapperCount_GATK not in ["0","1","2","3"]:
                        mapperCount_GATK = raw_input("mapperCount GATK variant caller (defualt = 3 provided that 3 mappers were used): ")
                        if mapperCount_GATK not in ["0","1","2","3"]:
                            print "Error, invalid selection. Selection must in either 0, 1, 2 or 3."
                            continue
                        else:
                            mapperCount_GATK = int(mapperCount_GATK)
                            break
                        
                    mapperCount_SAMTOOLS = ""
                    while mapperCount_SAMTOOLS not in ["0","1","2","3"]:
                        mapperCount_SAMTOOLS = raw_input("mapperCount SAMTOOLS mpileup variant caller (defualt = 0): ")
                        if mapperCount_SAMTOOLS not in ["0","1","2","3"]:
                            print "Error, invalid selection. Selection must in either 0, 1, 2 or 3."
                            continue
                        else:
                            mapperCount_SAMTOOLS = int(mapperCount_SAMTOOLS)
                            break

                    while True:
                        qualityCutOff_GATK = raw_input("Quality cutoff for GATK variants [0 to N]: ")
                        try:
                            qualityCutOff_GATK = float(qualityCutOff_GATK)
                            if qualityCutOff_GATK < 0:
                                print "error, the value must be a positive number"
                                continue
                            else:
                                break
                        except:
                            print "Error, invalid selection. Selection must be a positive number"
                            continue
                    while True:    
                        qualityCutOff_SAMTOOLS = raw_input("Quality cutoff for SAMTOOLS mpileup variants [0 to N]: ")
                        try:
                            qualityCutOff_SAMTOOLS = float(qualityCutOff_SAMTOOLS)
                            if qualityCutOff_SAMTOOLS < 0:
                                print "error, the value must be a positive number"
                                continue
                            else:
                                break
                            break
                        except:
                            print "Error, invalid selection. Selection must be a positive number"
                            continue

                    while True:    
                        minCoverage_GATK = raw_input("Minimum coverage for GATK variants [0 to N]: ")
                        try:
                            minCoverage_GATK = int(minCoverage_GATK)
                            break
                        except:
                            print "Error, invalid selection. Selection must be a number"
                            continue

                    while True:
                        minCoverage_SAMTOOLS = raw_input("Minimum coverage for SAMTOOLS Mpileup variants [0 to N]: ")
                        try:
                            minCoverage_SAMTOOLS = int(minCoverage_SAMTOOLS)
                            break
                        except:
                            print "Error, invalid selection. Selection must be a number"
                            continue

                    while True:
                        readFreqCutOff_GATK = raw_input("GATK variant Ratio of mutant / wild-type reads cutoff (mutant reads / total reads) [0.0 to 1.0]: ")
                        try:
                            readFreqCutOff_GATK = float(readFreqCutOff_GATK)
                            if readFreqCutOff_GATK >= 0.0 and readFreqCutOff_GATK <= 1.0:
                                break
                            else:
                                print "Error, invalid selection. Selection must be between 0.0 and 1.0"
                            continue
                        except:
                            print "Error, invalid selection. Selection must be a number"
                            continue

                    while True:    
                        readFreqCutOff_SAMTOOLS = raw_input("SAMTOOLS mpileup Ratio of mutant / wild-type reads cutoff (mutant reads / total reads) [0.0 to 1.0]: ")
                        try:
                            readFreqCutOff_SAMTOOLS = float(readFreqCutOff_SAMTOOLS)
                            if readFreqCutOff_SAMTOOLS >= 0.0 and readFreqCutOff_SAMTOOLS <= 1.0:
                                break
                            else:
                                print "Error, invalid selection. Selection must be between 0.0 and 1.0"
                                continue
                        except:
                            print "Error, invalid selection. Selection must be a number"
                            continue
                        
                    exclusionListFolder = refDir+detected_ref+"/EXCLUDE/"
                    filterSpecificPositions = ""
                    while filterSpecificPositions not in ["y","Y","N","n"]:
                        filterSpecificPositions = raw_input("Would you like to exclude custom variants detected in the exclustion folder under "+exclusionListFolder+" ? [Y/N]:")
                    if filterSpecificPositions in ["Y","y"]:
                        filterSpecificPositions = True
                        exclude_list = loadPostitionsToRemove(exclusionListFolder)
                        if exclude_list == {}:
                            print "No positions could be loaded from any .txt file in the folder: "+exclusionListFolder
                            raw_input("press enter to continue")
                            filterSpecificPositions = False
                    else:
                        filterSpecificPositions = False
                        exclude_list = {}

                    #print gatkFlag
                    #print samtoolsFlag

                    filterLowMappability = False
                    while filterLowMappability not in ["y","Y","N","n"]:
                        filterLowMappability = raw_input("Would you like to filter variants detected in regions of low mappability from folder  "+refDir+"/"+userRef+"/Mappability/"+" ? [Y/N]:")
                    if filterLowMappability in ["Y","y"]:
                        filterLowMappability = True
                        exclude_list2 = loadPostitionsToRemove(refDir+"/"+userRef+"/Mappability/")
                        
                        if exclude_list2 == {}:
                            print "Error, no positions could be loaded from any .txt file in the folder: "+ refDir+"/"+userRef+"/Mappability/"
                            print "Please run Reference mappability calculation using GMA (option 1 in this tool menu) first"
                            raw_input("press enter to continue without removing variants from low mappability regions.")
                            pass
                        exclude_list_final = exclude_list.copy()
                        exclude_list_final.update(exclude_list2)

                    
                
                    RemoveJunkFromVCF5(annotatedDir,outputDir,junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutOff_GATK, readFreqCutOff_SAMTOOLS, exclude_list_final ,filterSpecificPositions, gatkFlag, samtoolsFlag)
                else:
                    print "Using values loaded from userSettings.txt"
                    print "filterCustomPositions",filterCustomPositions
                    exclude_list = {}
                    if filterCustomPositions:
                        exclude_list = loadPostitionsToRemove(exclusionListFolder)
                        if exclude_list == {}:
                            print "No positions could be loaded from any .txt file in the folder: "+exclusionListFolder
                            raw_input("press enter to continue")
                            filterSpecificPositions = False
                    print "filterMappabilityPositions",filterMappabilityPositions
                    if filterMappabilityPositions == True:
                        exclude_list2 = loadPostitionsToRemove(refDir+"/"+userRef+"/Mappability/")
                        if exclude_list2 == {}:
                            print "Error, no positions could be loaded from any .txt file in the folder: "+ refDir+"/"+userRef+"/Mappability/"
                            print "Please run Reference mappability calculation using GMA (option 1 in this tool menu) first"
                            raw_input("press enter to continue without removing variants from low mappability regions.")
                            pass
                    exclude_list_final = exclude_list.copy()
                    exclude_list_final.update(exclude_list2)

                    #annotatedDir = inputDir
                    #outputDir = outputDir                    

                    filterSpecificPositions = filterMappabilityPositions or filterCustomPositions
                    print "readFreqCutoff_GATK", readFreqCutoff_GATK
                    print annotatedDir
                    print outputDir
                    print junkTerms
                    print mapperCount_GATK
                    print mapperCount_SAMTOOLS
                    print qualityCutOff_GATK
                    print qualityCutOff_SAMTOOLS
                    print minCoverage_GATK
                    print minCoverage_SAMTOOLS
                    print "readFreqCutoff_GATK", readFreqCutoff_GATK
                    print "readFreqCutOff_SAMTOOLS", readFreqCutOff_SAMTOOLS
                    #print exclude_list_final
                    print filterSpecificPositions
                    print gatkFlag
                    print samtoolsFlag
                    RemoveJunkFromVCF5(annotatedDir,outputDir,junkTerms,mapperCount_GATK,mapperCount_SAMTOOLS,qualityCutOff_GATK,qualityCutOff_SAMTOOLS,minCoverage_GATK,minCoverage_SAMTOOLS,readFreqCutoff_GATK, readFreqCutOff_SAMTOOLS, exclude_list_final ,filterSpecificPositions, gatkFlag, samtoolsFlag)
                            
                        
                #######################################################
                #filter the deletions:
                inputDir2 = detectedMainOutput+"/Results/ANNOTATED_DELETIONS/"
                outputDir2 = detectedMainOutput+"/Results/FILTERED_DELETIONS/"                
                filterDeletions(inputDir2,outputDir2, mapperCount_GATK, mapperCount_SAMTOOLS, junkTerms)
                print "Deletion filtering completed"
                #######################################################

                print "Filtering complete, attempting to update summary file."

                
                ################################################
                pheno = refDir+"/"+userRef+"/PhenotypeDB/"
                phenoAllowed = True
                
                print "Matching known variants to phenotype database"
                if debugMode:
                    raw_input("press enter to continue")
                try:
                    os.chdir(pheno)
                except:
                    print "No database of known molecular markers found (For disease/phenotype/drug resistance determination)."
                    phenoAllowed = False
                if phenoAllowed:
                    phenoFileList = []
                    phenoAllowed = True
                    for fileX in os.listdir(pheno):
                        if fileX.endswith(".txt"):
                            phenoFileList.append(fileX)
                    if len(phenoFileList) == 0:
                        print "No phenotype database was detected in: ", pheno
                        print "This wil not allow matching of detected variants to known phenotypes."
                        print "Refer to user manual on creating an appropriate phenotype database for your selected reference."
                        phenoAllowed = False 
        
                    if len(phenoFileList) > 1:
                        print "Error, more than one .txt file found in:", pheno
                        print "Please ensure that only one phenotype databse file is present in this folder." 
                        phenoAllowed = False
                if phenoAllowed:
                    print "Matching detected variants to known phenotype"
                    if "MycobacteriumTuberculosis_H37Rv" in userRef: 
                        MTB = True
                        print "Matching to Mycobacterium tuberculosis"
                    outputFolder = detectedMainOutput+"/Results/"
                    resultsFolder = outputFolder
                    FILTERED_VARIANTS = outputDir
                    FILTERED_DELETIONS = outputDir2 # params.mapperOut+"FILTERED_DELETIONS/"
                    
                    variantListName = pheno + fileX
                    annotationAllowed, BQSRPossible, emblFile = validateRefFiles(refDir,userRef)
                    MATCH_PHENO_TO_VARIANTS(variantListName, FILTERED_VARIANTS, FILTERED_DELETIONS, outputFolder, MTB, debugMode, annotationAllowed)
                    print "Phenotype matching to detected variants complete."
                    if debugMode:
                        print FILTERED_VARIANTS
                        print FILTERED_DELETIONS
                        print outputFolder
                        print MTB

                #--------------------------------------------
                mainOrExtraToolsMode = "extraTools"
                mapperOrderList = ["BWA","NOVO","SMALT"]
                mapperOut = resultsFolder
                spolPredOut = "SpolPredOut"
                BWAAligned = mapperOut+"BWA/"
                NOVOAligned = mapperOut+"NOVO/"
                SMALTAligned = mapperOut+"SMALT/"
                BWAAligned_aln = BWAAligned+"Alignment_Files/"
                NOVOAligned_aln = NOVOAligned+"Alignment_Files/"
                SMALTAligned_aln = SMALTAligned+"Alignment_Files/"
        
                makeSummaryFile(mainOrExtraToolsMode, debugMode, globalDir, fastQDir, mapperOrderList, mapperOut, MTB, spolPredOut, BWAAligned_aln, NOVOAligned_aln, SMALTAligned_aln, minCov, minMappedReads, phenoAllowed)            
                
                ans = "?" #reset user selection
            #####################################################################
            if ans == "3": #Create multi fasta for phylogeny
            #####################################################################    
                print "Running Whole Genome SNV generator for phylogeny"
                os.chdir(globalDir)
                detectedMainOutput = ""
                try:
                    f = open("userSettings.txt",'r')
                    for line in f:
                        temp = line.split("\t")
                        if temp[0] == "OUTPUT_DIRECTORY":
                            detectedMainOutput = temp[1].replace("\n","")
                except:
                    print "Error, the userSettings.txt file is missing from the expected location:", globalDir
                    raw_input("press enter to exit")
                    exit()
                filesForPhylo = detectedMainOutput+"/Results/FILTERED_VARIANTS/"
                BWAGenCov = detectedMainOutput+"/Results/BWA/GenomeCoverage/" 
                NOVOGenCov = detectedMainOutput+"/Results/NOVO/GenomeCoverage/" 
                SMALTGenCov = detectedMainOutput+"/Results/SMALT/GenomeCoverage/" 
                
                for genCovDir in [NOVOGenCov,BWAGenCov,SMALTGenCov]: 
                    try:
                        os.chdir(genCovDir) #find the first one that works
                        break
                    except:
                        continue    
                useCovData = True
                outputDir = detectedMainOutput+"/Results/"
                phyloAll(filesForPhylo, genCovDir, outputDir, useCovData)
                print "SNV FASTA created in folder:",outputDir 
                ans = "?" #reset user selection
            #####################################################################
            if ans == "4": #"Pairwise / Group variant comparison tool"
            #####################################################################    
                print "Pairwise / Group variant comparison tool"
                while not True:
                    print "This tool used two input directories A and B"
                    print "Please create two folders and place the relevant files into each (VCF, ANNOTATED or FILTERED"
                    dir1 = raw_input("Please enter the full path to the first folder or Q to exit: ")
                    if dir1 in ["q","Q"]:
                        ans = "?"
                        continue
                    if not dir1.endswith("/"):
                        dir1+= "/"
                    try:
                        os.chdir(dir1)
                    except:
                        print "error, could not access the folder", dir1
                        continue
                    
                    dir2 = raw_input("Please enter the full path to the second folder or Q to exit: ")
                    if dir2 in ["q","Q"]:
                        ans = "?"
                        continue
                    if not dir2.endswith("/"):
                        dir2+= "/"
                    try:
                        os.chdir(dir2)
                        break
                    except:
                        print "error, could not access the folder", dir2

                outputDir = dir1
                compareTwoDirectories2_main(dir1,dir2,outputDir)
                ans = "?" #reset user selection
            #####################################################################
            if ans == "5": #"SNP distance matrix / individual file comparison tool"
            #####################################################################
                print "SNP distance matrix / individual file comparison tool"
                '''
                1 Ask user to create one folders containing all VCFs to be included
                must copy the annotated or filtered vcfs into one folder
                then enter path 
                then run tool
                '''
                ############################################################################################################################################
                '''
                    F1 F2 F3
                F1
                F2
                F3
                '''
                '''
                #Change to suit your needs
                dir1 = "E:/Laura_VCF/raw_vcf_anno/new_filtered_bad_mapping_removed/pks1" 
                outputDir = dir1
                output_File_Name = "myTest123.txt"
                myOutputDir = "myDir"
                try:
                    os.mkdir(myOutputDir)
                except:
                    print myOutputDir,"already exists"
                outputDir_for_indiv_files = outputDir+"/"+myOutputDir
                snpDistanceMatrix(dir1,outputDir,outputDir_for_indiv_files,True,output_File_Name)
                '''
                ans = "?" #reset user selection
            #####################################################################
            if ans == "6": #"Find mutations in specific genes / positions 
            #####################################################################
                print "not implemented"
                ans = "?" #reset user selection
            
            #####################################################################
            if ans == "7": #"Convert USAP VCF to normal VCF
            #####################################################################
                os.chdir(globalDir)
                detectedMainOutput = ""
                try:
                    f = open("userSettings.txt",'r')
                    for line in f:
                        temp = line.split("\t")
                        if temp[0] == "OUTPUT_DIRECTORY":
                            detectedMainOutput = temp[1].replace("\n","")
                except:
                    print "Error, the userSettings.txt file is missing from the expected location:", globalDir
                    raw_input("press enter to exit")
                    exit()
                variantsDir =  detectedMainOutput+"/Results/FILTERED_VARIANTS/"
                outputDir = detectedMainOutput+"/Results/FILTERED_VARIANTS/VCF/"
                try:
                    os.mkdir(outputDir)
                except:
                    print "Could not create folder", outputDir, "might already exist."
                print "converting data to VCF..."
                
                convert_USAP_to_VCF(variantsDir,outputDir)
                ans = "?" #reset user selection
                
            #####################################################################
            if ans == "8": #"8: Create consensus sequence FASTA file for each file (Requires step 7)" 
            #####################################################################
                os.chdir(globalDir)
                detectedMainOutput = ""
                user_reference = ""
                try:
                    f = open("userSettings.txt",'r')
                    for line in f:
                        temp = line.split("\t")
                        if temp[0] == "OUTPUT_DIRECTORY":
                            detectedMainOutput = temp[1].replace("\n","")
                        if temp[0] == "reference":
                            user_reference = temp[1].replace("\n","")
                    f.close()
                except:
                    print "Error, the userSettings.txt file is missing from the expected location:", globalDir
                    raw_input("press enter to exit")
                    exit()
                refDir = globalDir+"/Reference/"
                refPath = refDir + user_reference +"/FASTA/"
                refFastaName  = ""
                for fileX in os.listdir(refPath):
                    if fileX.endswith(".FASTA"):
                        print "ERROR, the input fasta file must have extention .fasta, not .FASTA, please rename this file."
                        raw_input("Press enter to exit")
                        exit()
                    if fileX.endswith(".fasta"):
                        refFastaName = fileX
                        break
                if refFastaName == "":
                    print "error no reference fasta file could be found in ",refPath
                    ans = "?"
                    continue
                
                    
                vcf_dir = detectedMainOutput+"/Results/FILTERED_VARIANTS/VCF/"
                outputDir = detectedMainOutput+"/Results/FILTERED_VARIANTS/CONSENSUS_SEQ/"
                try:
                    os.mkdir(outputDir)
                except:
                    print "Could not create folder", outputDir, "might already exist."
                print "creating consensus sequence for each file..."
                
                create_consensus(globalDir,vcf_dir,outputDir,tools,refPath+refFastaName)
                ans = "?" #reset user selection                

            ############################################################################################################################################
            if ans == "9":
            ############################################################################################################################################
                #not implemented
                raw_input('''this should automatically run from annotation onwards on the new files since aa changes could be affected
                    should create new subfolder under anno and filtered
                    same names but add the freq range to each file''')
            ############################################################################################################################################
            if ans == "10":
            ############################################################################################################################################
                raw_input("here update the summary file") # S1 : data, S1_A : data, S1_B : data
                print "10: Reannotate decomposed variants and attempt matching to known mol markers"
            ############################################################################################################################################
            #End custom tools, hope they helped you.
            #########################################################################################################################################################

'''
%%%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%     %%%%%%%%%%
when running params.allow_dececonvolution_of_hetero_variants:
    need to make sure samples with clearly different hetero freq (ranges) are not grouped into one codon
    codons that are merged must be in same hetero freq ratio +- epsilon
%%%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%%     %%%%%%%%%%%%%%%     %%%%%%%%%%
'''

print "Coming soon: GUI version, additional mapper and variant caller support"
print "FreeBayes / SNVER / GNUMAP / Baysic variant callers"
print "Thank you for using USAP!"
if shutDownWhenDone:
    os.system("shutdown now -h")

