from rest_framework import serializers

from ..models import BlockProducer, BlockProducerData

class BlockProducerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockProducer
        fields = '__all__'