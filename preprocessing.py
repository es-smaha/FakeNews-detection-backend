from typing_extensions import Concatenate
import pandas as pd
import string
import re
import pymongo
import sklearn as sklearn
from mongoengine import connect
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC



def ExtractDataFromDb():
    try:
        # --- Connection to Mongodb --- #
        mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
        db = mongo.News

        # --- Connection to our database --- #
        connect('News', host='mongodb://localhost', alias='default')
        #fetch data
        cursor=db['app_news'].find()
        ids=[]
        classes=[]
        concat=[]
        #loop documents
        for doc in cursor:
            ids.append(doc['_id'])
            classes.append(doc['classe'])
            concat.append(doc['title']+''+doc['content'])
            
        content_toJson={}
        for i,cid in enumerate(ids):
            content_toJson[cid]=concat[i]
        
        return {'content':content_toJson,'classe':classes}

    except Exception as ex:
        print(ex)

# --- Put the list of content and title from a list of text into a string format --- #
def ConverttoString(listOfText):
    string_text = ''.join(listOfText)
    return string_text

# --- put the  collected data into a pandas DataFrame --- #
def putDataInDataFrame(string_text):
    data_df = pd.DataFrame.from_dict(string_text).transpose()
    data_df.columns = ['content']
    data_df = data_df.sort_index()
    return data_df

# --- Function to clean the data --- #
def cleanData(text):
    text = re.sub('\[.*?\]', '', text) 
    text = re.sub('\(.*?\)', '', text) 
    text = re.sub('\w*\d\w*', '', text) 
    text = re.sub('\n', '', text) 
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)
    return text

def organizeData(data_df,classes,cleaned_data):
    # --- Adding class column to dataframe --- #
    data_df['classe'] = classes
    return data_df