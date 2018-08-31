import requests
from bs4 import BeautifulSoup
from time import sleep
import pymysql
#pymysql.install_as_MySQLdb()
db=pymysql.connect('localhost','root','Bridge@1234','CogntiveScale')
#cursor=db.cursor()
def find_nth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

res=requests.get('http://www.moneycontrol.com/india/stockpricequote').content
s=BeautifulSoup(res,'html.parser')
p=s.find_all('a',{"class":'bl_12'})
#print (p)
sector_wise_company=[]
cursor=db.cursor()
cursor.execute('Drop table if exists sector_wise_company')
print "Table sector_wise_company dropped successfully"
sql = """CREATE TABLE sector_wise_company (
         url  CHAR(255),
         sector  CHAR(200),
        name CHAR(100) )"""
cursor.execute(sql)
print "Table sector_wise_company created successfully"
sql="Insert into sector_wise_company (url,sector,name) values (%s,%s,%s)"
for det in p:
    try:
        
        ex= det.get('href')
        name=(det.get('title')).encode('ascii','ignore')
        url=ex.encode('ascii','ignore')
        sector=url[find_nth(url,'/',4)+1:find_nth(url,'/',5)]
        if name not in 'Customize':
            print "Sector Name : "+ sector
            print "Company Name : "+name
            sector_wise_company.append([url,sector,name])
            
            cursor.execute(sql,(url,sector,name))
            db.commit()
    except:
        print "Not Found"
db.close()


#http://www.moneycontrol.com/india/stockpricequote/diversified/3mindia/MI42

