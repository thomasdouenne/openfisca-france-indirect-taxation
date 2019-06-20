# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core.reforms import Reform, update_legislation
import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie




def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "reformes_cae",
        "children": {
            "diesel_2022_in_2018": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2016-01-01', 'value': 3*2.6 + 265*(0.0862 - 0.0446)}] # Les contenus carbone sont déduis de l'art. 265 du code des douanes
                },
            "diesel_2022_in_2018_sans_rattrapage": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2016-01-01', 'value': 265*(0.0862 - 0.0446)}]
                },
            "essence_2022_in_2018": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2016-01-01', 'value': 228*(0.0862 - 0.0446)}],
                },
            "combustibles_liquides_2022_in_2018": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du fioul domestique (en euros par litre)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2016-01-01', 'value': 2.65*(0.0862 - 0.0446)}],
                },
            "gaz_ville_2022_in_2018": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2016-01-01', 'value': 0.182*(0.0862 - 0.0446)}],
                },
            },
        }

    reference_legislation_json_copy['children']['reformes_cae'] = reform_legislation_subtree
    return reference_legislation_json_copy



class reformes_cae(Reform):
    key = 'reformes_cae',
    name = u"Réforme de la fiscalité des énergies de 2018 par rapport aux taux de 2016",


    class cheques_energie_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des chèques énergie tels que prévus par la loi"
    
        def formula(self, simulation, period):
            revenu_fiscal = simulation.calculate('revdecm', period) / 1.22
            ocde10 = simulation.calculate('ocde10', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10

            cheque = (
                0 +
                144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1) +
                190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2) +
                227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2)) +
                96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1) +
                126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2) +
                152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2)) +
                48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1) +
                63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2) +
                76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))              
                )

            return cheque


    class cheques_energie_philippe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des chèques énergie tels que prévus par la loi"
    
        def formula(self, simulation, period):
            revenu_fiscal = simulation.calculate('revdecm', period) / 1.22
            ocde10 = simulation.calculate('ocde10', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10

            cheque = (
                0 +
                (144 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 == 1) +
                (190 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2) +
                (227 + 50) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2)) +
                (96 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1) +
                (126 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2) +
                (152 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2)) +
                (48 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1) +
                (63 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2) +
                (76 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2)) +
                (48) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 == 1) +
                (63) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 > 1) * (ocde10 < 2) +
                (76) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * ((ocde10 == 2) + (ocde10 > 2))              
                )

            return cheque


    class cheques_energie_etendu_majore_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des chèques énergie tels que prévus par la loi"
    
        def formula(self, simulation, period):
            revenu_fiscal = simulation.calculate('revdecm', period) / 1.22
            ocde10 = simulation.calculate('ocde10', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10

            cheque = (
                0 +
                (144 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 == 1) +
                (190 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2) +
                (227 + 50) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2)) +
                (96 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1) +
                (126 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2) +
                (152 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2)) +
                (48 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1) +
                (63 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2) +
                (76 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2)) +
                (48) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 == 1) +
                (63) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 > 1) * (ocde10 < 2) +
                (76) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * ((ocde10 == 2) + (ocde10 > 2))              
                ) * 2

            return cheque


    class combustibles_liquides_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de TICPE sur le combustibles_liquides domestique après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
    
            accise_combustibles_liquides_ticpe = (
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.gazole_fioul_domestique_hectolitre / 100
                )
            reforme_combustibles_liquides = \
                simulation.legislation_at(period.start).reformes_cae.combustibles_liquides_2022_in_2018
            accise_combustibles_liquides_ajustee = accise_combustibles_liquides_ticpe + reforme_combustibles_liquides
            prix_fioul_ttc = \
                simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_combustibles_liquides
    
            taux_implicite_combustibles_liquides_ajuste = (
                (accise_combustibles_liquides_ajustee * (1 + taux_plein_tva)) /
                (prix_fioul_ttc_ajuste - accise_combustibles_liquides_ajustee * (1 + taux_plein_tva))
                )
    
            depenses_combustibles_liquides_ajustees = simulation.calculate('depenses_combustibles_liquides_reformes_cae', period)
            depenses_combustibles_liquides_htva = \
                depenses_combustibles_liquides_ajustees - tax_from_expense_including_tax(depenses_combustibles_liquides_ajustees, taux_plein_tva)
            montant_combustibles_liquides_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_combustibles_liquides_htva, taux_implicite_combustibles_liquides_ajuste)
    
            return montant_combustibles_liquides_ticpe_ajuste
    
    
    class depenses_carburants_corrigees_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Depenses en carburants après reaction à la reforme"

        def formula(self, simulation, period):
            depenses_diesel_ajustees = simulation.calculate('depenses_diesel_corrigees_reformes_cae', period)
            depenses_essence_ajustees = simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees

    
    class depenses_carburants_corrigees_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Depenses en carburants après reaction à la reforme"

        def formula(self, simulation, period):
            depenses_diesel_ajustees_sans_rattrapage = simulation.calculate('depenses_diesel_corrigees_reformes_cae_sans_rattrapage', period)
            depenses_essence_ajustees = simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            depenses_carburants_ajustees_sans_rattrapage = depenses_diesel_ajustees_sans_rattrapage + depenses_essence_ajustees

            return depenses_carburants_ajustees_sans_rattrapage

    
    class depenses_combustibles_liquides_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en combustibles_liquides après réaction à la réforme"
    
        def formula(self, simulation, period):
            depenses_combustibles_liquides = simulation.calculate('depenses_combustibles_liquides', period)
            prix_fioul_ttc = \
                simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                simulation.legislation_at(period.start).reformes_cae.combustibles_liquides_2022_in_2018
            combustibles_liquides_elasticite_prix = simulation.calculate('elas_price_2_2', period)
            depenses_combustibles_liquides_reformes_cae = \
                depenses_combustibles_liquides * (1 + (1 + combustibles_liquides_elasticite_prix) * reforme_combustibles_liquides / prix_fioul_ttc)
    
            return depenses_combustibles_liquides_reformes_cae


    class depenses_diesel_corrigees_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en diesel après réaction à la réforme"
    
        def formula(self, simulation, period):
            depenses_diesel = simulation.calculate('depenses_diesel_corrigees', period)
            diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1', period)
            depenses_diesel_reformes_cae = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)
    
            return depenses_diesel_reformes_cae
    

    class depenses_diesel_corrigees_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en diesel après réaction à la réforme"
    
        def formula(self, simulation, period):
            depenses_diesel = simulation.calculate('depenses_diesel_corrigees', period)
            diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel_sans_rattrapage = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018_sans_rattrapage
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1', period)
            depenses_diesel_reformes_cae_sans_rattrapage = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel_sans_rattrapage / diesel_ttc)
    
            return depenses_diesel_reformes_cae_sans_rattrapage
    

    class depenses_energies_logement_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en énergies dans le logement après la réforme"
    
        def formula(self, simulation, period):
            depenses_electricite = simulation.calculate('depenses_electricite', period)
            depenses_gaz_ville_ajustees = simulation.calculate('depenses_gaz_ville_reformes_cae', period)
            depenses_gaz_liquefie = simulation.calculate('depenses_gaz_liquefie', period)
            depenses_combustibles_liquides_ajustees = simulation.calculate('depenses_combustibles_liquides_reformes_cae', period)
            depenses_combustibles_solides = simulation.calculate('depenses_combustibles_solides', period)
            depenses_energie_thermique = simulation.calculate('depenses_energie_thermique', period)
            depenses_energies_logement_reformes_cae = (
                depenses_electricite + depenses_gaz_ville_ajustees + depenses_gaz_liquefie +
                depenses_combustibles_liquides_ajustees + depenses_combustibles_solides + depenses_energie_thermique
                )
    
            return depenses_energies_logement_reformes_cae

    
    class depenses_essence_corrigees_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en essence après réaction à la réforme"
    
        def formula(self, simulation, period):
            depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
            super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1', period)
            depenses_essence_reformes_cae = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)
    
            return depenses_essence_reformes_cae
    
    
    class depenses_gaz_ville_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en gaz après réaction à la réforme"
    
        def formula(self, simulation, period):
            depenses_gaz_variables = simulation.calculate('depenses_gaz_variables', period)
            
            depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                simulation.legislation_at(period.start).reformes_cae.gaz_ville_2022_in_2018
            gaz_elasticite_prix = simulation.calculate('elas_price_2_2', period)
            depenses_gaz_variables = \
                depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
            depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees = depenses_gaz_variables + depenses_gaz_tarif_fixe
            depenses_gaz_ajustees = numpy.array(depenses_gaz_ajustees, dtype = float)
            depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
            depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0
    
            return depenses_gaz_ajustees


    class diesel_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de TICPE sur le diesel après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
    
            try:
                majoration_ticpe_diesel = \
                    simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
                accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
                accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
            except:
                accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
    
            reforme_diesel = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )
    
            depenses_diesel_reformes_cae = \
                simulation.calculate('depenses_diesel_corrigees_reformes_cae', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_reformes_cae -
                tax_from_expense_including_tax(depenses_diesel_reformes_cae, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )
    
            return montant_diesel_ticpe_ajuste

    
    class diesel_ticpe_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de TICPE sur le diesel après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

            try:
                majoration_ticpe_diesel = \
                    simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
                accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
                accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
            except:
                accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

            reforme_diesel_sans_rattrapage = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018_sans_rattrapage
            accise_diesel_ticpe_ajustee_sans_rattrapage = accise_diesel_ticpe + reforme_diesel_sans_rattrapage
            prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel_sans_rattrapage
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee_sans_rattrapage * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee_sans_rattrapage * (1 + taux_plein_tva))
                )

            depenses_diesel_reformes_cae_sans_rattrapage = \
                simulation.calculate('depenses_diesel_corrigees_reformes_cae_sans_rattrapage', period)
            depenses_diesel_htva_ajustees_sans_rattrapage = (
                depenses_diesel_reformes_cae_sans_rattrapage -
                tax_from_expense_including_tax(depenses_diesel_reformes_cae_sans_rattrapage, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste_sans_rattrapage = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees_sans_rattrapage, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste_sans_rattrapage

    
    class essence_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
    
        def formula_2009(self, simulation, period):    
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_reformes_cae', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_reformes_cae', period)
            sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_reformes_cae', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee
    
        def formula_2007(self, simulation, period):    
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_reformes_cae', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_reformes_cae', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee
    
        def formula_1990(self, simulation, period):    
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_reformes_cae', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_reformes_cae', period)
            super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_reformes_cae', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee


    class gains_tva_carburants_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes en TVA sur les carburants de la réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            depenses_carburants_corrigees_reformes_cae = \
                simulation.calculate('depenses_carburants_corrigees_reformes_cae', period)
            tva_depenses_carburants_corrigees_reformes_cae = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_carburants_corrigees_reformes_cae
                )
            depenses_carburants_corrigees = \
                simulation.calculate('depenses_carburants_corrigees', period)
            tva_depenses_carburants_corrigees = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_carburants_corrigees
                )
            gains_tva_carburants = (
                tva_depenses_carburants_corrigees_reformes_cae -
                tva_depenses_carburants_corrigees
                )
            return gains_tva_carburants
            
            
    class gains_tva_carburants_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes en TVA sur les carburants de la réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            depenses_carburants_corrigees_reformes_cae_sans_rattrapage = \
                simulation.calculate('depenses_carburants_corrigees_reformes_cae_sans_rattrapage', period)
            tva_depenses_carburants_corrigees_reformes_cae_sans_rattrapage = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_carburants_corrigees_reformes_cae_sans_rattrapage
                )
            depenses_carburants_corrigees = \
                simulation.calculate('depenses_carburants_corrigees', period)
            tva_depenses_carburants_corrigees = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_carburants_corrigees
                )
            gains_tva_carburants_sans_rattrapage = (
                tva_depenses_carburants_corrigees_reformes_cae_sans_rattrapage -
                tva_depenses_carburants_corrigees
                )
            return gains_tva_carburants_sans_rattrapage
            
            
    class gains_tva_combustibles_liquides_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes de la réforme en TVA sur les combustibles liquides"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            depenses_combustibles_liquides_reformes_cae = \
                simulation.calculate('depenses_combustibles_liquides_reformes_cae', period)
            tva_depenses_combustibles_liquides_reformes_cae = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_combustibles_liquides_reformes_cae
                )
            depenses_combustibles_liquides = \
                simulation.calculate('depenses_combustibles_liquides', period)
            tva_depenses_combustibles_liquides = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                depenses_combustibles_liquides
                )
            gains_tva_combustibles_liquides = (
                tva_depenses_combustibles_liquides_reformes_cae -
                tva_depenses_combustibles_liquides
                )
            return gains_tva_combustibles_liquides
            
            
    class gains_tva_gaz_ville_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes de la réforme en TVA sur le gaz naturel"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ville_reformes_cae = \
                simulation.calculate('depenses_gaz_ville_reformes_cae', period)
            tva_depenses_gaz_ville_reformes_cae = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                (depenses_gaz_ville_reformes_cae - depenses_gaz_tarif_fixe)
                )
            depenses_gaz_ville = \
                simulation.calculate('depenses_gaz_ville', period)
            tva_depenses_gaz_ville = (
                (taux_plein_tva / (1 + taux_plein_tva)) *
                (depenses_gaz_ville - depenses_gaz_tarif_fixe)
                )
            gains_tva_gaz_ville = (
                tva_depenses_gaz_ville_reformes_cae -
                tva_depenses_gaz_ville
                )
            return gains_tva_gaz_ville
            
            
    class gains_tva_total_energies_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes de la réforme en TVA sur toutes les énergies"
    
        def formula(self, simulation, period):
            gains_carburants = simulation.calculate('gains_tva_carburants_reformes_cae', period)
            gains_combustibles_liquides = simulation.calculate('gains_tva_combustibles_liquides_reformes_cae', period)
            gains_gaz_ville = simulation.calculate('gains_tva_gaz_ville_reformes_cae', period)

            somme_gains = gains_carburants + gains_combustibles_liquides + gains_gaz_ville
            return somme_gains


    class gains_tva_total_energies_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes de la réforme en TVA sur toutes les énergies"
    
        def formula(self, simulation, period):
            gains_carburants_sans_rattrapage = simulation.calculate('gains_tva_carburants_reformes_cae_sans_rattrapage', period)
            gains_combustibles_liquides = simulation.calculate('gains_tva_combustibles_liquides_reformes_cae', period)
            gains_gaz_ville = simulation.calculate('gains_tva_gaz_ville_reformes_cae', period)

            somme_gains = gains_carburants_sans_rattrapage + gains_combustibles_liquides + gains_gaz_ville
            return somme_gains


    # Vérifier que rien n'est oublié ici
    class pertes_financieres_avant_redistribution_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant total des pertes financières dues à la réforme, avant redistribution"
    
        def formula(self, simulation, period):
            depenses_energies_totales = simulation.calculate('depenses_energies_totales', period)
            depenses_energies_logement_reformes_cae = \
                simulation.calculate('depenses_energies_logement_reformes_cae', period)
            depenses_carburants_reformes_cae = \
                simulation.calculate('depenses_carburants_corrigees_reformes_cae', period)

            pertes = (
                depenses_energies_logement_reformes_cae +
                depenses_carburants_reformes_cae -
                depenses_energies_totales
                )

            return pertes


    class pertes_financieres_avant_redistribution_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant total des pertes financières dues à la réforme, avant redistribution"
    
        def formula(self, simulation, period):
            depenses_energies_totales = simulation.calculate('depenses_energies_totales', period)
            depenses_energies_logement_reformes_cae = \
                simulation.calculate('depenses_energies_logement_reformes_cae', period)
            depenses_carburants_reformes_cae_sans_rattrapage = \
                simulation.calculate('depenses_carburants_corrigees_reformes_cae_sans_rattrapage', period)

            pertes = (
                depenses_energies_logement_reformes_cae +
                depenses_carburants_reformes_cae_sans_rattrapage -
                depenses_energies_totales
                )

            return pertes


    class quantites_combustibles_liquides_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités de combustibles_liquides consommées après la réforme"

        def formula(self, simulation, period):
            depenses_combustibles_liquides_reformes_cae = \
                simulation.calculate('depenses_combustibles_liquides_reformes_cae', period)
            prix_fioul_ttc = \
                simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                simulation.legislation_at(period.start).reformes_cae.combustibles_liquides_2022_in_2018
            quantites_combustibles_liquides_ajustees = depenses_combustibles_liquides_reformes_cae / (prix_fioul_ttc + reforme_combustibles_liquides)
    
            return quantites_combustibles_liquides_ajustees
    
    
    class quantites_diesel_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités de diesel consommées après la réforme"

        def formula(self, simulation, period):
            depenses_diesel_reformes_cae = \
                simulation.calculate('depenses_diesel_corrigees_reformes_cae', period)
            diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018
            quantites_diesel_ajustees = depenses_diesel_reformes_cae / (diesel_ttc + reforme_diesel) * 100
    
            return quantites_diesel_ajustees
    
    
    class quantites_diesel_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités de diesel consommées après la réforme"

        def formula(self, simulation, period):
            depenses_diesel_reformes_cae_sans_rattrapage = \
                simulation.calculate('depenses_diesel_corrigees_reformes_cae_sans_rattrapage', period)
            diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel_sans_rattrapage = simulation.legislation_at(period.start).reformes_cae.diesel_2022_in_2018_sans_rattrapage
            quantites_diesel_ajustees_sans_rattrapage = depenses_diesel_reformes_cae_sans_rattrapage / (diesel_ttc + reforme_diesel_sans_rattrapage) * 100
    
            return quantites_diesel_ajustees_sans_rattrapage
    
    
    class quantites_essence_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités d'essence consommées par les ménages après réforme"
        definition_period = YEAR
    
        def formula_2009(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95_reformes_cae', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98_reformes_cae', period)
            quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_reformes_cae', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
            return quantites_essence_ajustees
    
        def formula_2007(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95_reformes_cae', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98_reformes_cae', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
            return quantites_essence_ajustees
    
        def formula_1990(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95_reformes_cae', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98_reformes_cae', period)
            quantites_super_plombe_ajustees = \
                simulation.calculate('quantites_super_plombe_reformes_cae', period)
            quantites_essence_ajustees = (
                quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
                )
            return quantites_essence_ajustees


    class quantites_gaz_final_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités de gaz consommées après la réforme"
    
        def formula(self, simulation, period):
            depenses_gaz_ville_reformes_cae = simulation.calculate('depenses_gaz_ville_reformes_cae', period)
            depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
            depenses_gaz_variables = depenses_gaz_ville_reformes_cae - depenses_gaz_tarif_fixe
    
            depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                simulation.legislation_at(period.start).reformes_cae.gaz_ville_2022_in_2018
    
            quantites_gaz_ajustees = depenses_gaz_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

            return quantites_gaz_ajustees
    
    
    class quantites_sp_e10_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités consommées de sans plomb e10 par les ménages après réforme"
    
        def formula(self, simulation, period):
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            depenses_sp_e10_ajustees = depenses_essence_reformes_cae * part_sp_e10
            super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100
    
            return quantite_sp_e10
    
    
    class quantites_sp95_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"
    
        def formula(self, simulation, period):
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp95_ajustees = depenses_essence_reformes_cae * part_sp95
            super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100
    
            return quantites_sp95_ajustees
    
    
    class quantites_sp98_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités consommées de sans plomb 98 par les ménages"
    
        def formula(self, simulation, period):
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp98_ajustees = depenses_essence_reformes_cae * part_sp98
            super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100
    
            return quantites_sp98_ajustees
    
    
    class quantites_super_plombe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Quantités consommées de super plombé par les ménages après réforme"
    
        def formula(self, simulation, period):
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_super_plombe = \
                simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_reformes_cae * part_super_plombe
            super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100
    
            return quantites_super_plombe_ajustees
    
    
    class revenu_reforme_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Revenu généré par la réforme officielle 2018 avant redistribution"
    
        def formula(self, simulation, period):
            total_taxes_energies = simulation.calculate('total_taxes_energies', period)
            total_taxes_energies_reformes_cae = \
                simulation.calculate('total_taxes_energies_reformes_cae', period)
            gains_tva_total_energies = simulation.calculate('gains_tva_total_energies_reformes_cae', period)

            revenu_reforme = (
                total_taxes_energies_reformes_cae - total_taxes_energies +
                gains_tva_total_energies
                )

            return revenu_reforme


    class revenu_reforme_logement_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Revenu généré par la réforme officielle 2018 avant redistribution"
    
        def formula(self, simulation, period):
            total_taxes_energies_logement = simulation.calculate('combustibles_liquides_ticpe', period) # 0 pour le gaz qui n'est pas calculé, on ne compte que la diféfrence
            total_taxes_energies_logement_reformes_cae = \
                simulation.calculate('total_taxes_logement_reformes_cae', period)
            gains_tva_total_energies_fioul = simulation.calculate('gains_tva_combustibles_liquides_reformes_cae', period)
            gains_tva_total_energies_gaz = simulation.calculate('gains_tva_gaz_ville_reformes_cae', period)
            gains_tva_total_energies_logement = gains_tva_total_energies_fioul + gains_tva_total_energies_gaz

            revenu_reforme = (
                total_taxes_energies_logement_reformes_cae - total_taxes_energies_logement +
                gains_tva_total_energies_logement
                )

            return revenu_reforme


    class revenu_reforme_transports_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Revenu généré par la réforme officielle 2018 avant redistribution"
    
        def formula(self, simulation, period):
            total_taxes_essence = simulation.calculate('essence_ticpe', period)
            total_taxes_diesel = simulation.calculate('diesel_ticpe', period)
            total_taxes_transports = total_taxes_essence + total_taxes_diesel
            total_taxes_transports_reformes_cae = \
                simulation.calculate('total_taxes_transports_reformes_cae', period)
            gains_tva_total_carburants = simulation.calculate('gains_tva_carburants_reformes_cae', period)

            revenu_reforme = (
                total_taxes_transports_reformes_cae - total_taxes_transports +
                gains_tva_total_carburants
                )

            return revenu_reforme


    class revenu_reforme_transports_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Revenu généré par la réforme officielle 2018 avant redistribution"
    
        def formula(self, simulation, period):
            total_taxes_essence = simulation.calculate('essence_ticpe', period)
            total_taxes_diesel = simulation.calculate('diesel_ticpe', period)
            total_taxes_transports = total_taxes_essence + total_taxes_diesel
            total_taxes_transports_reformes_cae = \
                simulation.calculate('total_taxes_transports_reformes_cae_sans_rattrapage', period)
            gains_tva_total_carburants = simulation.calculate('gains_tva_carburants_reformes_cae_sans_rattrapage', period)

            revenu_reforme = (
                total_taxes_transports_reformes_cae - total_taxes_transports +
                gains_tva_total_carburants
                )

            return revenu_reforme


    class revenu_reforme_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Revenu généré par la réforme officielle 2018 avant redistribution"
    
        def formula(self, simulation, period):
            total_taxes_energies = simulation.calculate('total_taxes_energies', period)
            total_taxes_energies_reformes_cae_sans_rattrapage = \
                simulation.calculate('total_taxes_energies_reformes_cae_sans_rattrapage', period)
            gains_tva_total_energies_sans_rattrapage = simulation.calculate('gains_tva_total_energies_reformes_cae_sans_rattrapage', period)

            revenu_reforme_sans_rattrapage = (
                total_taxes_energies_reformes_cae_sans_rattrapage - total_taxes_energies +
                gains_tva_total_energies_sans_rattrapage
                )

            return revenu_reforme_sans_rattrapage


    class sp_e10_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            try:
                accise_super_e10 = \
                    simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
                majoration_ticpe_super_e10 = \
                    simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
            except:
                accise_ticpe_super_e10 = \
                    simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
    
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
                (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_reformes_cae * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)
    
            return montant_sp_e10_ticpe_ajuste
    
    
    class sp95_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de TICPE sur le sp_95 après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
    
            try:
                accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
                majoration_ticpe_super95 = \
                    simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
            except:
                accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
    
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
                (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_reformes_cae * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )
    
            return montant_sp95_ticpe_ajuste
    
    
    class sp98_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de TICPE sur le sp_98 après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
    
            try:
                accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
                majoration_ticpe_super98 = \
                    simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
            except:
                accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
    
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
                (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_reformes_cae * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )
    
            return montant_sp98_ticpe_ajuste
    
    
    class super_plombe_ticpe_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de la TICPE sur le super plombé après réforme"
    
        def formula(self, simulation, period):
            taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
            accise_super_plombe_ticpe = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
    
            reforme_essence = simulation.legislation_at(period.start).reformes_cae.essence_2022_in_2018
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
                (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_reformes_cae = \
                simulation.calculate('depenses_essence_corrigees_reformes_cae', period)
            part_super_plombe = \
                simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_reformes_cae * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees -
                tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)
    
            return montant_super_plombe_ticpe_ajuste
    
    
    class taxe_gaz_ville_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Recettes de la taxe sur la consommation de gaz - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(self, simulation, period):
            quantites_gaz_ajustees = simulation.calculate('quantites_gaz_final_reformes_cae', period)
            reforme_gaz = simulation.legislation_at(period.start).reformes_cae.gaz_ville_2022_in_2018
            recettes_gaz = quantites_gaz_ajustees * reforme_gaz
    
            return recettes_gaz
    
    
    class ticpe_totale_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"
    
        def formula(self, simulation, period):
            essence_ticpe_ajustee = simulation.calculate('essence_ticpe_reformes_cae', period)
            diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_reformes_cae', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee
    
            return ticpe_totale_ajustee


    class ticpe_totale_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"
    
        def formula(self, simulation, period):
            essence_ticpe_ajustee = simulation.calculate('essence_ticpe_reformes_cae', period)
            diesel_ticpe_ajustee_sans_rattrapage = simulation.calculate('diesel_ticpe_reformes_cae_sans_rattrapage', period)
            ticpe_totale_ajustee_sans_rattrapage = diesel_ticpe_ajustee_sans_rattrapage + essence_ticpe_ajustee
    
            return ticpe_totale_ajustee_sans_rattrapage


    class total_taxes_energies_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"
    
        def formula(self, simulation, period):
            taxe_diesel = simulation.calculate('diesel_ticpe_reformes_cae', period)
            taxe_essence = simulation.calculate('essence_ticpe_reformes_cae', period)
            taxe_combustibles_liquides = simulation.calculate('combustibles_liquides_ticpe_reformes_cae', period)
            taxe_gaz_ville = simulation.calculate('taxe_gaz_ville_reformes_cae', period)
    
            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )
    
            return total
    
    
    class total_taxes_energies_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"
    
        def formula(self, simulation, period):
            taxe_diesel_sans_rattrapage = simulation.calculate('diesel_ticpe_reformes_cae_sans_rattrapage', period)
            taxe_essence = simulation.calculate('essence_ticpe_reformes_cae', period)
            taxe_combustibles_liquides = simulation.calculate('combustibles_liquides_ticpe_reformes_cae', period)
            taxe_gaz_ville = simulation.calculate('taxe_gaz_ville_reformes_cae', period)
    
            total_sans_rattrapage = (
                taxe_diesel_sans_rattrapage + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )
    
            return total_sans_rattrapage
    
    
    class total_taxes_logement_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"
    
        def formula(self, simulation, period):
            taxe_combustibles_liquides = simulation.calculate('combustibles_liquides_ticpe_reformes_cae', period)
            taxe_gaz_ville = simulation.calculate('taxe_gaz_ville_reformes_cae', period)
    
            total_sans_rattrapage = (
                taxe_combustibles_liquides + taxe_gaz_ville
                )
    
            return total_sans_rattrapage
    
    
    class total_taxes_transports_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"
    
        def formula(self, simulation, period):
            taxe_diesel_sans_rattrapage = simulation.calculate('diesel_ticpe_reformes_cae', period)
            taxe_essence = simulation.calculate('essence_ticpe_reformes_cae', period)
    
            total_sans_rattrapage = (
                taxe_diesel_sans_rattrapage + taxe_essence
                )
    
            return total_sans_rattrapage
    
    
    class total_taxes_transports_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"
    
        def formula(self, simulation, period):
            taxe_diesel_sans_rattrapage = simulation.calculate('diesel_ticpe_reformes_cae_sans_rattrapage', period)
            taxe_essence = simulation.calculate('essence_ticpe_reformes_cae', period)
    
            total_sans_rattrapage = (
                taxe_diesel_sans_rattrapage + taxe_essence
                )
    
            return total_sans_rattrapage
    
    
    class transferts_neutre_cinq_decile_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            eligible = 0 + 1 * (decile < 6)

            revenu_reforme = \
                simulation.calculate('revenu_reforme_reformes_cae', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)

            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen * eligible)
            transferts_eligibles = revenu_uc * ocde10 * eligible

            return transferts_eligibles


    class transferts_lisses_huit_decile_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_lisses = (
                    380 * (decile == 1) +
                    380 * (decile == 2) +
                    370 * (decile == 3) +
                    340 * (decile == 4) +
                    310 * (decile == 5) +
                    270 * (decile == 6) +
                    190 * (decile == 7) +
                    90 * (decile == 8)
                    )

            return transferts_lisses


    class transferts_geographiques_lisses_huit_decile_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_revenu = (
                    310 * (decile == 1) +
                    310 * (decile == 2) +
                    310 * (decile == 3) +
                    300 * (decile == 4) +
                    255 * (decile == 5) +
                    240 * (decile == 6) +
                    150 * (decile == 7) +
                    60 * (decile == 8)
                    )

            strate = simulation.calculate('strate', period)

            transfert_geographique = (
                    150 * (strate == 0) * (decile < 4) +
                    100 * (strate == 1) * (decile < 4) +
                    60 * (strate == 2) * (decile < 4) +
                    30 * (strate == 3) * (decile < 4) +
                    115 * (strate == 0) * (decile < 6) * (decile > 3) +
                    75 * (strate == 1) * (decile < 6) * (decile > 3) +
                    45 * (strate == 2) * (decile < 6) * (decile > 3) +
                    25 * (strate == 3) * (decile < 6) * (decile > 3) +
                    75 * (strate == 0) * (decile < 8) * (decile > 5) +
                    50 * (strate == 1) * (decile < 8) * (decile > 5) +
                    30 * (strate == 2) * (decile < 8) * (decile > 5) +
                    15 * (strate == 3) * (decile < 8) * (decile > 5)
                    )

            transferts = transferts_revenu + transfert_geographique

            return transferts


    class transferts_geographiques_lisses_bis_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_revenu = (
                    330 * (decile == 1) +
                    330 * (decile == 2) +
                    330 * (decile == 3) +
                    330 * (decile == 4) +
                    290 * (decile == 5) +
                    250 * (decile == 6) +
                    150 * (decile == 7) +
                    60 * (decile == 8)
                    )

            strate = simulation.calculate('strate', period)

            transfert_geographique = (
                    160 * (strate == 0) * (decile < 4) +
                    70 * (strate == 1) * (decile < 4) +
                    30 * (strate == 2) * (decile < 4) +
                    20 * (strate == 3) * (decile < 4) +
                    (-90) * (strate == 4) * (decile < 4) +
                    160 * (3/4) * (strate == 0) * (decile < 6) * (decile > 3) +
                    70 * (3/4) * (strate == 1) * (decile < 6) * (decile > 3) +
                    30 * (3/4) * (strate == 2) * (decile < 6) * (decile > 3) +
                    20 * (3/4) * (strate == 3) * (decile < 6) * (decile > 3) +
                    (-90) * (3/4) * (strate == 4) * (decile < 6) * (decile > 3) +
                    160 * (1/2) * (strate == 0) * (decile < 8) * (decile > 5) +
                    70 * (1/2) * (strate == 1) * (decile < 8) * (decile > 5) +
                    30 * (1/2) * (strate == 2) * (decile < 8) * (decile > 5) +
                    20 * (1/2) * (strate == 3) * (decile < 8) * (decile > 5) +
                    (-90) * (1/2) * (strate == 4) * (decile < 8) * (decile > 5)
                    )

            transferts = transferts_revenu + transfert_geographique

            return transferts


    class transferts_geographiques_economies_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"transfert visant à reproduire les effets redistributifs du cas sans différenciation géographique tout en conservant des recettes"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_revenu = (
                    348 * (decile == 1) +
                    324 * (decile == 2) +
                    304 * (decile == 3) +
                    300 * (decile == 4) +
                    247 * (decile == 5) +
                    240 * (decile == 6) +
                    158 * (decile == 7) +
                    90 * (decile == 8)
                    )

            strate = simulation.calculate('strate', period)

            transfert_geographique = (
                    160 * (strate == 0) * (decile < 4) +
                    70 * (strate == 1) * (decile < 4) +
                    30 * (strate == 2) * (decile < 4) +
                    20 * (strate == 3) * (decile < 4) +
                    (-90) * (strate == 4) * (decile < 4) +
                    160 * (3/4) * (strate == 0) * (decile < 6) * (decile > 3) +
                    70 * (3/4) * (strate == 1) * (decile < 6) * (decile > 3) +
                    30 * (3/4) * (strate == 2) * (decile < 6) * (decile > 3) +
                    20 * (3/4) * (strate == 3) * (decile < 6) * (decile > 3) +
                    (-90) * (3/4) * (strate == 4) * (decile < 6) * (decile > 3) +
                    160 * (1/2) * (strate == 0) * (decile < 8) * (decile > 5) +
                    70 * (1/2) * (strate == 1) * (decile < 8) * (decile > 5) +
                    30 * (1/2) * (strate == 2) * (decile < 8) * (decile > 5) +
                    20 * (1/2) * (strate == 3) * (decile < 8) * (decile > 5) +
                    (-90) * (1/2) * (strate == 4) * (decile < 8) * (decile > 5)
                    )

            transferts = transferts_revenu + transfert_geographique

            return transferts


    class transferts_energie_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_revenu = (
                    310 * (decile == 1) +
                    310 * (decile == 2) +
                    305 * (decile == 3) +
                    300 * (decile == 4) +
                    255 * (decile == 5) +
                    230 * (decile == 6) +
                    135 * (decile == 7) +
                    60 * (decile == 8)
                    )

            fioul = simulation.calculate('combustibles_liquides', period)
            gaz = simulation.calculate('gaz_ville', period)
            transfert_energie = (
                    200 * (fioul == 1) * (decile < 4) +
                    120 * (gaz == 1) * (decile < 4) +
                    150 * (fioul == 1) * (decile < 6) * (decile > 3) +
                    90 * (gaz == 1) * (decile < 6) * (decile > 3) +
                    100 * (fioul == 1) * (decile < 8) * (decile > 5) +
                    60 * (gaz == 1) * (decile < 8) * (decile > 5)
                    )

            transferts = transferts_revenu + transfert_energie

            return transferts


    class transferts_geographiques_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            strate = simulation.calculate('strate', period)
            strate_0 = 1 * (strate == 0)
            strate_1 = 1 * (strate == 1)
            strate_2 = 1 * (strate == 2)
            strate_3 = 1 * (strate == 3)
            
            cheque_strate_0 = 206 * strate_0 * ocde10
            cheque_strate_1 = 139 * strate_1 * ocde10
            cheque_strate_2 = 132 * strate_2 * ocde10
            cheque_strate_3 = 99 * strate_3 * ocde10
            
            cheques_geographique = cheque_strate_0 + cheque_strate_1 + cheque_strate_2 + cheque_strate_3
            somme_cheques_geographique = numpy.sum(cheques_geographique * pondmen)

            revenu_reforme = \
                simulation.calculate('revenu_reforme_reformes_cae', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            revenu_restant = somme_revenu - somme_cheques_geographique

            revenu_restant_uc = revenu_restant / numpy.sum(ocde10 * pondmen)
            transferts_revenu_restant = revenu_restant_uc * ocde10
            
            transferts = transferts_revenu_restant + cheques_geographique

            return transferts


    class transferts_neutre_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)

            revenu_reforme = \
                simulation.calculate('revenu_reforme_reformes_cae', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)

            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen)
            transferts = revenu_uc * ocde10

            return transferts


    class transferts_neutre_reformes_cae_sans_rattrapage(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)

            revenu_reforme_sans_rattrapage = \
                simulation.calculate('revenu_reforme_reformes_cae_sans_rattrapage', period)
            somme_revenu_sans_rattrapage = numpy.sum(revenu_reforme_sans_rattrapage * pondmen)

            revenu_uc_sans_rattrapage = somme_revenu_sans_rattrapage / numpy.sum(ocde10 * pondmen)
            transferts_sans_rattrapage = revenu_uc_sans_rattrapage * ocde10

            return transferts_sans_rattrapage


    class transferts_terra_nova_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            decile = simulation.calculate('niveau_vie_decile', period)
            transferts_terra_nova = (
                    500 * (decile == 1) +
                    400 * (decile == 2) +
                    300 * (decile == 3) +
                    200 * (decile == 4) +
                    100 * (decile == 5)
                    )

            return transferts_terra_nova


    class transferts_terra_nova_geographique_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            decile = simulation.calculate('niveau_vie_decile', period)
            strate = simulation.calculate('strate', period)
            #ocde10 = simulation.calculate('ocde10', period)
            transferts_terra_nova = (
                    500 * (decile == 1) +
                    400 * (decile == 2) +
                    300 * (decile == 3) +
                    200 * (decile == 4) +
                    100 * (decile == 5)
                    )

            modulation_geographique = (
                    206 * (strate == 0) * (decile < 4) +
                    139 * (strate == 1) * (decile < 4) +
                    132 * (strate == 2) * (decile < 4) +
                    99 * (strate == 3) * (decile < 4) +
                    (206 * 0.75) * (strate == 0) * (decile < 6) * (decile > 3) +
                    (139 * 0.75) * (strate == 1) * (decile < 6) * (decile > 3) +
                    (132 * 0.75) * (strate == 2) * (decile < 6) * (decile > 3) +
                    (99 * 0.75) * (strate == 3) * (decile < 6) * (decile > 3) +
                    (206 * 0.5) * (strate == 0) * (decile < 8) * (decile > 5) +
                    (139 * 0.5) * (strate == 1) * (decile < 8) * (decile > 5) +
                    (132 * 0.5) * (strate == 2) * (decile < 8) * (decile > 5) +
                    (99 * 0.5) * (strate == 3) * (decile < 8) * (decile > 5)
                    )

            transferts_terra_nova_geographique = transferts_terra_nova + modulation_geographique

            return transferts_terra_nova_geographique


    class transferts_propotionnel_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            pondmen = simulation.calculate('pondmen', period)
            revenu_menage = simulation.calculate('rev_disponible', period)

            revenu_reforme = \
                simulation.calculate('revenu_reforme_reformes_cae', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)

            revenu_total_menages = numpy.sum(revenu_menage * pondmen)
            transferts_proportionnel = somme_revenu * revenu_menage / revenu_total_menages

            return transferts_proportionnel


    class transferts_semi_propotionnel_reformes_cae(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"..."
    
        def formula(self, simulation, period):
            decile = simulation.calculate('niveau_vie_decile', period)
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)
            revenu_menage = simulation.calculate('rev_disponible', period)
            eligible = 0 + 1 #* (decile < 6)

            revenu_reforme = \
                simulation.calculate('revenu_reforme_reformes_cae', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)

            revenu_uc_transfert_fixe = (0.3 * somme_revenu) / numpy.sum(ocde10 * pondmen * eligible)
            transferts_fixe_eligibles = revenu_uc_transfert_fixe * ocde10 * eligible
            
            revenu_total_menages = numpy.sum(revenu_menage * pondmen)
            transferts_proportionnel = (0.7 * somme_revenu) * revenu_menage / revenu_total_menages

            transferts_semi_proportionnel = transferts_fixe_eligibles + transferts_proportionnel

            return transferts_semi_proportionnel


    def apply(self):
        self.update_variable(self.cheques_energie_reformes_cae)
        self.update_variable(self.cheques_energie_philippe_reformes_cae)
        self.update_variable(self.cheques_energie_etendu_majore_reformes_cae)
        self.update_variable(self.combustibles_liquides_ticpe_reformes_cae)
        self.update_variable(self.depenses_carburants_corrigees_reformes_cae)
        self.update_variable(self.depenses_carburants_corrigees_reformes_cae_sans_rattrapage)
        self.update_variable(self.depenses_combustibles_liquides_reformes_cae)
        self.update_variable(self.depenses_diesel_corrigees_reformes_cae)
        self.update_variable(self.depenses_diesel_corrigees_reformes_cae_sans_rattrapage)
        self.update_variable(self.depenses_energies_logement_reformes_cae)
        self.update_variable(self.depenses_essence_corrigees_reformes_cae)
        self.update_variable(self.depenses_gaz_ville_reformes_cae)
        self.update_variable(self.diesel_ticpe_reformes_cae)
        self.update_variable(self.diesel_ticpe_reformes_cae_sans_rattrapage)
        self.update_variable(self.essence_ticpe_reformes_cae)
        self.update_variable(self.gains_tva_carburants_reformes_cae)
        self.update_variable(self.gains_tva_carburants_reformes_cae_sans_rattrapage)
        self.update_variable(self.gains_tva_combustibles_liquides_reformes_cae)
        self.update_variable(self.gains_tva_gaz_ville_reformes_cae)
        self.update_variable(self.gains_tva_total_energies_reformes_cae)
        self.update_variable(self.gains_tva_total_energies_reformes_cae_sans_rattrapage)
        self.update_variable(self.pertes_financieres_avant_redistribution_reformes_cae)
        self.update_variable(self.pertes_financieres_avant_redistribution_reformes_cae_sans_rattrapage)
        self.update_variable(self.quantites_combustibles_liquides_reformes_cae)
        self.update_variable(self.quantites_diesel_reformes_cae)
        self.update_variable(self.quantites_diesel_reformes_cae_sans_rattrapage)
        self.update_variable(self.quantites_essence_reformes_cae)
        self.update_variable(self.quantites_gaz_final_reformes_cae)
        self.update_variable(self.quantites_sp_e10_reformes_cae)
        self.update_variable(self.quantites_sp95_reformes_cae)
        self.update_variable(self.quantites_sp98_reformes_cae)
        self.update_variable(self.quantites_super_plombe_reformes_cae)
        self.update_variable(self.revenu_reforme_reformes_cae)
        self.update_variable(self.revenu_reforme_reformes_cae_sans_rattrapage)
        self.update_variable(self.revenu_reforme_logement_reformes_cae)
        self.update_variable(self.revenu_reforme_transports_reformes_cae)
        self.update_variable(self.revenu_reforme_transports_reformes_cae_sans_rattrapage)
        self.update_variable(self.sp_e10_ticpe_reformes_cae)
        self.update_variable(self.sp95_ticpe_reformes_cae)
        self.update_variable(self.sp98_ticpe_reformes_cae)
        self.update_variable(self.super_plombe_ticpe_reformes_cae)
        self.update_variable(self.taxe_gaz_ville_reformes_cae)
        self.update_variable(self.ticpe_totale_reformes_cae)
        self.update_variable(self.ticpe_totale_reformes_cae_sans_rattrapage)
        self.update_variable(self.total_taxes_energies_reformes_cae)
        self.update_variable(self.total_taxes_energies_reformes_cae_sans_rattrapage)
        self.update_variable(self.total_taxes_logement_reformes_cae)
        self.update_variable(self.total_taxes_transports_reformes_cae)
        self.update_variable(self.total_taxes_transports_reformes_cae_sans_rattrapage)
        self.update_variable(self.transferts_neutre_cinq_decile_reformes_cae)
        self.update_variable(self.transferts_lisses_huit_decile_reformes_cae)
        self.update_variable(self.transferts_geographiques_lisses_bis_reformes_cae)
        self.update_variable(self.transferts_geographiques_lisses_huit_decile_reformes_cae)
        self.update_variable(self.transferts_geographiques_economies_reformes_cae)
        self.update_variable(self.transferts_geographiques_reformes_cae)
        self.update_variable(self.transferts_energie_reformes_cae)
        self.update_variable(self.transferts_neutre_reformes_cae)
        self.update_variable(self.transferts_neutre_reformes_cae_sans_rattrapage)
        self.update_variable(self.transferts_terra_nova_reformes_cae)
        self.update_variable(self.transferts_terra_nova_geographique_reformes_cae)
        self.update_variable(self.transferts_propotionnel_reformes_cae)
        self.update_variable(self.transferts_semi_propotionnel_reformes_cae)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
