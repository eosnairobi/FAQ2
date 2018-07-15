import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import BlockProducer, Country

# # Create your views here.


def home(request):
    return render(request, 'map.html')


def countries(request):
    countries = serialize('geojson', Country.objects.all())
    return HttpResponse(countries, content_type='json') 

# def bps(request):
#     bps = serialize('geojson', BlockProducer.objects.all())
#     return HttpResponse(bps, content_type='json')



def bps(request):
    points_as_geojson = serialize( 'geojson',BlockProducer.objects.all()[:30])
    return JsonResponse(json.loads(points_as_geojson))


def render_missing(request):
    return render(request, 'dashboard/missing-bp-json.html')