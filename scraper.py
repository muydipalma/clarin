import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time
import sqlite3
import pandas as pd
import unicodedata



df=pd.read_csv('p12_2010.csv')

class p12():
    
    def __init__(self):
        self.url='https://www.pagina12.com.ar'
    
    def get(self,url):
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.volanta=unicodedata.normalize("NFKD",sopa.find('p',{'class':'volanta'}).get_text(strip=True))
        self.titulo=unicodedata.normalize("NFKD",sopa.find('h2').get_text(strip=True))
        self.bajada=unicodedata.normalize("NFKD",sopa.find('p',{'class':'intro'}).get_text(strip=True))
        self.cuerpo=unicodedata.normalize("NFKD",sopa.find('div',{'id':'cuerpo'}).get_text(strip=True))
        self.url=url

data=[]
for x in df.urls[:10000]:
    nota=p12()
    try:
        nota.get(x)
        data.append([nota.volanta,nota.titulo,nota.bajada,nota.cuerpo,nota.url])
    except:
        pass
    time.sleep(0.2)
    
    
df2=pd.DataFrame.from_records(data,columns=['volanta','titulo','bajada','cuerpo','url'])

con = sqlite3.connect('data.sqlite')
df2.to_sql('data', con)
