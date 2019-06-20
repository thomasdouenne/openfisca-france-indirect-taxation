# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


# Import general modules
from __future__ import division


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'depenses_diesel_corrigees',
    'depenses_essence_corrigees',
    'depenses_carburants_corrigees',
    'depenses_energies_logement',
    'depenses_tot',
    'strate',
    'rural',
    'petite_ville',
    'moyenne_ville',
    'grande_ville',
    'paris',
    'niveau_de_vie',
    'carburants',
    'diesel',
    'essence',
    'combustibles_liquides',
    'gaz_ville',
    'agepr',
    'isolation_murs',
    'isolation_fenetres',
    'majorite_double_vitrage',
    'nactifs',
    'nenfants',
    'ocde10',
    'rev_disp_loyerimput',
    'rev_disponible',
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

df = dataframe_by_group(survey_scenario, 'niveau_vie_decile', simulated_variables)
df['depenses_tot_uc'] = df['depenses_tot'] / df['ocde10']

df['part_depenses_carburants'] = df['depenses_carburants_corrigees'] / df['rev_disponible'] 
print df['part_depenses_carburants'].mean()

df['part_depenses_energies_logement'] = df['depenses_energies_logement'] / df['rev_disponible'] 
print df['part_depenses_energies_logement'].mean()

df['check'] = df['rural'] + df['petite_ville'] + df['moyenne_ville'] + df['grande_ville'] + df['paris']
print df['check']
