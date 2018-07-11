import pickle
import pandas as pd
import numpy as np
import itertools
import Function_distance_PSSM as fun
import sys
#load dictionary of matrix
with open('rfam_PPM_dic_qbear_50.pickle', 'rb') as afile:
        PPM_dic=pickle.load(afile)
        
with open('rfam_PSSM_dic_qbear_50.pickle', 'rb') as afile:
        PSSM_dic=pickle.load(afile)
        
#fam=list(PSSM_dic.keys())
#coppie=list(itertools.combinations(fam,2))

c_min=int(sys.argv[1])
c_max=int(sys.argv[2])
#l_alph=PSSM_q.shape[0]
c=open('coppie.txt').readlines()[c_min:c_max]
coppie=[(x.split()[0], x.split()[1]) for x in c]

d_KLD_family={}
for coppia in coppie:
    print(coppia)
    d_KLD_family[coppia]=[]
    
    
    PSSM_q=pd.DataFrame(PSSM_dic[coppia[0]])
    PPM_q=pd.DataFrame(PPM_dic[coppia[0]])
    
    PSSM_t=pd.DataFrame(PSSM_dic[coppia[1]])
    PPM_t=pd.DataFrame(PPM_dic[coppia[1]])

    l_finestra=min(len(PSSM_q.columns.values),len(PSSM_t.columns.values))
    diff=len(PSSM_q.columns.values)-len(PSSM_t.columns.values)
    #print(diff)
    
    kld_fin=fun.KLD_fin(l_finestra, diff, PPM_q, PPM_t, PSSM_q, PSSM_t, PSSM_q.shape[0])
    
    d_KLD_family[coppia]=kld_fin
    #print('FINE_coppia'+coppia)
    
    
with open('r_KLD/KLD_family_dic_'+str(c_min)+'_'+str(c_max)+'.pickle', 'wb') as handle:
    pickle.dump(d_KLD_family, handle)
    
