# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 14:27:34 2021

@author: samtr
"""
import pandas as pd
import numpy as np
df = pd.read_pickle("ncaa.pkl")

def colley_iter(df,t):
    r = np.array((1 + df.wins)/(2 + df.wins + df.losses))
    effwins = np.zeros(df.shape[0])
    n=0
    q = 1000000
    while q > t:
        n = n+1
        r1 = r.copy()
        for i in range(len(df.wins)):
           effwins[i] = np.array((df.wins[i] - df.losses[i])/2 + sum(r[df.opponents[i]]))
        r = np.array((1 + effwins)/(2 + df.wins + df.losses))
        q = max(abs(r1-r))
        
    df2 = pd.DataFrame({"team": df['team'],"score": r})
    df2 = df2.sort_values(by=['score'],ascending=False)
    result = [df2, n]
    return(result)
    
    