import requests

from bs4 import BeautifulSoup
import pymongo
import csv 
import uuid 

def extractUrl(URL):
    markup = requests.get(f'URL').text
    soup = BeautifulSoup(markup, 'html.parser')
    return soup 
def saveCSV():
     
    with open('O:\Databrute2.csv','w') as file:
        wr = csv.writer(file)
        wr.writerow(["Text","score"])
   
    

  
#from https://blog.digimind.com/fr/tendances/covid-30-fake-news-les-plus-repandues-sur-medias-sociaux
def fakenewsDB(score):
    mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
    db = mongo.News
    i=1
    text=[]
    markup = requests.get(f'https://blog.digimind.com/fr/tendances/covid-30-fake-news-les-plus-repandues-sur-medias-sociaux').text
    soup = BeautifulSoup(markup, 'html.parser')
    parent = soup.find('table',attrs={'style':'border-color: #f4cccc; border-collapse: collapse; table-layout: fixed; margin-left: auto; margin-right: auto; height: 1188px; width: 681px; border-style: dotted;'})
    for Fchild in parent.find_all('tbody'):
        rows = Fchild.find_all('tr')
        for td in rows:
             subteam =td.find_all('td')
             for sub in subteam:
                 i=i+1-2
                 span={}
                 span['id']=uuid.uuid1()
                 span['title']="About Covid-19  "
                 span['content']=sub.find('span').text.strip()
                 span['classe']=score
                 text.append(span)
    list=text[1::2]
    dbResponse = db.app_news.insert_many(list)
    print(dbResponse.inserted_ids)
    
mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
db = mongo.News

def TrueNews(score):
     more_links = True
     page = 1
     mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
     db = mongo.News
     text=[]
     for page in range(2,20):
         markup = requests.get(f'https://www.francetvinfo.fr/sante/maladie/coronavirus/{page}.html').text
         soup = BeautifulSoup(markup, 'html.parser')
         parent = soup.find('ul',attrs={'class':'taxonomy-contents taxonomy-contents--default'})
         for li in parent.find_all('li'):
             article = li.find_all('article')
             for a in article:
                 span={}
                 span['id']=uuid.uuid1()
                 div = a.find_all('div',attrs={'class':'taxonomy-content__text-wrapper'})
                 for p in div:
                     span['title']= p.find('p').text.strip()
                 #print(text)
                 for div in div:
                     span['content']= div.find('div').text.strip()
                     span['classe']=score
                 text.append(span)
         
         print(f'scraped page {page}')
       
     
     dbResponse = db.app_news.insert_many(text)
     
     print(dbResponse.inserted_ids)

def insertdb(content):
    mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
    db = mongo.News
    text=[]
    span={}
    span['id']=uuid.uuid1()
    span['title']="About Covid-19  "
    span['content']=content
    span['classe']=0
    text.append(span)
    dbResponse = db.app_news.insert_many(text)


# insertdb('Les mesures de protection dans les prisons marocaines ne sont pas suffisantes.')
# insertdb('Les médicaments contre l’hypertension augmentent le risque de contracter la maladie du Covid-19 ou d’en développer des formes sévères')
# insertdb('L’Organisation mondiale de la santé (OMS) admet que les vaccins ne fonctionneront pas contre le coronavirus.')
# insertdb('Acquisition, par le ministère de la santé, de tests de diagnostic rapide du coronavirus dont la date de validité a expiré')
# insertdb('L’application « Wiqaytna » de notification d’exposition au nouveau coronavirus (Covid-19) collecte les données de contact')
# insertdb('Pour ceux qui le peuvent, il est important de s’exposer le plus possible au soleil en accord avec vos conditions climatiques actuelles.')
# insertdb('Prendre un bain chaud pour tuer le virus. ')
# insertdb('Surtout éviter de boire de l’eau glacée ou de sucer des glaces ou glaçons ou la neige pour ceux qui sont à la montagne, en particulier les enfants')
# insertdb('Le coronavirus, avant d’arriver aux poumons, reste dans la gorge pendant quatre jours et la personne a mal à la gorge et tousse. Si la personne boit souvent de l’eau et se gargarise avec de l’eau chaude, du sel et du vinaigre, elle éliminera le virus.')
# insertdb(' Se rincez le nez avec de l’eau salée protège contre le coronavirus')
# insertdb('le Covid-19 a  été créé dans un laboratoire en France')
# insertdb('le virus est une création de l’homme')
# insertdb('e virus s’est échappé d’un laboratoire P4 installé à Wuhan')
# insertdb('Le froid peut tuer le coronavirus ')
# insertdb('Les Africains sont plus résistants face au virus')
# insertdb('urine des enfants désinfecte efficacement et protège du virus')
# insertdb('Le cannibalisme est à l’origine du virus')
# insertdb('Le virus se transmet par les moustiques')
# insertdb('Les chauves-souris sont à l’origine de la propagation du virus')
# insertdb('les vaccins contre la COVID-19  contiennent  de tissus embryons humains')
# insertdb('les vaccins à ARN messager modifient l’ADN')
# insertdb('Les masques  provoquent  cérébrale')
# insertdb('Les mesures de protection dans les prisons marocaines ne sont pas suffisantes.')

fakenewsDB(0)
TrueNews(1)


 








#fakenewsDB('https://blog.digimind.com/fr/tendances/covid-30-fake-news-les-plus-repandues-sur-medias-sociaux','0')

#saveCSV()

