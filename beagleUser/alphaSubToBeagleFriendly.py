import argparse
import pickle
import sys

import numpy as np
import pandas as pd


parser = argparse.ArgumentParser()

##parser definition
parser.add_argument("-m", "--matrix", help="the substitution matrix path, in a tsv",)
parser.add_argument("-a", "--alphamap", help="the mapping path, in a txt file",)
parser.add_argument("-e", "--ext", help="the out file extension",)

parser.add_argument("-v", "--verbose", help="toggle verbosity", action="store_true")

args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_usage(sys.stderr)
    sys.exit(1)
args=parser.parse_args()

if (not args.matrix) or (not args.alphamap):
	raise OSError('\n-m (subs matrix df pickle) and -a (alphabet mapping in dict pickle) are required!\n')

if (not args.ext):
	EXT = "noname"
else:
	EXT = args.ext
#variable reading
alphasub = pd.read_table(args.matrix, index_col=0)

alphastring = "".join(list(alphasub.index))
bearstring = "abcdefghi=lmnopqrstuvwxyz^!\"#$%&\'()+234567890>[]:ABCDEFGHIJKLMNOPQRSTUVW{YZ~?_|/\\}@"


f = open(args.alphamap)

alphamap = {}
for line in f:
	if line:
		mapped = line.split()[1].strip()
		for ch in line.split()[0].strip():
			alphamap[ch] = mapped

print(alphamap)

Lalpha = len(alphastring)
Lbear = len(bearstring)

alphabearsub = np.zeros((Lbear,Lbear))

#filling
for ix, bearchar_i in enumerate(bearstring):
	for jx, bearchar_j in enumerate(bearstring):
		alphaix = alphastring.index(alphamap[bearchar_i])
		alphajx = alphastring.index(alphamap[bearchar_j])

		alphascore = alphasub.iloc[alphaix, alphajx]
		alphabearsub[ix,jx] = alphascore

###saving the matrix in beagle way
print(alphabearsub)
with open(f'friendlyMats/convertedMatrix_{EXT}','w') as f:
	for i, row in enumerate(alphabearsub):
		if args.verbose:
			print(f'filling row {i}')
		r = "\t".join([str(value) for value in row])
		f.write(r+"\n")
