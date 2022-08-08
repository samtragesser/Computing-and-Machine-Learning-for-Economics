# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Part 1
import pandas as pd
fulldata = pd.read_csv("london_crime.csv")
fulldata["crimerate"] = (fulldata.crime)/(fulldata.population)
fulldata["policerate"] = (fulldata.police)/(fulldata.population)
import numpy as np
fulldata["lcrime"] = np.log(fulldata.crimerate)
fulldata["lpolice"] = np.log(fulldata.policerate)
fulldata["lemp"] = np.log(fulldata.emp)
fulldata["lun"] = np.log(fulldata.un)
fulldata["lymale"] = np.log(fulldata.ymale)
fulldata["lwhite"] = np.log(fulldata.white)
import statsmodels.formula.api as smf
model1 = smf.ols("lcrime ~ lpolice + lemp + lun + lymale + lwhite",data=fulldata).fit()

#Part2
dlcrime = (np.array(fulldata.lcrime[fulldata.week >= 53])) - (np.array(fulldata.lcrime[fulldata.week <= 52]))
dlpolice = (np.array(fulldata.lpolice[fulldata.week >= 53])) - (np.array(fulldata.lpolice[fulldata.week <= 52]))
dlun = (np.array(fulldata.lun[fulldata.week >= 53])) - (np.array(fulldata.lun[fulldata.week <= 52]))
dlemp = (np.array(fulldata.lemp[fulldata.week >= 53])) - (np.array(fulldata.lemp[fulldata.week <= 52]))
dlymale = (np.array(fulldata.lymale[fulldata.week >= 53])) - (np.array(fulldata.lymale[fulldata.week <= 52]))
dlwhite = (np.array(fulldata.lwhite[fulldata.week >= 53])) - (np.array(fulldata.lwhite[fulldata.week <= 52]))
diffdata = pd.DataFrame({"dlcrime": dlcrime,"dlpolice": dlpolice,"dlun": dlun,"dlemp": dlemp,"dlymale": dlymale,"dlwhite": dlwhite})
model2 = smf.ols("dlcrime ~ dlpolice + dlemp + dlun + dlymale + dlwhite",data=diffdata).fit()

#Part3
diffdata["sixweeks"] = np.array((fulldata[fulldata.week > 52].week >= 80) & (fulldata[fulldata.week > 52].week <= 85), dtype = int)
diffdata["treat"] = np.array((fulldata[fulldata.week > 52].borough == 1) | (fulldata[fulldata.week > 52].borough == 2) | (fulldata[fulldata.week > 52].borough ==3 ) | (fulldata[fulldata.week > 52].borough == 6) | (fulldata[fulldata.week > 52].borough == 14))
diffdata["sixweeks_treat"] = diffdata.sixweeks * diffdata.treat
model3 = smf.ols("dlcrime ~ dlemp + dlun + dlymale + dlwhite + sixweeks + sixweeks_treat",data=diffdata).fit()