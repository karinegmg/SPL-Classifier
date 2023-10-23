fileName = 'automatic_classification_output/rc_linux_classification.csv'
qtd_remainingCommits = 1896

def getPatterns(queryList):
    file_tags = open(fileName, 'r')
    count = 0
    dictTags = {}
    for commit in file_tags:
        lines = commit.split(',')
        hashCommit = lines[0][0:10]
        tags = lines[2] + lines[3] + lines[4]
        dictTags[hashCommit] = tags

    for key, v in dictTags.items():
        aux = 0
        for q in queryList:
            if(q in v):
                aux = aux + 1
            if(aux == len(queryList)):
                count = count + 1
                print(key)
                #print('match: ', v)
    result = '{} commits ({:.2f} %) apresentam as modificações classificadas com as tags {}'.format(count, (count/qtd_remainingCommits)*100, queryList)
        
    return result

def getPatternsForSpace(spaceName, queryTagsFm, queryTagsCk, queryTagsAm):
    file_tags = open(fileName, 'r')
    count = 0
    #dictTags = {}
    dictAm = {}
    dictFM = {}
    dictCK = {}
    for commit in file_tags:
        lines = commit.split(',')
        hashCommit = lines[0]
        tags = lines[2] + lines[3] + lines[4]
        dictAm[hashCommit] = lines[4]
        dictFM[hashCommit] = lines[2]
        dictCK[hashCommit] = lines[3]
        #dictTags[hashCommit] = tags
    
    if('AM' in spaceName):
        for key, v in dictAm.items():
            aux = 0
            for q in queryTagsAm:
                if(q in v):
                    aux = aux + 1
                if(aux == len(queryTagsAm)):
                    count = count + 1
                #print('match: ', v)
    result = '{} commits ({:.2f} %) apresentam as modificações classificadas com as tags {}'.format(count, (count/qtd_remainingCommits)*100, queryList)
  

'''
Change Type = Added, Modify, Remove, New
Tags FM = ('Added' | 'Feature'), ('Added' | 'Depends'), ('Added' | 'Default'), ('Added' | 'Select')
Tags CK = ('Modify' | 'Mapping'), ('Modify' | 'ifdef'), ('Modify' | 'build')]
Tags AM = 'changeAsset', 'addAsset', 'removeAsset'
No tags in each space = no-fm-tag-changed or no-ck-tag-changed or no-am-tag-changed
'''
# Query Example: How often commits present changes which add feature in Kconfig and a mapping in Makefile?
queryList = ["('Added' | 'Feature')", "('Modify' | 'Mapping')", "'addAsset'"]
query = getPatterns(queryList)

print(query)