# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 11:40:33 2021

@author: samtr
"""

from bs4 import BeautifulSoup
import urllib.request as url
import pandas as pd


def worldbankimport(code,year):
    urlstring = "https://api.worldbank.org/v2/country/all/indicator/"+(code)+"?date="+str(year)+""
    req = url.Request(urlstring)    
    file = url.urlopen(req)
    soup = BeautifulSoup(file,"xml")
    xmldf = pd.DataFrame()
    catalog=soup.contents[0]
    for i in range(len(catalog.find_all(True, recursive=False))):
        row=catalog.find_all(True, recursive=False)[i]
        cells = row.contents
        rowdict = {}
        for j in range(len(cells)):
            rowdict[cells[j].name] = cells[j].string
        xmldf=xmldf.append(rowdict,ignore_index=True)
    pages = int(catalog["pages"]) + 1
    for i in range(2,pages):
         urlstring = "https://api.worldbank.org/v2/country/all/indicator/"+(code)+"?date="+str(year)+"&page="+str(i)+""
         req = url.Request(urlstring)    
         file = url.urlopen(req)
         soup = BeautifulSoup(file,"xml")
         catalog=soup.contents[0]
         for i in range(len(catalog.find_all(True, recursive=False))):
             row=catalog.find_all(True, recursive=False)[i]
             cells = row.contents
             rowdict = {}
             for j in range(len(cells)):
                 rowdict[cells[j].name] = cells[j].string
             xmldf=xmldf.append(rowdict,ignore_index=True)
    xmldf = xmldf.iloc[: , 1:]
    return(xmldf)
