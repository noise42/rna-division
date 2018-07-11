#!/usr/bin/env python3

from Bio import AlignIO
import urllib
import requests
import sys
import os
import errno
import gzip
import pathlib
import re


def eprint(*args, **kwargs):
	# http://stackoverflow.com/questions/5574702/
	print(*args, file=sys.stderr, **kwargs)


def download_seed(rfam_version, outdir, force=False):
	outfile = os.path.join(outdir,"Rfam.seed.gz")
	if os.path.isfile(outfile) and not force:
		print("Rfam.seed.gz already present.\nUse force option if you want to download it again!\n")
		return
	else:
		url = "ftp://ftp.ebi.ac.uk/pub/databases/Rfam/%s.0/Rfam.seed.gz" %(rfam_version)
		output = open(outfile, "wb")
		try:
			response = urllib.request.urlopen(url)
			output.write(response.read())
		except:
			output.close()
			raise
	
def get_families_acc(rfam_dir):
	acc = []
	seed = os.path.join(rfam_dir,"Rfam.seed.gz")
	with gzip.open(seed, "rt", encoding="ISO-8859-1") as fh:
		for line in fh:
			if line[0:7] == "#=GF AC":
				rf_acc = line.strip().split(None)[2]
				acc.append(rf_acc)
	return acc


def create_url(rfam_acc):

	url = "http://rfam.xfam.org/family/%s/alignment/stockholm" %(rfam_acc)

	return(url)

def retrieve_alignment(rfam_acc,out="ali_tmp"):
	output = open(out, "w")
	try:
		response = urllib.request.urlopen(create_url(rfam_acc))
		output.write(response.read().decode('utf-8'))
	except:
		output.close()
		eprint(rfam_acc + " does not exist")
		return

	return out

def create_constraint(rfam_acc, ali_stock, outdir):
	#p = re.compile('>+?(?=[\.x])') #need to remove the closing parenthesis from beginning of the string
	p = re.compile('.+?(?=<)')
	
	IUPAC=["R","Y","M","K","S","W","B","D","H","V","N"]
	CONSTRAINTS=[">","<","_"]

	ss_cons = ["."] * ali_stock.get_alignment_length()

	try:
		SS = ali_stock.column_annotations["secondary_structure"]
		RF = ali_stock.column_annotations["reference_annotation"]
	except:
		eprint("No constraints possible for %s!" %(rfam_acc))
		return False

	outfile = os.path.join(outdir,"constraints",rfam_acc+".constraints")
#	pathlib.Path(outfile).mkdir(parents=True, exist_ok=True) 
	out_fasta=open(outfile,"w")

	
	brackets = [idx for idx, ss in enumerate(SS) if ss in CONSTRAINTS[0:2] ]

	for idx in brackets:
		ss_cons[idx] = SS[idx]

	conserved = [idx for idx, rf in enumerate(RF) if rf.istitle() and 
							not rf in IUPAC]

	for idx in set(conserved) - set(brackets):
		ss_cons[idx] = "x"
	
	for record in ali_stock:
		out_fasta.write(">" + record.id + "\n")
		gaps = [idx for idx, nuc in enumerate(record.seq) if nuc == "-"]

		out_fasta.write(str(record.seq).replace("-","") + "\n")
		
		final = "".join([ss_con for idx, ss_con in enumerate(ss_cons) if not idx in gaps])
		m = p.match(final)
		
		if m:
			final = final[m.span()[0]:m.span()[1]].replace(">",".")  + final[m.span()[1]:]
		else:
			out_fasta.write( final + "\n")
		
	out_fasta.close()



	

#Input the Rfam version you want to use
rfam_version = sys.argv[1]
rfam_dir = "Rfam_"+str(rfam_version)

try:
    os.makedirs(rfam_dir)
    os.makedirs(rfam_dir+"/constraints")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

download_seed(rfam_version,rfam_dir)

acc = get_families_acc(rfam_dir)

seed = os.path.join(rfam_dir,"Rfam.seed.gz")

count = 0

with gzip.open(seed, "rt", encoding="ISO-8859-1") as handle:
	for record in AlignIO.parse(handle, "stockholm"):
		rfam_acc = acc[count]
		create_constraint(rfam_acc, record, rfam_dir)
		count += 1


#ali_fh = open(seed, encoding = "ISO-8859-1")	
#alis = AlignIO.parse(ali_fh, "stockholm")
#Old verion one file at the time
#acc = []
#for i in range(1,177):
#	rfam_acc = "RF" + str(i).zfill(5)
#	ali_fnp = retrieve_alignment(rfam_acc)
#	ali_fh = open(ali_fnp, encoding = "ISO-8859-1")
#	ali = AlignIO.read(ali_fh, "stockholm")
#	crea_constraint(rfam_acc, ali)	
