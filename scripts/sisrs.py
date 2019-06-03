'''
Script Developed by Devin J. McConnell
Schwartz Lab May 2019
'''

from sisrs_01_folder_setup import *
from sisrs_02_read_trimmer import *
from sisrs_03_read_subsetter import *
from cmdCheck import *

'''
Function to run all of the first script
'''
def sisrs01(taxon_ID_file,data_path,sisrs_dir,trimed):
    taxa_list = []
    if taxon_ID_file != "":
        taxa_list = devTaxaList(taxon_ID_file)
    else:
        taxa_list = readTaxaFromFolders(data_path)

    fileStructure(sisrs_dir, taxa_list)

    if data_path != "" :
        if trimed:
            makeLinks(data_path, sisrs_dir, taxa_list, True)
        else:
            makeLinks(data_path, sisrs_dir, taxa_list, False)

'''
Function to run all of the second script
'''
def sisrs2(trimed,processors,sisrs_dir):
    if not trimed:
        bbduk_adapter = findAdapter()
        out = setup(sisrs_dir)

        # raw_fastqc_command
        fastqcCommand(processors,out[3],out[0])

        trim(out[5],out[1],bbduk_adapter,out[2])

        # trim_fastqc_command
        fastqcCommand(processors,out[4],out[1])
    else:
        print("FILES ALREADY TRIMMED")

'''
Function to run all of the thrid script
'''
def sisrs3(genomeSize, sisrs_dir):
    setupInfo = setupDir(sisrs_dir,genomeSize)

    df, compiled_paired, compiled_single_end = countBasePair(setupInfo[3],setupInfo[6], setupInfo[7],setupInfo[5])

    print("Based on a genome size estimate of " + str(genomeSize) + " bp, and with " + str(len(setupInfo[3])) + " species, the requested subset depth is " + str(setupInfo[4]) + " bp per species")

    out = checkCoverage(df,setupInfo[4],setupInfo[1],compiled_paired, compiled_single_end)

    # Subset Single End
    subset(compiled_single_end,out[2],setupInfo[0],setupInfo[1],setupInfo[2],False)

    #Subset paired ends
    subset(compiled_paired,out[2],setupInfo[0],setupInfo[1],setupInfo[2],True)

if __name__ == '__main__':
    cmdln = sys.argv
    rtn = commandLine(cmdln)
    #sisrs01(rtn[1],rtn[2],rtn[0],rtn[3])
    #sisrs2(rtn[3],rtn[4],rtn[0])
    sisrs3(rtn[5],rtn[0])