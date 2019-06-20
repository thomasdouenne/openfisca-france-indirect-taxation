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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class age_carte_grise(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"âge de la carte grise du véhicule principal"


class age_vehicule(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"âge du véhicule principal"


class aides_logement(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage touche des aides au logement"


class bat_av_49(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le bâtiment date d'avant 1949"


class bat_49_74(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le bâtiment date d'entre 1949 et 1974"


class bat_ap_74(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le bâtiment date d'après 1974"


class cataeu(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"catégorie de la commune de résidence 2011"


class chaufp(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"chauffage individuel ou collectif"


class dip14pr(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Diplôme de la personne de référence"


class grande_ville(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Le ménage vit dans une petite ville"


class ident_men(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Identifiant du ménage"


class isolation_fenetres(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Qualité de l'isolation des fenêtres"


class isolation_murs(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Qualité de l'isolation des murs"


class isolation_toit(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Qualité de l'isolation du toit"


class identifiant_menage(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Code identifiant le ménage"


class log_indiv(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage vie dans un logement individuel"


class majorite_double_vitrage(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Majorité de double vitrage dans le logement"


class ocde10(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"unités de consommation"


class ouest_sud(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage vit dans l'ouest ou le sud de la France"


class petite_ville(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Le ménage vit dans une petite ville"


class pondmen(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Pondération du ménage"


class situacj(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Situation du conjoint vis-à-vis du travail"


class situapr(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Situation de la personne de référence vis-à-vis du travail"


class surfhab_d(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Taille du logement en m2"


class strate(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"catégorie de la commune de résidence"


class stalog(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Statut du logement (1 = propriétaire)"


class tchof(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"unité urbaine"


class tuu(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"unité urbaine"


class typmen(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"type du ménage"


class vag(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"numéro de la vague d'interrogation du ménage"


class ville_moyenne(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Le ménage vit dans une petite ville"


class vp_deplacements_pro(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage utilise son véhicule particulier pour ses déplacements pro"


class vp_domicile_travail(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage utilise son véhicule particulier pour se rendre à son travail"


class zeat(YearlyVariable):
    column = EnumCol(
        enum = Enum([
            u"DOM",
            u"Région parisienne",
            u"Bassin parisien",
            u"Nord",
            u"Est",
            u"Ouest",
            u"Sud-Ouest",
            u"Centre-Est",
            u"Méditerrannée"], start = 0)
        )
    entity = Menage
    label = u"Zone d'étude et d'aménagement du territoire"


class grande_ville(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage vit dans une grande ville"

    def formula(self, simulation, period):
        strate = simulation.calculate('strate', period)
        grande_ville = 0 + 1 * (strate == 3)
    
        return grande_ville


class moyenne_ville(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage vit dans une ville moyenne"

    def formula(self, simulation, period):
        strate = simulation.calculate('strate', period)
        moyenne_ville = 0 + 1 * (strate == 2)
    
        return moyenne_ville


class paris(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Le ménage vit en région parisienne"

    def formula(self, simulation, period):
        strate = simulation.calculate('strate', period)
        paris = 0 + 1 * (strate == 4)
    
        return paris


class petite_ville(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Le ménage vit dans une petite ville"

    def formula(self, simulation, period):
        strate = simulation.calculate('strate', period)
        petite_ville = 0 + 1 * (strate == 1)
    
        return petite_ville


class rural(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Le ménage vit en région parisienne"

    def formula(self, simulation, period):
        strate = simulation.calculate('strate', period)
        rural = 0 + 1 * (strate == 0)
    
        return rural
