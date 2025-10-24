from django.db import models
from django.contrib.auth.models import User


class CachedProduct(models.Model):
    warehouse_id = models.IntegerField(unique=True)  # ID из основной системы
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sector_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CachedSector(models.Model):
    warehouse_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class LocalRequest(models.Model):
    warehouse_id = models.IntegerField(unique=True, null=True, blank=True)
    product_warehouse_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_sync = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} шт."


class SyncLog(models.Model):
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} - {self.status}"
