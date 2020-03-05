import pandas as pd
import time
import os
import dash

import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import plotly.express as px

Col_avantage = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'avant_date_signature', 'avant_montant_ttc', 'avant_nature']
Col_convention = ['ligne_identifiant', 'denomination_sociale', 'categorie', 'qualite', 'benef_codepostal', 'benef_ville', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'ligne_type', 'conv_date_signature']
Col_remuneration = ['entreprise_identifiant', 'denomination_sociale', 'benef_categorie_code', 'qualite', 'benef_codepostal', 'pays', 'benef_titre_libelle', 'benef_speicalite_libelle', 'benef_etablissement_codepostal', 'remu_date', 'remu_montant_ttc']
Col_entreprise = ['identifiant', 'pays', 'secteur', 'code_postal', 'ville']

#D_avantage = pd.read_csv("C:/Users/Utilisateur/Desktop/Python/Simplon-Dataviz-Gr6/Base/declaration_avantage_2020_02_19_04_00.csv", sep = ";", usecols = Col_avantage)
#D_Convention = pd.read_csv("C:/Users/Utilisateur/Desktop/Python/Simplon-Dataviz-Gr6/Base/declaration_convention_2020_02_19_04_00.csv", sep = ";", usecols = Col_convention)
D_Remuneration = pd.read_csv("C:/Users/Utilisateur/Desktop/Python/Simplon-Dataviz-Gr6/Base/declaration_remuneration_2020_02_19_04_00.csv", sep = ";", usecols = Col_remuneration)
#Entreprise = pd.read_csv("C:/Users/Utilisateur/Desktop/Python/Simplon-Dataviz-Gr6/Base/entreprise_2020_02_19_04_00.csv", sep = ",", usecols = Col_entreprise)

##### DASH #####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig1 = px.histogram(D_Remuneration, x="qualite", y="remu_montant_ttc", histfunc="avg", title = 'Moyenne des rémunérations par qualité', labels = {'qualite':'Qualité' , 'remu_montant_ttc':'Montant moyen TTC de la rémunération'})

app.layout = html.Div(children=[
    html.H1(children='Transparence Santé'),

    html.Div(children='''
        Visualisation de données à partir de la base de données publique Transparence - Santé
    ''' ),

    dcc.Graph(
        id = 'Montant rému par qualité',
        figure = fig1
    ),

    html.Div(html.Img(src='https://www.monoprix.fr/assets/images/grocery/3500013/580x580.jpg')),

    html.Div(children = [
        html.H1(children = 'Test iframe'),

        html.Iframe(src = f'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6', height = 1300, width = 1000)
    ]

    )
])


##### RUN DASH #####

if __name__ == '__main__':
    app.run_server(debug=True)

