from pydriller import RepositoryMining, GitRepository
import datetime
from splClassifier import SPLClassifier
from features import getFeaturesList, getLinuxFeatures
from commits import getCommits
import os
from dotenv import load_dotenv

'''
Optional parameters to use in RepositoryMining class: 
dt1 and dt2 = only commits after dt1 and up dt2 will be analyzed, 
commitList = only these commits will be analyzed,
singleCommit = only this commit will be analyzed,
linuxFeatures = to get easier the extraction of the Linux features
'''
dt1 = datetime.datetime(2017, 3, 8, 0, 0, 0)
dt2 = datetime.datetime(2017, 12, 31, 0, 0, 0)
#commitsList = getCommits()
#singleCommit = str(os.getenv("SINGLE_COMMIT"))
#linuxFeatures = getLinuxFeatures()

load_dotenv()
pathRepository = str(os.getenv("REPOSITORY_PATH"))
print(pathRepository)
features = getFeaturesList(pathRepository)
outputPathName = str(os.getenv("OUTPUT_FILE"))
outputFile = open(outputPathName,'w')

commitResultsList = []
commitResultsList.append('Hash,date,KC-Tags,MF-Tags,AM-Tags\n')


GR = GitRepository(pathRepository)

#for commit in RepositoryMining(pathRepository, only_commits=commitsList).traverse_commits():
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
    mountStr = '{},{},{},{},{}\n'.format(commit.hash, commit.committer_date.date, kconfig_commit_tags, makefile_commit_tags, am_commit_tags)
    commitResultsList.append(mountStr)

outputFile.writelines(commitResultsList)
