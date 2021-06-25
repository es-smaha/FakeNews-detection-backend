from django_elasticsearch_dsl import Document , fields
from django_elasticsearch_dsl.registries import registry
from .models import news


@registry.register_document
class NewsDocument(Document):
    class Index:
        name = 'news'

    
    class Django:
        model = news
        fields=['title','content']


