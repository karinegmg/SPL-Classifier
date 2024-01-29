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
    result = '{} commits ({:.2f} %) present the modification classified as the following tags: {}'.format(count, (count/qtd_remainingCommits)*100, queryList)
        
    return result

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