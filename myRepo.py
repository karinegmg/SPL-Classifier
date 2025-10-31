from pydriller import RepositoryMining, GitRepository
import datetime
from splclassifier import SPLClassifier
from utils.features import getFeaturesList, getLinuxFeatures
from utils.utils import *

'''
linuxFeatures = to get easier the extraction of the Linux features
'''

features = []
pathRepository = getVarFromEnv(REPOSITORY_PATH)
print(pathRepository)

if ("torvalds/linux.git" in pathRepository):
    linuxFeatures = getLinuxFeatures()
else:
    features = getFeaturesList(pathRepository)

outputPathName = getVarFromEnv(OUTPUT_FILE)
outputFile = open(outputPathName,'w')

commitResultsList = []
commitResultsList.append('Hash,author,date,KC-Tags,MF-Tags,AM-Tags\n')

GR = GitRepository(pathRepository)

for commit in RepositoryMining(pathRepository).traverse_commits():
    kconfig_commit_tags = []
    makefile_commit_tags = []
    am_commit_tags = []
    commitResults = []

    for modification in commit.modifications:

        files_changing_tags = []
        
        if(('kconfig' in modification.filename.lower() or 'makefile' in modification.filename.lower()) and modification.change_type.value == 5):
            diff = modification.diff
            parsed_lines = GR.parse_diff(diff)
            added = parsed_lines['added']
            removed = parsed_lines['deleted']
            file_source_code = modification.source_code.split('\n')
            classifier = SPLClassifier(added, removed, file_source_code)
            files_changing_tags = classifier.classify(modification.filename.lower(),features)
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
                    files_changing_tags.append('addAsset')
            if(modification.change_type.value == 4 and ('kconfig' not in modification.filename.lower() and 'makefile' not in modification.filename.lower())):
                files_changing_tags.append('removeAsset')

        for file_tag in files_changing_tags:
            if('kconfig' in modification.filename.lower() and (file_tag not in kconfig_commit_tags)):
                kconfig_commit_tags.append(file_tag)
            elif('makefile' in modification.filename.lower() and (file_tag not in makefile_commit_tags)):
                makefile_commit_tags.append(file_tag)
            elif('kconfig' not in modification.filename.lower() and 'makefile' not in modification.filename.lower() and file_tag not in am_commit_tags and 'build' not in file_tag):
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
    mountStr = '{},{},{},{},{},{}\n'.format(commit.hash, commit.author.name, commit.committer_date, kconfig_commit_tags, makefile_commit_tags, am_commit_tags)
    commitResultsList.append(mountStr)

outputFile.writelines(commitResultsList)
