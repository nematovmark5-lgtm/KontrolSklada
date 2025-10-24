from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Sum
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Sector, Product, PickupPoint, ProductRequest, ProductMovement, Report
from .report_utils_simple import report_generator


def home(request):
    return render(request, 'warehouse/home.html')


@login_required
def warehouse_dashboard(request):

    total_products = Product.objects.count()
    total_sectors = Sector.objects.count()
    pending_requests = ProductRequest.objects.filter(status='pending').count()
    low_stock_products = Product.objects.filter(quantity__lt=10).count()
    
    recent_requests = ProductRequest.objects.select_related('pickup_point', 'product').order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_sectors': total_sectors,
        'pending_requests': pending_requests,
        'low_stock_products': low_stock_products,
        'recent_requests': recent_requests,
    }
    return render(request, 'warehouse/warehouse_dashboard.html', context)


@login_required
def pickup_dashboard(request):
    try:
        pickup_point = PickupPoint.objects.filter(manager=request.user).first()
    except PickupPoint.DoesNotExist:
        pickup_point = None
    
    user_requests = ProductRequest.objects.filter(requested_by=request.user)
    pending_requests = user_requests.filter(status='pending').count()
    approved_requests = user_requests.filter(status='approved').count()

    recent_requests = user_requests.order_by('-created_at')[:10]
    
    context = {
        'pickup_point': pickup_point,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'recent_requests': recent_requests,
    }
    return render(request, 'warehouse/pickup_dashboard.html', context)


@login_required
def products_list(request):
    products = Product.objects.select_related('sector').all()
    sectors = Sector.objects.all()
    
    sector_id = request.GET.get('sector')
    search = request.GET.get('search')
    
    if sector_id:
        products = products.filter(sector_id=sector_id)
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(article__icontains=search)
        )
    
    context = {
        'products': products,
        'sectors': sectors,
        'selected_sector': int(sector_id) if sector_id else None,
        'search': search or '',
    }
    return render(request, 'warehouse/products_list.html', context)


@login_required
def sectors_list(request):
    sectors = Sector.objects.annotate(
        product_count=Count('product')
    ).all()
    
    context = {'sectors': sectors}
    return render(request, 'warehouse/sectors_list.html', context)


@login_required
def requests_list(request):
    requests = ProductRequest.objects.select_related(
        'pickup_point', 'product', 'requested_by'
    ).order_by('-created_at')
    
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)
    
    context = {
        'requests': requests,
        'selected_status': status,
        'status_choices': ProductRequest.STATUS_CHOICES,
    }
    return render(request, 'warehouse/requests_list.html', context)


@login_required
def create_request(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        try:
            product = Product.objects.get(id=product_id)
            quantity = int(quantity)
            
            pickup_point = PickupPoint.objects.filter(manager=request.user).first()
            if not pickup_point:
                messages.error(request, 'Вы не привязаны к ПВЗ. Обратитесь к администратору.')
                return redirect('pickup_dashboard')
            
            ProductRequest.objects.create(
                pickup_point=pickup_point,
                product=product,
                quantity=quantity,
                requested_by=request.user
            )
            
            messages.success(request, f'Запрос на {quantity} шт. товара "{product.name}" создан')
            return redirect('pickup_dashboard')
            
        except (Product.DoesNotExist, ValueError):
            messages.error(request, 'Ошибка при создании запроса')
    
    products = Product.objects.filter(quantity__gt=0)
    context = {'products': products}
    return render(request, 'warehouse/create_request.html', context)


@login_required
def approve_request(request, request_id):

    product_request = get_object_or_404(ProductRequest, id=request_id)
    
    if product_request.approve():
        messages.success(request, f'Запрос одобрен. Товар списан со склада.')
    else:
        messages.error(request, 'Не удалось одобрить запрос. Недостаточно товара на складе.')
    
    return redirect('requests_list')


@login_required
def reject_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)
    
    if product_request.reject():
        messages.success(request, f'Запрос отклонен.')
    else:
        messages.error(request, 'Не удалось отклонить запрос.')
    
    return redirect('requests_list')



@login_required
def reports_dashboard(request):

    total_products = Product.objects.count()
    total_requests = ProductRequest.objects.count()
    pending_requests = ProductRequest.objects.filter(status='pending').count()
    

    recent_reports = Report.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    

    import json
    chart_data = {
        'inventory_by_sector': json.dumps(report_generator.generate_chart_data('inventory_by_sector')),
        'requests_by_status': json.dumps(report_generator.generate_chart_data('requests_by_status')),
        'requests_timeline': json.dumps(report_generator.generate_chart_data('requests_timeline'))
    }
    
    context = {
        'total_products': total_products,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'recent_reports': recent_reports,
        'chart_data': chart_data,
    }
    return render(request, 'warehouse/reports_dashboard.html', context)


