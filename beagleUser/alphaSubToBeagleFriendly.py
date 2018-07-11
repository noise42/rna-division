import argparse
import pickle

import numpy as np
import pandas as pd


parser = argparse.ArgumentParser()

##parser definition
parser.add_argument("-m", "--matrix", help="the substitution matrix path, in a pickled dataframe",)
parser.add_argument("-a", "--alphamap", help="the mapping path, in a pickled dict",)
parser.add_argument("-v", "--verbose", help="toggle verbosity", action="store_true")

args = parser.parse_args()
if (not args.matrix) or (not args.alphamap):
	raise OSError('\n-m (subs matrix df pickle) and -a (alphabet mapping in dict pickle) are required!\n')

#variable reading
alphasub = pickle.load(open(args.matrix, 'rb'))

alphastring = "".join(list(alphasub.index))
bearstring = "abcdefghi=lmnopqrstuvwxyz^!\"#$%&\'()+234567890>[]:ABCDEFGHIJKLMNOPQRSTUVW{YZ~?_|/\\}@"


alphamap = pickle.load(open(args.alphamap, 'rb'))


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
with open('convertedMatrix','w') as f:
	for i, row in enumerate(alphabearsub):
		if args.verbose:
			print(f'filling row {i}')
		for value in row:
			f.write(value)
