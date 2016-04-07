# -*- coding: utf-8 -*-

from __future__ import division


import pandas as pd
import numpy as np
import os
import pkg_resources


from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import \
    df_indice_prix_produit
from openfisca_france_indirect_taxation.almost_ideal_demand_system.utils import \
    add_area_dummy, add_stalog_dummy, add_vag_dummy, electricite_only, indices_prix_carbus, price_carbu_pond, \
    price_carbu_from_quantities, price_energy_from_contracts


assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

# On importe la dataframe qui recense les indices de prix. Notre objectif est de construire une nouvelle dataframe avec
# le reste des informations, i.e. la consommation et autres variables pertinentes concernant les ménages.

# On commence par cinstruire une dataframe appelée data_conso rassemblant les informations sur les dépenses des ménages.
data_frame_for_reg = None
data_frame_all_years = pd.DataFrame()
for year in [2011]:
    aggregates_data_frame = get_input_data_frame(year)

    # Pour estimer QAIDS, on se concentre sur les biens non-durables.
    # On élimine donc les biens durables de cette dataframe: 442 : redevance d'enlèvement des ordures, 711, 712, 713 :
    # achat de véhicules, 911, 912, 9122, 913, 9151 : technologies high-tech, 9211, 921, 923: gros équipements loisirs,
    # 941, 960 : voyages séjours et cadeaux, 10i0 : enseignement, 12.. : articles de soin et bijoux

    biens_durables = ['poste_04_4_1_3_1', 'poste_07_1_1_1_1', 'poste_07_1_1_2_1', 'poste_07_1_2_1_1', 'poste_07_1_3',
        'poste_09_1_1_1_2', 'poste_09_1_1_1_3', 'poste_09_1_2_1_1_a', 'poste_09_1_2_1_1_b', 'poste_09_1_3_1_1', 'poste_09_1_5_1_1',
        'poste_09_2_1_1_1', 'poste_09_2_2_2', 'poste_09_2_1_1_3', 'poste_09_2_3_1', 'poste_09_6_1_1_1',
        'poste_09_4_1_1_2', 'poste_10_1', 'poste_10_5_1', 'poste_10_5_2', 'poste_10_2',
        'poste_10_4', 'poste_10_5', 'poste_12_1_3_3_3', 'poste_12_3_1_1_1', 'poste_12_3_3_1_1',
        'poste_12_4_1_1_1', 'poste_12_7_1_1_1', 'poste_1_10_1', 'poste_1_10_2', 'poste_14_1_1_1'] + \
            [x for x in aggregates_data_frame.columns if x[6:8]=='13']

    for bien in biens_durables:
        try:
            aggregates_data_frame = aggregates_data_frame.drop(bien, axis = 1)
        except:
            aggregates_data_frame = aggregates_data_frame

    energie_logement = ['poste_04_5_1_1_1_b', 'poste_04_5_1_1_1_b1', 'poste_04_5_2_1_1', 'poste_04_5_2_2_1',
        'poste_04_5_3_1_1', 'poste_04_5_4_1_1', 'poste_04_5_5_1_1', 'poste_04_5_5_2']

    produits = [column for column in aggregates_data_frame.columns if column[:6] == 'poste_']
    del column

    aggregates_data_frame['depenses_carbu'] = aggregates_data_frame['poste_07_2_2_1_1']

    aggregates_data_frame['depenses_logem'] = 0
    for logem in energie_logement:
        try:
            aggregates_data_frame['depenses_logem'] += aggregates_data_frame[logem]
        except:
            pass

    aggregates_data_frame['depenses_tot'] = 0
    for produit in produits:
        if produit[13:15] != '99' and produit[13:15] != '13':
            aggregates_data_frame['depenses_tot'] += aggregates_data_frame[produit]

    aggregates_data_frame['depenses_autre'] = (
        aggregates_data_frame['depenses_tot'] - aggregates_data_frame['depenses_carbu'] -
        aggregates_data_frame['depenses_logem'])

    data_conso = aggregates_data_frame[produits + ['vag', 'ident_men', 'depenses_autre', 'depenses_carbu',
        'depenses_logem']].copy()

    # On renverse la dataframe pour obtenir une ligne pour chaque article consommé par chaque personne
    df = pd.melt(data_conso, id_vars = ['vag', 'ident_men'], value_vars=produits,
        value_name = 'depense_bien', var_name = 'bien')

    df_indice_prix_produit = df_indice_prix_produit[['indice_prix_produit', 'prix', 'temps', 'mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['bien'] + '_' + df['vag']

    # On merge les prix des biens avec les dépenses déjà présentes dans df. Le merge se fait sur 'indice_prix_produit'
    # Indice prix produit correspond à poste_xyz_vag
    df_depenses_prix = pd.merge(df, df_indice_prix_produit, on = 'indice_prix_produit')

    # df_depenses_prix contient les dépenses de consommation et les prix associés à ces dépenses.
    # Il faut maintenant construire les catégories de biens que l'on souhaite comparer.
    df_depenses_prix['type_bien'] = 'autre'
    df_depenses_prix.loc[df_depenses_prix['bien'] == 'poste_07_2_2_1_1', 'type_bien'] = 'carbu'
    for logem in energie_logement:
        df_depenses_prix.loc[df_depenses_prix['bien'] == logem, 'type_bien'] = 'logem'
    del logem, produit

    # Construire les indices de prix pondérés pour les deux catégories
    df_depenses_prix[['type_bien', 'ident_men']] = df_depenses_prix[['type_bien', 'ident_men']].astype(str)
    df_depenses_prix['id'] = df_depenses_prix['type_bien'] + '_' + df_depenses_prix['ident_men']

    data_conso['ident_men'] = data_conso['ident_men'].astype(str)
    df_depenses_prix = pd.merge(
        df_depenses_prix, data_conso[['depenses_autre', 'depenses_carbu', 'depenses_logem', 'ident_men']],
        on = 'ident_men')
    del data_conso
    df_depenses_prix[['depenses_autre', 'depense_bien', 'depenses_carbu', 'depenses_logem', 'prix']] = \
        df_depenses_prix[['depenses_autre', 'depense_bien', 'depenses_carbu', 'depenses_logem', 'prix']].astype(float)

    df_depenses_prix['part_bien_categorie'] = 0
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'autre', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_autre']
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'carbu', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_carbu']
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'logem', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_logem']

    df_depenses_prix.fillna(0, inplace=True)

    # Les parts des biens dans leur catégorie permettent de construire des indices de prix pondérés (Cf. Lewbel)
    df_depenses_prix['indice_prix_pondere'] = 0
    # On utilise les contrats imputés pour affiner les prix du gaz et de l'électricité
    df_depenses_prix = price_energy_from_contracts(df_depenses_prix, year)
    df_depenses_prix['indice_prix_pondere'] = df_depenses_prix['part_bien_categorie'] * df_depenses_prix['prix']

    # grouped donne l'indice de prix pondéré pour chacune des deux catégories pour chaque individu
    # On met cette dataframe en forme pour avoir pour chaque individu l'indice de prix pour chaque catégorie
    # Cela donne df_prix_to_merge
    df_depenses_prix.sort_values(by = ['id'])
    grouped = df_depenses_prix['indice_prix_pondere'].groupby(df_depenses_prix['id'])
    assert len(grouped) == 3 * len(aggregates_data_frame), 'There is an issue in the aggregation of prices'
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    grouped['categorie'] = grouped['id'].str[:5]
    categories = ['autre', 'carbu', 'logem']
    for categorie in categories:
        grouped['prix_' + categorie] = 0
        grouped.loc[grouped['categorie'] == categorie, 'prix_' + categorie] = grouped['indice_prix_pondere']

    grouped_autre = grouped[grouped['categorie'] == 'autre'].copy()
    grouped_autre['ident_men'] = grouped_autre['id'].str[6:]
    grouped_carbu = grouped[grouped['categorie'] == 'carbu'].copy()
    grouped_carbu['ident_men'] = grouped_carbu['id'].str[6:]
    grouped_logem = grouped[grouped['categorie'] == 'logem'].copy()
    grouped_logem['ident_men'] = grouped_logem['id'].str[6:]

    df_prix_to_merge = pd.merge(grouped_carbu[['ident_men', 'prix_carbu']], grouped_autre[['ident_men', 'prix_autre']],
        on = 'ident_men')
    df_prix_to_merge = pd.merge(df_prix_to_merge, grouped_logem[['ident_men', 'prix_logem']], on = 'ident_men')
    del grouped, grouped_autre, grouped_carbu, grouped_logem

    # Problème: ceux qui ne consomment pas de carbu ou d'alimentaire se voient affecter un indice de prix égal à 0. Ils
    # sont traités plus bas.

    # On crée une variable dummy pour savoir si le ménage ne consomme que de l'électricité ou aussi du gaz.
    # Si seulement électricité, elle est égale à 1.
    aggregates_data_frame = electricite_only(aggregates_data_frame)
    # On récupère les informations importantes sur les ménages, dont les variables démographiques
    df_info_menage = aggregates_data_frame[['agepr', 'depenses_autre', 'depenses_carbu',
        'depenses_logem', 'depenses_tot', 'dip14pr', 'elect_only', 'ident_men', 'nenfants', 'nactifs', 'ocde10',
        'revtot', 'situacj', 'situapr', 'stalog', 'strate', 'typmen', 'vag', 'veh_diesel',
        'veh_essence']].copy()
    df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)
    df_info_menage['part_autre'] = df_info_menage['depenses_autre'] / df_info_menage['depenses_tot']
    df_info_menage['part_carbu'] = df_info_menage['depenses_carbu'] / df_info_menage['depenses_tot']
    df_info_menage['part_logem'] = df_info_menage['depenses_logem'] / df_info_menage['depenses_tot']

    # On merge les informations sur les caractéristiques du ménage et leurs consommations avec les indices de prix
    # pondérés pour les deux catégories
    dataframe = pd.merge(df_info_menage, df_prix_to_merge, on = 'ident_men')
    del df_info_menage, df_prix_to_merge
    # Pour ceux qui ne consomment pas de carburants, on leur associe le prix correspondant à leur vague d'enquête
    price_carbu = \
        df_indice_prix_produit[df_indice_prix_produit['indice_prix_produit'].str[:16] == 'poste_07_2_2_1_1'].copy()
    price_carbu['vag'] = price_carbu['indice_prix_produit'].str[17:].astype(int)
    price_carbu = price_carbu[['vag', 'prix']]
    price_carbu['prix'] = price_carbu['prix'].astype(float)
    dataframe = pd.merge(dataframe, price_carbu, on = 'vag')
    del price_carbu
    dataframe.loc[dataframe['prix_carbu'] == 0, 'prix_carbu'] = dataframe['prix']

    dataframe['depenses_par_uc'] = dataframe['depenses_tot'] / dataframe['ocde10']

    dataframe = dataframe[['ident_men', 'part_carbu', 'part_logem', 'part_autre', 'prix_carbu', 'prix_logem',
        'prix_autre', 'agepr', 'depenses_par_uc', 'depenses_tot', 'dip14pr', 'elect_only', 'nactifs', 'nenfants',
        'situacj', 'situapr', 'stalog', 'strate', 'typmen', 'vag', 'veh_diesel', 'veh_essence']]

    # On supprime de la base de données les individus pour lesquels on ne dispose d'aucune consommation alimentaire.
    # Leur présence est susceptible de biaiser l'analyse puisque de toute évidence s'ils ne dépensent rien pour la
    # nourriture ce n'est pas qu'ils n'en consomment pas, mais qu'ils n'en ont pas acheté sur la période (réserves, etc)
    dataframe = dataframe.query('prix_logem != 0')

    # On enlève les outliers, que l'on considère comme les individus dépensant plus de 25% de leur budget en carburants
    # Cela correspond à 16 et 13 personnes pour 2000 et 2005 ce qui est négligeable, mais 153 i.e. 2% des consommateurs
    # pour 2011 ce qui est assez important. Cette différence s'explique par la durée des enquêtes (1 semaine en 2011)
    dataframe = dataframe.query('part_carbu < 0.25')

    if year == 2011:
        dataframe = price_carbu_from_quantities(dataframe, 2011)
    else:
        indices_prix_carburants = indices_prix_carbus(year)
        dataframe = pd.merge(dataframe, indices_prix_carburants, on = 'vag')
        dataframe = price_carbu_pond(dataframe)
    dataframe['year'] = year

    dataframe = add_area_dummy(dataframe)
    dataframe = add_stalog_dummy(dataframe)
    dataframe = add_vag_dummy(dataframe)

    data_frame_for_reg = dataframe.rename(columns = {'part_carbu': 'w1', 'part_logem': 'w2',
        'part_autre': 'w3', 'prix_carbu': 'p1', 'prix_logem': 'p2', 'prix_autre': 'p3'})

    data_frame_all_years = pd.concat([data_frame_all_years, data_frame_for_reg])
    data_frame_all_years.fillna(0, inplace = True)

'''

    data_frame_for_reg.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_energy_no_alime_{}.csv'.format(year)), sep = ',')

data_frame_all_years.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_energy_no_alime_all_years.csv'), sep = ',')

# Dataframe par groupes spécifiques (hauts revenus, bas revenus, ruraux, etc.)

data_frame_not_elect_only = data_frame_all_years.query('elect_only == 0')
data_frame_not_elect_only.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_no_elect_only_no_alime_all_years.csv'), sep = ',')

mediane_depenses_par_uc = data_frame_all_years['depenses_par_uc'].median()
data_frame_high_income = data_frame_all_years.query('depenses_par_uc > {}'.format(mediane_depenses_par_uc))
data_frame_low_income = data_frame_all_years.query('depenses_par_uc < {}'.format(mediane_depenses_par_uc))

data_frame_high_income.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_high_income_no_alime_all_years.csv'), sep = ',')
data_frame_low_income.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_low_income_no_alime_all_years.csv'), sep = ',')

data_frame_rural = \
    data_frame_all_years.query('strate == 400 | strate == 112 | strate == 212 | strate == 222 | strate == 0')
data_frame_large_cities = \
    data_frame_all_years.query('strate == 111 | strate == 4 | strate == 3 | strate == 2')
data_frame_rural.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_rural_no_alime_all_years.csv'), sep = ',')
data_frame_large_cities.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quaids', 'data_frame_large_cities_no_alime_all_years.csv'), sep = ',')


# Must correct what is useless, improve demographics : dip14
# dip14 : use only dip14pr (good proxy for dip14cj anyway), but change the nomenclature to have just 2 or 3 dummies
# describing whether they attended college or not, etc.
# Use more functions in utils

'''
