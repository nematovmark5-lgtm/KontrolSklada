from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sector(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название сектора")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    article = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    description = models.TextField(blank=True, verbose_name="Описание")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name="Сектор")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.article})"


class PickupPoint(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ПВЗ")
    address = models.TextField(verbose_name="Адрес")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Менеджер")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, verbose_name="ПВЗ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Запрошено пользователем")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Обработано")
    notes = models.TextField(blank=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Запрос товара"
        verbose_name_plural = "Запросы товаров"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pickup_point.name} - {self.product.name} ({self.quantity}шт)"

    def approve(self):
        if self.status == 'pending' and self.product.quantity >= self.quantity:
            self.status = 'approved'
            self.processed_at = timezone.now()
            self.product.quantity -= self.quantity
            self.product.save()
            self.save()
            return True
        return False

    def reject(self):
        if self.status == 'pending':
            self.status = 'rejected'
            self.processed_at = timezone.now()
            self.save()
            return True
        return False


class ProductMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Поступление'),
        ('out', 'Списание'),
        ('transfer', 'Перемещение'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, verbose_name="Тип движения")
    quantity = models.IntegerField(verbose_name="Количество")
    from_sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.SET_NULL, related_name='movements_out')
    to_sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.SET_NULL, related_name='movements_in')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Движение товара"
        verbose_name_plural = "Движения товаров"

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"


class Report(models.Model):
    REPORT_TYPES = [
        ('inventory', 'Отчет по остаткам'),
        ('movements', 'Отчет по движению товаров'),
        ('requests', 'Отчет по запросам ПВЗ'),
        ('statistics', 'Статистический отчет'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название отчета")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name="Тип отчета")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создал")
    created_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField(null=True, blank=True, verbose_name="Дата с")
    date_to = models.DateField(null=True, blank=True, verbose_name="Дата по")
    
    sectors = models.ManyToManyField(Sector, blank=True, verbose_name="Секторы")
    pickup_points = models.ManyToManyField(PickupPoint, blank=True, verbose_name="ПВЗ")
    
    pdf_file = models.FileField(upload_to='reports/pdf/', null=True, blank=True, verbose_name="PDF файл")
    excel_file = models.FileField(upload_to='reports/excel/', null=True, blank=True, verbose_name="Excel файл")
    
    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
