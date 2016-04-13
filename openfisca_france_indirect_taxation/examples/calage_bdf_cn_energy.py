# -*- coding: utf-8 -*-

from __future__ import division

import os
import pkg_resources
import csv

import pandas
from pandas import concat

from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.build_survey_data.utils import find_nearest_inferior


data_years = [2000, 2005, 2011]


def get_bdf_aggregates_energy(data_year = None):
    assert data_year is not None

    depenses = get_input_data_frame(data_year)
    depenses['somme_coicop12'] = 0
    for i in range(1, 13):
        depenses['somme_coicop12'] += depenses['coicop12_{}'.format(i)]
    depenses_energie = pandas.DataFrame()
    variables_energie = ['poste_coicop_451', 'poste_coicop_452', 'poste_coicop_453', 'poste_coicop_454',
        'poste_coicop_722', 'rev_disponible', 'loyer_impute', 'rev_disp_loyerimput', 'somme_coicop12']
    for energie in variables_energie:
        if depenses_energie is None:
            depenses_energie = depenses['{}'.format(energie)]
        else:
            depenses_energie = concat([depenses_energie, depenses['{}'.format(energie)]], axis = 1)

    depenses_energie = concat([depenses_energie, depenses['pondmen']], axis = 1)
    bdf_aggregates_by_energie = pandas.DataFrame()
    for energie in variables_energie:
        bdf_aggregates_by_energie.loc[energie, 'bdf_aggregates'] = (
            depenses_energie[energie] * depenses_energie['pondmen']
            ).sum()

    return bdf_aggregates_by_energie


def get_cn_aggregates_energy(target_year = None):
    assert target_year is not None
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        'Parametres fiscalite indirecte.xls'
        )

    masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', target_year]].copy()

    masses_cn_data_frame['poste'] = 0
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.1', 'poste'] = 'poste_coicop_451'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.2', 'poste'] = 'poste_coicop_452'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.3', 'poste'] = 'poste_coicop_453'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.4', 'poste'] = 'poste_coicop_454'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            07.2.2', 'poste'] = 'poste_coicop_722'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == u'01..12+15 (HS)', 'poste'] = \
        'somme_coicop12'
    masses_cn_energie = masses_cn_data_frame.query('poste != 0')
    del masses_cn_energie['Code']

    masses_cn_energie.rename(
        columns = {
            target_year: 'conso_CN_{}'.format(target_year),
            },
        inplace = True,
        )

    masses_cn_energie.set_index('poste', inplace = True)
    masses_cn_energie = masses_cn_energie * 1e6

    masses_cn_revenus_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "revenus_CN")
    masses_cn_revenus_data_frame.rename(
        columns = {
            'annee': 'year',
            'Revenu disponible brut': 'rev_disponible',
            'Loyers imputes': 'loyer_impute'
            },
        inplace = True
        )
    masses_cn_revenus_data_frame = masses_cn_revenus_data_frame[masses_cn_revenus_data_frame.year == target_year]
    revenus_cn = masses_cn_revenus_data_frame[['loyer_impute'] + ['rev_disponible']].copy()
    # On redéfinie le revenu disponible de la compta nat en enlevant le loyer imputé pour faire concorder la définition
    # avec BdF.
    revenus_cn['rev_disp_loyerimput'] = revenus_cn['rev_disponible'].copy()
    revenus_cn['rev_disponible'] = revenus_cn['rev_disponible'] - revenus_cn['loyer_impute']
    revenus_cn = pandas.melt(revenus_cn)
    revenus_cn = revenus_cn.set_index('variable')
    revenus_cn.rename(columns = {'value': 'conso_CN_{}'.format(target_year)}, inplace = True)
    revenus_cn = revenus_cn * 1e9

    masses_cn = pandas.concat([masses_cn_energie, revenus_cn])

    return masses_cn


def get_inflators_bdf_to_cn_energy(data_year):
    '''
    Calcule les ratios de calage (bdf sur cn pour année de données)
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_cn = get_cn_aggregates_energy(data_year)
    data_bdf = get_bdf_aggregates_energy(data_year)
    masses = data_cn.merge(
        data_bdf, left_index = True, right_index = True
        )
    masses.rename(columns = {'bdf_aggregates': 'conso_BDF_{}'.format(data_year)}, inplace = True)
    return (
        masses['conso_CN_{}'.format(data_year)] / masses['conso_BDF_{}'.format(data_year)]
        ).to_dict()


def get_inflators_cn_to_cn_energy(target_year):
    '''
        Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    data_year_cn_aggregates = get_cn_aggregates_energy(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates_energy(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    return dict(
        (key, target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        for key in data_year_cn_aggregates.keys()
        )


def get_inflators_energy(target_year):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    inflators_bdf_to_cn = get_inflators_bdf_to_cn_energy(data_year)
    inflators_cn_to_cn = get_inflators_cn_to_cn_energy(target_year)

    ratio_by_variable = dict()
    for key in inflators_cn_to_cn.keys():
        ratio_by_variable[key] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]

    return ratio_by_variable


def get_inflators_by_year_energy(rebuild = False):
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in range(2000, 2015):
            inflators = get_inflators_energy(target_year)
            inflators_by_year[target_year] = inflators

        writer_inflators = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation',
            'assets', 'inflateurs', 'inflators_by_year_wip.csv'), 'wb'))
        for year in range(2000, 2015):
            for key, value in inflators_by_year[year].items():
                writer_inflators.writerow([key, value, year])

        return inflators_by_year

    else:
        re_build_inflators = dict()
        inflators_from_csv = pandas.DataFrame.from_csv(os.path.join(assets_directory,
            'openfisca_france_indirect_taxation', 'assets', 'inflateurs', 'inflators_by_year_wip.csv'),
            header = -1)
        for year in range(2000, 2015):
            inflators_from_csv_by_year = inflators_from_csv[inflators_from_csv[2] == year]
            inflators_to_dict = pandas.DataFrame.to_dict(inflators_from_csv_by_year)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators