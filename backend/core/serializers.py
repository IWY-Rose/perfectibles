from rest_framework import serializers
from .models import Noticias

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'  # or specify the fields you want to include
