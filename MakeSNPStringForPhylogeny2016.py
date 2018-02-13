'''
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
along with USAP. If not, see <http://www.gnu.org/licenses/>.
'''


import os
import time
#import string
'''
snp bases phylogeny:
use whole genome SNPS, use WT not mutated, but use special char for deletion if there is no coverage
If the read is present and WT- assign WT
If the read is absent - assign deletion "-"
The coverage MUST be above thereshold value
This tool takes as input the VCF file and the zero-coverage file from USAP
'''
def load_deletion_data(dirX,vcf_name):
    #loads all deleted positions into a dictionary
    deletedBPS = set()
    '''Assumtion: sorted lists'''
    fileX = vcf_name.replace(".vcf",".txt")
    os.chdir(dirX)
    try:
        f = open(fileX,'r')
    except:
        f = open(fileX.replace("FILTERED","trim_novo_realigned_resorted_dedup_genomecov=0_collapsed"))
        
    for line in f:
        del_range = line.split()
##        print del_range
##        raw_input()
        if len(del_range) == 1:
            deletedBPS.add(int(del_range[0]))
        elif len(del_range) == 2:
            for x in range(int(del_range[0]),int(del_range[1])+1):
                deletedBPS.add(x)
    f.close()
    return deletedBPS

def isThisBPDeleted_mem(vcf_name,snpPos,deletionDict):
    return snpPos in deletionDict
       
def isThisBPDeleted(dirX,vcf_name,snpPos):
    '''Assumtion: sorted lists'''
    #if "_" in vcf_name:
    #    fileX=vcf_name.split("_")[0]+"_genomecov=0_collapsed.txt"
    #else:
    #    fileX=vcf_name.split(".")[0]+"_genomecov=0_collapsed.txt"
    fileX = vcf_name.replance(".vcf",".txt")
    os.chdir(dirX)
    #print dirX
    #raw_input()
    f = open(fileX,'r')
    iterations = 0
    for line in f:
        iterations += 1
        del_range = line.split()
##        print del_range
##        raw_input()
        if len(del_range) == 1:
            if snpPos == int(del_range[0]):
##                print "iterations:",iterations
                return True
            if snpPos < int(del_range[0]):
##                print "iterations:",iterations
                return False
        elif len(del_range) == 2:
            if snpPos >= int(del_range[0]) and snpPos <= int(del_range[1]):
##                print "iterations:",iterations
                return True
            if snpPos < int(del_range[1]):
##                print "iterations:",iterations
                return False
    return False
    f.close()

def getMapper_cols(header):
        bwa = 0
        novo = 0
        smalt = 0
        pos = -1
        for element in header.split("\t"):
            pos += 1
            if element == "mut_BWA_GATK":
                bwa = pos
            if element == "mut_NOVO_GATK":
                novo = pos
            if element == "mut_NOVO_SMALT":
                smalt = pos
            if element == "ref_NOVO_GATK":
                ref = pos
        return bwa, novo, smalt, ref     
        
                
def loadAllRefereceSNPS(main):    
    '''
    this creates a dictionary of all the bp position snp info...
    '''
    genome = {} # {100:"A",200:"G"}
    totalLoaded = 0
    totalSNPS = 0
    #fileArray = []
    os.chdir(main)
    print main        
    for fileX in os.listdir(main):
        if fileX.endswith(".vcf"):
            totalLoaded +=1
            #print "reading file: ",fileX
            inFile = open(fileX, 'r')
            header = inFile.readline()
            bwaPos,novoPos,smaltPos, refPos = getMapper_cols(header)
            #bwaPos -= 1
            #novoPos -= 1
            #smaltPos -= 1
            tempSNPNUM  = 0
            for line in inFile:
                temp = line.split('\t')
                #print temp[0], temp[0] in genome
                #raw_input()
                #print bwaPos,novoPos,smaltPos,"    -->     ",temp[novoPos], temp[novoPos-1]
                #raw_input()
                #print [temp[0]], temp[0] in genome
                #raw_input("ok?")
                if temp[0] not in genome: #this bp pos is already in genome
                    if novoPos <> -1:
                        tempSNPNUM += 1
                        #print temp[novoPos], temp[novoPos-1]
                        if len(temp[novoPos]) == 1 and len(temp[novoPos-1]) == 1:
                            genome[temp[0]] = temp[novoPos-1]
                    elif bwaPos <> -1:
                        if len(temp[bwaPos]) == 1 and len(temp[bwaPos-1]) == 1:
                            genome[temp[0]] = temp[bwaPos-1]
                    elif smaltPos <> -1:
                        if len(temp[smaltPos]) == 1 and len(temp[smaltPos-1]) == 1:
                            genome[temp[0]] = temp[smaltPos-1]
                #print genome
                #raw_input()
            print fileX,"--> ",len(genome),"total snps", tempSNPNUM, "new snps"
            inFile.close()
            totalSNPS += len(genome)
            
    print "A total of ",totalLoaded,"files were loaded which contains a total of",totalSNPS,"SNPS, unique snps:", len(genome)
    #raw_input("press enter to continue")
    return genome

def convertDictToSortedList (dictX): 
    listX = []
    for x in dictX:
        listX.append([x,dictX[x]])
    listX.sort() #sorts by first element
