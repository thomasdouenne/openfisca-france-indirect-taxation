# -*- coding: utf-8 -*-


import os
import pandas
import pkg_resources

from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_indirect_taxation.utils import get_parametres_fiscalite_data_frame


year = 2011
aliss_survey_collection = SurveyCollection.load(
    collection = 'aliss', config_files_directory = config_files_directory
    )
aliss_survey_collection
survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

df = survey.get_values(table = 'Base_ALISS_2011')


liste_produits_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    'liste_produits.xlsx'
    )

liste_produits = pandas.read_excel(liste_produits_path)
liste_produits.columns
sous_codes = liste_produits.sous_code.dropna().tolist()
postes = list()
for sous_code in sous_codes:
    postes.append(int(sous_code[0:4]))


taxe_by_categorie_fiscale_number = {
    1: 'tva_taux_super_reduit',
    2: 'tva_taux_reduit',
    3: 'tva_taux_plein',
    4: 'tva_taux_intermediaire',
    7: 'cigarettes',
    8: 'cigares',
    9: 'tabac_a_rouler',
    10: 'alcools_forts',
    11: 'tva_taux_plein',
    12: 'vin',
    13: 'biere',
    14: 'ticpe',
    15: 'assurance_transport',
    16: 'assurance_sante',
    17: 'autres_assurances'
    }

categories_fiscales_data_frame = get_parametres_fiscalite_data_frame()[
    ['posteCOICOP', 'annee', 'description', 'categoriefiscale']].copy()

categories_fiscales = categories_fiscales_data_frame.query('annee == @year')
produit_by_categorie_fiscale = categories_fiscales.loc[
    categories_fiscales.posteCOICOP.astype(str).str[:2].isin(['11', '21'])]

produit_by_taxe = produit_by_categorie_fiscale.replace({'categoriefiscale': taxe_by_categorie_fiscale_number})

# TODO check notamment problème avec sucre confiseries