from django.shortcuts import render
import os
from django.conf import settings
# Remove JsonResponse import if no longer needed elsewhere
# from django.http import JsonResponse
from .models import Noticias, FeaturedNewsOrder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoticiaSerializer, FeaturedNewsOrderSerializer
# Create your views here.

def home(request):
    return render(request, 'core/template.html')

def historia(request):
    return render(request, 'core/template.html')

@api_view(['GET'])
def noticias(request):
    noticias_list = Noticias.objects.all().order_by('-datetime').prefetch_related('embedded_media')
    serializer = NoticiaSerializer(noticias_list, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_featured_noticias(request):
    featured_items = FeaturedNewsOrder.objects.all().select_related('noticia').prefetch_related('noticia__embedded_media').order_by('custom_order', '-added_datetime')
    serializer = FeaturedNewsOrderSerializer(featured_items, many=True, context={'request': request})
    return Response(serializer.data)

def contacto(request):
    return render(request, 'core/template.html')

def frontend(request):
    return render(request, os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html'))

@api_view(['GET'])
def get_noticia(request, id):
    try:
        noticia = Noticias.objects.prefetch_related('embedded_media').get(id=id)
        serializer = NoticiaSerializer(noticia, context={'request': request})
        return Response(serializer.data)
    except Noticias.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)