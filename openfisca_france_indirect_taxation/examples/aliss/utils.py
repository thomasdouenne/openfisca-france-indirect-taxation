# -*- coding: utf-8 -*-


from __future__ import division

import numpy as np
import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import get_adjusted_input_data_frame


def build_aggreggates(variables, by = 'niveau_vie_decile', survey_scenario = None, adjusted_survey_scenario = None):
    aggregates = dict()
    reference_aggregates = dict()
    adjusted_aggregates = dict()
    for variable in variables:
        aggregates[variable] = survey_scenario.compute_aggregate(variable) / 1e9
        reference_aggregates[variable] = (
            survey_scenario.compute_aggregate(variable, reference = True) / 1e9
            if np.isfinite(survey_scenario.compute_aggregate(variable, reference = True)) else 0
            )

        adjusted_aggregates[variable] = adjusted_survey_scenario.compute_aggregate(variable) / 1e9
    aggregates = pd.DataFrame({
        'reform': aggregates,
        'reference': reference_aggregates,
        'adjusted': adjusted_aggregates,
        })
    aggregates['reform - reference'] = aggregates.reform - aggregates.reference
    aggregates['adjusted - reform'] = aggregates.adjusted - aggregates.reform
    aggregates['adjusted - reference'] = aggregates.adjusted - aggregates.reference
    return aggregates


def build_pivot_table(variables, by = 'niveau_vie_decile', survey_scenario = None, adjusted_survey_scenario = None):
    pivot_table = pd.DataFrame()
    reference_pivot_table = pd.DataFrame()
    adjusted_pivot_table = pd.DataFrame()
    for variable in variables:
        pivot_table = pd.concat([
            pivot_table,
            survey_scenario.compute_pivot_table(values = [variable], columns = [by])
            ])
        reference_pivot_table = pd.concat([
            reference_pivot_table.fillna(0),
            survey_scenario.compute_pivot_table(values = [variable], columns = [by],
                                               reference = True)
            ])
        adjusted_pivot_table = pd.concat([
            adjusted_pivot_table,
            adjusted_survey_scenario.compute_pivot_table(values = [variable], columns = [by])
            ])
    pivot_table = pd.concat({
        'reform': pivot_table,
        'reference': reference_pivot_table,
        'adjusted': adjusted_pivot_table,
        'reform-reference': pivot_table - reference_pivot_table,
        'adjusted-reform': adjusted_pivot_table - pivot_table,
        'adjusted-reference': adjusted_pivot_table - reference_pivot_table,
        })
    return pivot_table.reset_index().rename(columns = {u'level_0': 'simulation', u'level_1': 'variable'})


def build_scenarios(data_year = 2011, reform_key = None, year = 2014):
    scenario_kwargs = dict(year = year, data_year = data_year, reform_key = reform_key)
    survey_scenario = SurveyScenario.create(**scenario_kwargs)
    #
    adjusted_scenario_kwargs = dict(scenario_kwargs)
    adjusted_scenario_kwargs.update(dict(
        data_year = None,
        input_data_frame = get_adjusted_input_data_frame(reform_key = reform_key[6:])
        ))
    adjusted_survey_scenario = SurveyScenario.create(**adjusted_scenario_kwargs)
    return survey_scenario, adjusted_survey_scenario


def run_reform(reform_key = None):
    survey_scenario, adjusted_survey_scenario = build_scenarios(reform_key = reform_key)
    alimentation_domicile_hors_alcool = [
        "depenses_ht_{}".format(key) for key in survey_scenario.tax_benefit_system.column_by_name.keys()
        if key.startswith(u'poste_01')
        ]
    alimentation_domicile = alimentation_domicile_hors_alcool + [
        'depenses_biere',
        'depenses_vin',
        'depenses_alcools_forts'
        ]
    depenses_ht_tvas = [
        "depenses_ht_{}".format(key) for key in survey_scenario.tax_benefit_system.column_by_name.keys()
        if key.startswith(u'tva_taux_')
        ]
    tvas = [
        key for key in survey_scenario.tax_benefit_system.column_by_name.keys()
        if key.startswith(u'tva_taux_')
        ] + ['tva_total']
    variables = alimentation_domicile + ['poste_agrege_01', 'poste_agrege_02', ] + depenses_ht_tvas + tvas
    aggregates = build_aggreggates(
        variables, survey_scenario = survey_scenario, adjusted_survey_scenario = adjusted_survey_scenario)
    pivot_table = build_pivot_table(
        variables, survey_scenario = survey_scenario, adjusted_survey_scenario = adjusted_survey_scenario)

    # Some tests
    assert (pd.DataFrame(
        aggregates.loc[aliment, 'reform'] - aggregates.loc[aliment, 'reform'] for aliment in alimentation_domicile
        ) == 0).all().all()

    assert aggregates.loc['poste_agrege_02', 'reform'] - aggregates.loc['poste_agrege_02', 'reference'] < 1e-7

    return aggregates, pivot_table