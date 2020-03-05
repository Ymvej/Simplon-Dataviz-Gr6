

import pandas as pd
import time
import os
import pygal
from progress.bar import Bar


Col_avantage = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'avant_date_signature', 'avant_montant_ttc']
Col_convention = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'conv_date_signature', 'conv_montant_ttc']
Col_remuneration = ['entreprise_identifiant', 'denomination_sociale', 'benef_categorie_code', 'qualite', 'benef_codepostal', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'remu_date', 'remu_montant_ttc']
Col_entreprise = ['pays','secteur','code_postal','ville']



start = time.perf_counter() # getting starting timestamp
print('Starting import...\n\n')
print('Importing D_avantage...')
# D_avantage = pd.read_csv("Base/declaration_avantage_2020_02_19_04_00.csv", sep = ";", usecols = Col_avantage)
print('D_avantage successfully imported. 3 more to go.')
print('Importing D_Convention...')
D_Convention = pd.read_csv("Base/declaration_convention_2020_02_19_04_00.csv", sep = ";", usecols = Col_convention)
D_Convention.name = 'Conventions'
print('D_Convention successfully imported. 2 more to go.')
print('Importing D_Remuneration...')
# D_Remuneration = pd.read_csv("Base/declaration_remuneration_2020_02_19_04_00.csv", sep = ";", usecols = Col_remuneration)
print('D_Remuneration successfully imported. 1 more to go.')
print('Importing Entreprise...')
# Entreprise = pd.read_csv("Base/entreprise_2020_02_19_04_00.csv", sep = ",", usecols = Col_entreprise)
print('Entreprise successfully imported.')
success = time.perf_counter() # getting ending timestamp
import_time = int(success - start) 
print('All csv successfully imported in %s seconds.'%(import_time))





def comparator3000(df, fetch):
    '''

    '''
    print('Started importing %s from %s.'%(fetch, df.name) )
    dic = dict()
    bar = Bar('Processing...', suffix='%(percent)d%%')
    start = time.perf_counter()
    q = list(df.index)
    fc = 0
    sc = 0
    for i in q:

        cp = df['benef_codepostal'][i]
        ttc = df[str(fetch)][i]

        cp = str(cp)
        cp = cp[:2]
    
        try:
            cp = int(cp)
            ttc = int(ttc)
            sc += 1
        except ValueError:
            fc += 1
            continue

        if cp in dic:
            dic[cp] += ttc

        else:
            dic[cp] = ttc

        if i % 8500 == 0:
            bar.next()
    bar.finish()

    success = time.perf_counter()
    ns = int(success - start) 

    
    

    print('Succesfully imported %s from %s in %s seconds | %s rows had one or more missing values and were omitted | %s rows were usable'%(fetch, df, ns, sc, fc))        

    return dic


jpp = comparator3000(D_Convention, 'conv_montant_ttc')

def get_map(dic, title, subtitle):
    fr_chart = pygal.maps.fr.Departments(human_readable=True)
    fr_chart.title = str(title)
    fr_chart.add(str(subtitle), jpp)
    fr_chart.render_in_browser()
    
get_map(jpp, 'Test', 'Subtest')