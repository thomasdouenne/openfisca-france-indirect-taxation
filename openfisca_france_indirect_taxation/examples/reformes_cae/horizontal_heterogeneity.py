# -*- coding: utf-8 -*-

# This script computes the share of households that financial lose from the reform,
# after transfers. This share is given by category (in particular by income deciles).
# Losses are computed on the basis of total financial gains and losses : a person
# loses from the reform if the transfer is lower than the additional spending induced
# by the reform.


from __future__ import division

import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'revenu_reforme_reformes_cae',
    'revenu_reforme_reformes_cae_sans_rattrapage',
    'revenu_reforme_logement_reformes_cae',
    'revenu_reforme_transports_reformes_cae',
    'revenu_reforme_transports_reformes_cae_sans_rattrapage',
    'ocde10',
    'transferts_neutre_cinq_decile_reformes_cae',
    'transferts_geographiques_reformes_cae',
    'transferts_energie_reformes_cae',
    'transferts_neutre_reformes_cae',
    'transferts_neutre_reformes_cae_sans_rattrapage',
    'transferts_terra_nova_reformes_cae',
    'transferts_terra_nova_geographique_reformes_cae',
    'transferts_semi_propotionnel_reformes_cae',
    'transferts_propotionnel_reformes_cae',
    'cheques_energie_etendu_majore_reformes_cae',
    'transferts_lisses_huit_decile_reformes_cae',
    'transferts_geographiques_economies_reformes_cae',
    'transferts_geographiques_lisses_bis_reformes_cae',
    'transferts_geographiques_lisses_huit_decile_reformes_cae',
    'niveau_vie_decile',
    'pondmen',
    'strate',
    'rev_disp_loyerimput'
    ]


def distribution_net_transfers_by_group(df_reform, group):

    i_min = df_reforme[group].min()
    i_max = df_reforme[group].max()
    df_by_categ = pd.DataFrame(index = range(i_min, i_max+1),
        columns = ['quantile_10', 'quantile_25', 'quantile_50', 'quantile_75', 'quantile_90']
        )


    for i in range(i_min, i_max+1):
        df_by_categ['quantile_10'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transfert_net_apres_compensation_uc'].quantile(0.1)
        df_by_categ['quantile_25'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transfert_net_apres_compensation_uc'].quantile(0.25)
        df_by_categ['quantile_50'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transfert_net_apres_compensation_uc'].quantile(0.5)
        df_by_categ['quantile_75'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transfert_net_apres_compensation_uc'].quantile(0.75)
        df_by_categ['quantile_90'][i] = df_reforme.query('{} == {}'.format(group, i))[u'transfert_net_apres_compensation_uc'].quantile(0.9)


    graph_builder_bar(df_by_categ[[u'quantile_10'] + [u'quantile_25'] + ['quantile_50'] + ['quantile_75'] + ['quantile_90']], False)
    save_dataframe_to_graph(df_by_categ, 'Monetary/distribution_loosers_within_{}.csv'.format(group))
    
    return df_by_categ
    

if __name__ == '__main__':
    year = 2016
    data_year = 2011
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    #elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, True)
    
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'reformes_cae',
        year = year,
        data_year = data_year
        )

    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    df_reforme[u'transfert_net_apres_compensation_uc'] = (
        df_reforme['transferts_geographiques_economies_reformes_cae']
        - df_reforme['revenu_reforme_reformes_cae']
        ) / df_reforme['ocde10']


    df_to_plot = distribution_net_transfers_by_group(df_reforme, 'niveau_vie_decile')
    print df_to_plot

   
    assert(
            (df_reforme['revenu_reforme_reformes_cae'] * df_reforme['pondmen']).sum()
            >
            0.999 * (df_reforme['transferts_geographiques_reformes_cae'] * df_reforme['pondmen']).sum()
            )
    assert(
            0.999 * (df_reforme['revenu_reforme_reformes_cae'] * df_reforme['pondmen']).sum()
            <
            (df_reforme['transferts_geographiques_reformes_cae'] * df_reforme['pondmen']).sum()
            )

    print (df_reforme['revenu_reforme_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['revenu_reforme_reformes_cae_sans_rattrapage'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_neutre_cinq_decile_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_lisses_huit_decile_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_geographiques_lisses_bis_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_geographiques_economies_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_geographiques_lisses_huit_decile_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_geographiques_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_energie_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06    
    print (df_reforme['transferts_neutre_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_terra_nova_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_terra_nova_geographique_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_semi_propotionnel_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['transferts_propotionnel_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06
    print (df_reforme['cheques_energie_etendu_majore_reformes_cae'] * df_reforme['pondmen']).sum() / 1e06

    df_reforme['benef'] = 0 + 1 * (df_reforme['cheques_energie_etendu_majore_reformes_cae'] > 0)
    print (df_reforme['benef'] * df_reforme['pondmen']).sum()

    df_reforme['check'] = (
            df_reforme['revenu_reforme_logement_reformes_cae']
            + df_reforme['revenu_reforme_transports_reformes_cae_sans_rattrapage']
            - df_reforme['revenu_reforme_reformes_cae_sans_rattrapage']
            )

print df_reforme.query('strate == 0').query('niveau_vie_decile < 6')['transfert_net_apres_compensation_uc'].mean()
print df_reforme.query('strate == 1').query('niveau_vie_decile < 6')['transfert_net_apres_compensation_uc'].mean()
print df_reforme.query('strate == 2').query('niveau_vie_decile < 6')['transfert_net_apres_compensation_uc'].mean()
print df_reforme.query('strate == 3').query('niveau_vie_decile < 6')['transfert_net_apres_compensation_uc'].mean()
print df_reforme.query('strate == 4').query('niveau_vie_decile < 6')['transfert_net_apres_compensation_uc'].mean()

print float(len(df_reforme.query('strate == 0').query('niveau_vie_decile < 6').query('transfert_net_apres_compensation_uc < 0'))) / (len(df_reforme.query('strate == 0').query('niveau_vie_decile < 6'))) * 100
print float(len(df_reforme.query('strate == 1').query('niveau_vie_decile < 6').query('transfert_net_apres_compensation_uc < 0'))) / (len(df_reforme.query('strate == 1').query('niveau_vie_decile < 6'))) * 100
print float(len(df_reforme.query('strate == 2').query('niveau_vie_decile < 6').query('transfert_net_apres_compensation_uc < 0'))) / (len(df_reforme.query('strate == 2').query('niveau_vie_decile < 6'))) * 100
print float(len(df_reforme.query('strate == 3').query('niveau_vie_decile < 6').query('transfert_net_apres_compensation_uc < 0'))) / (len(df_reforme.query('strate == 3').query('niveau_vie_decile < 6'))) * 100
print float(len(df_reforme.query('strate == 4').query('niveau_vie_decile < 6').query('transfert_net_apres_compensation_uc < 0'))) / (len(df_reforme.query('strate == 4').query('niveau_vie_decile < 6'))) * 100
