# ---------- Init -----------
import pandas as pd

import time
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pygal # Python SVG graph plotting library
from pygal.style import NeonStyle # sexy af

os.system('clear')

# Constants containing the columns we want to fetch from the csv's.
COLS_AVANTAGE = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'avant_date_signature', 'avant_montant_ttc']
COLS_CONVENTION = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'conv_date_signature', 'conv_objet', 'conv_montant_ttc']
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

    # Core
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
            cp = str(cp)
            if len(cp) == 1:
                cp = '0' + cp
            else:
                pass
            ttc = int(ttc)
            sc += 1
        except ValueError:
            fc += 1
            continue

    

        # Populating dictionary while correcting issues
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
    Creates a html file from a dictionary generated by comparator3000().
    Asks for a Title (displayed at the top of the page) and a subtitle
    (displayed over each department).
    '''

    # Core
    fr_chart = pygal.maps.fr.Departments(human_readable=True, style=NeonStyle)
    fr_chart.title = str(title)
    fr_chart.add(str(subtitle), dic)

    # Renders it and outputs to file in the current working directory
    fr_chart.render_to_file('%s.html'%(title))

def dash_runtime():

    # Import feuille de style CSS
    print('Styling...')
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # Définition des plots à afficher
    print('fig1 start')
    fig1 = px.histogram(D_Remuneration, x="qualite", y="remu_montant_ttc", histfunc="avg", title = 'Moyenne des rémunérations par qualité', labels =    {'qualite':'Qualité' , 'remu_montant_ttc':'Montant moyen TTC de la rémunération'}).update_xaxes(categoryorder="total descending")
    print('fig1 done')

    print('fig2 start')
    fig2 = px.histogram(D_avantage, x="qualite", y="avant_montant_ttc", histfunc="avg", title = 'Moyenne des avantages accordés par qualité', labels =    {'qualite':'Qualité' , 'avant_montant_ttc':'Montant moyen TTC des avantages accordés'}).update_xaxes(categoryorder="total descending")
    print('fig2 done')

    print('fig3 start')
    fig3 = px.histogram(D_Convention, x="conv_objet", y="conv_montant_ttc", histfunc="avg", title = 'Moyenne des conventions signées par type', labels =    {'qualite':'Type de convention' , 'conv_montant_ttc':'Montant moyen TTC des conventions signées'}).update_xaxes(categoryorder="total descending")
    print('fig3 done')


    # Layout Dash
    app.layout = html.Div(children=[
        html.H1(children='Transparence Santé'),

        html.Div(children='''
            Visualisation de données à partir de la base de données publique "Transparence - Santé"
        ''' ),
        # Affichage des plots définis plus haut 
        dcc.Graph(
            id = 'Remun',
            figure = fig1
        ),

        html.Div(children='''
            Visualisation de données à partir de la base de données publique "Transparence - Santé"
        ''' ),
        # Affichage des plots définis plus haut 
        dcc.Graph(
            id = 'Avant',
            figure = fig2
        ),

        html.Div(children='''
            Visualisation de données à partir de la base de données publique "Transparence - Santé"
        ''' ),
        # Affichage des plots définis plus haut 
        dcc.Graph(
            id = 'Conv',
            figure = fig3

        )
    ])


    # Run Dash server
    if __name__ == '__main__':
        app.run_server(debug=True)

# ---------- Execution ----------

# Maps
rconv = comparator3000(D_Convention, 'conv_montant_ttc')
ravant = comparator3000(D_avantage, 'avant_montant_ttc')
rremu = comparator3000(D_Remuneration, 'remu_montant_ttc')

get_map(rconv, 'Conventions', 'Valeur totale des conventions passées par département en €')
get_map(ravant, 'Avantage', 'Montant total des avantages accordés par département en €')
get_map(rremu, 'Rémunérations', 'Montant total des salaires versés par département en €')

# Dash
dash_runtime()
