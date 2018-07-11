#!/usr/bin/env python3

import pickle
import json
import requests
import urllib.error
import urllib.request

def getRFAMalignment(accession):
    targets={}
    contents = urllib.request.urlopen('http://rfam.xfam.org/family/{}/alignment/fasta'.format(accession)).read()
    #print(contents)
    con = contents.decode('UTF-8').strip().split("\n")
    i=0
    while(i < len(con)):
        if con[i].startswith('>'):
            ID = con[i]
            i+=1
            seqchunk = ""
            while( i < len(con) and not con[i].startswith('>') ):
                seqchunk += con[i]
                i+=1
            targets[ID] = {'sequence': seqchunk}
        else : i+=1
    return targets ##single dict with ID keys and { 'sequence': seq } as value

def getAllRfamAlignments(RFUPPER = 3000):
    families = {}
    for i in range(RFUPPER): #RF upper limit for now
        try:
            accession = 'RF'+ str(i).zfill(5)
            RFalign = getRFAMalignment(accession)
            families[accession] = RFalign

        except urllib.error.HTTPError as err:
            print('{} does not exist, passing'.format(accession))
            pass
    return families

aligns = getAllRfamAlignments()