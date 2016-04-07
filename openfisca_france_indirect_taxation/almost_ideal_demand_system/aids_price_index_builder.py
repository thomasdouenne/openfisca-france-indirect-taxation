# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
import datetime as dt

import os
import pkg_resources


def date_to_vag(date):
    args = date.split('_') + ['1']
    args = [int(arg) for arg in args]
    datetime = dt.datetime(*args)

    for vague in vagues:
        if vague['start'] <= datetime <= vague['end']:
            return vague['number']

    return None

# We want to obtain prices from the Excel file:

default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
indice_prix_mensuel_98_2015 = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'indice_prix_mensuel_98_2015.csv'
        ), sep =';', decimal = ','
    )

correspondance = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'correspondance_noms_coicop.csv'
        ), sep =';', header = -1
    )

correspondance.rename(columns = {0: 'nouveau_code', 1: 'ancien_code'}, inplace = True)
correspondance['ancien_code'] = correspondance['ancien_code'].astype(int)
correspondance['ancien_code'] = correspondance['ancien_code'].astype(str)

correspondance_dict = dict()
for instance in correspondance.iterrows():
    correspondance_dict[instance[1]['nouveau_code']] = instance[1]['ancien_code']

for key, value in correspondance_dict.iteritems():
    try:
        indice_prix_mensuel_98_2015[key] = indice_prix_mensuel_98_2015['_' + value]
    except:
        indice_prix_mensuel_98_2015[key] = 0

