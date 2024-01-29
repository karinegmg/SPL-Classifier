fileName = 'linux_data_get_dummies_teste.csv'
fileIn = open(fileName, 'r')
tagsDiff = []
dictCommits = {}
dictTagsAndAmount = {}
countPattern = 0 
dictHashCommit = {}

fileOutName = 'tags_patterns_with_hashes.csv'
fileOut = open(fileOutName, 'w')

countTagsAndAmount = '0'
countHashCommit = '0'


fileOut.write('qty, hash, tags\n')
for fi in fileIn:
    line = fi.strip().split(',')
    tags = line[2].split('|')
    hashCommit = line[0]
    sortedTags = str(sorted(tags))


    dictHashCommit[hashCommit[0:10]] = sortedTags

    if(not sortedTags in dictTagsAndAmount):
        dictCommits[(tags[0])[0:10]] = sortedTags
        dictTagsAndAmount[sortedTags] = '0'
    
    if(sortedTags in dictTagsAndAmount):
        countTag = dictTagsAndAmount[sortedTags]
        dictTagsAndAmount[sortedTags] = str(int(countTag) + 1)

for i in dictTagsAndAmount:
    fileOut.write('{},,Tags = {}\n'.format(dictTagsAndAmount[i], i.replace(',', "|")))
    for hashC in dictHashCommit:

        if(i in dictHashCommit[hashC]):
            fileOut.write(',{}\n'.format(hashC))
            print(dictHashCommit[hashC])

fileOut.close()
