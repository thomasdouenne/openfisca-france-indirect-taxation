# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore


class contributions_additionnelles_gaz_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Recettes de la hausse de cce 2014-2015 sur la consommation de gaz - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_cce_2014_2015', period)
        reforme_gaz = simulation.legislation_at(period.start).contribution_climat_energie_reforme.gaz_2014_2015
        recettes_gaz = quantites_gaz_ajustees * reforme_gaz

        return period, recettes_gaz


class contributions_additionnelles_gaz_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Recettes de la hausse de cce 2014-2016 sur la consommation de gaz - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_cce_2014_2016', period)
        reforme_gaz = simulation.legislation_at(period.start).contribution_climat_energie_reforme.gaz_2014_2016
        recettes_gaz = quantites_gaz_ajustees * reforme_gaz

        return period, recettes_gaz


class contributions_additionnelles_gaz_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Recettes de la taxe carbone sur la consommation de gaz - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_taxe_carbone', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz
        recettes_gaz = quantites_gaz_ajustees * reforme_gaz

        return period, recettes_gaz


class contributions_additionnelles_electricite_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Recettes de la taxe carbone sur la consommation d'électricité - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_electricite_ajustees = simulation.calculate('quantites_electricite_ajustees_taxe_carbone', period)
        reforme_electricite = simulation.legislation_at(period.start).taxe_carbone.electricite
        recettes_electricite = quantites_electricite_ajustees * reforme_electricite

        return period, recettes_electricite


class diesel_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).contribution_climat_energie_reforme.diesel_2014_2015
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_diesel_ajustees_cce_2014_2015', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_cce_2014_2015 -
            tax_from_expense_including_tax(depenses_diesel_ajustees_cce_2014_2015, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class diesel_ticpe_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).contribution_climat_energie_reforme.diesel_2014_2016
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_diesel_ajustees_cce_2014_2016', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_cce_2014_2016 -
            tax_from_expense_including_tax(depenses_diesel_ajustees_cce_2014_2016, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class diesel_ticpe_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).taxe_carbone.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_taxe_carbone = \
            simulation.calculate('depenses_diesel_ajustees_taxe_carbone', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_taxe_carbone -
            tax_from_expense_including_tax(depenses_diesel_ajustees_taxe_carbone, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class diesel_ticpe_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).taxes_carburants.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_taxes_carburants = \
            simulation.calculate('depenses_diesel_ajustees_taxes_carburants', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_taxes_carburants -
            tax_from_expense_including_tax(depenses_diesel_ajustees_taxes_carburants, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class difference_ticpe_diesel_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def function(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2015', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_diesel_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def function(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2016', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_diesel_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def function(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_taxe_carbone', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_diesel_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def function(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_taxes_carburants', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_essence_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class difference_ticpe_essence_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2016', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class difference_ticpe_essence_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_taxe_carbone', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class difference_ticpe_essence_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_taxes_carburants', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class difference_ticpe_totale_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE avant et après la réforme"

    def function(self, simulation, period):
        ticpe_totale_ajustee = simulation.calculate('ticpe_totale_ajustee_taxe_carbone', period)
        ticpe_totale = simulation.calculate('ticpe_totale', period)
        difference = ticpe_totale_ajustee - ticpe_totale

        return period, difference


class difference_ticpe_totale_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE avant et après la réforme"

    def function(self, simulation, period):
        ticpe_totale_ajustee = simulation.calculate('ticpe_totale_ajustee_taxes_carburants', period)
        ticpe_totale = simulation.calculate('ticpe_totale', period)
        difference = ticpe_totale_ajustee - ticpe_totale

        return period, difference


class essence_ticpe_ajustee_cce_2014_2015(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class essence_ticpe_ajustee_cce_2014_2016(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2016', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2016', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee_cce_2014_2016', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2016', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2016', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2016', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2016', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee_cce_2014_2016', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class essence_ticpe_ajustee_taxe_carbone(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxe_carbone', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxe_carbone', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee_taxe_carbone', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxe_carbone', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxe_carbone', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxe_carbone', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxe_carbone', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee_taxe_carbone', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class essence_ticpe_ajustee_taxes_carburants(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxes_carburants', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxes_carburants', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee_taxes_carburants', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxes_carburants', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxes_carburants', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_taxes_carburants', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_taxes_carburants', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee_taxes_carburants', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class sp_e10_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

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

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp_e10_ticpe_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

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

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp_e10_ticpe_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

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

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp_e10_ticpe_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

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

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxes_carburants = \
            simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp95_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp95_ticpe_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp95_ticpe_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp95_ticpe_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxes_carburants = \
            simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp98_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class sp98_ticpe_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class sp98_ticpe_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class sp98_ticpe_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxes_carburants = \
            simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class super_plombe_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class super_plombe_ticpe_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class super_plombe_ticpe_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class super_plombe_ticpe_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxes_carburants = \
            simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxes_carburants * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class ticpe_totale_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2015', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2015', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee


class ticpe_totale_ajustee_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2016', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2016', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee


class ticpe_totale_ajustee_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_taxe_carbone', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_taxe_carbone', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee


class ticpe_totale_ajustee_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_taxes_carburants', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_taxes_carburants', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee
