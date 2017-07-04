# -*- coding: utf-8 -*-

from __future__ import division


# Dans ce script on compare la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    homogenize_variables_definition_bdf_enl


data = homogenize_variables_definition_bdf_enl()    
data_enl = data[0]
data_bdf = data[1]


# aba - aides au logement
# 1 = Oui, 2 = Non, 0 = ?
for i in [0, 1, 2]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.aba == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]
    
    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.aba == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # fonctionne bien


# amr - montant des aides au logement
amr_bdf = data_bdf.query('aba == 1')
amr_enl = data_enl.query('aba == 1')
print (amr_bdf['amr'] * amr_bdf['pondmen']).sum() / amr_bdf['pondmen'].sum()
print (amr_enl['amr'] * amr_enl['pondmen']).sum() / amr_enl['pondmen'].sum()

print data_bdf['amr'].quantile([0.8, 0.85, .9, 0.95, 0.99, 0.995, 0.999])
print data_enl['amr'].quantile([0.8, 0.85, .9, 0.95, 0.99, 0.995, 0.999])
del amr_bdf, amr_enl
# fonctionne moyennement : plus d'aide au logement dans l'ENL


# cataeu - catégorie de la commune
# 111 : grand pôle, 112 : couronne d'un GP, 120: multipolarisé grande aire urbaine,
# 211 : moyen pôle, 212 : couronne MP, 221 : petit pôle, 222 : couronne PP,
# 300 : autre multipolarisé, 400 : isolée
for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]: 
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cataeu == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]
    
    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.cataeu == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # fonctionne plutôt bien


