# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:21:51 2021

@author: samtr
"""


import itertools
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


def bestsubset(X,y): 
    mse=np.empty(0)
    cs=[]
    mse2=np.empty(0)
    cs2=[]
    for k in range(X.shape[1]):
        for c in itertools.combinations(range(X.shape[1]),k+1):
            Xc=X.iloc[:,list(c)]
            modelc = LinearRegression()
            modelc.fit(Xc,y)
            yc_pred=modelc.predict(Xc)
            mse_sq=mean_squared_error(y,yc_pred)
            mse=np.append(mse,mse_sq)
            cs.append(c)
        argm=np.argmin(mse)
        Xc=X.iloc[:,list(cs[argm])]
        scores=cross_val_score(LinearRegression(),Xc,y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
        mse2=np.append(mse2,np.mean(scores))
        cs2.append(cs[argm])
    i=np.argmax(mse2)
    Xc=X.iloc[:,list(cs2[i])]
    model=LinearRegression()
    model.fit(Xc,y)
    model.coef_
    ret = [list(cs2[i]),model.coef_]
    return ret



def forwardsubset1(X,y):
    mse=np.empty(0)
    cs=[]
    mse2=np.empty(0)
    cs2=[]
    for k in range(X.shape[1]):
        for c in range(X.shape[1]):
            if k == 0:
                c=[c]
                Xc=X.iloc[:,c]
            elif k != 0:
                Xc1=X.iloc[:,c]
                Xc=X.iloc[:,list(cs2[k-1])]
                Xc=pd.merge(Xc,Xc1, left_index=True, right_index=True)
            modelc = LinearRegression()
            modelc.fit(Xc,y)
            yc_pred=modelc.predict(Xc)
            mse_sq=mean_squared_error(y,yc_pred)
            mse=np.append(mse,mse_sq)
            cs.append(c)
        argm=np.argmin(mse)
        Xc=X.iloc[:,list(cs[argm])]
        scores=cross_val_score(LinearRegression(),Xc,y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
        mse2=np.append(mse2,np.mean(scores))
        cs2.append(cs[argm])
    i=np.argmax(mse2)
    Xc=X.iloc[:,list(cs2[i])]
    model=LinearRegression()
    model.fit(Xc,y)
    model.coef_
    ret = [list(cs2[i]),model.coef_]
    return ret


def forwardsubset(X,y):
    mse=np.empty(0)
    cs=[]
    mse2=np.empty(0)
    cs2=[]
    par = []
    var = list(np.arange(0,X.shape[1]))
    for k in range(X.shape[1]):
        for c in itertools.combinations(var,1):
            p = list(c) + par
            Xc=X.iloc[:,list(p)]
            modelc = LinearRegression()
            modelc.fit(Xc,y)
            yc_pred=modelc.predict(Xc)
            mse_sq=mean_squared_error(y,yc_pred)
            mse=np.append(mse,mse_sq)
            cs.append(c)
        argm=np.argmin(mse)
        par.append(cs[argm][0])
        cs2.append(par.copy())
        var.remove(par[k])
    for j in range(X.shape[1]):
        Xc=X.iloc[:,cs2[j]]
        modelj = cross_val_score( LinearRegression(), Xc, y, cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
        mse2=np.append(mse2,np.mean(modelj))
    i=np.argmax(mse2)
    Xc=X.iloc[:,cs2[i]]
    model=LinearRegression()
    model.fit(Xc,y)
    model.coef_
    ret = [list(cs2[i]),model.coef_]
    return ret
   
