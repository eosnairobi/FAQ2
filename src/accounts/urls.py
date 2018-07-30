from django.urls import path
from djgeojson.views import GeoJSONLayerView, TiledGeoJSONLayerView
from rest_framework.routers import DefaultRouter

from .api.views import bp_data, missing_info, BPDataModelViewSet
from .models import BlockProducer
from .views import bps, countries, render_missing

router = DefaultRouter()

router.register('data-filter', BPDataModelViewSet, base_name='api/data-filter')

urlpatterns = [
   
    path('countries/', countries, name='countries'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=BlockProducer), name='data1'),
    path('data.geojson',TiledGeoJSONLayerView.as_view(model=BlockProducer), name='data'),
    path('data/', bp_data, name='bp_data'),
    path('api/missing-fields/', missing_info, name='missing'),
    path('bps/', bps, name='bps'),
    path('missing/', render_missing, name='render_missing')


]

urlpatterns += router.urls