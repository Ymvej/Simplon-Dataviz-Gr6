import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv


# Lecture des fichiers csv

Entreprise = pd.read_csv("Base/entreprise_2020_02_19_04_00.csv",sep = ",")

compte = Entreprise['pays'].value_counts()
print(compte)

secteurs = Entreprise['secteur'].value_counts()
print(secteurs)