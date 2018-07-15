import os
from django.contrib.gis.utils import LayerMapping

from .models import Country


country_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}

world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data', 'world.shp'))

def run(verbose=True):
    # Save data to DB
    lm = LayerMapping(Country, world_shp, country_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)