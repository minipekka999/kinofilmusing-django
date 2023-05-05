import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import *

# class MovieModel:
#     def __init__(self, title, content):
#        self.title = title
#        self.content = content
#

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("__all__")




# def encode():
#     model = MovieModel('Tokaev alga', 'Content:Tokaev')
#     model_sr = MovieSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Tokaev alga","content":"Content:Tokaev"}')
#     data = JSONParser().parse(stream)
#     serializer = MovieSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)