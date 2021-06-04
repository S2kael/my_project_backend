from rest_framework import serializers
from .models import Product, Store, PendingStore, Tag


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'



class PendingStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingStore
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'