from collections import Counter
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import subprocess


def run_blustClust(cartella, identita, name, identity):
    #cartella contiene per ogni famiglia solo nome e sequenze
    #identita sara la soglia di identita espressa come x %
    
    os.mkdir('not_similar_'+name+'_'+identity+'/')
    os.chdir(cartella)
    os.system('for file in *; do blastclust -i $file -o ../not_similar_'+name+'_'+identity+'/$file -p F -S '+identita+' ; done')
    os.chdir('../')
    print 'Fine BlustClust'
    
    
def filtro_n_seq(cartella, n_seq_family, name, identity):  
    #cartella sara la not_similar creata da blustClust
    #n_seq_family sara i numero minimo di sequenze per famiglia
    
    os.mkdir('filtro_n_seq_'+name+'_'+identity+'/')
    lista_fam=os.listdir(cartella)
    
    #creo una nuova cartella dove copio solo famiglia con piu di 5 membri
    for fam in lista_fam:
        output=subprocess.check_output("wc -l "+cartella+fam, shell=True)
        if int(output.strip().split()[0])>=int(n_seq_family):
            os.system('cp '+cartella+'/'+fam+' filtro_n_seq_'+name+'_'+identity+'/'+fam)
                
    print 'Fine filtro 5 sequenze'
    
    
    
def get_bear(cartella, cartella_bear, name, identity):    
    #cartella sara la filtro_n_seq creata dalla funzione con lo stesso nome 
    #cartella bear sara la cartella con le sequenze nome-seq-dot-bear
    #prendo bear delle sequenze in filtro_n_seq
    os.mkdir('bear_filtered_'+name+'_'+identity+'/')
    
    lista_fam_filter=os.listdir(cartella)
    for fam_clean in lista_fam_filter:
        seq=[]
        f=open(cartella+fam_clean).readlines()
        for riga in f:
            seq.append(riga.split()[0])

        o=open('bear_filtered_'+name+'_'+identity+'/'+fam_clean, "w")
        f2=open(cartella_bear+fam_clean)
        line=f2.readline()
        while(line):
            if line[0]==">" and line[1:-1] in seq:
                o.write(line)
                line=f2.readline()
                o.write(line)
                line=f2.readline()
                o.write(line)
                line=f2.readline()
                o.write(line)
                line=f2.readline()
            else:
                line=f2.readline()
        o.close()
        
    print 'Fine Bear sequence research'
    

def distributeGaps(gappedReference, ungappedString):
    assert len(gappedReference.replace('-','')) == len(ungappedString), 'ungapped strings should be equal' 
    result = list(ungappedString)
    gaplist = [ m.start() for m in re.finditer('-', gappedReference)]

    for gap in gaplist:    
        result.insert(gap, '-')
    result = "".join(result)    
    return result

assert(distributeGaps('--abcdef-g-', 'bombasi') == '--bombas-i-')


def add_gap(cartella, seed_rfam, name, identity):

    #cartella=bear_filtered
    #seed_rfam
    
    #aggiungo gap alle sequenze bear sulla base degli allineamenti di RFAM
    lista_fam_filter2=os.listdir(cartella)
    os.mkdir('bear_alignment_'+name+'_'+identity+'/')
    c=0
    for famiglia in lista_fam_filter2:
        c+=1
        o=open('bear_alignment_'+name+'_'+identity+'/'+famiglia, "w")
        f=open(cartella+famiglia)
        line=f.readline()
        while(line):
            if line[0]==">":
                nome=line[1:-1]
                #output=subprocess.check_output("wc -l not_similar/"+fam, shell=True)
                seq_alignment=subprocess.check_output('grep '+nome+' '+seed_rfam, shell=True)
                line=f.readline()
                prova=distributeGaps(seq_alignment.split()[1], line[0:-1])

                line=f.readline()
                line=f.readline()
                bear_seq=line

                gap_pos=[]
                for i, el in enumerate(prova):
                    if el=='-':
                        gap_pos.append(i)

                for i in gap_pos:
                    bear_seq=bear_seq[:i] + "-" + bear_seq[i:]

                #print prova
                #print bear_seq
                o.write(bear_seq)
            else:
                line=f.readline()
        o.close()

        print famiglia+"\t"+str(c)+" famiglie su "+str(len(lista_fam_filter2))
        
        
    print 'Allineamenti con gap conclusi'
    print 'Sequenze Bear con gap in cartella bear_alignment/'
    




