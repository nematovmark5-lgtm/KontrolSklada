import io
import json
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.core.files.base import ContentFile


class ReportGenerator:

    def __init__(self):
        pass

    def generate_inventory_report(self, sectors=None, low_stock_threshold=10):
        from .models import Product
        products = Product.objects.select_related('sector').all()
        if sectors:
            products = products.filter(sector__in=sectors)

        data = []
        total_products = 0
        low_stock_count = 0

        for product in products:
            total_products += product.quantity
            if product.quantity < low_stock_threshold:
                low_stock_count += 1

            data.append({
                'sector': product.sector.name,
                'name': product.name,
                'article': product.article,
                'quantity': product.quantity,
                'status': 'Мало товара' if product.quantity < low_stock_threshold else 'В наличии'
            })

        summary = {
            'total_items': len(data),
            'total_quantity': total_products,
            'low_stock_items': low_stock_count,
            'sectors_count': products.values('sector').distinct().count()
        }

        return data, summary

    def generate_movement_report(self, date_from=None, date_to=None, sectors=None):
        from .models import ProductMovement
        movements = ProductMovement.objects.select_related('product', 'user').all()

        if date_from:
            movements = movements.filter(created_at__date__gte=date_from)
        if date_to:
            movements = movements.filter(created_at__date__lte=date_to)
        if sectors:
            movements = movements.filter(
                Q(from_sector__in=sectors) | Q(to_sector__in=sectors)
            )

        data = []
        total_in = 0
        total_out = 0

        for movement in movements:
            data.append({
                'date': movement.created_at.strftime('%d.%m.%Y %H:%M'),
                'product': movement.product.name,
                'type': movement.get_movement_type_display(),
                'quantity': movement.quantity,
                'user': movement.user.get_full_name() or movement.user.username,
                'notes': movement.notes or '-'
            })

            if movement.movement_type == 'in':
                total_in += movement.quantity
            elif movement.movement_type == 'out':
                total_out += movement.quantity

        summary = {
            'total_movements': len(data),
            'total_in': total_in,
            'total_out': total_out,
            'net_change': total_in - total_out
        }

        return data, summary

    def generate_requests_report(self, date_from=None, date_to=None, pickup_points=None):
        from .models import ProductRequest
        requests = ProductRequest.objects.select_related(
            'pickup_point', 'product', 'requested_by'
        ).all()

        if date_from:
            requests = requests.filter(created_at__date__gte=date_from)
        if date_to:
            requests = requests.filter(created_at__date__lte=date_to)
        if pickup_points:
            requests = requests.filter(pickup_point__in=pickup_points)

        data = []
        status_counts = {'pending': 0, 'approved': 0, 'rejected': 0}

        for request in requests:
            data.append({
                'date': request.created_at.strftime('%d.%m.%Y %H:%M'),
                'pickup_point': request.pickup_point.name,
                'product': request.product.name,
                'quantity': request.quantity,
                'status': request.get_status_display(),
                'requested_by': request.requested_by.get_full_name() or request.requested_by.username
            })

            status_counts[request.status] += 1

        summary = {
            'total_requests': len(data),
            'pending_requests': status_counts['pending'],
            'approved_requests': status_counts['approved'],
            'rejected_requests': status_counts['rejected']
        }

        return data, summary

    def generate_simple_report_file(self, title, data, summary, report_type):
        buffer = io.StringIO()
        
        buffer.write(f"{title}\n")
        buffer.write("="*50 + "\n\n")
        buffer.write(f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
        
        buffer.write("СВОДКА ПО ОТЧЕТУ\n")
        buffer.write("-"*20 + "\n")
        for key, value in summary.items():
            buffer.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        buffer.write("\n\nДЕТАЛЬНЫЕ ДАННЫЕ\n")
        buffer.write("-"*20 + "\n")
        
        if data:
            if report_type == 'inventory':
                buffer.write("Сектор | Товар | Артикул | Количество | Статус\n")
                buffer.write("-"*70 + "\n")
                for item in data:
                    buffer.write(f"{item['sector']} | {item['name']} | {item['article']} | {item['quantity']} | {item['status']}\n")
            
            elif report_type == 'movements':
                buffer.write("Дата | Товар | Тип | Количество | Пользователь\n")
                buffer.write("-"*70 + "\n")
                for item in data:
                    buffer.write(f"{item['date']} | {item['product']} | {item['type']} | {item['quantity']} | {item['user']}\n")
            
            elif report_type == 'requests':
                buffer.write("Дата | ПВЗ | Товар | Количество | Статус\n")
                buffer.write("-"*70 + "\n")
                for item in data:
                    buffer.write(f"{item['date']} | {item['pickup_point']} | {item['product']} | {item['quantity']} | {item['status']}\n")
        
        content = buffer.getvalue()
        buffer.close()
        
        return io.BytesIO(content.encode('utf-8'))

    def generate_pdf_report(self, title, data, summary, report_type):
        return self.generate_simple_report_file(title, data, summary, report_type)

    def generate_excel_report(self, title, data, summary, report_type):
        return self.generate_simple_report_file(title, data, summary, report_type)

    def generate_chart_data(self, report_type, date_from=None, date_to=None):
        from .models import Product, ProductRequest
        
        if report_type == 'inventory_by_sector':
            sectors_data = Product.objects.values('sector__name').annotate(
                total=Sum('quantity')
            ).order_by('-total')
            
            return {
                'labels': [item['sector__name'] for item in sectors_data],
                'data': [item['total'] for item in sectors_data],
                'chart_type': 'pie'
            }
        
        elif report_type == 'requests_by_status':
            status_data = ProductRequest.objects.values('status').annotate(
                count=Count('id')
            )
            
            status_labels = {'pending': 'Ожидают', 'approved': 'Одобрено', 'rejected': 'Отклонено'}
            
            return {
                'labels': [status_labels.get(item['status'], item['status']) for item in status_data],
                'data': [item['count'] for item in status_data],
                'chart_type': 'doughnut'
            }
        
        elif report_type == 'requests_timeline':
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
            
            timeline_data = []
            current_date = start_date
            
            while current_date <= end_date:
                count = ProductRequest.objects.filter(
                    created_at__date=current_date
                ).count()
                timeline_data.append({
                    'date': current_date.strftime('%d.%m'),
                    'count': count
                })
                current_date += timedelta(days=1)
            
            return {
                'labels': [item['date'] for item in timeline_data],
                'data': [item['count'] for item in timeline_data],
                'chart_type': 'line'
            }
        
        return {'labels': [], 'data': [], 'chart_type': 'bar'}

report_generator = ReportGenerator()