import pickle
import json
import requests
import urllib.error
import urllib.request

def getRFAMalignment(accession):
    targets={}
    contents = urllib.request.urlopen('http://rfam.xfam.org/family/{}/alignment?content-type=text/html'.format(accession)).read()
    #print(contents)
    con = contents.decode('UTF-8', 'ignore').strip().split("\n")

    sscons = [c for c in con if c.startswith("#=GC SS_cons")][0]
    return sscons.split()[2]
    

def getAllRfamAlignments(RFUPPER = 3000):
    families = {}
    for i in range(RFUPPER): #RF upper limit for now

        try:
            accession = 'RF'+ str(i).zfill(5)
            print(f'testing {accession}')
            RFalign = getRFAMalignment(accession)
            families[accession] = RFalign

        except urllib.error.HTTPError as err:
            print('{} does not exist, passing'.format(accession))
            pass
    return families


def wussToDBN(wuss):
    """converts wuss to dotbracket for varna"""
    ###VARNA reads wuss, function not needed
    return wuss


#print(getRFAMalignment('RF00032'))
fams = getAllRfamAlignments()
pickle.dump(fams, open('../sscons.pkl', 'wb'))