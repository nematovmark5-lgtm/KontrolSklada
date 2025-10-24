from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sector, Product, PickupPoint, ProductRequest, ProductMovement, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'article', 'description', 'sector', 'sector_name', 
                 'quantity', 'created_at', 'updated_at']


class PickupPointSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    
    class Meta:
        model = PickupPoint
        fields = ['id', 'name', 'address', 'manager', 'manager_name', 'created_at']


class ProductRequestSerializer(serializers.ModelSerializer):
    pickup_point_name = serializers.CharField(source='pickup_point.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.username', read_only=True)
    
    class Meta:
        model = ProductRequest
        fields = ['id', 'pickup_point', 'pickup_point_name', 'product', 'product_name',
                 'quantity', 'status', 'requested_by', 'requested_by_name', 'created_at', 'processed_at', 'notes']
        read_only_fields = ['requested_by']

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class ProductMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductMovement
        fields = ['id', 'product', 'product_name', 'movement_type', 
                 'quantity', 'notes', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'report_type', 'file_path', 'created_at']