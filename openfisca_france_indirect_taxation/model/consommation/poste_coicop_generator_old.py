
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

from openfisca_france_indirect_taxation.model.base import *


class poste_111(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Pain et céréales"

class poste_112(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Viande"

class poste_113(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Poisson et fruits de mer"

class poste_114(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Lait, fromage et œufs"

class poste_115(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Huiles et graisses"

class poste_1151(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Margarines et autres graisses végétales"

class poste_116(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Fruits"

class poste_117(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Légumes"

class poste_118(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Sucre, confiture, miel, chocolat et confiserie"

class poste_1181(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Confiserie"

class poste_119(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Produits alimentaires non compris ailleurs"

class poste_121(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Café, thé et cacao"

class poste_122(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Eaux minérales, boissons rafraîchissantes, jus de fruits et  de légumes"

class poste_211(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Alcools de bouche "

class poste_212(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Vin et boissons fermentées"

class poste_213(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Bière"

class poste_2201(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Cigarettes"

class poste_2202(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Cigares et cigarillos"

class poste_2203(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Tabac sous d'autres formes"

class poste_230(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Stupéfiants"

class poste_311(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Tissus pour habillement"

class poste_312(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Vêtements"

class poste_313(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres articles et accessoires d'habillement"

class poste_314(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Nettoyage, réparation et location d'articles d'habillement"

class poste_321(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Chaussures diverses"

class poste_322(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Cordonnerie et location de chaussures"

class poste_411(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Loyers effectivement payés par les locataires"

class poste_412(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres loyers effectifs"

class poste_421(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Loyers fictifs des propriétaires occupants"

class poste_422(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres loyers fictifs"

class poste_431(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Fournitures pour travaux d'entretien et de réparation des logements"

class poste_432(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services concernant l'entretien et les réparations du logement"

class poste_441(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Alimentation en eau"

class poste_04_4_1_3_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Collecte des ordures ménagères"

class poste_443(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Reprise des eaux usées"

class poste_444(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Service divers liés au logement non compris ailleurs"

class poste_04_5_1_1_1_b(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Electricité"

class poste_04_5_1_1_1_b1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Facture EDF GDF non dissociables"

class poste_04_5_2_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Gaz"

class poste_04_5_2_2_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Achat de butane, propane"

class poste_04_5_3_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Combustibles liquides"

class poste_04_5_4_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Combustibles solides"

class poste_04_5_5_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Energie thermique"

class poste_511(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Meubles et articles d'ameublement"

class poste_512(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Tapis et revêtements de sols divers"

class poste_513(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation de meubles, d'articles d'ameublement et de revêtements souples pour le sol"

class poste_520(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Article de ménage en textiles"

class poste_531(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Gros appareils ménagers, électriques ou non"

class poste_532(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Petits appareils électroméangers"

class poste_533(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation d'appareils ménagers"

class poste_540(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Verrerie, vaisselle et ustensiles de ménage"

class poste_551(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Gros outillage et matériel"

class poste_552(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Petit outillage et accessoires divers"

class poste_561(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Biens d'équipement ménager non durables"

class poste_562(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services domestiques et services ménagers"

class poste_611(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Produits pharmaceutiques"

class poste_612(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Produits médicaux divers"

class poste_613(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Appareils et matériel thérapeutiques"

class poste_621(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services médicaux"

class poste_622(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services dentaires"

class poste_623(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services paramédicaux"

class poste_630(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services hospitaliers"

class poste_07_1_1_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Voitures automobiles"

class poste_07_1_2_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Motocycles"

class poste_07_1_3(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Bicyclettes"

class poste_721(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Pièces de rechange et accessoires pour véhicules de tourisme "

class poste_722(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Carburants et lubrifiants pour véhicules de tourisme"

class poste_723(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Entretien et réparation de véhicules particuliers"

class poste_724(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services divers liés aux véhicules particuliers"

class poste_731(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Transport ferroviaire de passagers"

class poste_732(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Transport routier de passagers"

class poste_733(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Transport aérien de passagers"

class poste_734(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Transport maritime et fluvial de passagers"

class poste_735(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Transport combiné de passagers"

class poste_736(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services de transport divers"

class poste_810(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services postaux"

class poste_831(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de téléphonie et de télécopie"

class poste_832(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services de téléphonie et de télécopie"

class poste_911(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de réception, d'enregistrement et de reproduction du son et de l'image"

class poste_09_1_2_1_1_a(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel photographique et cinématographique et appareils optiques"

class poste_09_1_3_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de traitement de l'information"

class poste_09_1_4_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Supports d'enregistrement"

class poste_915(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation de matériel audiovisuel, photographique et de traitement de l'information"

class poste_09_2_2_2(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Biens durables pour loisirs de plein air"

class poste_09_2_1_1_3(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Instruments de musique et biens durables destinés aux loisirs d'intérieur"

class poste_09_2_3_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Entretien et réparation des autres biens durables à fonction récréatives et culturelles"

class poste_931(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Jeux, jouets et passe-temps"

class poste_932(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Articles de sport, matériel de camping et matériel pour activités de plein air"

class poste_933(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Produits pour jardin, plantes et fleurs"

class poste_934(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Animaux de compagnie et articles connexes"

class poste_935(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services vétérinaires et autres services pour animaux de compagnie"

class poste_09_4_1_1_2(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services récréatifs et sportifs"

class poste_942(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services culturels"

class poste_943(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Jeux de hasard"

class poste_951(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Livre"

class poste_952(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Journaux et publications périodiques"

class poste_953(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Imprimés divers"

class poste_954(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Papeterie et matériel de dessin"

class poste_09_6_1_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Forfaits touristiques "

class poste_10_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement préélémentaire et primaire"

class poste_10_2(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement secondaire"

class poste_10_3(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement postsecondaire non supérieur"

class poste_10_4(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement supérieur"

class poste_10_5(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement non défini par niveau"

class poste_11112(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Restauration à emporter"

class poste_11113(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Restauration sur place"

class poste_11114(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u">>> Consommation de boissons alcoolisées"

class poste_1112(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Cantines"

class poste_1120(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Services d'hébergement"

class poste_1211(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Salons de coiffure et instituts de soins et de beauté"

class poste_12_1_3_3_3(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Appareils électriques pour soins corporels"

class poste_1213(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres appareils, articles et produits pour soins corporels"

class poste_1220(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Prostitution"

class poste_12_3_1_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Articles de bijouterie et horlogerie"

class poste_1232(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres effets personnels"

class poste_12_3_3_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Protection sociale"

class poste_1251(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance vie"

class poste_1252(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance habitation"

class poste_1253(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance maladie"

class poste_1254(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance transports"

class poste_1255(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres assurances"

class poste_1261(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Coûts des services d'intermédiation financière indirectement mesurés"

class poste_1262(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres services financiers non compris ailleurs"

class poste_12_7_1_1_1(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Autres services non compris ailleurs"

class poste_9901(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"caution pour la location d'un logement"

class poste_9902(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"achats de logements, garages, parkings, box et terrains"

class poste_9903(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Gros travaux d'entretien dans les logements"

class poste_9911(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"impôts et taxes de la résidence principale"

class poste_9912(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"impôts et taxes résidence secondaire ou autre logement"

class poste_9913(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"impôts sur le revenu"

class poste_9914(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"taxes automobile"

class poste_9915(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"autres impôts et taxes"

class poste_9921(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"remboursements de prêts résidence principale"

class poste_9922(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"remboursements de prêts résidence secondaire ou autre logement"

class poste_9923(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"autres remboursements de prêts"

class poste_9931(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"argent donné au sein du ménage"

class poste_9932(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"aides et cadeaux en argent offerts par le ménage (à des membres de la famille ne"

class poste_9933(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"cadeaux offerts (argent ou bien) sai"

class poste_9941(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"prélèvements de l'employeur"
