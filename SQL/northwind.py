# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 00:37:34 2021

@author: samtr
"""

import sqlite3
import pandas as pd

con = sqlite3.connect("northwind.db") 
con.text_factory = lambda b: b.decode(errors = 'ignore')  #a "hack" because some album names in this database have characters that cause an error to be thrown 

d1 = pd.read_sql_query("select * from Orders where ShipCountry='USA'",con)
d2 = pd.read_sql_query("select distinct Country from Customer",con)
d3 = pd.read_sql_query("select Country, count(Id) from Customer group by Country having count(Id)>1 order by Count(Id) desc" ,con)
d4 = pd.read_sql_query("select Orders.Id from Orders join Customer on Orders.CustomerId=Customer.Id where ShipCountry!=Country",con)
d5 = pd.read_sql_query("select OrderId,sum((1-Discount)*UnitPrice*Quantity) as Revenue from OrderDetail group by OrderId",con)
d6 = pd.read_sql_query("select Orders.Id,OrderDate,sum((1-Discount)*UnitPrice*Quantity) as Revenue from Orders join OrderDetail on Orders.Id=OrderDetail.OrderId join Customer on Orders.CustomerId=Customer.Id where Customer.Country='USA' group by OrderId",con)
d7 = pd.read_sql_query("select distinct CompanyName from Customer join Orders on Orders.CustomerId=Customer.Id where ShipCity='Eugene'",con)
d8 = pd.read_sql_query("select distinct CompanyName from Customer join Orders as O1 on O1.CustomerId=Customer.Id join Orders as O2 on O2.CustomerId=Customer.Id where O1.ShipCity='Eugene' and O2.ShipCity='Eugene' and O1.CustomerId=O2.CustomerId and O1.Id!=O2.Id",con)

def orderlookup(city, country):
    d9 = pd.read_sql_query("select * from Orders where ShipCity=? and ShipCountry=?",con, params=[city,country])
    return(d9)

