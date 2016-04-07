# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame

for year in [2000, 2005, 2011]:
    aggregates_data_frame = get_input_data_frame(year)
    if year == 2000:
        df = aggregates_data_frame[['poste_07_2_2_1_1', 'coicop12_7', 'poste_07_1_1_1_1'] +
            ['poste_07_1_2_1_1', 'poste_07_1_3', 'poste_721', 'poste_723'] +
            ['poste_724', 'poste_731', 'poste_732', 'poste_733'] +
            ['poste_734', 'poste_736']].copy()
        df['check'] = (
            df['poste_07_1_1_1_1'] + df['poste_07_1_2_1_1'] + df['poste_07_1_3'] + df['poste_721'] +
            df['poste_07_2_2_1_1'] + df['poste_723'] + df['poste_724'] + df['poste_731'] +
            df['poste_732'] + df['poste_733'] + df['poste_734'] + df['poste_736'] -
            df['coicop12_7']
            )
    else:
        df = aggregates_data_frame[['poste_07_2_2_1_1', 'coicop12_7', 'poste_07_1_1_1_1'] +
            ['poste_07_1_2_1_1', 'poste_735', 'poste_07_1_3', 'poste_721'] +
            ['poste_723', 'poste_724', 'poste_731', 'poste_732'] +
            ['poste_733', 'poste_734', 'poste_736']].copy()
        df['check'] = (
            df['poste_07_1_1_1_1'] + df['poste_07_1_2_1_1'] + df['poste_07_1_3'] + df['poste_721'] +
            df['poste_07_2_2_1_1'] + df['poste_723'] + df['poste_724'] + df['poste_731'] +
            df['poste_732'] + df['poste_733'] + df['poste_734'] + df['poste_736'] +
            df['poste_735'] - df['coicop12_7']
            )
    assert_near(df['check'].any(), 0, 0.0001), "the total of transport differs from the sum of its components"
