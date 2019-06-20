# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, graph_builder_line, save_dataframe_to_graph, \
    dataframe_by_group, age_group, energy_modes
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


# Homogeneous + SL :
#elasticities['elas_price_1_1'] = -0.466
#elasticities['elas_price_2_2'] = -0.214

# Homogeneous, no SL :
#elasticities['elas_price_1_1'] = -0.440
#elasticities['elas_price_2_2'] = -0.139

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reformes_cae',
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'chaufp',
    'revenu_reforme_reformes_cae',
    'revenu_reforme_reformes_cae_sans_rattrapage',
    'depenses_diesel_corrigees',
    'depenses_essence_corrigees',
    'depenses_carburants_corrigees',
    'transferts_neutre_reformes_cae',
    'transferts_neutre_reformes_cae_sans_rattrapage',
    'strate',
    'niveau_vie_decile',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'agepr',
    'nactifs',
    'nenfants',
    'niveau_vie_decile',
    'ocde10',
    'rev_disp_loyerimput',
    'situacj',
    'situapr',
    'log_indiv',
    'bat_av_49',
    'bat_49_74',
    'ouest_sud',
    'surfhab_d',
    'aides_logement',
    'typmen',
    'age_vehicule',
    'stalog',
    'situapr',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['cout_reforme_avant_compensation_reformes_cae'] = - df_reforme['revenu_reforme_reformes_cae']
df_reforme['cout_reforme_avant_compensation_reformes_cae_sans_rattrapage'] = - df_reforme['revenu_reforme_reformes_cae_sans_rattrapage']

df_reforme[u'transfert_net_apres_compensation_uc'] = (
    df_reforme['transferts_neutre_reformes_cae_sans_rattrapage']
    - df_reforme['revenu_reforme_reformes_cae_sans_rattrapage']
    ) / df_reforme['ocde10']

df_reforme = age_group(df_reforme)
df_reforme = energy_modes(df_reforme)

df_reforme['proprietaire'] = 0
df_reforme.loc[df_reforme.stalog.isin([1, 2]), 'proprietaire'] = 1

df_reforme['etudiant'] = 0
df_reforme.loc[df_reforme.situapr == 3, 'etudiant'] = 1

df_reforme['diesel'] = 0 + 1 * (df_reforme['depenses_diesel_corrigees'] > 0)
df_reforme['essence'] = 0 + 1 * (df_reforme['depenses_essence_corrigees'] > 0)
df_reforme['carburants'] = 0 + 1 * (df_reforme['depenses_carburants_corrigees'] > 0)# * (df_reforme['depenses_diesel_corrigees'] == 0)



df_2_rural_fioul_diesel = df_reforme.query('strate == 0').query('combustibles_liquides == 1').query('niveau_vie_decile == 2').query('diesel == 1')
print len(df_2_rural_fioul_diesel), float(df_2_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae_sans_rattrapage'].mean()) / df_2_rural_fioul_diesel['ocde10'].mean()
print len(df_2_rural_fioul_diesel), float(df_2_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_2_rural_fioul_diesel['ocde10'].mean()

df_2_paris_gaz_novp = df_reforme.query('niveau_vie_decile == 2').query('strate == 4').query('gaz_ville == 1').query('carburants == 0')
print len(df_2_paris_gaz_novp), float(df_2_paris_gaz_novp['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_2_paris_gaz_novp['ocde10'].mean()

df_5_moyenne_gaz_essence = df_reforme.query('niveau_vie_decile == 5').query('strate == 2').query('gaz_ville == 1').query('essence == 1').query('diesel == 0')
print len(df_5_moyenne_gaz_essence), float(df_5_moyenne_gaz_essence['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_5_moyenne_gaz_essence['ocde10'].mean()

df_5_rural_fioul_diesel = df_reforme.query('niveau_vie_decile == 5').query('strate == 0').query('combustibles_liquides == 1').query('diesel == 1')
print len(df_5_rural_fioul_diesel), float(df_5_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae_sans_rattrapage'].mean()) / df_5_rural_fioul_diesel['ocde10'].mean()
print len(df_5_rural_fioul_diesel), float(df_5_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_5_rural_fioul_diesel['ocde10'].mean()

df_9_paris_gaz_novp = df_reforme.query('niveau_vie_decile == 9').query('strate == 4').query('gaz_ville == 1').query('carburants == 0')
print len(df_9_paris_gaz_novp), float(df_9_paris_gaz_novp['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_9_paris_gaz_novp['ocde10'].mean()

df_9_rural_fioul_diesel = df_reforme.query('niveau_vie_decile == 9').query('strate == 0').query('combustibles_liquides == 1').query('diesel == 1')
print len(df_9_rural_fioul_diesel), float(df_9_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae_sans_rattrapage'].mean()) / df_9_rural_fioul_diesel['ocde10'].mean()
print len(df_9_rural_fioul_diesel), float(df_9_rural_fioul_diesel['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_9_rural_fioul_diesel['ocde10'].mean()

print "Ensemble", float(df_reforme['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme['ocde10'].mean()
print "Fioul", float(df_reforme.query('combustibles_liquides == 1')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('combustibles_liquides == 1')['ocde10'].mean()
print "Gaz", float(df_reforme.query('gaz_ville == 1')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('gaz_ville == 1')['ocde10'].mean()
print "Autre", float(df_reforme.query('gaz_ville == 0').query('combustibles_liquides == 0')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('gaz_ville == 0').query('combustibles_liquides == 0')['ocde10'].mean()
print "Diesel", float(df_reforme.query('diesel == 1')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('diesel == 1')['ocde10'].mean()
print "Essence", float(df_reforme.query('essence == 1').query('diesel == 0')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('essence == 1').query('diesel == 0')['ocde10'].mean()
print "Carburants", float(df_reforme.query('carburants == 0')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('carburants == 0')['ocde10'].mean()
print "Ruraux", float(df_reforme.query('strate == 0')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('strate == 0')['ocde10'].mean()
print "Paris", float(df_reforme.query('strate == 4')['cout_reforme_avant_compensation_reformes_cae'].mean()) / df_reforme.query('strate == 4')['ocde10'].mean()
