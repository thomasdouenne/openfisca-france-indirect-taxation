# -*- coding: utf-8 -*-

from __future__ import division


import pandas as pd


df_voyage = pd.read_stata('C:/Users/t.douenne/Documents/Data/data_entd/entd_2008/Stata/k_voyage.dta')
df_voyage_det = pd.read_stata('C:/Users/t.douenne/Documents/Data/data_entd/entd_2008/Stata/k_voydepdet.dta')
df_mobilite = pd.read_stata('C:/Users/t.douenne/Documents/Data/data_entd/entd_2008/Stata/k_mobilite.dta')
df_deploc = pd.read_stata('C:/Users/t.douenne/Documents/Data/data_entd/entd_2008/Stata/k_deploc.dta')
df_menage = pd.read_stata('C:/Users/t.douenne/Documents/Data/data_entd/entd_2008/Stata/q_menage.dta')

print df_voyage_det['v2_oldmt1s']
print len(df_voyage_det.query('v2_oldmt1s == 7.70'))

bibi = df_voyage_det.drop_duplicates('ident_men')
print len(bibi.query('v2_oldmt1s == 7.70'))

bobo = df_voyage_det.query('v2_oldmt1s == 7.70')
print len(bobo.drop_duplicates('ident_men'))



data_menage_voyage = df_voyage.merge(df_menage, on = 'ident_men')
data = data_menage_voyage.drop_duplicates('ident_men')
