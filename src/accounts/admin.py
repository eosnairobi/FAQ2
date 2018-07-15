from django.contrib import admin
from .models import User, BlockProducer, BlockProducerData, Node, Country
from leaflet.admin import LeafletGeoAdmin

class BlockProducerAdmin(LeafletGeoAdmin):
    list_display = ('account_name', 'geom')

class CountryAdmin(LeafletGeoAdmin):
    pass


admin.site.register(User)
admin.site.register(BlockProducer, BlockProducerAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(BlockProducerData)
admin.site.register(Node)
