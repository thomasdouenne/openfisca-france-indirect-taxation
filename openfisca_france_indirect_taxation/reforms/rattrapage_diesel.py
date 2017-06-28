# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
from openfisca_core.reforms import Reform, update_legislation

from ..model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie


# Cette réforme consiste en un rattrapage de la fiscalité du diesel sur celle de l'essence. Les valeurs imputées
# correspondent donc à la différence entre la fiscalité des deux carburants à ces dates.

# On propose aussi deux réformes de redistribution : un abaissement de 1 point de TVA à taux plein, ou un abaissement
# de 0.5 point accompagné d'une baisse d'un point sur la TVA à taux réduit et super réduit. Ces redistributions sont
# telles que le budget doit être constant lorsqu'on simule sur les données 2011 inflatées pour 2014.


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "rattrapage_diesel",
        "children": {
            "diesel": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 17.85},
                    {'start': u'2015-01-01', 'stop': '2015-12-31', 'value': 15.59},
                    {'start': u'2016-01-01', 'stop': '2017-12-31', 'value': 15.31},
                    ],
                },
            "essence": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0},
                    ],
                },
            "abaissement_tva_taux_plein": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            "abaissement_tva_taux_plein_bis": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.005},
                    ],
                },
            "abaissement_tva_taux_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux réduit pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            "abaissement_tva_taux_super_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux super réduit pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            },
        }

    reference_legislation_json_copy['children']['rattrapage_diesel'] = reform_legislation_subtree
    return reference_legislation_json_copy


class depenses_diesel_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).rattrapage_diesel.diesel
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_diesel_ajustees_rattrapage_diesel = \
            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

        return period, depenses_diesel_ajustees_rattrapage_diesel

class depenses_essence_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_essence_ajustees_rattrapage_diesel = \
            depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

        return period, depenses_essence_ajustees_rattrapage_diesel

class depenses_tva_taux_plein_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_plein
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_ajustees

class depenses_tva_taux_plein_bis_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_plein_bis
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees

class depenses_tva_taux_reduit_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees

class depenses_tva_taux_super_reduit_ajustees_rattrapage_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA tx super reduit après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_super_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = (
            depenses_tva_taux_super_reduit *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))
            )
        return period, depenses_tva_taux_super_reduit_ajustees

class diesel_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le diesel après réforme"
    reference = ticpe.diesel_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).rattrapage_diesel.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_diesel_ajustees_rattrapage_diesel', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_rattrapage_diesel -
            tax_from_expense_including_tax(depenses_diesel_ajustees_rattrapage_diesel, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste

class emissions_CO2_carburants(Variable):
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"
    reference = emissions_co2.emissions_CO2_carburants

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees

class essence_ticpe(DatedVariable):
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
    reference = ticpe.essence_ticpe

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class quantites_diesel(Variable):
    label = u"Quantités de diesel consommées après la réforme - taxe carburants"
    reference = quantites_energie.quantites_diesel

    def function(self, simulation, period):
        depenses_diesel_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_diesel_ajustees_rattrapage_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).rattrapage_diesel.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees_rattrapage_diesel / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_sp_e10(Variable):
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - taxe carburants"
    reference = quantites_energie.quantites_sp_e10

    def function(self, simulation, period):
        depenses_essence_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp95(Variable):
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"
    reference = quantites_energie.quantites_sp95

    def function(self, simulation, period):
        depenses_essence_ajustees_rattrapage_diesel = simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp98(Variable):
    label = u"Quantités consommées de sans plomb 98 par les ménages"
    reference = quantites_energie.quantites_sp98

    def function(self, simulation, period):
        depenses_essence_ajustees_rattrapage_diesel = simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_super_plombe(Variable):
    label = u"Quantités consommées de super plombé par les ménages après réforme"
    reference = quantites_energie.quantites_super_plombe

    def function(self, simulation, period):
        depenses_essence_ajustees_rattrapage_diesel = simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees

class quantites_essence(DatedVariable):
    label = u"Quantités d'essence consommées par les ménages après réforme"
    reference = quantites_energie.quantites_essence

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees

class sp_e10_ticpe(Variable):
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"
    reference = ticpe.sp_e10_ticpe

    def function(self, simulation, period):
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

        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste

class sp95_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"
    reference = ticpe.sp95_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste

class sp98_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"
    reference = ticpe.sp98_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste

class super_plombe_ticpe(Variable):
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"
    reference = ticpe.super_plombe_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).rattrapage_diesel.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_rattrapage_diesel = \
            simulation.calculate('depenses_essence_ajustees_rattrapage_diesel', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste

class ticpe_totale(Variable):
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"
    reference = ticpe.ticpe_totale

    def function(self, simulation, period):
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        ticpe_totale = diesel_ticpe + essence_ticpe

        return period, ticpe_totale

class tva_taux_plein(Variable):
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxes carburants"
    reference = tva.tva_taux_plein

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_ajustees_rattrapage_diesel', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_plein
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

class tva_taux_plein_bis(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_bis_ajustees_rattrapage_diesel', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_plein_bis
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

class tva_taux_reduit(Variable):
    label = u"Contribution sur la TVA à taux reduit après réaction à la réforme - taxes carburants"
    reference = tva.tva_taux_reduit

    def function(self, simulation, period):
        depenses_tva_taux_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_reduit_ajustees_rattrapage_diesel', period)

        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_reduit
        nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

        return period, tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)

class tva_taux_super_reduit(Variable):
    label = u"Contribution sur la TVA à taux super reduit après réaction à la réforme - taxes carburants"
    reference = tva.tva_taux_super_reduit

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_super_reduit_ajustees_rattrapage_diesel', period)

        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = \
            simulation.legislation_at(period.start).rattrapage_diesel.abaissement_tva_taux_super_reduit
        nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

        return period, \
            tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)

class tva_total(Variable):
    label = u"Différence de contribution sur la TVA après réaction à la réforme - rattrapage diesel"
    reference = tva.tva_total

    def function(self, simulation, period):
        taux_plein = simulation.calculate('tva_taux_plein_bis', period)
        taux_reduit = simulation.calculate('tva_taux_reduit', period)
        taux_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
        taux_intermediaire = simulation.calculate('tva_taux_intermediaire', period)

        total = (taux_plein + taux_reduit + taux_super_reduit + taux_intermediaire)

        return period, total

class rattrapage_diesel(Reform):
    key = 'rattrapage_diesel',
    name = u"Réforme de l'imposition indirecte des carburants",



    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)
        variables = [
            depenses_diesel_ajustees_rattrapage_diesel,
            depenses_essence_ajustees_rattrapage_diesel,
            # TODO add other variables
            ]
        for variable in variables:
            self.add_variable(variable)
