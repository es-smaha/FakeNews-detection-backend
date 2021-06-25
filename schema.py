import graphene
from graphene_django import DjangoObjectType, DjangoListField 

from nltk import tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.stem.snowball import SnowballStemmer
from .nlp import *
import re
import string
import json
from io import StringIO
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pandas as pd
from .models import *
from .Training import *

class TextType(DjangoObjectType): 
    class Meta:
        model = Text
        fields = "__all__"

class OperType(DjangoObjectType): 
    class Meta:
        model = Operation
        fields = "__all__"

class FakeType(DjangoObjectType): 
    class Meta:
        model = FakeContent
        fields = "__all__"

class NewsType(DjangoObjectType): 
    class Meta:
        model = news 
        fields = "__all__"

class Query(graphene.ObjectType):
    all_Text = graphene.List(TextType)
    Text = graphene.Field(TextType, Text_id=graphene.Int())
    all_operation = graphene.List(OperType)
    all_fake = graphene.List(FakeType)
    all_news = graphene.List(NewsType)

    def resolve_all_Text(self, info, **kwargs):
        return Text.objects.all()

    def resolve_text(self, info, Text_id):
        return Text.objects.get(pk=Text_id)

    def resolve_all_operation(self, info,**kwargs):
        return Operation.objects.all()

    def resolve_all_fake(self, info,**kwargs):
        return FakeContent.objects.all()
    
    def resolve_all_news(self, info,**kwargs):
        return news.objects.all()


    
# creation text for testing queries 
class TextInput(graphene.InputObjectType):
    
    title = graphene.String()
    content = graphene.String()
   
class CreateText(graphene.Mutation):
    class Arguments:
        text_data = TextInput(required=True)

    text = graphene.Field(TextType) 
    #define the model we are working with

    @staticmethod
    def mutate(root, info, text_data=None):
        text_instance = Text( 
            title=text_data.title,
            content=text_data.content,
         
        )
        text_instance.save()
        return CreateText(text=text_instance)



# create schema for showing data



#create operation for NLP 

class CreateOperation(graphene.Mutation):
    class Arguments:
         title = graphene.String()
         operationType = graphene.String()
    #result
    opera= graphene.Field(OperType)
    def mutate(self, info, title,operationType):
      
        if operationType == "Tokenization":
            result = Tokenization.tokenizationProcess(title)
        if operationType == "Lemmatization":
            result = Lemmatization.getLemmatization(title)
        if operationType == "StopWords":
            result = StopWords.deleteStopWords(title)
        if operationType == "Stemming":
            result =Stemming.defineStemming(title)
        if operationType == "BagOfWordsEn":
            result = BagOfWordsFR.getbagOfWords(title)
        if operationType == "PosTagging":
            result = PosTagging.getpos(title)
        if operationType == "TFIDF":
            result = TFIDF.gettf(title)

        
        opera =  Operation(title = title , result = result ,operationType = operationType  )
        opera.save()
        return CreateOperation(opera = opera)

    


#Create user Input for fake news detections

class CreateFake(graphene.Mutation):
    class Arguments:
         content = graphene.String()
        
         
    #result
    opera= graphene.Field(FakeType)
    def mutate(self, info, content):
        result= getFake(content)
        opera =  FakeContent(content = content, result = result   )
        opera.save()
        return CreateFake(opera = opera)

class Mutation(graphene.ObjectType):
    create_text = CreateText.Field()
    create_operation = CreateOperation.Field()
    create_fake =CreateFake.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)





# --------------------------