def decode(bear):
    
    alph_bear={'abc':'a', 'def':'A', 'ghi=':'=',
          'lmnop':'l', 'qrstu':'L', 'vwxyz^':'^',
          '!"#': 'i', '$%&':'I', '\'()+':'+',
          '234':'n', '567':'N', '890>':'>',
          'ABC':'s', 'DEF':'S', 'GHIJ':'~',
          'KLMN':'b', 'OPQR':'B', 'STUVW':'|',
          'YZ~':'y', '?_|':'Y', '/\\@':'@',
          '{}[]':'[', ':':':' , '-':'-'}
    
    result=""
    for ch in bear:
        for key in alph_bear:
            if ch in key:
                result += alph_bear[key]
    return result


#deconding2 from text
def decode_from_file(bear, file_name):
    f=open(file_name).readlines()
    alph_bear=[i.split() for i in f]
    alph_bear.append(['-','-'])
    result=""
    for ch in bear:
        for gruppo in alph_bear:
            if ch in gruppo[0]:
                #print ch, gruppo[0], gruppo[1]
                result += gruppo[1]
    return result



def convert_new_bear(cartella, name, identity):
    #cartella=bear_alignment
    
    #conversione del bear nel nuovo alfabeto
    famiglie_bear=os.listdir(cartella)
    os.mkdir('bear_new_alignment_'+name+'_'+identity+'/')
    
    
    for famiglia in famiglie_bear:
        o=open('bear_new_alignment_'+name+'_'+identity+'/'+famiglia, "w")
        f=open(cartella+famiglia)
        line=f.readline()
        while(line):
            o.write(decode(line)+"\n")
            line=f.readline()
        o.close()
    
    print 'Fine decodifica bear'
    
def convert_new_bear_file(cartella, file_name, name, identity):
    #cartella=bear_alignment
    
    #conversione del bear nel nuovo alfabeto
    famiglie_bear=os.listdir(cartella)
    os.mkdir('bear_new_alignment_'+name+'_'+identity+'/')
    
    
    for famiglia in famiglie_bear:
        o=open('bear_new_alignment_'+name+'_'+identity+'/'+famiglia, "w")
        f=open(cartella+famiglia)
        line=f.readline()
        while(line):
            o.write(decode_from_file(line, file_name)+"\n")
            line=f.readline()
        o.close()
    
    print 'Fine decodifica bear'
    


def crea_blocchi(cartella, name, identity):
    #cartella=bear_new_alignment

    os.mkdir('blocchi_new_bear_'+name+'_'+identity+'/')
    famiglie=os.listdir(cartella)
    for fam in famiglie:
        o=open('blocchi_new_bear_'+name+'_'+identity+'/'+fam, "w")
        f=open(cartella+fam).readlines()
        zipped=zip(*f)[:-1]
        v=[]
        for colonna in zipped:
            if '-' not in colonna:
                c=Counter(colonna)
                for chiave in c:
                    if float(c[chiave])/float(len(colonna))>0.5:
                        v.append(colonna)
        new=zip(*v)
        for seq in new:
            o.write(''.join(seq)+"\n")
            
            
            
