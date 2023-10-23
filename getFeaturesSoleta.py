from pydriller import RepositoryMining, GitRepository

pathSoletta = '../../spl_repositorios/soletta'

for commit in RepositoryMining(pathSoletta).traverse_commits():
    
    featuresSoletta = open('featuresSolettaTeste.csv', 'a')

    for modification in commit.modifications:
        featuresSol = []
        if('Kconfig' in modification.filename):
            listDiff = modification.diff.split('\n')
            #print(type(listDiff))
            #print(listDiff[1])

            for line in listDiff:

                if('+config ' in line or '+ config' in line):
                    print(line)
                    feature = line[8:]
                    
                    if(feature in featuresSol):
                        featuresSoletta.write('{}\n'.format(feature))
                    else:
                        print(feature)
                        featuresSol.append(feature)
    featuresSoletta.close()
            

