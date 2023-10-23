import random

randomList = []

while (len(randomList) < 30):
    num = random.randint(1, 765)
    if (num not in randomList):
        randomList.append(num)
    
fileName = 'changeAsset.csv'
automaticResultsFile = open(fileName, 'r')
listCommits = []

for commit in automaticResultsFile:
    listCommits.append(commit)


outputFile = 'random_commits-change-asset.csv'
randomCommits = open(outputFile, 'w')

randomCommits.write('Hash,author,KC-Tags,MF-Tags,AM-Tags\n')

for item in randomList:
    randomCommits.write(listCommits[item])

randomCommits.close()