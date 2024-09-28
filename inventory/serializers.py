from rest_framework import serializers
from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'quantity', 'price']

    def validate_name(self, value):
        if InventoryItem.objects.filter(name=value).exists():
            raise serializers.ValidationError("Item already exists.")
        return value