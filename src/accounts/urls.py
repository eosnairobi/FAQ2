from django.urls import path
from djgeojson.views import GeoJSONLayerView, TiledGeoJSONLayerView

from .models import BlockProducer
from .views import bps, countries, home, render_missing
from .api.views import bp_data, missing_info

urlpatterns = (
    path('', home, name='home'),
    path('countries/', countries, name='countries'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=BlockProducer), name='data1'),
    path('data.geojson',TiledGeoJSONLayerView.as_view(model=BlockProducer), name='data'),
    path('data/', bp_data, name='bp_data'),
    path('api/missing-fields/', missing_info, name='missing'),
    path('bps/', bps, name='bps'),
    path('missing/', render_missing, name='render_missing')


)
