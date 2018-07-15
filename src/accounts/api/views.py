from rest_framework import viewsets
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from ..models import BlockProducer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def bp_data(request):
    bps = BlockProducer.objects.all()
    response = {}
    points = []
    for bp in bps:
        # {latLng: [41.50, -87.37], name: 'Chicago'}
        if bp.display_name:
            display_name = bp.display_name
        else:
            display_name = bp.account_name
        if bp.latitude and bp.longitude:
            points.append(
                {'latLng': [bp.latitude, bp.longitude], 'name': display_name})
    return Response(points)




@api_view(['GET'])
def missing_info(request):
    bps = BlockProducer.objects.all()

    missing = []
    for bp in bps:
        longitude, logo, latitude, display_name = 'Present', 'Present', 'Present', bp.display_name

        fields = []
        if not bp.display_name:
            display_name = 'Missing'
        if not bp.url:
            fields.append('URL Field')
        if not bp.latitude:
            latitude = 'Missing'
        if not bp.longitude:
            longitude = 'Missing'
        if not bp.logo:
            logo = 'Missing'
        if not bp.latitude or not bp.longitude or not bp.display_name or not bp.logo:
            missing.append({'BP':bp.account_name, 'Display Name':display_name, 'Latitude':latitude, 'Longitude':longitude, 'Logo':logo})
    return Response(missing)