def frequenze_attese(cartella,alph_bear):
    #cartella=blocchi_new_bear
    
    lista=os.listdir(cartella)
    for famiglia in lista:
        f=open(cartella+famiglia)

        line=f.readline()
        while(line):
            c=Counter(line.strip())
            #print c
            for chiave in c:
                alph_bear[chiave].append(c[chiave])
            #print alph_bear
            line=f.readline()
    
    for chiave in alph_bear:
        alph_bear[chiave]=sum(alph_bear[chiave])
    
    
    #nuovo dizionario con le frequenze dei caratteri singoli
    c=0
    for chiave in alph_bear:
        c+=alph_bear[chiave]
    for chiave in alph_bear:
        alph_bear[chiave]=float(alph_bear[chiave])/float(c)
        
        
    v_bear=['a','A','=','l','L','^','i','I','+','n','N','>','s','S','~','b','B','|','y','Y','@','[', ':']

    fr_attese=pd.DataFrame(columns=v_bear, index=v_bear)
    
    for index, row in fr_attese.iterrows():
        for colonna in v_bear:
            if index==colonna:
                fr_attese.ix[index, colonna] = alph_bear[index]*2
            else:
                fr_attese.ix[index, colonna] = 2*alph_bear[index]*alph_bear[colonna]
                
    fr_attese.to_csv('frequenze_attese.tsv',sep="\t")
    return fr_attese
    
    print 'Fine frequenze attese'
    

def sostituzioni_osservate(cartella, v_bear, name, identity):
    #corrisponde ad f_ij
    
    #cartella=blocchi_new_bear
    #v_bear= vettore con caratteri bear
    #esempio=['a','A','=','l','L','^','i','I','+','n','N','>','s','S','~','b','B','|','y','Y','@','[', ':']

    #sostituzioni osservate
    sostituzioni=pd.DataFrame(1.0, columns=v_bear, index=v_bear)
    
    lista=os.listdir(cartella)
    
    for famiglia in lista:
        print famiglia
        f=open(cartella+famiglia).readlines()
        v1, v2 = np.triu_indices(len(f))
        for k in range(0, len(v1)):
            if v1[k]!=v2[k]:
                for i, el in enumerate(f[v1[k]].strip()):
                    sostituzioni.ix[el, f[v2[k]].strip()[i]]+=1.0
                    sostituzioni.ix[f[v2[k]].strip()[i], el]+=1.0
                        
    print 'Fine sostituzioni'
    sostituzioni.to_csv('sostituzioni_'+name+'_'+identity+'.tsv', sep="\t") 
    return sostituzioni


    
def make_q(sostituzioni, v_bear, name, identity):
    #sostituzioni=dataframe con le occorrenze delle coppie come creato dalla funzione sostituzioni_osservate
    #v_bear= vettore con caratteri bear
    #esempio=['a','A','=','l','L','^','i','I','+','n','N','>','s','S','~','b','B','|','y','Y','@','[', ':']

    
    #prendo solo valori della diagonale
    number_couple=0
    for j in range(0, len(v_bear)):
        number_couple+=sostituzioni.iloc[j,j:].sum()
    
    print number_couple
    
    q_ij=sostituzioni.divide(number_couple)
    q_ij.to_csv('q_ij_'+name+'_'+identity+'.tsv', sep="\t")

    return q_ij
    print 'Fine costruzione q_ij'
    

    
def make_p(q_ij, v_bear):
    #q_ij come creato dalla funzione precedente make_q
    p_i=dict.fromkeys(v_bear, 0)

    for char in v_bear:
        uguale=q_ij[char][char]
        altri=(sum(q_ij[char])-uguale)/2
        p_i[char]+=uguale+altri

    return p_i
    print 'Fine creazione dizionario p_i'

def make_e(p_i, v_bear, name, identity):
    e_ij=pd.DataFrame(1.0, columns=v_bear, index=v_bear)
    for char in v_bear:
        for char2 in v_bear:
            if char==char2:
                e_ij.ix[char, char2]=p_i[char]*p_i[char2]
            else:
                e_ij.ix[char, char2]=2*p_i[char]*p_i[char2]
    
    e_ij.to_csv('E_ij_'+name+'_'+identity+'.tsv', sep='\t')
    return e_ij
    
    print 'fine costruzione e_ij'
    
    
    
