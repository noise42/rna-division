import pickle
import pandas as pd

rigdatapaths = ["bear_50_RIGs.tsv",]
""""bear_90_RIGs.tsv",
"qbear_50_RIGs.tsv",
"qbear_90_RIGs.tsv",
"zbear_50_RIGs.tsv",
"zbear_90_RIGs.tsv"]"""

sscons = pickle.load(open('../sscons.pkl', 'rb'))

print(sscons)

for rigpath in rigdatapaths:
	df = pd.read_csv(rigpath, index_col=0)
	print(df)

##leggere tsv in dict

##verificare lunghezze

##lanciare varna con le due stringhe

###domanda... anche la sequenza nell img? in caso bisogna mettere anche GC RF nel pkl