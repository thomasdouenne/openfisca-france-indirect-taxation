# -*- coding: utf-8 -*-

# In this script we take the estimates obtained in the estimation with ENL,
# and we compute the probabilities of being cold for BdF households.
# We then replicate this with adjusted expenditures and do the difference.

# Import general modules
from __future__ import division

import statsmodels.formula.api as smf
import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


def estimate_froid():
    
    stock_variables = [
        'agepr',
        'aides_logement',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'dip14pr',
        'electricite',
        'gaz_ville',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'majorite_double_vitrage',
        'nactifs',
        'nenfants',
        'npers',
        'ocde10',
        'ouest_sud',
        'paris',
        'petite_ville',
        'rural',
        'surfhab_d',
        'typmen',
        ]

    simulated_variables = stock_variables + ['quantites_combustibles_liquides', 'quantites_electricite_selon_compteur',
        'quantites_gaz_final', 'niveau_vie_decile',
        'froid_4_criteres_3_deciles', 'revtot']

    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    year = 2014
    data_year = 2011
    elasticities = get_elasticities(data_year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )
    
    dataframe = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    dataframe = dataframe.query('niveau_vie_decile < 4')
    
    dataframe['froid_4_criteres_3_deciles'] = \
        dataframe['froid_4_criteres_3_deciles'].astype(int)
    dataframe = dataframe.query('revtot > 0')
    dataframe['monoparental'] = 0
    dataframe.loc[dataframe['typmen'] == 2, 'monoparental'] = 1
    
    
    #dataframe['part_energies_revtot'] = dataframe['depenses_energies_logement'] / dataframe['revtot']
    
    # OLS regression
    new_stock_variables = list(stock_variables)
    max_rsquared_adj = 0.000001
    current_max_rsquared_adj = 0
    variable_to_include = None
    variables_kept = []
    while max_rsquared_adj > current_max_rsquared_adj:
        current_max_rsquared_adj = max_rsquared_adj
        if variable_to_include is not None:
            new_stock_variables.remove(variable_to_include)
            variables_kept = variables_kept + [variable_to_include]
        for variable in new_stock_variables:
            variables = variables_kept + [variable]
    
            regressors = ' ' 
            for element in variables:
                if regressors == ' ':
                    regressors = element
                else:
                    regressors = regressors + ' + {}'.format(element)

            regression_ols = smf.ols(formula = 'froid_4_criteres_3_deciles ~ revtot + \
                quantites_combustibles_liquides + quantites_electricite_selon_compteur + quantites_gaz_final + {}'.format(regressors),
                data = dataframe).fit()
            rsquared_adj = regression_ols.rsquared_adj
            max_rsquared_adj = max(max_rsquared_adj, rsquared_adj)
            if rsquared_adj == max_rsquared_adj:
                variable_to_include = variable
            else:
                continue

    # Logisctic regression    
    regressors = [
        'revtot',
        'quantites_combustibles_liquides',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final',
        'isolation_murs',
        'isolation_fenetres',
        'isolation_toit',
        'majorite_double_vitrage',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'ouest_sud',
        'rural',
        'paris',
        'surfhab_d',
        'aides_logement',
        'electricite',
        'agepr',
        'npers',
        'monoparental',
        ]
    regression_logit = smf.Logit(dataframe['froid_4_criteres_3_deciles'], dataframe[regressors]).fit()
    
    return regression_ols, regression_logit


if __name__ == "__main__":
    estimations = estimate_froid()
    regression_ols = estimations[0]
    regression_logit = estimations[1]

    print regression_ols.summary()
    print regression_logit.summary()