def crea_matrice(freq_observed, fr_attese, name, identity):
    #freq_observed=dataframe con frequenze osservate (q_ij)
    #fr_attese=dataframe con frequenze attese (e_ij)

    #Matrice di probabilita
    probability_matrix=freq_observed.divide(fr_attese)
    probability_matrix.to_csv('matrice_probabilita_'+name+'_'+identity+'.tsv', sep="\t")
    
    print 'Fine matrice probabilita'
    
    #Matrice di punteggio
    mbr_new=probability_matrix.applymap(np.log2)
    mbr_new.to_csv('MBR_'+name+'_'+identity+'.tsv', sep="\t")
    print 'Fine matrice punteggio'
    
    return mbr_new


def distribuzione_2punti(cartella):
    famiglie_bear=os.listdir(cartella)
    conta_2punti=[]
    for famiglia in famiglie_bear:
        f=open(cartella+'/'+famiglia)
        line=f.readline()
        while(line):
            c=Counter(line)
            conta_2punti.append(float(c[':'])/(len(line)-c['-']))
            line=f.readline()


    plt.hist(conta_2punti, bins=50)
    plt.ylim([0, 4000])
    plt.savefig('distribution_2punti_no_gap.pdf')
    #plt.show()
    plt.close()
    
    
def Expected_score(s_ij, p_i):
    E=0
    for i, char in enumerate(s_ij.columns.values):
        for i2, char2 in enumerate(s_ij.columns.values):
            if i2>=i:
                #print char, char2
                E+=s_ij.ix[char, char2]*p_i[char]*p_i[char2]

    print E
    return E


def entropy(q_ij, s_ij):
    H=0
    lunghezza=len(q_ij.columns.value_counts())

    for j in range(0, lunghezza):
        H+=(q_ij.iloc[j,j:]*s_ij.iloc[j,j:]).sum()
    
    print H
    return H
    
    
def make_heatmap(S_ij, name, identity):
    sns.set(font_scale=2.0)
    plt.figure(figsize=(10,10))
    ax=sns.heatmap(S_ij, xticklabels=1, yticklabels=1,cmap="YlGnBu")
    plt.savefig('matrix_'+name+'_'+identity+'.pdf')
    #plt.show()
    plt.close()
    
    
def CheVojDePiu(folder, folder_bear, RFAM_seed_file, id_blustClust, filtro_nSeq, file_alph, file_info):
    name=file_alph.split('.')[0]
    f=open(file_alph).readlines()
    o=open(file_info, "w")
    #run_blustClust(folder, id_blustClust, name, id_blustClust)
    #filtro_n_seq('not_similar_'+name+'_'+id_blustClust+'/', filtro_nSeq, name, id_blustClust)
    #get_bear('filtro_n_seq_'+name+'_'+id_blustClust+'/', folder_bear, name, id_blustClust)
    #add_gap('bear_filtered_'+name+'_'+id_blustClust+'/', RFAM_seed_file, name, id_blustClust)
    #convert_new_bear_file('bear_alignment_'+name+'_'+id_blustClust+'/', file_alph, name, id_blustClust)

    #crea_blocchi('bear_new_alignment_'+name+'_'+id_blustClust+'/', name, id_blustClust)
    
    v_char=[x.split()[1] for x in f]
    sost=sostituzioni_osservate('blocchi_new_bear_'+name+'_'+id_blustClust+'/', v_char, name, id_blustClust)

    q_ij=make_q(sost, v_char, name, id_blustClust) 

    p_i=make_p(q_ij, v_char)

    e_ij=make_e(p_i, v_char, name, id_blustClust)

    S_ij=crea_matrice(q_ij, e_ij, name, id_blustClust)
    
    E=Expected_score(S_ij, p_i)
    H=entropy(q_ij, S_ij)
    o.write('Expected_score:\t'+str(E)+'\nEntropy:\t'+str(H))
    o.close()
    make_heatmap(S_ij, name, id_blustClust)
    
    