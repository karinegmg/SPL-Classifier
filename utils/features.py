from pydriller import RepositoryMining
from utils.utils import CURRENT_PATH

featuresPath = f"{CURRENT_PATH}/config_files/features.csv"

def getFeaturesList(repositoryPath):
    featuresList = open(featuresPath, 'a')
    features = []
    featureName = ''
    for commit in RepositoryMining(repositoryPath).traverse_commits():
    
        for modification in commit.modifications:
            
            if('Kconfig' in modification.filename):
                listDiff = modification.diff.split('\n')

                for line in listDiff:
                    if('+config ' in line or '+ config' in line):
                        featureName = line[8:]
                    if(featureName not in features):
                        featuresList.write('{}\n'.format(featureName))
                        features.append(featureName)
    featuresList.close()
    return features

def getLinuxFeatures():
    featPath = f"{CURRENT_PATH}/config_files/featuresLinux.csv"
    features = []
    featLinux = open(featPath, 'r')

    for f in featLinux:
        featureName = '{}{}'.format('CONFIG_',f.strip())
        features.append(featureName)
    
    return features
