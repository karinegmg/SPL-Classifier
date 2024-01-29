'''
exclusion criteria:
- merge commits
- commits with >20 modified files
'''

from pydriller import RepositoryMining, GitRepository
from commits import getCommits

dictListaC = {}
listaCommits = getCommits()
pathLinux = '../../spl_repositorios/linux'
fileInName = 'tags_patterns_with_hashes.csv'
fileOutName = 'tags_patterns_merge_large.csv'

fileOut = open(fileOutName, 'w')
hashes = open(fileInName, 'r')

for commit in RepositoryMining(pathLinux, only_commits=listaCommits).traverse_commits():
    if (commit.merge == True):
        dictListaC[(commit.hash)[0:10]] = "merge scenario"

    elif(len(commit.modifications) > 20):
        dictListaC[(commit.hash)[0:10]] = "> 20 modified files"
       
    else:
        dictListaC[(commit.hash)[0:10]] = "review"
       

for h in hashes:
    line = h.strip().split(',')
    qty = line[0]
    hashC = line[1].strip()

    
    if(len(line) > 2):    
        
        tags = line[2]
        fileOut.write('{},{},{}\n'.format(qty, hashC, tags))
        
    else:
        if("merge scenario" in dictListaC[hashC]):
            qty = "merge"
            fileOut.write('{},{}\n'.format(qty, hashC))
        elif(dictListaC[hashC] == "> 20 modified files"):
            qty = "> 20 files"
            fileOut.write('{},{}\n'.format(qty, hashC))
        else:
            qty = "review"
            fileOut.write('{},{}\n'.format(qty, hashC))



    