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


from openfisca_core import reforms


def preprocess_legislation(legislation_json):
    '''
    Preprocess the legislation parameters to add prices and amounts from national accounts
    '''
    import os
    import pkg_resources
    import pandas as pd

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_annuel_carburants = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'prix_annuel_carburants.csv'
            ), sep =';'
        )
    prix_annuel_carburants['Date'] = prix_annuel_carburants['Date'].astype(int)
    prix_annuel_carburants = prix_annuel_carburants.set_index('Date')
    all_values = {}
    prix_carburants = {
        "@type": "Node",
        "description": "prix des carburants en euros par hectolitre",
        "children": {},
        }
    for element in ['diesel_ht', 'diesel_ttc', 'super_95_ht', 'super_95_ttc', 'super_98_ht', 'super_98_ttc',
            'super_95_e10_ht', 'super_95_e10_ttc', 'gplc_ht', 'gplc_ttc', 'super_plombe_ht', 'super_plombe_ttc']:
        assert element in prix_annuel_carburants.columns
        prix_annuel = prix_annuel_carburants[element]
        all_values[element] = []
        for year in range(1990, 2015):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = prix_annuel.loc[year] * 100
            all_values[element].append(values)

        prix_carburants['children'][element] = {
            "@type": "Parameter",
            "description": element.replace('_', ' '),
            "format": "float",
            "values": all_values[element]
            }

    legislation_json = {
        "start": u'2000-01-01',
        "stop": u'2014-12-31',
        "@type": "Node",
        "children": {
            "imposition_indirecte": {
                "@type": "Node",
                "description": "Impôts et taxes indirectes",
                "children": {
                    "prix_carburants": prix_carburants,
                    "alcool_conso_et_vin": {
                        "@type": "Node",
                        "description": "alcools",
                        "children": {
                            "vin": {
                                "@type": "Node",
                                "description": "Pour calculer le taux de taxation implicite sur le vin",
                                "children": {
                                    "droit_cn_vin": {
                                        "@type": "Parameter",
                                        "description": u"Masse droit vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 129},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 130},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 129},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 132},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 133},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 127},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 127},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 127},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 127},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 125},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 117},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 119},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 117},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 114},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 117},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 119},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 118},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 120},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 122},
                                            # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                            ],
                                        },
                                    "masse_conso_cn_vin": {
                                        "@type": "Parameter",
                                        "description": u"Masse consommation vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 7191},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 7419},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 7636},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 8025},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 8451},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 8854},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 9168},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 9476},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 9695},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 9985},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 9933},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 10002},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 10345},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 10461},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 10728},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 11002},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 11387},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 11407},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 11515},
                                            # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                            ],
                                        },
                                    },
                                },
                            "biere": {
                                "@type": "Node",
                                "description": "Pour calculer le taux de taxation implicite sur la bière",
                                "children": {
                                    "droit_cn_biere": {
                                        "@type": "Parameter",
                                        "description": "Masse droit biere selon comptabilité nationale",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 361},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 366},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 364},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 365},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 380},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 359},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 364},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 361},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 370},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 378},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 364},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 396},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 382},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 375},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 376},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 375},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 393},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 783},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 897},
                                            # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                            ],
                                        },
                                    "masse_conso_cn_biere": {
                                        "@type": "Parameter",
                                        "description": u"Masse consommation biere selon comptabilité nationale",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 2111},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 2144},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 2186},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 2291},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 2334},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 2290},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 2327},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 2405},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 2554},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 2484},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 2466},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 2486},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 2458},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2287},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2375},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2461},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 2769},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2868},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 3321},
                                            # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                            ],
                                        },
                                    },
                                },
                            "alcools_forts": {
                                "@type": "Node",
                                "description": "Pour calculer le taux de taxation implicite sur alcools forts",
                                "children": {
                                    "droit_cn_alcools": {
                                        "@type": "Parameter",
                                        "description": "Masse droit alcool selon comptabilité nationale sans droits sur les produits intermediaires et cotisation spéciale alcool fort",
                                        "format": "float",
                                        "values": [
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 1872},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 1957},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 1932},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 1891},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 1908},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 1842},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 1954},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 1990},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2005},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2031},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2111},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 2150},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2225},
                                            # TODO: Problème pour les alcools forts chiffres différents entre les deux bases excel !
                                            ],
                                        },
                                    "droit_cn_alcools_total": {
                                        "@type": "Parameter",
                                        "description": u"Masse droit alcool selon comptabilité nationale avec les differents droits",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 2337},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 2350},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 2366},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 2369},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 2385},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 2416},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 2514},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 2503},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 2453},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 2409},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 2352},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 2477},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 2516},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2528},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2629},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2734},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 3078},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2718},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 3022},
                                            # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                            ],
                                        },
                                    "masse_conso_cn_alcools": {
                                        "@type": "Parameter",
                                        "description": u"Masse consommation alcool selon comptabilité nationale",
                                        "format": "float",
                                        "values": [
                                            {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 4893},
                                            {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 5075},
                                            {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 5065},
                                            {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 5123},
                                            {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 5234},
                                            {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 5558},
                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 5721},
                                            {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 5932},
                                            {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 5895},
                                            {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 5967},
                                            {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 5960},
                                            {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 6106},
                                            {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 6142},
                                            {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 6147},
                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 6342},
                                            {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 6618},
                                            {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 6680},
                                            {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 6996},
                                            {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 7022},
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    legislation_json['children']['imposition_indirecte']['children']['prix_carburants'] = prix_carburants


    return legislation_json
