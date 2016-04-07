#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


import logging
# import numpy
# import pandas


from openfisca_survey_manager.temporary import temporary_store_decorator
from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection


# from openfisca_france_indirect_taxation.utils import get_transfert_data_frames


log = logging.getLogger(__name__)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def build_depenses_homogenisees(temporary_store = None, year = None):
    """Build menage consumption by categorie fiscale dataframe """
    assert temporary_store is not None
    assert year is not None

    year = 2011
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory
        )
    survey = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year))

    # Homogénéisation des bases de données de dépenses
    if year == 1995:
        socioscm = survey.get_values(table = "socioscm")
        poids = socioscm[['mena', 'ponderrd', 'exdep', 'exrev']]
        # cette étape de ne garder que les données dont on est sûr de la qualité et de la véracité
        # exdep = 1 si les données sont bien remplies pour les dépenses du ménage
        # exrev = 1 si les données sont bien remplies pour les revenus du ménage
        poids = poids[(poids.exdep == 1) & (poids.exrev == 1)]
        del poids['exdep'], poids['exrev']
        poids.rename(
            columns = {
                'mena': 'ident_men',
                'ponderrd': 'pondmen',
                },
            inplace = True
            )
        poids.set_index('ident_men', inplace = True)

        conso = survey.get_values(table = "depnom")
        conso = conso[["valeur", "montant", "mena", "nomen5"]]
        conso = conso.groupby(["mena", "nomen5"]).sum()
        conso = conso.reset_index()
        conso.rename(
            columns = {
                'mena': 'ident_men',
                'nomen5': 'poste{}'.format(year),
                'valeur': 'depense',
                'montant': 'depense_avt_imput',
                },
            inplace = True
            )

        # Passage à l'euro
        conso.depense = conso.depense / 6.55957
        conso.depense_avt_imput = conso.depense_avt_imput / 6.55957
        conso_small = conso[[u'ident_men', u'poste1995', u'depense']]

        conso_unstacked = conso_small.set_index(['ident_men', 'poste1995']).unstack('poste1995')
        conso_unstacked = conso_unstacked.fillna(0)

        levels = conso_unstacked.columns.levels[1]
        labels = conso_unstacked.columns.labels[1]
        conso_unstacked.columns = levels[labels]
        conso_unstacked.rename(index = {0: 'ident_men'}, inplace = True)
        conso = conso_unstacked.merge(poids, left_index = True, right_index = True)
        conso = conso.reset_index()

    if year == 2000:
        conso = survey.get_values(table = "consomen")
        conso.rename(
            columns = {
                'ident': 'ident_men',
                'pondmen': 'pondmen',
                },
            inplace = True,
            )
        for variable in ['ctotale', 'c99', 'c99999'] + \
                        ["c0{}".format(i) for i in range(1, 10)] + \
                        ["c{}".format(i) for i in range(10, 14)]:
            del conso[variable]

    if year == 2005:
        conso = survey.get_values(table = "c05d")

    if year == 2011:
        try:
            conso = survey.get_values(table = "C05")
        except:
            conso = survey.get_values(table = "c05")
        conso.rename(
            columns = {
                'ident_me': 'ident_men',
                },
            inplace = True,
            )
        del conso['ctot']

    # Grouping by coicop

    poids = conso[['ident_men', 'pondmen']].copy()
    poids.set_index('ident_men', inplace = True)
    conso.drop('pondmen', axis = 1, inplace = True)
    conso.set_index('ident_men', inplace = True)

    from openfisca_france_indirect_taxation.scripts.build_coicop_bdf import bdf
    coicop_poste_bdf = bdf(year = year)[['code_bdf', 'code_coicop']].copy()

    assert not set(conso.columns).difference(set(coicop_poste_bdf.code_bdf))
    assert not set(coicop_poste_bdf.code_bdf.dropna()).difference(set(conso.columns))

    coicop_poste_bdf['formatted_poste'] = u'poste_' + coicop_poste_bdf.code_coicop.str.replace('.', u'_')
    coicop_by_poste_bdf = coicop_poste_bdf.dropna().set_index('code_bdf').to_dict()['code_coicop']
    assert not set(coicop_by_poste_bdf.keys()).difference(set(conso.columns))
    assert not set(set(conso.columns)).difference(coicop_by_poste_bdf.keys())
    formatted_poste_by_poste_bdf = coicop_poste_bdf.dropna().set_index('code_bdf').to_dict()['formatted_poste']
    coicop_data_frame = conso.rename(columns = formatted_poste_by_poste_bdf)
    depenses = coicop_data_frame.merge(poids, left_index = True, right_index = True)

