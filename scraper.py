import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time
import sqlite3
import pandas as pd
import unicodedata


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

con = sqlite3.connect('data.sqlite')
c = con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS data (volanta, titulo, bajada,cuerpo,url)""")        

urls=[]
for z in range(5):
    for y in range(13):
        for x in range(32):
            try:
                year=2012+k
                url='https://www.pagina12.com.ar/diario/secciones/index-'+str(year)+'-'+str(y)+'-'+str(x)+'.html'
                req=r.get(url)
                sopa=bs(req.content)
                for x in sopa.find('div',{'class':"columna476 left12"}).find_all('li'):
                    urls.append(uri+x.find('a').get('href'))
            except:
                pass
            time.sleep(0.2)
        time.sleep(0.2)          
    time.sleep(0.2)

data=[]
for x in urls:
    nota=p12()
    try:
        nota.get(x)
        row=[nota.volanta,nota.titulo,nota.bajada,nota.cuerpo,nota.url]
        c.execute('insert into data2 values (?,?,?,?,?)', row)
        con.commit()        
    except:
        pass
    time.sleep(0.2)
    

