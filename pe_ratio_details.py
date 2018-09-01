import pymysql
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from pandas.io import sql
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:"+'Bridge@1234'+"@localhost/CogntiveScale")
db=pymysql.connect('localhost','root','Bridge@1234','CogntiveScale')
cursor=db.cursor()
sql='select name,url from sector_wise_company;'

df2=pd.read_sql(sql,db)


all_info=[]
bucket_array=np.linspace(0,699,num=700/5)
#print type(bucket_array)
# n denotes the number of companies, here just for sample I have taken 100
n=100
for info in range(0,n):
    #len(df2['name'])
    url=df2.iloc[info][1]
    company_name=df2.iloc[info][0]
    #print company_name
    res=requests.get(url).content
    s=BeautifulSoup(res,'lxml',from_encoding="windows-1259")

    all=s.find_all('div',{'class':"PA7 brdb"})

    #print all
    #print type(all[0])
    count=1
    
    l=[]
    l.append(company_name)
    for attr in all:
        #print attr
        col_name=(attr.find('div',{'class':"FL gL_10 UC"})).text
        if col_name == 'P/E' and count==1:
            #print "P/E  Standalone:" + (attr.find('div',{'class':"FR gD_12"})).text
            count=2
            l.append(((attr.find('div',{'class':"FR gD_12"})).text).encode('ascii','ignore'))
        elif col_name == 'P/E' and count==2:
            #print "P/E  Consolidated:" + (attr.find('div',{'class':"FR gD_12"})).text
            count=1
            l.append(((attr.find('div',{'class':"FR gD_12"})).text).encode('ascii','ignore'))
            break
          
    all_info.append(l)


df=pd.DataFrame(all_info,columns=['Company Name','P/E  Standalone','P/E  Consolidated'])

stand = []
conso=[]
for x in df['P/E  Standalone']:
    try:
        stand.append(float(x.encode('ascii','ignore')))
    except:
        stand.append(0)

for x in df['P/E  Consolidated']:
    try:
        conso.append(float(x.encode('ascii','ignore')))
    except:
        conso.append(0)


df['P/E  Standalone Bucket'] = pd.cut(np.array(stand),bucket_array)
df['P/E  Consolidated Bucket'] = pd.cut(np.array(conso), bucket_array)
print df.groupby('P/E  Standalone Bucket')['Company Name'].apply(list)

print df.groupby('P/E  Consolidated Bucket')['Company Name'].apply(list)