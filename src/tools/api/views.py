from ..models import Tool, Category
from rest_framework import viewsets

from .serializers import CategoryModelSerializer, ToolModelSerializer

class ToolModelViewSet(viewsets.ModelViewSet):
    serializer_class = ToolModelSerializer
    queryset = Tool.objects.all()


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()


