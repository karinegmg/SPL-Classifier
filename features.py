from pydriller import RepositoryMining, GitRepository
import datetime
import re

def getLinuxF():
    featuresL = []
    featLinux = open('featuresLinuxTeste.csv', 'r')
    #testeString = ''

    for f in featLinux:
        #print(f.strip())
        testeString = '{}{}'.format('CONFIG_',f.strip())
        #print(testeString)
        featuresL.append(testeString)
    
    return featuresL

def getFeatures():
    featuresL = []
    fileName = 'features_soletta.csv'
    featuresFile = open(fileName, 'r')
    for f in featuresFile:
        #print(f.strip())
        featName = f.strip()
        #print(featName)
        featuresL.append(featName)
    return featuresL
