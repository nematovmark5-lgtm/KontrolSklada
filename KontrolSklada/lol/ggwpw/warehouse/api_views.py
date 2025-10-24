from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db import transaction
from .models import Sector, Product, PickupPoint, ProductRequest, ProductMovement, Report
from .serializers import (
    UserSerializer, SectorSerializer, ProductSerializer, 
    PickupPointSerializer, ProductRequestSerializer, 
    ProductMovementSerializer, ReportSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            user_data = UserSerializer(user).data
            response.data['user'] = user_data
        return response


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related('sector')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.query_params.get('sector', None)
        if sector is not None:
            queryset = queryset.filter(sector_id=sector)

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
            
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_products = self.get_queryset().filter(quantity__gt=0)
        serializer = self.get_serializer(available_products, many=True)
        return Response(serializer.data)


class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PickupPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupPoint.objects.all().select_related('manager')
    serializer_class = PickupPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(manager=self.request.user)
        return queryset


class ProductRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductRequest.objects.all().select_related('pickup_point', 'product')
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            user_pickup_points = PickupPoint.objects.filter(manager=self.request.user)
            queryset = queryset.filter(pickup_point__in=user_pickup_points)
        return queryset
    
    def perform_create(self, serializer):
        pickup_point = serializer.validated_data['pickup_point']
        if not self.request.user.is_staff and pickup_point.manager != self.request.user:
            raise PermissionDenied("Вы можете создавать запросы только для своего ПВЗ")
        serializer.save(requested_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        product_request = self.get_object()
        
        if product_request.status != 'pending':
            return Response(
                {'error': 'Запрос уже обработан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = product_request.product
        if product.quantity < product_request.quantity:
            return Response(
                {'error': 'Недостаточно товара на складе'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            product.quantity -= product_request.quantity
            product.save()
            
            product_request.status = 'approved'
            product_request.save()
            
            ProductMovement.objects.create(
                product=product,
                movement_type='out',
                quantity=product_request.quantity,
                notes=f'Отправлено в ПВЗ: {product_request.pickup_point.name}'
            )
        
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        product_request = self.get_object()
        
        if product_request.status != 'pending':
            return Response(
                {'error': 'Запрос уже обработан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notes = request.data.get('notes', '')
        product_request.status = 'rejected'
        product_request.notes = notes
        product_request.save()
        
        return Response({'status': 'rejected'})


class ProductMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductMovement.objects.all().select_related('product')
    serializer_class = ProductMovementSerializer
    permission_classes = [permissions.IsAdminUser]


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """API для просмотра отчетов"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]