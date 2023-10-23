from pyexcel_ods import get_data

#hashLinux = open('rc_fh.csv', 'r')
#hashLinux = open('rc_linux.csv', 'r')


def getLinuxCommits():
    hashLinux = open('rc_linux.csv', 'r')
    linuxCommits = []
    for c in hashLinux:
        linuxCommits.append(c.strip())
        #print(c)
    return linuxCommits
