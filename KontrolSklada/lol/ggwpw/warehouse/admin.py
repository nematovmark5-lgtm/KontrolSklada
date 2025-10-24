from django.contrib import admin
from .models import Sector, Product, PickupPoint, ProductRequest, ProductMovement, Report


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'quantity', 'sector', 'updated_at')
    list_filter = ('sector', 'created_at')
    search_fields = ('name', 'article')
    list_editable = ('quantity',)


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager', 'created_at')
    search_fields = ('name', 'address')


@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ('pickup_point', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'pickup_point', 'created_at')
    search_fields = ('product__name', 'pickup_point__name')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        approved_count = 0
        for req in queryset.filter(status='pending'):
            if req.approve():
                approved_count += 1
        self.message_user(request, f'Одобрено {approved_count} запросов.')

    def reject_requests(self, request, queryset):
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'Отклонено {rejected_count} запросов.')

    approve_requests.short_description = "Одобрить выбранные запросы"
    reject_requests.short_description = "Отклонить выбранные запросы"


@admin.register(ProductMovement)
class ProductMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'user', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'created_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    filter_horizontal = ('sectors', 'pickup_points')