##    for x in listX:
##        print x
##        raw_input()
    return listX

def loadVariantsFromAnnotatedVCF(fileX,dirX):      
    #returns all the variants for one file only
    genome = {}
    totalLoaded = 0
    #fileArray = []
    os.chdir(dirX)
    if fileX.endswith(".vcf"):
        totalLoaded +=1
##        print "getting variants from: ",fileX
        inFile = open(fileX, 'r')
        header = inFile.readline()
        bwaPos,novoPos,smaltPos, refPos = getMapper_cols(header)
        for line in inFile:           
            temp = line.split("\t")
            #if temp[0] not in genome:
            if novoPos <> 0:
                if len(temp[novoPos]) == 1 and len(temp[novoPos-1]) == 1: #not an indel
                    genome[temp[0]] = temp[novoPos]
            elif bwaPos <> 0:
                if len(temp[bwaPos]) == 1 and len(temp[bwaPos-1]) == 1: #not an indel
                    genome[temp[0]] = temp[bwaPos]
            elif smaltPos <> 0:
                if len(temp[smaltPos]) == 1 and len(temp[smaltPos-1]) == 1: #not an indel
                    genome[temp[0]] = temp[smaltPos]
            else:
                continue
        inFile.close()
        print "A total of ",len(genome) ,"SNPS were loaded from :", fileX
    return genome


def overlayRefAndCurrentFileSNPs_with_genome_cov_lookup(vcf_name,dirX,refGenomeDict,currGenomeDict,delData): #takes 1 SORTED list and one dict
    # output the overlayed
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
        if snp[0] in currGenomeDict:
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
            if isThisBPDeleted_mem(vcf_name,int(snp[0]),delData):
##                print "IT DOES NOT HAVE COVERAGE"
##                print snp
##                raw_input()
                resultList.append([snp[0],"-"])
                deletionList.append([snp[0],vcf_name])
            else:
                resultList.append([snp[0],snp[1]])
    resultList = sorted(resultList, key = lambda i : int(i[0]))
    
    #test if it is sorted
    previousPos = -1


    f= open("del_list2.txt",'a')
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
            print "multiple base pair found, this should not happen"
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
            print "multiple base pair found, this should not happen"
            print x[1]
            raw_input()
        previousPos = x[0]

    finalSeq = ''
    for x in resultList:
        finalSeq += x[1]    
    return finalSeq


def phyloAll(dirX,output):  
    start = time.time()      
    #allSNPData = []
    totalLoaded = 0
    #totalSNPS = 0
    #fileArray = []
    #snpFileData = ""
    #First make a list of all snps storing snp pos and reference bp
    allRefSNPs = loadAllRefereceSNPS(dirX) #all snps - for use as a reference SNP data  - dictionary of all snps which exist -
    
    
    refGenomeList = convertDictToSortedList(allRefSNPs) #convert dict to sorted LIST
    #print type(refGenomeList)
    #print len(refGenomeList)
    #print "total snps according to len of refgenomelist = ",len(refGenomeList)
    #print "ok"

    os.chdir(output) 
    snpFile = open('allSNPForPhylo_usap.FASTA', 'w')  #This clears the file
    snpFile.close()                              #This clears the file
    fileCount = 0
    for fileX in os.listdir(dirX):
        if fileX.endswith(".vcf"):
            fileCount += 1
    
    for fileX in os.listdir(dirX):

        if not fileX.endswith(".vcf"):
            #print "skipping file:",fileX
            continue
        #print "Reading file: ",fileX
        totalLoaded += 1
        print "progress:",str(totalLoaded)," / ",str(fileCount),"--> ",str(int(round((float(totalLoaded)/fileCount),2)*100)),"% complete..."
        currGenome = loadVariantsFromAnnotatedVCF(fileX,dirX) # a dictionary
        del_data = load_deletion_data(dirX,fileX)
            
        # resultSeq = overlayRefAndCurrentFileSNPs(refGenomeList,currGenome)# <---------------PREVIOUS VERSION-------------------------------------------------
        '''Note the previous version did not take into account if the curr genome file actually has read data for the WT snps forced to be present in its snp string'''
            
        resultSeq = overlayRefAndCurrentFileSNPs_with_genome_cov_lookup(fileX,dirX,refGenomeList,currGenome,del_data)
##            print "testing overlayed list"
##            print len(overlayedList)
##            raw_input()
        os.chdir(output) 
        snpFile = open('allSNPForPhylo_usap.FASTA', 'a+')
        snpFile.write(">"+str(fileX)+"\n")
        snpFile.write(resultSeq+"\n")
    print totalLoaded
    print "Multi-FASTA file created consisting of a SNP string of length", len(allRefSNPs)
    if time.time() - start < 1.0:
        print "total runtime:", (time.time() - start),"seconds."
    else:
        print "total runtime:", ((time.time() - start) / 60.0),"min."
    snpFile.close()



#############################################################################################################
#############################################################################################################
filesForPhylo = "/home/adippenaar/Dominic_vcfs" 
outputDir = filesForPhylo
#outputDir = "/home/adippenaar/Dominic_phylo"
phyloAll(filesForPhylo, outputDir)
#############################################################################################################
#############################################################################################################








