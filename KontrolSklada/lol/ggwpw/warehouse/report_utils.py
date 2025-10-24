import io
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

    def generate_pdf_report(self, title, data, summary, report_type):
        """Генерирует PDF отчет"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        story = []
        
        title_para = Paragraph(title, self.title_style)
        story.append(title_para)
        story.append(Spacer(1, 20))
        
        date_para = Paragraph(f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}", self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))

        summary_title = Paragraph("Сводка по отчету", self.styles['Heading2'])
        story.append(summary_title)
        
        for key, value in summary.items():
            summary_item = Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", self.styles['Normal'])
            story.append(summary_item)
        
        story.append(Spacer(1, 20))
        
        if data:
            data_title = Paragraph("Детальные данные", self.styles['Heading2'])
            story.append(data_title)
            
            if report_type == 'inventory':
                table_data = [['Сектор', 'Товар', 'Артикул', 'Количество', 'Статус']]
                for item in data:
                    table_data.append([
                        item['sector'], item['name'], item['article'], 
                        str(item['quantity']), item['status']
                    ])
            elif report_type == 'movements':
                table_data = [['Дата', 'Товар', 'Тип', 'Количество', 'Пользователь']]
                for item in data:
                    table_data.append([
                        item['date'], item['product'], item['type'],
                        str(item['quantity']), item['user']
                    ])
            elif report_type == 'requests':
                table_data = [['Дата', 'ПВЗ', 'Товар', 'Количество', 'Статус']]
                for item in data:
                    table_data.append([
                        item['date'], item['pickup_point'], item['product'],
                        str(item['quantity']), item['status']
                    ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_excel_report(self, title, data, summary, report_type):
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчет"
        
        title_font = Font(size=16, bold=True, color="1F4E79")
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        
        ws['A1'] = title
        ws['A1'].font = title_font
        
        ws['A3'] = f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        row = 5
        ws[f'A{row}'] = "СВОДКА ПО ОТЧЕТУ"
        ws[f'A{row}'].font = Font(bold=True)
        row += 1
        
        for key, value in summary.items():
            ws[f'A{row}'] = key.replace('_', ' ').title()
            ws[f'B{row}'] = value
            row += 1

        row += 2
        ws[f'A{row}'] = "ДЕТАЛЬНЫЕ ДАННЫЕ"
        ws[f'A{row}'].font = Font(bold=True)
        row += 1
        
        if data:
            if report_type == 'inventory':
                headers = ['Сектор', 'Товар', 'Артикул', 'Количество', 'Статус']
            elif report_type == 'movements':
                headers = ['Дата', 'Товар', 'Тип', 'Количество', 'Пользователь', 'Примечания']
            elif report_type == 'requests':
                headers = ['Дата', 'ПВЗ', 'Товар', 'Количество', 'Статус', 'Запросил']
            
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=row, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
            
            row += 1
            
            for item in data:
                if report_type == 'inventory':
                    values = [item['sector'], item['name'], item['article'], 
                             item['quantity'], item['status']]
                elif report_type == 'movements':
                    values = [item['date'], item['product'], item['type'],
                             item['quantity'], item['user'], item['notes']]
                elif report_type == 'requests':
                    values = [item['date'], item['pickup_point'], item['product'],
                             item['quantity'], item['status'], item['requested_by']]
                
                for col, value in enumerate(values, 1):
                    ws.cell(row=row, column=col, value=value)
                row += 1
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column].width = adjusted_width
        
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer

    def generate_chart_data(self, report_type, date_from=None, date_to=None):
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

report_generator = ReportGenerator()