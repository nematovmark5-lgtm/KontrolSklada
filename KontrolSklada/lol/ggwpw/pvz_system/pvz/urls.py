from django.urls import path
from . import views

app_name = 'pvz'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products_list, name='products_list'),
    path('requests/', views.requests_list, name='requests_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('api/sync-status/', views.sync_status, name='sync_status'),
]