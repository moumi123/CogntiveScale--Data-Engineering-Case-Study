import requests
from bs4 import BeautifulSoup
from time import sleep
import pymysql
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:"+'Bridge@1234'+"@localhost/CogntiveScale")
db=pymysql.connect('localhost','root','Bridge@1234','CogntiveScale')
cursor=db.cursor()
cursor.execute('Drop table if exists market_cap')


df=pd.read_html('https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html',attrs = {"class":'tbldata14'})
df=df[0]

df.columns=df.iloc[0]


df=df.drop(df.index[0])

df['new_company_name']=map(lambda x:x.replace('Add to Watchlist  Add to Portfolio',''),df['Company Name'])
df=df.drop(['Company Name','Last Price','% Chg', '52 wkHigh','52 wkLow'],axis=1)
df. rename(columns={'new_company_name': 'Company_Name'}, inplace=True)
df. rename(columns={'Market Cap(Rs. cr)': 'Market_Cap_Value'}, inplace=True)
df.to_sql("market_cap",engine,if_exists='replace')

sql="select * from (\
(select Company_Name,sector,Market_Cap_Value \
from (select Company_Name,sector,Market_Cap_Value from Market_cap  mc join sector_wise_company swc on mc.Company_Name=swc.name)temp1 \
where 3=(select count(distinct Market_Cap_Value) from (select Company_Name,sector,Market_Cap_Value from Market_cap  mc join sector_wise_company swc on mc.Company_Name=swc.name) temp2 \
where temp1.sector=temp2.sector and temp1.Market_Cap_Value<=temp2.Market_Cap_Value) \
order by Company_Name) \
union \
(\
select Company_Name,sector,Market_Cap_Value \
from (select Company_Name,sector,Market_Cap_Value from Market_cap  mc join sector_wise_company swc on mc.Company_Name=swc.name)temp1 \
where 4=(select count(distinct Market_Cap_Value) from (select Company_Name,sector,Market_Cap_Value from Market_cap  mc join sector_wise_company swc on mc.Company_Name=swc.name) temp2 \
where temp1.sector=temp2.sector and temp1.Market_Cap_Value<=temp2.Market_Cap_Value) \
order by Company_Name\
)) p \
order by sector,Market_Cap_Value desc;"
df2=pd.read_sql(sql,db)
print df2
