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
        # {latLng: [41.50, -87.37], name: 'Chicago'},
        if bp.display_name:
            display_name = bp.display_name
        else:
            display_name = bp.account_name
        points.append(
            {'latLng': [bp.latitude, bp.longitude], 'name': display_name})
    return Response(points)