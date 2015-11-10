# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:27:47 2015

@author: thomas.douenne
"""

import pandas as pd
import pkg_resources
import os

# Import data_quaids to get the results of the estimation run on Stata.
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
data_quaids = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'almost_ideal_demand_system',
        'data_quaids_2005.csv'
        ), sep =',')

# Compute a weighted average of the elasticity of each household
# weights are the share of the household in total consumption
data_quaids['part_depenses_tot'] = data_quaids['depenses_tot'] / sum(data_quaids['depenses_tot'])
data_quaids.fillna(0, inplace=True)
assert 0.999 < sum(data_quaids['part_depenses_tot']) < 1.001, "the sum of the shares is not equal to 1"

for i in range(1, 4):
    data_quaids['el_{}'.format(i)] = \
        data_quaids['mu_{}'.format(i)] * data_quaids['part_depenses_tot']

# Compute the estimation of the income elasticities of consumption
resultats_elasticite_depenses = dict()
for i in range(1, 4):
    resultats_elasticite_depenses['el_{}'.format(i)] = sum(data_quaids['el_{}'.format(i)])

# Compute the 95% confidence interval for those elasticities
borne_inferieure_el_dep = dict()
borne_superieure_el_dep = dict()
for i in range(1, 4):
    borne_superieure_el_dep['borne_sup_{}'.format(i)] = (
        resultats_elasticite_depenses['el_{}'.format(i)] + 1.96 *
        (data_quaids['mu_{}'.format(i)].describe()['std'] /
        len(data_quaids['mu_{}'.format(i)]) ** 0.5)
        )
    borne_inferieure_el_dep['borne_inf_{}'.format(i)] = (
        resultats_elasticite_depenses['el_{}'.format(i)] - 1.96 *
        (data_quaids['mu_{}'.format(i)].describe()['std'] /
        len(data_quaids['mu_{}'.format(i)]) ** 0.5)
        )

