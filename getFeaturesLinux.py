from pydriller import RepositoryMining, GitRepository

pathLinux = '../../spl_repositorios/linux'

for commit in RepositoryMining(pathLinux).traverse_commits():
    
    featuresLinux = open('featuresLinuxTeste.csv', 'a')

    for modification in commit.modifications:
        featuresLin = []
        if('Kconfig' in modification.filename):
            listDiff = modification.diff.split('\n')
            #print(type(listDiff))
            #print(listDiff[1])

            for line in listDiff:

                if('+config ' in line or '+ config' in line):
                    #print(line)
                    feature = line[8:]
                    
                    if(feature not in featuresLin):
                        featuresLinux.write('{}\n'.format(feature))
                        featuresLin.append(feature)
            
featuresLinux.close()
            