@login_required
def create_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        sector_ids = request.POST.getlist('sectors')
        pvz_ids = request.POST.getlist('pickup_points')
        

        date_from = datetime.strptime(date_from, '%Y-%m-%d').date() if date_from else None
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date() if date_to else None
        

        sectors = Sector.objects.filter(id__in=sector_ids) if sector_ids else None
        pickup_points = PickupPoint.objects.filter(id__in=pvz_ids) if pvz_ids else None
        
        if report_type == 'inventory':
            data, summary = report_generator.generate_inventory_report(sectors=sectors)
        elif report_type == 'movements':
            data, summary = report_generator.generate_movement_report(
                date_from=date_from, date_to=date_to, sectors=sectors
            )
        elif report_type == 'requests':
            data, summary = report_generator.generate_requests_report(
                date_from=date_from, date_to=date_to, pickup_points=pickup_points
            )
        else:
            messages.error(request, 'Неизвестный тип отчета')
            return redirect('create_report')
        
        report = Report.objects.create(
            title=title,
            report_type=report_type,
            description=description,
            created_by=request.user,
            date_from=date_from,
            date_to=date_to
        )
        
        if sectors:
            report.sectors.set(sectors)
        if pickup_points:
            report.pickup_points.set(pickup_points)
        
        try:
            txt_buffer = report_generator.generate_pdf_report(title, data, summary, report_type)
            txt_filename = f"report_{report.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report.pdf_file.save(txt_filename, ContentFile(txt_buffer.getvalue()))

            txt_buffer2 = report_generator.generate_excel_report(title, data, summary, report_type)
            txt_filename2 = f"report_{report.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_data.txt"
            report.excel_file.save(txt_filename2, ContentFile(txt_buffer2.getvalue()))
            
            messages.success(request, f'Отчет "{title}" успешно создан и сохранен')
            return redirect('reports_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при создании файлов отчета: {str(e)}')
            report.delete()
            return redirect('create_report')
    
    sectors = Sector.objects.all()
    pickup_points = PickupPoint.objects.all()
    
    context = {
        'sectors': sectors,
        'pickup_points': pickup_points,
        'report_types': Report.REPORT_TYPES,
    }
    return render(request, 'warehouse/create_report.html', context)


@login_required
def reports_list(request):
    reports = Report.objects.select_related('created_by').all().order_by('-created_at')
    
    report_type = request.GET.get('type')
    if report_type:
        reports = reports.filter(report_type=report_type)
    
    context = {
        'reports': reports,
        'report_types': Report.REPORT_TYPES,
        'selected_type': report_type,
    }
    return render(request, 'warehouse/reports_list.html', context)


@login_required
def view_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    if report.report_type == 'inventory':
        data, summary = report_generator.generate_inventory_report(
            sectors=report.sectors.all() if report.sectors.exists() else None
        )
    elif report.report_type == 'movements':
        data, summary = report_generator.generate_movement_report(
            date_from=report.date_from,
            date_to=report.date_to,
            sectors=report.sectors.all() if report.sectors.exists() else None
        )
    elif report.report_type == 'requests':
        data, summary = report_generator.generate_requests_report(
            date_from=report.date_from,
            date_to=report.date_to,
            pickup_points=report.pickup_points.all() if report.pickup_points.exists() else None
        )
    else:
        data, summary = [], {}
    
    context = {
        'report': report,
        'data': data[:50], 
        'summary': summary,
        'total_records': len(data),
    }
    return render(request, 'warehouse/view_report.html', context)


@login_required
def download_report(request, report_id, file_type):
    report = get_object_or_404(Report, id=report_id)
    
    if file_type == 'pdf' and report.pdf_file:
        response = HttpResponse(report.pdf_file.read(), content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{report.title}_report.txt"'
        return response
    elif file_type == 'excel' and report.excel_file:
        response = HttpResponse(report.excel_file.read(), content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{report.title}_data.txt"'
        return response
    else:
        messages.error(request, 'Файл отчета не найден')
        return redirect('view_report', report_id=report_id)


@login_required
def delete_report(request, report_id):
    """Удаление отчета"""
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        # Удаляем файлы
        if report.pdf_file:
            report.pdf_file.delete()
        if report.excel_file:
            report.excel_file.delete()
        
        title = report.title
        report.delete()
        messages.success(request, f'Отчет "{title}" удален')
        return redirect('reports_list')
    
    return render(request, 'warehouse/confirm_delete_report.html', {'report': report})


@login_required
def chart_data_api(request, chart_type):
    """API для получения данных графиков"""
    try:
        data = report_generator.generate_chart_data(chart_type)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
