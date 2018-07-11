import numpy as np
import pandas as pd

alphastring = ""
bearstring = ""

alphamap = {}

Lalpha = len(alphastring)
Lbear = len(bearstring)

alphasub = pd.read_table(alphasubpath)
alphabearsub = np.zeros((Lbear,Lbear))

for ix, bearchar_i in enumerate(bearstring):
	for jx, bearchar_j in enumerate(bearstring):
		alphaix = alphastring.index(alphamap[bearchar_i])
		alphajx = alphastring.index(alphamap[bearchar_j])

		alphascore = alphasub.iloc[alphaix, alphajx]
		alphabearsub[ix,jx] = alphascore

###TODO save or print the matrix in beagle way
print(alphabearsub)
