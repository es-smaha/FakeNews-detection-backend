
from nltk import tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.stem.snowball import SnowballStemmer
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

class Tokenization():
    def getData(self):
        pass

    def tokenizationProcess(example_sent):

        tokens = word_tokenize(example_sent)
        return tokens

class Lemmatization():

    def getLemmatization(example_sent):
        lemmatizer = WordNetLemmatizer()
        word_tokens = Tokenization.tokenizationProcess(example_sent)
        lemmatized = []
        for word in word_tokens:
            lemmatized.append(nltk.ISRIStemmer().suf32(word))
        
        return lemmatized


class StopWords():
    #---------- french
    def deleteStopWords(example_sent):
        stopwords_list = stopwords.words('french')
        word_tokens = Tokenization.tokenizationProcess(example_sent)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stopwords_list:
                filtered_sentence.append(w)
        return filtered_sentence


class Stemming():
    def getData(self):
        pass

    def defineStemming(example_sent):
        word_tokens = Tokenization.tokenizationProcess(example_sent)
        filtered_sentence = []
        ps = nltk.ISRIStemmer()
        for w in word_tokens:
            filtered_sentence.append(ps.stem(w))
        return filtered_sentence
     

class StemmingEn():
    def getData(self):
        pass

    def defineStemming(example_sent):
        word_tokens = Tokenization.tokenizationProcess(example_sent)
        filtered_sentence = []
        ps = PorterStemmer()
        for w in word_tokens:
            filtered_sentence.append(ps.stem(w))
        return filtered_sentence



class BagOfWordsFR():

    def getbagOfWords(example_sent):
        vect = CountVectorizer()
        bag_of_words = vect.transform(example_sent).toarray()

        return bag_of_words

class PosTagging():

    def getpos(example_sent):
        stop_words = set(stopwords.words('french'))
        tokens = sent_tokenize(example_sent)
        for i in tokens:

            word_list = nltk.word_tokenize(i)
            word_list = [word for word in word_list if not word in stop_words]
            pos = nltk.pos_tag(word_list)
        return pos

class TFIDF():

    def gettf(example_sent):
        tokens = word_tokenize(example_sent)
        tfidf = TfidfVectorizer(tokenizer=tokens, stop_words=stopwords.words('french'))
        return tfidf