# Now we want to fill the empty columns with a given price index.
indice_prix_mensuel_98_2015['poste_02_2_1'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['poste_02_2_2'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['poste_02_2_3'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['poste_02_3'] = indice_prix_mensuel_98_2015['_2000']
indice_prix_mensuel_98_2015['poste_02_4'] = indice_prix_mensuel_98_2015['_2000']
indice_prix_mensuel_98_2015['poste_04_2_1'] = indice_prix_mensuel_98_2015['poste_04_1_1_1_1']
indice_prix_mensuel_98_2015['poste_04_5_5_2'] = indice_prix_mensuel_98_2015['poste_04_5_5_1_1']
indice_prix_mensuel_98_2015['poste_05_2_1_1_3'] = indice_prix_mensuel_98_2015['poste_05_1_2_1_1']
indice_prix_mensuel_98_2015['poste_05_2_1_2_1'] = indice_prix_mensuel_98_2015['poste_05_1_2_1_1']
indice_prix_mensuel_98_2015['poste_05_5_2_3'] = indice_prix_mensuel_98_2015['poste_05_5_1_3']
indice_prix_mensuel_98_2015['poste_05_7_1'] = indice_prix_mensuel_98_2015['_5000']
indice_prix_mensuel_98_2015['poste_05_7_2'] = indice_prix_mensuel_98_2015['_5000']
indice_prix_mensuel_98_2015['poste_06_1_1_2_1'] = indice_prix_mensuel_98_2015['_6110']
indice_prix_mensuel_98_2015['poste_06_1_1_3_1'] = indice_prix_mensuel_98_2015['_6110']
indice_prix_mensuel_98_2015['poste_06_3'] = indice_prix_mensuel_98_2015['_6000']
indice_prix_mensuel_98_2015['poste_06_4_2'] = indice_prix_mensuel_98_2015['_6000']
indice_prix_mensuel_98_2015['poste_07_1_2_1_2'] = indice_prix_mensuel_98_2015['poste_07_1_2_1_1']
indice_prix_mensuel_98_2015['poste_08_2'] = indice_prix_mensuel_98_2015['_8000']
indice_prix_mensuel_98_2015['poste_08_1_2_1_1'] = indice_prix_mensuel_98_2015['_8120']
indice_prix_mensuel_98_2015['poste_08_1_2_2_1'] = indice_prix_mensuel_98_2015['_8120']
indice_prix_mensuel_98_2015['poste_09_2_1_1_3'] = indice_prix_mensuel_98_2015['poste_09_2_2_2']
indice_prix_mensuel_98_2015['poste_09_2_3_1'] = indice_prix_mensuel_98_2015['poste_09_2_2_2']
indice_prix_mensuel_98_2015['poste_09_4_3'] = indice_prix_mensuel_98_2015['poste_09_3_1_1_1']
indice_prix_mensuel_98_2015['poste_10_5_1'] = indice_prix_mensuel_98_2015['poste_10_1']
indice_prix_mensuel_98_2015['poste_10_5_2'] = indice_prix_mensuel_98_2015['poste_10_1']
indice_prix_mensuel_98_2015['poste_10_2'] = indice_prix_mensuel_98_2015['poste_10_1']
indice_prix_mensuel_98_2015['poste_10_3'] = indice_prix_mensuel_98_2015['poste_10_1']
indice_prix_mensuel_98_2015['poste_10_4'] = indice_prix_mensuel_98_2015['poste_10_1']
indice_prix_mensuel_98_2015['poste_11_1_1_1_2'] = indice_prix_mensuel_98_2015['poste_11_1_1_1_1']
indice_prix_mensuel_98_2015['poste_12_1_3_3_3'] = indice_prix_mensuel_98_2015['_12000']
indice_prix_mensuel_98_2015['poste_12_5_1_1_1'] = indice_prix_mensuel_98_2015['_12500']
indice_prix_mensuel_98_2015['poste_12_5_5_1_1'] = indice_prix_mensuel_98_2015['_12500']
to_delete = [column for column in indice_prix_mensuel_98_2015.columns if column[:1] == '_']
for column in to_delete:
    del indice_prix_mensuel_98_2015[column]

indice_prix_mensuel_98_2015[['Annee', 'Mois']] = indice_prix_mensuel_98_2015[['Annee', 'Mois']].astype(str)
indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015[u'Annee'] + '_' + indice_prix_mensuel_98_2015[u'Mois']
indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']] = indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']].astype(float)
indice_prix_mensuel_98_2015['temps'] = \
    ((indice_prix_mensuel_98_2015[u'Annee'] - 1998) * 12) + indice_prix_mensuel_98_2015[u'Mois']
del indice_prix_mensuel_98_2015[u'Annee']
indice_prix_mensuel_98_2015['mois'] = indice_prix_mensuel_98_2015[u'Mois'].copy()
del indice_prix_mensuel_98_2015[u'Mois']

produits = list(column for column in indice_prix_mensuel_98_2015.columns if column[:6] == 'poste_')

df_indice_prix_produit = pd.melt(indice_prix_mensuel_98_2015, id_vars = ['date', 'temps', 'mois'], value_vars=produits,
    value_name = 'prix', var_name = 'bien')
# df_indice_prix_produit.bien = df_indice_prix_produit.bien.str.split('_').str[1]

vagues = [
    dict(
        number = 9,
        start = dt.datetime(2000, 5, 9),
        end = dt.datetime(2000, 6, 18),
        ),
    dict(
        number = 10,
        start = dt.datetime(2000, 6, 19),
        end = dt.datetime(2000, 7, 30),
        ),
    dict(
        number = 11,
        start = dt.datetime(2000, 8, 14),
        end = dt.datetime(2000, 9, 24),
        ),
    dict(
        number = 12,
        start = dt.datetime(2000, 9, 25),
        end = dt.datetime(2000, 11, 5),
        ),
    dict(
        number = 13,
        start = dt.datetime(2000, 11, 6),
        end = dt.datetime(2000, 12, 17),
        ),
    dict(
        number = 14,
        start = dt.datetime(2001, 1, 2),
        end = dt.datetime(2001, 2, 11),
        ),
    dict(
        number = 15,
        start = dt.datetime(2001, 2, 12),
        end = dt.datetime(2001, 3, 25),
        ),
    dict(
        number = 16,
        start = dt.datetime(2001, 3, 26),
        end = dt.datetime(2001, 5, 6),
        ),
    dict(
        number = 17,
        start = dt.datetime(2005, 3, 1),
        end = dt.datetime(2005, 4, 24),
        ),
    dict(
        number = 18,
        start = dt.datetime(2005, 4, 25),
        end = dt.datetime(2005, 6, 19),
        ),
    dict(
        number = 19,
        start = dt.datetime(2005, 6, 20),
        end = dt.datetime(2005, 8, 28),
        ),
    dict(
        number = 20,
        start = dt.datetime(2005, 8, 29),
        end = dt.datetime(2005, 10, 23),
        ),
    dict(
        number = 21,
        start = dt.datetime(2005, 10, 24),
        end = dt.datetime(2005, 12, 18),
        ),
    dict(
        number = 22,
        start = dt.datetime(2006, 1, 2),
        end = dt.datetime(2006, 2, 27),
        ),
    dict(
        number = 23,
        start = dt.datetime(2010, 10, 4),
        end = dt.datetime(2010, 11, 27),
        ),
    dict(
        number = 24,
        start = dt.datetime(2010, 11, 29),
        end = dt.datetime(2011, 1, 29),
        ),
    dict(
        number = 25,
        start = dt.datetime(2011, 1, 31),
        end = dt.datetime(2011, 3, 26),
        ),
    dict(
        number = 26,
        start = dt.datetime(2011, 3, 28),
        end = dt.datetime(2011, 5, 21),
        ),
    dict(
        number = 27,
        start = dt.datetime(2011, 5, 23),
        end = dt.datetime(2011, 7, 23),
        ),
    dict(
        number = 28,
        start = dt.datetime(2011, 8, 1),
        end = dt.datetime(2011, 10, 1),
        ),
    ]

df_indice_prix_produit['vag'] = df_indice_prix_produit['date'].map(date_to_vag)
df_indice_prix_produit = df_indice_prix_produit.dropna()
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(int)  # delete the .0 after each number
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(str)
df_indice_prix_produit['indice_prix_produit'] = df_indice_prix_produit['bien'] + '_' + df_indice_prix_produit['vag']
df_indice_prix_produit = df_indice_prix_produit.drop_duplicates(
    subset = ['indice_prix_produit'], keep = 'last')
