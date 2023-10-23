from pyexcel_ods import get_data
import datetime
import json

def getManualResults():
    data = get_data("results-manual.ods")
    allHashs = []
    for i in range(1,len(data['FM'])-1):
        if(len(data['FM'][i]) > 0):
            allHashs.append(data['FM'][i][0])
    return allHashs

def getMakeFileResultsManual():
    arq = open('mf-manual.csv', 'r')
    commits = []
    for line in arq:
        commits.append(line.split(',')[0])
    return commits