import re
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternAnalyzer,PatternTagger





# Implémentation du pippeline NLP
def nlp_pipeline(text):

    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\;\%\(\)\/\"]", "", text)
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
    text = re.sub(r"\=", "", text)
    text = re.sub(r"\§", "", text)
    text = re.sub(r"\_", "", text)

    return text

#Analyse de sentiment
def analysentiment(text):
    text=nlp_pipeline(text)
    pol=TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]
    return pol

