# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 00:07:00 2021

@author: samtr
"""

import pandas as pd
import numpy as np
ncaa = pd.read_pickle("ncaa.pkl")


def colley_rank(ncaa):
    A = np.zeros((len(ncaa),len(ncaa)))
    b = np.zeros(len(ncaa))
    for i in range(0,len(ncaa)):
        A[i,i] = 2+(ncaa.opponents[i].size)
        b[i] = 1 + (ncaa.wins[i] - ncaa.losses[i])/2
        for j in ncaa.opponents[i]:
            A[i,j] = A[i,j] - 1
    x = np.matmul(np.linalg.inv(A),b)
    df2 = pd.DataFrame({"team": ncaa['team'],"score": x})
    df2 = df2.sort_values(by=['score'],ascending=False)
    result = [df2,A,b]
    return(result)

