import sys
from pydriller import RepositoryMining, GitRepository
import datetime
from splclassifier import SPLClassifier
#from manualcommits import getManualResultsKconfig, getMakeFileResultsManual, getAMFileResultsManual
from features import getLinuxF, getFeatures
from getCommitsLinux import getLinuxCommits
from getCommits import getListCommits
import re

dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)



#listaCommitsLinux = getLinuxCommits()
#features = getFeatures()
features = getLinuxF()
arq = open('automatic_classification_output/rc_linux_classification_with_date_unique.csv','w')
listaCommits = getListCommits()

'''
fileKind = sys.argv[1]
if(fileKind == 'makefile'):
    print("SOU MAKEFILE")
    listaCommits = getListCommits()
    features = getFeatures()
    arq = open('automated-rc-soletta-retest.csv','w')
        
elif(fileKind == 'kconfig'):
    print("SOU KCONFIG")
    arq = open('automated-results-kconfig-uclibc.csv','w')
else:
    print("SOU AM")
    arq = open('automated-results-am-linux.csv','w')
'''

#listaCommitResults = ['Hash,author,KC-Tags,MF-Tags,AM-Tags']

listaCommitResults = ['Hash,date,KC-Tags,MF-Tags,AM-Tags']

pathSoletta = '../../spl_repositorios/soletta'
pathLinux = '../../spl_repositorios/linux'
pathAxtls = '../../spl_repositorios/axtls'
pathUclibc = '../../spl_repositorios/uClibc'
githubLinux = 'https://github.com/torvalds/linux.git'

GR = GitRepository(pathSoletta)

singleCommit = 'd86b9f94c6599ef2e8e9c855f3dfb4cfcfddc019'


#for commit in RepositoryMining(pathSoletta,only_commits=listaCommits).traverse_commits():
for commit in RepositoryMining(pathLinux, only_commits=listaCommits).traverse_commits():
    
    kconfig_commit_tags = []
    makefile_commit_tags = []
    am_commit_tags = []
    commitResults = []
    # if(commit.hash in listaC):
    #     print('funfouuuu')

    for modification in commit.modifications:
        #print('entrou nas modss')

        files_changing_tags = []
        if(('kconfig' in modification.filename.lower() or 'makefile' in modification.filename.lower()) and modification.change_type.value == 5):
            #print('sou kconfig and mod type = {}'.format(modification.change_type))
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            added = parsed_lines['added']
            removed = parsed_lines['deleted']
            file_source_code = modification.source_code.split('\n')
            classifier = SPLClassifier(added, removed, file_source_code)
            files_changing_tags = classifier.classify(modification.filename.lower(),features)
        # elif((re.match(r'\S*\.c', modification.filename.lower()) != None) or re.match(r'\S*\.h', modification.filename.lower()) != None):
        else:            
            if(modification.change_type.value != 1 and modification.change_type.value != 4):
                
                diff = modification.diff
                parsed_lines = GR.parse_diff(diff)
                added = parsed_lines['added']
                removed = parsed_lines['deleted']
                file_source_code = modification.source_code.split('\n')
                classifier = SPLClassifier(added, removed, file_source_code)
                files_changing_tags = classifier.classify(modification.filename.lower(),features)
                files_changing_tags.append('changeAsset')
            
            if(modification.change_type.value == 1):
                if(('kconfig' in modification.filename.lower() or 'makefile' in modification.filename.lower())):
                    diff = modification.diff
                    parsed_lines = GR.parse_diff(diff)
                    added = parsed_lines['added']
                    removed = parsed_lines['deleted']
                    file_source_code = modification.source_code.split('\n')
                    classifier = SPLClassifier(added, removed, file_source_code)
                    files_changing_tags = classifier.classify(modification.filename.lower(),features)
                
                else:
                    #print('NOME DO ARQ ADD ASSET = {}'.format(modification.filename))
                    files_changing_tags.append('addAsset')
            if(modification.change_type.value == 4 and ('kconfig' not in modification.filename.lower() and 'makefile' not in modification.filename.lower())):
                files_changing_tags.append('removeAsset')

        for file_tag in files_changing_tags:
            if('kconfig' in modification.filename.lower() and (file_tag not in kconfig_commit_tags)):
                kconfig_commit_tags.append(file_tag)
            elif('makefile' in modification.filename.lower() and (file_tag not in makefile_commit_tags)):
                makefile_commit_tags.append(file_tag)
            elif('kconfig' not in modification.filename.lower() and 'makefile' not in modification.filename.lower() and file_tag not in am_commit_tags and 'build' not in file_tag):
                #print('FILE TAGG:', file_tag)
                am_commit_tags.append(file_tag)
    if(len(kconfig_commit_tags) > 0):
        print(kconfig_commit_tags)
        kconfig_commit_tags = str(kconfig_commit_tags).replace(',',' |')
        
    else:
        kconfig_commit_tags = 'no-fm-tag-changed'
    if(len(makefile_commit_tags) > 0):
        makefile_commit_tags = str(makefile_commit_tags).replace(',',' |')
    else:
        makefile_commit_tags = 'no-ck-tag-changed'
    if(len(am_commit_tags) > 0):
        am_commit_tags = str(am_commit_tags).replace(',',' |')
    else:
        am_commit_tags = 'no-am-tag-changed'
    mountStr = '{},{},{},{},{}\n'.format(commit.hash, commit.committer_date.date, kconfig_commit_tags, makefile_commit_tags, am_commit_tags)
    listaCommitResults.append(mountStr)

#arqOut = open('output-linux.csv','w')
arq.writelines(listaCommitResults)
    



