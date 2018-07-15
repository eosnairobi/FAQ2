from django.urls import path
from djgeojson.views import GeoJSONLayerView, TiledGeoJSONLayerView

from .models import BlockProducer
from .views import bps, countries, home
from .api.views import bp_data

urlpatterns = (
    path('', home, name='home'),
    path('countries/', countries, name='countries'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=BlockProducer), name='data1'),
    path('data.geojson',TiledGeoJSONLayerView.as_view(model=BlockProducer), name='data'),
    path('data/', bp_data, name='bp_data'),
    path('bps/', bps, name='bps')


)
