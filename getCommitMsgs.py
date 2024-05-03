from commits import getCommits
from pydriller import RepositoryMining
import os
from dotenv import load_dotenv

load_dotenv()
repositoryPath = "..\linux_repo\linux"
commitsList = getCommits()
outputFilename = 'prefix-commits-msg.csv'
output = open(outputFilename, 'w')

def getCommitMsgs():
    commitMsgs = []
    prefix = ""
    prefixList = []
    for commit in RepositoryMining(repositoryPath, only_commits=commitsList).traverse_commits():
        
        if(not commit.merge):
            prefix = commit.msg.split(":")
            uniqPrefix = prefix[0]
            commitMsgs.append("1,{},{}\n".format(commit.hash, uniqPrefix))
            prefixList.append(uniqPrefix)
            
    print("count, prefix")
    for unit in prefixList:
        print("{}, {}".format(prefixList.count(unit), unit))
           
    for msg in commitMsgs:
        output.write(msg)


getCommitMsgs()