# mfac_eau1_d - montant annuel des dépenses d'eau, redressé
print (data_bdf['mfac_eau1_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['mfac_eau1_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_enl['mfac_eau1_d'].mean()
# fonctionne mal, dépenses beaucoup plus importantes dans ENL


# poste_coicop_45(1,2,3) - dépenses d'électricité, de gaz et de fioul domestique
for i in [1, 2, 3]:
    print (data_bdf['poste_coicop_45{}'.format(i)] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    print (data_enl['poste_coicop_45{}'.format(i)] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
    print ' '
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf['poste_coicop_45{}'.format(i)] > 0] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl['poste_coicop_45{}'.format(i)] > 0] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Fonctionne plutôt bien


# poste_coicop_4511 - déclaration jointe gaz-électricité
print (data_bdf['poste_coicop_4511'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['coml13'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

data_bdf['pondmen_bis'] = 0
data_bdf['pondmen_bis'].loc[data_bdf['poste_coicop_4511'] > 0] = data_bdf['pondmen']
part_bdf = data_bdf['pondmen_bis'].sum() / data_bdf['pondmen'].sum()
del data_bdf['pondmen_bis']

data_enl['pondmen_bis'] = 0
data_enl['pondmen_bis'].loc[data_enl['coml13'] > 0] = data_enl['pondmen']
part_enl = data_enl['pondmen_bis'].sum() / data_enl['pondmen'].sum()
del data_enl['pondmen_bis']

print (part_bdf * 100), 'BdF'
print (part_enl * 100), 'ENL'
print ' '
del part_bdf, part_enl
# Très mauvaises performances : beaucoup plus de déclarations jointes dans BdF


# Dépenses énergies logement
data_bdf['energies'] = (
    data_bdf['poste_coicop_4511'] + data_bdf['poste_coicop_451']
    + data_bdf['poste_coicop_452'] + data_bdf['poste_coicop_453']
    )
data_enl['energies'] = (
    data_enl['coml13'] + data_enl['poste_coicop_451']
    + data_enl['poste_coicop_452'] + data_enl['poste_coicop_453']
    )
print (data_bdf['energies'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['energies'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_bdf['energies'].quantile([0.8, 0.85, .9, 0.95, 0.99, 0.995, 0.999])
print data_enl['energies'].quantile([0.8, 0.85, .9, 0.95, 0.99, 0.995, 0.999])

data_bdf_limited = data_bdf.query('energies < 6000')
data_bdf_limited['energies'].hist(cumulative=True, normed=1, bins=100)
data_enl_limited = data_enl.query('energies < 6000')
cumul_enl = data_enl_limited['energies'].hist(cumulative=True, normed=1, bins=100)
zero_bdf = data_bdf.query('energies == 0')
zero_enl = data_enl.query('energies == 0')
# Fonctionne plutôt bien


# nbh1 - nombre d'enfants vivant hors du domicile
for i in [0, 1, 2, 3, 4, 5]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nbh1 == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]
    
    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.nbh1 == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Fonctionne très bien (mais variable probablement inutile...)


# mchof_d - montant annuel des dépenses en chauffage collectif
print (data_bdf['mchof_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['mchof_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
# Catastrophique...


# nbphab - nombre de pièces habitables
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nbphab == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]
    
    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.nbphab == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Très Bonnes performances


# surfhab_d - surface habitable en m²
print (data_bdf['surfhab_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['surfhab_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_bdf['surfhab_d'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
print data_enl['surfhab_d'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
# Très bon en moyenne, mais sans les pondérations les surfaces sont un peu inférieures dans ENL


# htl - type de logement
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.htl == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.htl == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Assez bonnes performances -> revoir la définition


# ancons - année de construction
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ancons == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.ancons == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Petit problème sur 8, 9 et 10 + problème des 99 de BdF -> revoir la définition


# mloy_d - montant mensuel du loyer hors charges
print (data_bdf['mloy_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['mloy_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_enl['mloy_d'].mean()
# résultats catastrophiques


# agepr - age de la personne de référence
print (data_bdf['agepr'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['agepr'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_bdf['agepr'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
print data_enl['agepr'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
# Bons résultats


# cs42pr - catégorie socioprofessionnelle de la personne de référence
for i in range(11,87):
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cs42pr == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.cs42pr == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # 13 et 44 produisent des mauvais résultats, pour le reste ça va


# cs42cj - catégorie socioprofessionnelle du conjoint
for i in range(11,87):
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cs42cj == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.cs42cj == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # 12, 13, 23 en particulier sont mauvais, pas mal dans l'ensemble


# dip14pr - diplôme de la personne de référence
for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.dip14pr == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.dip14pr == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Bien


# nenfants - nombre d'enfants à charge
for i in [0, 1, 2, 3, 4, 5, 6]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nenfants == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.nenfants == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Bon dans l'ensemble


# nactifs - nombre d'actifs
for i in [0, 1, 2, 3, 4]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nactifs == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.nactifs == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Super


# revtot - revenu total du ménage
print (data_bdf['revtot'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
print (data_enl['revtot'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

print data_bdf['revtot'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
print data_enl['revtot'].quantile([0.05, 0.2, 0.4, .6, 0.8, 0.95])
# Plutôt bon, mais la distribution de l'ENL est un peu plus dispersée


# situapr - occupation principale de la personne de référence
for i in [1, 2, 3, 4, 5, 6, 7]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.situapr == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.situapr == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Plutôt bien


# situacj - occupation principale de la personne de référence
for i in [1, 2, 3, 4, 5, 6, 7]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.situacj == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.situacj == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Bien
    

# ocde10 - unités de consommations
for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ocde10 == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.ocde10 == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Bien


# tau - taille de l'aire urbaine par tranche
for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tau == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.tau == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Quelques petits soucis (2,5,6) mais ça va


# tuu - taille de l'unité urbaine par tranche
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tuu == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.tuu == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Pas mal


# zeat - zone d'étude et d'aménagement du territoire
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    data_bdf['pondmen_{}'.format(i)] = 0
    data_bdf['pondmen_{}'.format(i)].loc[data_bdf.zeat == i] = data_bdf['pondmen']
    part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
    del data_bdf['pondmen_{}'.format(i)]

    data_enl['pondmen_{}'.format(i)] = 0
    data_enl['pondmen_{}'.format(i)].loc[data_enl.zeat == i] = data_enl['pondmen']
    part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
    del data_enl['pondmen_{}'.format(i)]

    print (part_bdf * 100), 'BdF', '{}'.format(i)
    print (part_enl * 100), 'ENL', '{}'.format(i)
    print ' '
    del part_bdf, part_enl
    # Très bien !