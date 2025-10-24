from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import (
    CustomTokenObtainPairView, ProductViewSet, SectorViewSet,
    PickupPointViewSet, ProductRequestViewSet, ProductMovementViewSet, ReportViewSet
)

# Создаем роутер для API
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'pickup-points', PickupPointViewSet)
router.register(r'requests', ProductRequestViewSet)
router.register(r'movements', ProductMovementViewSet)
router.register(r'reports', ReportViewSet)

app_name = 'warehouse_api'

urlpatterns = [
    # JWT аутентификация
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('', include(router.urls)),
]