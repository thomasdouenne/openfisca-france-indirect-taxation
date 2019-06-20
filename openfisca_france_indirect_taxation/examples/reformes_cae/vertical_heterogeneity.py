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

simulated_variables = [
    'revenu_reforme_reformes_cae',
    'revenu_reforme_reformes_cae_sans_rattrapage',
    'revenu_reforme_logement_reformes_cae',
    'revenu_reforme_transports_reformes_cae',
    'revenu_reforme_transports_reformes_cae_sans_rattrapage',
    'ocde10',
    'transferts_neutre_cinq_decile_reformes_cae',
    'transferts_lisses_huit_decile_reformes_cae',
    'transferts_geographiques_lisses_huit_decile_reformes_cae',
    'transferts_geographiques_reformes_cae',
    'transferts_energie_reformes_cae',
    'transferts_neutre_reformes_cae',
    'transferts_neutre_reformes_cae_sans_rattrapage',
    'transferts_terra_nova_reformes_cae',
    'transferts_terra_nova_geographique_reformes_cae',
    'transferts_semi_propotionnel_reformes_cae',
    'cheques_energie_etendu_majore_reformes_cae',
    'pondmen',
    'strate',
    'rev_disp_loyerimput',
    'depenses_tot',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reformes_cae',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
df = dataframe_by_group(survey_scenario, 'niveau_vie_decile', simulated_variables)

def plot_vertical_heterogeneity(compensation):
    
    if compensation == 'aucune_compensation_sans_rattrapage':
        df['regressivite_revenu_transports_{}'.format(compensation)] = df['revenu_reforme_transports_reformes_cae_sans_rattrapage'] / df['rev_disp_loyerimput']
        df['regressivite_revenu_logement_{}'.format(compensation)] = df['revenu_reforme_logement_reformes_cae'] / df['rev_disp_loyerimput']
        df['regressivite_revenu_{}'.format(compensation)] = df['revenu_reforme_reformes_cae_sans_rattrapage'] / df['rev_disp_loyerimput']
        df['regressivite_depenses_transports_{}'.format(compensation)] = df['revenu_reforme_transports_reformes_cae_sans_rattrapage'] / df['depenses_tot']
        df['regressivite_depenses_logement_{}'.format(compensation)] = df['revenu_reforme_logement_reformes_cae'] / df['depenses_tot']
        df['regressivite_depenses_{}'.format(compensation)] = df['revenu_reforme_reformes_cae_sans_rattrapage'] / df['depenses_tot']

    elif compensation == 'aucune_compensation_avec_rattrapage':
        df['regressivite_revenu_transports_{}'.format(compensation)] = df['revenu_reforme_transports_reformes_cae'] / df['rev_disp_loyerimput']
        df['regressivite_revenu_logement_{}'.format(compensation)] = df['revenu_reforme_logement_reformes_cae'] / df['rev_disp_loyerimput']
        df['regressivite_revenu_{}'.format(compensation)] = df['revenu_reforme_reformes_cae'] / df['rev_disp_loyerimput']
        df['regressivite_depenses_transports_{}'.format(compensation)] = df['revenu_reforme_transports_reformes_cae'] / df['depenses_tot']
        df['regressivite_depenses_logement_{}'.format(compensation)] = df['revenu_reforme_logement_reformes_cae'] / df['depenses_tot']
        df['regressivite_depenses_{}'.format(compensation)] = df['revenu_reforme_reformes_cae'] / df['depenses_tot']

    else:
        df['transferts_nets_uc_{}'.format(compensation)] = (
            df[compensation] - df['revenu_reforme_reformes_cae']
            ) / df['ocde10']

    if compensation[:6] == 'aucune':
        df_to_plot = df[
            ['regressivite_revenu_{}'.format(compensation)]
            + ['regressivite_revenu_logement_{}'.format(compensation)]
            + ['regressivite_revenu_transports_{}'.format(compensation)]
            + ['regressivite_depenses_{}'.format(compensation)]
            + ['regressivite_depenses_logement_{}'.format(compensation)]
            + ['regressivite_depenses_transports_{}'.format(compensation)]
            ]       
        graph_builder_bar(df_to_plot['regressivite_revenu_{}'.format(compensation)], False)
        graph_builder_bar(df_to_plot['regressivite_depenses_{}'.format(compensation)], False)
    
    else:
        df_to_plot = df[
            ['transferts_nets_uc_{}'.format(compensation)]
            ]       
        graph_builder_bar(df_to_plot['transferts_nets_uc_{}'.format(compensation)], False)

    return df_to_plot


if __name__ == "__main__":

    compensation = 'aucune_compensation_avec_rattrapage'
    df_to_plot = plot_vertical_heterogeneity(compensation)
