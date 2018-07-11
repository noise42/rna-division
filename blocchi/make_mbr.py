
import function_mbr as fun
fun.run_blustClust('seq/', '50')
fun.filtro_n_seq('not_similar/', 5)
fun.get_bear('filtro_n_seq/', 'bear/')
fun.add_gap('bear_filtered/', 'Rfam_no_double.seed')
fun.convert_new_bear('bear_alignment/')

fun.crea_blocchi('bear_new_alignment/')
alph_bear={'a':[], 'A':[], '=':[],
           'l':[], 'L':[], '^':[],
           'i':[], 'I':[], '+':[],
           'n':[], 'N':[], '>':[],
           's':[], 'S':[], '~':[],
           'b':[], 'B':[], '|':[],
           'y':[], 'Y':[], '@':[],
           '[':[], ':':[]}

f_att=fun.frequenze_attese('blocchi_new_bear/', alph_bear)

v_bear=['a','A','=','l','L','^','i','I','+','n','N','>','s','S','~','b','B','|','y','Y','@','[', ':']

f_oss=fun.frequenze_osservate('blocchi_new_bear/', v_bear)

mbr=fun.crea_matrice(f_oss, f_att)
