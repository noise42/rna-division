import pickle
import pandas as pd
import numpy as np
import itertools

def make_kdl(l_alph,PPM_q, PPM_t, PSSM_t, PSSM_q, x, y):
    tot_x=0
    tot_y=0
    #per ogni carattere della colonna calcolo il kdl
    for ch in range(0, l_alph):
        tot_x+=(PPM_q.iloc[ch, x]*(PSSM_q.iloc[ch,x]-PSSM_t.iloc[ch,y]))
        tot_y+=(PPM_t.iloc[ch, y]*(PSSM_t.iloc[ch,y]-PSSM_q.iloc[ch,x]))
    kld_coppia_col=(0.5*(tot_x+tot_y))
    return kld_coppia_col

def KLD_fin(l_finestra, diff, PPM_q, PPM_t, PSSM_q, PSSM_t, l_alph):
    kld_finestre=[]
    if diff<0: #se la PSSM query e piu piccola della target, scorro sulla target.
        print('diff<0')
        for shift in range(0, -diff):
            #la differenza corrisponde al numero di finestre
            #inizializzo la finestra a 0
            kld_finestra=0
            for x in range(0, l_finestra):
                #scorro lungo il dataframe piu corto, in questo caso la query
                #y=posizione di inizio del target che cambia ad ogni finestra
                y=x+shift
                kdl_coppia_col=make_kdl(l_alph,PPM_q, PPM_t, PSSM_t, PSSM_q, x, y)
                kld_finestra+=kdl_coppia_col
            #kdl_finestre contiene tutti i valori di kdl delle possibili finestre nella coppia
            kld_finestre.append(kld_finestra)
            
    elif diff>0: #se la PSSM query e piu grande della target, scorro sulla query.
        print('diff>0')
        for shift in range(0, diff):
            #la differenza corrisponde al numero di finestre
            #inizializzo la finestra a 0
            kld_finestra=0
            for y in range(0, l_finestra):
                #scorro lungo il dataframe piu corto, in questo caso il target
                #x=posizione di inizio della query che cambia ad ogni finestra
                x=y+shift
                kdl_coppia_col=make_kdl(l_alph,PPM_q, PPM_t, PSSM_t, PSSM_q, x, y)
                kld_finestra+=kdl_coppia_col
            #kdl_finestre contiene tutti i valori di kdl delle possibili finestre nella coppia
            kld_finestre.append(kld_finestra)
    else:
        print('diff==0') #la PSSM query e uguale alla target
        #qui ci sara solo una finestra
        kld_finestra=0
        #per ogni carattere della colonna calcolo il kdl
        for x in range(0, l_finestra):
            y=x
            kdl_coppia_col=make_kdl(l_alph,PPM_q, PPM_t, PSSM_t, PSSM_q, x, y)
            kld_finestra+=kdl_coppia_col
        #kdl_finestre contiene il valore di kdl della finestra nella coppia
        kld_finestre.append(kld_finestra)

    return kld_finestre


def make_allr(l_alph,PFM_q, PFM_t, PSSM_t, PSSM_q, x, y):
    tot_x=0
    tot_y=0
    den=0
    #per ogni carattere della colonna calcolo l'allr
    for ch in range(0, l_alph):
        tot_x+=(PFM_q.iloc[ch, x]*PSSM_t.iloc[ch, y])
        tot_y+=(PFM_t.iloc[ch, y]*PSSM_q.loc[ch,x])
        den+=PFM_q.iloc[ch, x]+PFM_t.iloc[ch, y]
        num=tot_x+tot_y
        #aggiungo al allr della finestra il valore di allr della coppia di colonne
    allr_coppia_col=(num/den)
    return allr_coppia_col
    
def ALLR_fin(l_finestra, diff, PFM_q, PFM_t, PSSM_q, PSSM_t,l_alph):
    allr_finestre=[]
    if diff<0: #se la PSSM query e piu piccola della target, scorro sulla target.
        print('diff<0')
        for shift in range(0, -diff):
            #la differenza corrisponde al numero di finestre
            #inizializzo la finestra a 0
            allr_finestra=0
            for x in range(0, l_finestra):
                #scorro lungo il dataframe piu corto, in questo caso la query
                #y=posizione di inizio del target che cambia ad ogni finestra
                y=x+shift
                allr_coppia_col=make_allr(l_alph,PFM_q, PFM_t, PSSM_t, PSSM_q, x, y)
                #aggiungo al allr della finestra il valore di allr della coppia di colonne
                allr_finestra+=allr_coppia_col
            #allr_finestre contiene i valori di allr della finestra nella coppia
            allr_finestre.append(allr_finestra)  
              
            
            
    elif diff>0: #se la PSSM query e piu grande della target, scorro sulla query.
        print('diff>0')
        for shift in range(0, diff):
            allr_finestra=0
            for y in range(0, l_finestra):
                x=y+shift
                allr_coppia_col=make_allr(l_alph,PFM_q, PFM_t, PSSM_t, PSSM_q, x, y)
                #aggiungo al allr della finestra il valore di allr della coppia di colonne
                allr_finestra+=allr_coppia_col
                
            allr_finestre.append(allr_finestra)
    else:
        print('diff==0')
        allr_finestra=0
        for x in range(0, l_finestra):
            y=x
            allr_coppia_col=make_allr(l_alph,PFM_q, PFM_t, PSSM_t, PSSM_q, x, y)
            #aggiungo al allr della finestra il valore di allr della coppia di colonne
            allr_finestra+=allr_coppia_col
        allr_finestre.append(allr_finestra)
    return allr_finestre
