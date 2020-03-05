# ---------- Init -----------
import pandas as pd
import time
import os
import pygal # Python SVG graph plotting library
from pygal.style import NeonStyle # sexy af


# Constants containing the columns we want to fetch from the csv's.
COLS_AVANTAGE = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'avant_date_signature', 'avant_montant_ttc']
COLS_CONVENTION = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'conv_date_signature', 'conv_montant_ttc']
COLS_REMUNERATION = ['entreprise_identifiant', 'denomination_sociale', 'benef_categorie_code', 'qualite', 'benef_codepostal', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'remu_date', 'remu_montant_ttc']
COLS_ENTREPRISE = ['pays','secteur','code_postal','ville']


start = time.perf_counter() # starting time counter

# Sequentially reads CSVs while displaying some basic progress info
# Uses usecols= to only take columns defined in the constants above
print('Started import.')
print('-----------------------')

print('Importing D_avantage...')
D_avantage = pd.read_csv("Base/declaration_avantage_2020_02_19_04_00.csv", sep = ";", usecols = COLS_AVANTAGE)
D_avantage.name = 'D_avantage'
print('D_avantage successfully imported. 3 more to go.')

print('Importing D_Convention...')
D_Convention = pd.read_csv("Base/declaration_convention_2020_02_19_04_00.csv", sep = ";", usecols = COLS_CONVENTION)
D_Convention.name = 'D_Convention'
print('D_Convention successfully imported. 2 more to go.')

print('Importing D_Remuneration...')
D_Remuneration = pd.read_csv("Base/declaration_remuneration_2020_02_19_04_00.csv", sep = ";", usecols = COLS_REMUNERATION)
D_Remuneration.name = 'D_Remuneration'
print('D_Remuneration successfully imported. 1 more to go.')

print('Importing Entreprise...')
Entreprise = pd.read_csv("Base/entreprise_2020_02_19_04_00.csv", sep = ",", usecols = COLS_ENTREPRISE)
Entreprise.name = 'Entreprise'
print('Entreprise successfully imported.')

# Calculates and prints compute time
success = time.perf_counter() 
import_time = int(success - start) 
print('-----------------------')
print('All csv successfully imported in %s seconds.\n\n'%(import_time))


# ---------- Functions ----------

def comparator3000(df, fetch):
    '''
    Creates a dictionary {'Postal Code' : 'Total € given'} with a 
    dataframe and a column of that dataframe.
    '''

    print('Started importing %s from %s.'%(fetch, df.name) )

    # Init 
    dic = dict() 
    start = time.perf_counter()
    q = list(df.index)
    fc = 0
    sc = 0

    # Main loop
    for i in q:

        # Progress bar
        if i % int((len(q)/100)) == 0: 
            aa = int(i / len(q) * 100) 
            aa = str(aa)
            print('%s %% processed.'%(aa))

        # Dynamically assigning relevant column values from row i
        cp = df['benef_codepostal'][i]
        ttc = df[fetch][i]

        # Type verification, splicing, and success/fail counts.
        cp = str(cp)
        cp = cp[:2]
        try:
            cp = int(cp)
            ttc = int(ttc)
            sc += 1
        except ValueError:
            fc += 1
            continue

        # Populating dictionary
        if cp in dic:
            dic[cp] += ttc
        else:
            dic[cp] = ttc

    # Reporting compute time and successes/fails
    success = time.perf_counter()
    ns = int(success - start) 
    print('Succesfully imported %s from %s in %s seconds | %s rows had one or more missing values and were omitted | %s rows were usable\n'%(fetch, df.name, ns, sc, fc))        

    return dic


def get_map(dic, title, subtitle):
    '''
    Creates a html file
    '''
    fr_chart = pygal.maps.fr.Departments(human_readable=True, width=1080, height=1080, style=NeonStyle)
    fr_chart.title = str(title)
    fr_chart.add(str(subtitle), dic)
    # fr_chart.add(str(subtitle), jpp3)

    # fr.chart.render_in_browser() = 
    fr_chart.render_to_file('%s.html'%(title))

# jpp2 = comparator3000(D_Convention, 'conv_montant_ttc')
# jpp = comparator3000(D_avantage, 'avant_montant_ttc')
jpp3 = comparator3000(D_Remuneration, 'remu_montant_ttc')

get_map(jpp3, 'Test', 'Moins test')



# array_ = []

# def aggregator3000(array, df, fetch):

#     for i in enumerate(fetch):
#         print(i)
#         print(list_fetch)
#         fetched = comparator3000(df, fetch)
#         array.append(fetched)
    
    

# print(array_)
# aggregator3000(array_, D_avantage, ['avant_montant_ttc'])
# aggregator3000(array_, D_Convention, ['conv_montant_ttc'])
# aggregator3000(array_, D_Remuneration, ['remu_montant_ttc'])
# print(array_)

# for i in array_:
#     get_map(array_[i], 'Titletest', 'Subtitletest')