#    # Création de gros postes, les 12 postes sur lesquels le calage se fera
#    def select_gros_postes(coicop):    
#        try:
#            coicop = unicode(coicop)
#        except:
#            coicop = coicop
#        normalized_coicop = normalize_code_coicop(coicop)
#        grosposte = normalized_coicop[0:2]
#        return int(grosposte)
#
#    grospostes = [
#        select_gros_postes(coicop)
#        for coicop in coicop_data_frame.columns
#        ]
#    tuples_gros_poste = zip(coicop_data_frame.columns, grospostes)
#    coicop_data_frame.columns = pandas.MultiIndex.from_tuples(tuples_gros_poste, names=['coicop', 'grosposte'])
#
#    depenses_by_grosposte = coicop_data_frame.groupby(level = 1, axis = 1).sum()
#    depenses_by_grosposte = depenses_by_grosposte.merge(poids, left_index = True, right_index = True)
#
#    # TODO : understand why it does not work: depenses.rename(columns = {u'0421': 'poste_421'}, inplace = True)
#
#    produits = [column for column in depenses.columns if column.isdigit()]
#    for code in produits:
#        if code[-1:] == '0':
#            depenses.rename(columns = {code: code[:-1]}, inplace = True)
#        else:
#            depenses.rename(columns = {code: code}, inplace = True)
#    produits = [column for column in depenses.columns if column.isdigit()]
#    for code in produits:
#        if code[0:1] == '0':
#            depenses.rename(columns = {code: code[1:]}, inplace = True)
#        else:
#            depenses.rename(columns = {code: code}, inplace = True)
#    produits = [column for column in depenses.columns if column.isdigit()]
#    for code in produits:
#        depenses.rename(columns = {code: 'poste_' + code}, inplace = True)

    temporary_store['depenses_{}'.format(year)] = depenses

#    depenses_by_grosposte.columns = depenses_by_grosposte.columns.astype(str)
#    liste_grospostes = [column for column in depenses_by_grosposte.columns if column.isdigit()]
#    for grosposte in liste_grospostes:
#        depenses_by_grosposte.rename(columns = {grosposte: 'coicop12_' + grosposte}, inplace = True)
#
#    temporary_store['depenses_by_grosposte_{}'.format(year)] = depenses_by_grosposte

#def normalize_code_coicop(code):
#    '''Normalize_coicop est function d'harmonisation de la colonne d'entiers posteCOICOP de la table
#matrice_passage_data_frame en la transformant en une chaine de 5 caractères afin de pouvoir par la suite agréger les postes
#COICOP selon les 12 postes agrégés de la nomenclature de la comptabilité nationale. Chaque poste contient 5 caractères,
#les deux premiers (entre 01 et 12) correspondent à ces postes agrégés de la CN.
#
#    '''
#    # TODO: vérifier la formule !!!
#
#    try:
#        code = unicode(code)
#    except:
#        code = code
#    if len(code) == 3:
#        code_coicop = "0" + code + "0"  # "{0}{1}{0}".format(0, code)
#    elif len(code) == 4:
#        if not code.startswith("0") and not code.startswith("1") and not code.startswith("45") and not code.startswith("9"):
#            code_coicop = "0" + code
#            # 022.. = cigarettes et tabacs => on les range avec l'alcool (021.0)
#        elif code.startswith("0"):
#            code_coicop = code + "0"
#        elif code in ["1151", "1181", "4552", "4522", "4511", "9122", "9151", "9211", "9341", "1411"]:
#            # 1151 = Margarines et autres graisses végétales
#            # 1181 = Confiserie
#            # 04522 = Achat de butane, propane
#            # 04511 = Facture EDF GDF non dissociables
#            code_coicop = "0" + code
#        else:
#            # 99 = loyer, impots et taxes, cadeaux...
#            code_coicop = code + "0"
#    elif len(code) == 5:
#        if not code.startswith("13") and not code.startswith("44") and not code.startswith("51"):
#            code_coicop = code
#        else:
#            code_coicop = "99000"
#    else:
#        log.error("Problematic code {}".format(code))
#        raise()
#    return code_coicop


if __name__ == '__main__':
    import sys
    import time
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    deb = time.clock()
    year = 2011
    build_depenses_homogenisees(year = year)
    log.info("duration is {}".format(time.clock() - deb))
