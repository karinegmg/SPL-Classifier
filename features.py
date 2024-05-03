from pydriller import RepositoryMining


def getFeaturesList(repositoryPath):
    featuresList = open('features.csv', 'a')
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
    features = []
    featLinux = open('featuresLinux.csv', 'r')

    for f in featLinux:
        featureName = '{}{}'.format('CONFIG_',f.strip())
        features.append(featureName)
    
    return features
