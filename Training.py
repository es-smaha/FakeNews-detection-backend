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
from  .preprocessing import *
#Training Models
class TrainingModels():
    def train(organizeData):
        #remove dataframe index
        organizeData.reset_index(drop=True, inplace=True)  # Remove dataframe indexes
        Y=organizeData['classe']
        X=organizeData.drop(columns=['classe']) # on supprime la colonne classe
        X=X['content']
        #splitting data into train & test data
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3)
        # pipeline 
        pipe = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('model', SVC())])
        # Support Vector Machine (SVM)
      
        model=pipe.fit(X_train,Y_train)
        pickle.dump(model, open('model.sav', 'wb'))
        #Predictions
        prediction = model.predict(X_test)
        print(prediction)

        # Accuracy calcul
        print("SVC accuracy: {}%".format(round(accuracy_score(Y_test, prediction) * 100, 2)))
        return model

        # --- Prediction function --- #

    def predict(model, text):
        prediction = model.predict([text])
        return prediction


def getFake(content):
    data = ExtractDataFromDb()['content']
    string_text = {key: [ConverttoString(value)] for (key, value) in data.items()}
    data_df = putDataInDataFrame(string_text)
    data_cleaning = lambda x: cleanData(x)
    # --- Organizing data in a pandas dataframe --- #
    cleaned_data = pd.DataFrame(data_df.content.apply(data_cleaning))
    organized_data = organizeData(data_df, ExtractDataFromDb()['classe'], cleaned_data)
    # --- Training data --- #
    model = TrainingModels.train(organized_data)
    prediction = TrainingModels.predict(model, content)
    #0 pour fake 1 pour real
    return prediction[0]

















