from rest_framework import serializers

from ..models import Category, Tool


class ToolModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

