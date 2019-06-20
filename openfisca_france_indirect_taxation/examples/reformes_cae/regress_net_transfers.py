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
    'distance',
    'distance_routiere_hebdomadaire_teg',
    'duree_moyenne_trajet_aller_retour_teg',
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

df_reforme['rev_disp_loyerimput_2'] = df_reforme['rev_disp_loyerimput'] ** 2
df_reforme['alone'] = 0 + (1 * df_reforme['situacj'] == 0)
df_reforme['occupe_both'] = (1 * (df_reforme['situapr'] < 4)) * (1 * (df_reforme['situacj'] < 4))
for i in range(0, 5):
    df_reforme['strate_{}'.format(i)] = 0
    df_reforme.loc[df_reforme['strate'] == i, 'strate_{}'.format(i)] = 1

df_reforme['agepr_2'] = df_reforme['agepr'] ** 2

df_reforme['proprietaire'] = 0
df_reforme.loc[df_reforme.stalog.isin([1, 2]), 'proprietaire'] = 1

df_reforme['etudiant'] = 0
df_reforme.loc[df_reforme.situapr == 3, 'etudiant'] = 1

df_reforme['distance_routiere_hebdomadaire_teg'] = (
    df_reforme['distance_routiere_hebdomadaire_teg'] * (df_reforme['distance'] > 0)
    )
df_reforme['part_distance_teg'] = \
    df_reforme['distance_routiere_hebdomadaire_teg'] / df_reforme['distance']
df_reforme['part_distance_teg'] = df_reforme['part_distance_teg'].fillna(0) * 47

df_reforme['diesel'] = 0 + 1 * (df_reforme['depenses_diesel_corrigees'] > 0)
df_reforme['carburants'] = 0 + 1 * (df_reforme['depenses_carburants_corrigees'] > 0)# * (df_reforme['depenses_diesel_corrigees'] == 0)

df_reforme.rename(
    columns = {
        'cout_reforme_avant_compensation_reformes_cae_sans_rattrapage' : 'Cost_reform_before_compensation_without_catchup_diesel',
        'cout_reforme_avant_compensation_reformes_cae' : 'Cost_reform_before_compensation',
        'transfert_net_apres_compensation_uc' : 'Net_transfers_by_cu_after_recycling',
        'rev_disp_loyerimput' : 'Disposable_income',
        'rev_disp_loyerimput_2' : 'Disposable_income_squared',
        'combustibles_liquides' : 'Domestic_fuel',
        'diesel' : 'Diesel',
        'carburants' : 'Transport_fuels',
        'gaz_ville' : 'Natural_gas',
        'strate_0' : 'Rural',
        'strate_1' : 'Small_cities',
        'strate_3' : 'Large_cities',
        'strate_4' : 'Paris',
        'ouest_sud' : 'Ouest_south',
        'surfhab_d' : 'Living_area_m2',
        'aides_logement' : 'Housing_benefits',
        'etudiant': 'Student',
        'agepr' : 'Age_representative',
        'agepr_2' : 'Age_representative_squared',
        'nactifs' : 'Number_in_labor_force',
        'age_vehicule' : 'Vehicule_age',
        'part_distance_teg' : 'Share_distance_to_work',
        'ocde10' : 'Consumption_units',
        'bat_av_49' : 'Building_before_1949',
        'bat_49_74' : 'Building_1949_74',
        'log_indiv' : 'Individual_housing',
        'proprietaire' : 'Owner'
        },
    inplace = True)


regression_ols_urbanity = smf.ols(formula = 'Cost_reform_before_compensation ~ \
    Disposable_income + Disposable_income_squared + \
    Rural + Small_cities + Large_cities + Paris',
    data = df_reforme).fit()

regression_ols_urbanity_sans_rattrapage = smf.ols(formula = 'Cost_reform_before_compensation_without_catchup_diesel ~ \
    Disposable_income + Disposable_income_squared + \
    Rural + Small_cities + Large_cities + Paris',
    data = df_reforme).fit()

regression_ols_energy = smf.ols(formula = 'Cost_reform_before_compensation ~ \
    Disposable_income + Disposable_income_squared + \
    Domestic_fuel + Natural_gas + Diesel + Transport_fuels',
    data = df_reforme).fit()

regression_ols_energy_sans_rattrapage = smf.ols(formula = 'Cost_reform_before_compensation_without_catchup_diesel ~ \
    Disposable_income + Disposable_income_squared + \
    Domestic_fuel + Natural_gas + Diesel + Transport_fuels',
    data = df_reforme).fit()

regression_ols_all_included = smf.ols(formula = 'Cost_reform_before_compensation ~ \
    Disposable_income + Disposable_income_squared + \
    Domestic_fuel + Natural_gas + Diesel + Transport_fuels + \
    Rural + Small_cities + Large_cities + Paris + Ouest_south + \
    Building_before_1949 + Building_1949_74 + Individual_housing + Owner + \
    Living_area_m2 + \
    Consumption_units + Number_in_labor_force + Student + Age_representative + Age_representative_squared + \
    Share_distance_to_work + Vehicule_age',
    data = df_reforme).fit()


regression_ols_all_included_sans_rattrapage = smf.ols(formula = 'Cost_reform_before_compensation_without_catchup_diesel ~ \
    Disposable_income + Disposable_income_squared + \
    Domestic_fuel + Natural_gas + Diesel + Transport_fuels + \
    Rural + Small_cities + Large_cities + Paris + Ouest_south + \
    Building_before_1949 + Building_1949_74 + Individual_housing + Owner + \
    Living_area_m2 + \
    Consumption_units + Number_in_labor_force + Student + Age_representative + Age_representative_squared + \
    Share_distance_to_work + Vehicule_age',
    data = df_reforme).fit()


print regression_ols_urbanity.summary()
#print regression_ols_energy_sans_rattrapage.summary()
print regression_ols_all_included_sans_rattrapage.summary()

params = regression_ols_energy.params
params = params.to_frame().T
print params.Disposable_income * 1e03

bse = regression_ols_urbanity.bse
bse = bse.to_frame().T
#print bse.Disposable_income * 1e05
