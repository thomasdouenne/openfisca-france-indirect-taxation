# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph


def distribution_net_transfers_by_group(df_reform, group):

    i_min = df_reforme[group].min()
    i_max = df_reforme[group].max()
    df_by_categ = pd.DataFrame(index = range(i_min, i_max+1),
        columns = ['quantile_10', 'quantile_25', 'quantile_50', 'quantile_75', 'quantile_90']
        )


    for i in range(i_min, i_max+1):
        df_by_categ['quantile_10'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transferts_nets_apres_redistribution_uc'].quantile(0.1)
        df_by_categ['quantile_25'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transferts_nets_apres_redistribution_uc'].quantile(0.25)
        df_by_categ['quantile_50'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transferts_nets_apres_redistribution_uc'].quantile(0.5)
        df_by_categ['quantile_75'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transferts_nets_apres_redistribution_uc'].quantile(0.75)
        df_by_categ['quantile_90'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transferts_nets_apres_redistribution_uc'].quantile(0.9)


    graph_builder_bar(df_by_categ[[u'quantile_10'] + [u'quantile_25'] + ['quantile_50'] + ['quantile_75'] + ['quantile_90']], False)


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
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'cheque_differencie_modestes_officielle_2018_in_2016',
    'revenu_taxes_officielle_2018_in_2016',
    'depenses_diesel_corrigees',
    'depenses_carburants_corrigees',
    'strate',
    'niveau_vie_decile',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'niveau_vie_decile',
    'ocde10',
    'rev_disp_loyerimput',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['transferts_nets_apres_redistribution_uc'] = (
    df_reforme['cheque_differencie_modestes_officielle_2018_in_2016'] -
    df_reforme['revenu_taxes_officielle_2018_in_2016']
    ) / df_reforme['ocde10']

assert (
    (df_reforme['cheque_differencie_modestes_officielle_2018_in_2016'] * df_reforme['pondmen']).sum()
    > 0.999 * (df_reforme['revenu_taxes_officielle_2018_in_2016'] * df_reforme['pondmen']).sum()
    )
assert (
    0.999 * (df_reforme['cheque_differencie_modestes_officielle_2018_in_2016'] * df_reforme['pondmen']).sum()
    < (df_reforme['revenu_taxes_officielle_2018_in_2016'] * df_reforme['pondmen']).sum()
    )

df_to_plot = distribution_net_transfers_by_group(df_reforme, 'niveau_vie_decile')

