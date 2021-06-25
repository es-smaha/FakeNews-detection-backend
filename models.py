from django.db import models
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField, IntField
)

class Text(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=50)
  
    def __str__(self):
        return self.title 

# ce modele va representer les input des utilisateurs
# pour faire les operation nlp  
  
class Operation(models.Model):
    title = models.CharField(max_length=100)
    result = models.CharField(max_length=50)
    operationType = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class FakeContent(models.Model):
    content = models.CharField(max_length=100)
    result = models.CharField(max_length=50)
    opr= models.CharField(max_length=50)
   

    def __str__(self):
        return self.content



class news(models.Model):
    
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)
   

    def __str__(self):
        return self.title