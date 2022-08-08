# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 21:30:03 2021

@author: samtr
"""

import pandas as pd

  
def ncaaimport(year):
    df= pd.read_fwf("https://wilson.engr.wisc.edu/rsfc/history/howell/cf"+str(year)+"gms.txt", [(0,10),(10,39),(39,41),(41,71),(71,73),(73,123)], header=None, names=['date','awayteam', 'awayscore', 'hometeam', 'homescore', 'location'])
    df2 = df.groupby("awayteam")[["awayteam"]].count()
    df3 = df.groupby("hometeam")[["hometeam"]].count()
    df4 = pd.merge(df2,df3,left_index=True,right_index=True,how='outer').reset_index()
    df4.rename(columns={'index': 'TeamName'}, inplace=True)
    df4["TotalGames"] = df4.awayteam + df4.hometeam
    df4=df4[df4.TotalGames>=6]
    d1team=df4.TeamName.tolist()
    df=df[df['awayteam'].isin(d1team)] 
    df=df[df['hometeam'].isin(d1team)]
    df = df[df.awayscore != df.homescore]
    df["awaywin"] = df.awayscore>df.homescore
    df["homewin"] = df.homescore>df.awayscore       
    df5 = df.groupby(["awayteam"]).agg({"awayteam":"count","awaywin":"sum"})
    df5['team'] = df5.index
    df6 = df.groupby(["hometeam"]).agg({"hometeam":"count","homewin":"sum"})
    df6['team'] = df6.index
    df7 = pd.merge(df5,df6,left_on="team",right_on="team")
    df7["wins"] = df7.awaywin + df7.homewin
    df7["losses"] = df7.awayteam + df7.hometeam - df7.wins
    mapping = pd.Series(range(len(df7)),df7.team)
    df["homeid"] = df.awayteam.map(mapping)
    df["awayid"] = df.hometeam.map(mapping)
    homeops = df.groupby("homeid").agg({"awayid":list}).reset_index()
    awayops = df.groupby("awayid").agg({"homeid":list}).reset_index()
    df_opp = pd.merge(homeops, awayops, right_index=True,left_index=True,how='outer').reset_index()
    df_opp['opponents'] = df_opp.awayid_x + df_opp.homeid_y
    df_opp = df_opp.dropna()  
    df_final = pd.DataFrame({"team":df7.team,"wins":df7.wins,"losses":df7.losses,"opponents":df_opp.opponents})
    return(df_final)

