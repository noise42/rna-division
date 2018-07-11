import pickle
import pandas as pd
import numpy as np
import itertools
import Function_distance_PSSM as fun
import sys
#load dictionary of matrix
with open('rfam_PFM_dic_qbear_50.pickle', 'rb') as afile:
        PFM_dic=pickle.load(afile)
        
with open('rfam_PSSM_dic_qbear_50.pickle', 'rb') as afile:
        PSSM_dic=pickle.load(afile)
        
#fam=list(PSSM_dic.keys())
#coppie=list(itertools.combinations(fam,2))

c_min=int(sys.argv[1])
c_max=int(sys.argv[2])
#l_alph=PSSM_q.shape[0]
c=open('coppie.txt').readlines()[c_min:c_max]
coppie=[(x.split()[0], x.split()[1]) for x in c]

d_ALLR_family={}

for coppia in coppie:
    print(coppia)
    d_ALLR_family[coppia]=[]
    
    
    PSSM_q=pd.DataFrame(PSSM_dic[coppia[0]])
    PFM_q=pd.DataFrame(PFM_dic[coppia[0]])
    
    PSSM_t=pd.DataFrame(PSSM_dic[coppia[1]])
    PFM_t=pd.DataFrame(PFM_dic[coppia[1]])

    l_finestra=min(len(PSSM_q.columns.values),len(PSSM_t.columns.values))
    diff=len(PSSM_q.columns.values)-len(PSSM_t.columns.values)
    #print(diff)
    
    allr_fin=fun.ALLR_fin(l_finestra, diff, PFM_q, PFM_t, PSSM_q, PSSM_t, PSSM_q.shape[0])
    
    d_ALLR_family[coppia]=allr_fin
    #print('FINE_coppia'+coppia)
    
    
with open('r_ALLR/ALLR_family_dic_'+str(c_min)+'_'+str(c_max)+'.pickle', 'wb') as handle:
    pickle.dump(d_ALLR_family, handle) 