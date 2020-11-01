import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time

class clarin():
    def __init__(self):
        self.url='https://www.clarin.com'
    
    
    urlc='https://login.clarin.com/comments.getComments'
    urlcp='https://login.clarin.com/comments.getComments?categoryID=Com_03&streamID=H1Y2WMTS-&includeSettings=true&threaded=true&includeStreamInfo=true&includeUserOptions=true&includeUserHighlighting=true&lang=es&ctag=comments_v2&APIKey=2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW&source=showCommentsUI&sourceData=%7B%22categoryID%22%3A%22Com_03%22%2C%22streamID%22%3A%22H1Y2WMTS-%22%7D&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fwww.clarin.com%2Fpolitica%2Facuerdo-cambiemos-massismo-echar-vido-camara-diputados_0_H1Y2WMTS-.html&format=jsonp&callback=gigya.callback&context=R4169081209'
    urlp=urllib.parse.urlparse(urlcp)
    keys=urllib.parse.parse_qs(urlp.query)
 
    
    def get(self,url):

        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','body-nota').findAll('p')
        st=sopa.find('div','body-nota').findAll('strong')
        self.volanta=sopa.find('p','volanta').text
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div','bajada').find('h2').text
        texto=list()
        for p in ps:
            if p.text == "COMENTARIOS":
                break
            texto.append(p.text)
        bolds=list()    
        for b in st:
            bolds.append(b.text)            
        self.cuerpo=' '.join(texto)
        self.bold=' '.join(bolds)
        self.bolds=bolds
        keys=self.keys
        keys['pageURL'][0]=url
        keys['streamID'][0]=url[-14:-5]
        cm=r.get(self.urlc,params=keys)
        d = json.loads(cm.text[15:-2])
        self.comm=[x['commentText'] for x in d['comments']]
        self.com=' '.join(self.comm)
      
    def hoy(self):            
        notas=r.get(self.url)
        sopa=bs(notas.content,features="lxml")
        urls=[x.find('a').get('href') for x in sopa.find_all('article')]
        boxs=list()

        for x in sopa.find_all('div', {'class':'on-demand'}):
            boxs.append(self.url+x.get('data-src'))

        reqs=list()
        # son 69 pero hasta el 8 tienen cosas
        for x in boxs[:9]:
            reqs.append(r.get(x))
            #para evitar ban pongo pausa
            time.sleep(0.2)

        box0=json.loads(reqs[0].content.decode().strip('()'))['data']
        sopa0=bs(box0,features="lxml")

        for x in sopa0.find_all('a'): 
            urls.append(x.get('href'))


        for n,x in enumerate(reqs[1:]):
            box=json.loads(x.content.decode().strip('()'))['data']
            sopa=bs(box,features="lxml")
            for y in sopa.find_all('article'):      
                urls.append(y.find('a').get('href'))                                        

        box7=json.loads(reqs[7].content.decode().strip('()'))['data']
        sopa7=bs(box7,features="lxml")
        for x in sopa7.find('div',{'class':'mas-vistas'}).find_all('div')[1].find_all('div',{'onclick' : True}):
            urls.append(x.get('onclick')[13:-11])  
        urls2=list()    
        for u in urls:
            if u[:4] == 'http':
                urls2.append(u)
            else:
                urls2.append('https://www.clarin.com'+u)
        self.urls=urls2   


def get(lista):
    arts=list()
    print('total notas: '+ str(len(lista)))
    for j,u in enumerate(lista):
        if u[:23] == 'https://www.clarin.com/':
            art=clarin()
            try:
                art.get(u)
                time.sleep(0.2)
                #print(j,u)
                #print('ok')
                arts.append(art)
            except:
                print(j,u)
                print('fail') 
        else:
            pass
    return(arts)   


cl=clarin()
cl.hoy()
urls=cl.urls

get(urls)