from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .warehouse_service import warehouse_api
from .models import CachedProduct, CachedSector, LocalRequest, SyncLog
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pvz:dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'pvz/login.html')


def logout_view(request):
    logout(request)
    return redirect('pvz:login')


@login_required
def dashboard(request):
    try:
        products_data = warehouse_api.get_available_products()
        requests_data = warehouse_api.get_requests()

        if products_data:
            _update_products_cache(products_data)
        
        if requests_data:
            _update_requests_cache(requests_data)
        
        context = {
            'products_count': CachedProduct.objects.count(),
            'pending_requests': LocalRequest.objects.filter(status='pending').count(),
            'approved_requests': LocalRequest.objects.filter(status='approved').count(),
            'recent_requests': LocalRequest.objects.all()[:5],
            'online_status': True if products_data else False
        }
        
    except Exception as e:
        logger.error(f"Ошибка подключения к складу: {e}")
        context = {
            'products_count': CachedProduct.objects.count(),
            'pending_requests': LocalRequest.objects.filter(status='pending').count(),
            'approved_requests': LocalRequest.objects.filter(status='approved').count(),
            'recent_requests': LocalRequest.objects.all()[:5],
            'online_status': False,
            'error_message': f'Автономный режим: {str(e)[:100]}'
        }
    
    return render(request, 'pvz/dashboard.html', context)


@login_required
def products_list(request):
    try:
        products_data = warehouse_api.get_available_products()
        if products_data:
            _update_products_cache(products_data)
            online_status = True
        else:
            online_status = False
    except Exception:
        online_status = False
    
    products = CachedProduct.objects.all()

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    sector = request.GET.get('sector')
    if sector:
        products = products.filter(sector_name=sector)
    
    sectors = CachedSector.objects.all()
    
    context = {
        'products': products,
        'sectors': sectors,
        'search': search,
        'selected_sector': sector,
        'online_status': online_status
    }
    
    return render(request, 'pvz/products_list.html', context)


@login_required
def requests_list(request):
    try:
        requests_data = warehouse_api.get_requests()
        if requests_data:
            _update_requests_cache(requests_data)
            online_status = True
        else:
            online_status = False
    except Exception:
        online_status = False
    
    requests = LocalRequest.objects.all()
    
    context = {
        'requests': requests,
        'online_status': online_status
    }
    
    return render(request, 'pvz/requests_list.html', context)


@login_required
def create_request(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = CachedProduct.objects.get(warehouse_id=product_id)
            
            try:
                pickup_points = warehouse_api.get_pickup_points()
                if pickup_points and pickup_points['results']:
                    pickup_point_id = pickup_points['results'][0]['id']
                    
                    result = warehouse_api.create_request(pickup_point_id, product_id, quantity)
                    
                    if result:
                        LocalRequest.objects.create(
                            warehouse_id=result['id'],
                            product_warehouse_id=product_id,
                            product_name=product.name,
                            quantity=quantity,
                            status='pending'
                        )
                        messages.success(request, 'Запрос успешно создан!')
                    else:
                        LocalRequest.objects.create(
                            product_warehouse_id=product_id,
                            product_name=product.name,
                            quantity=quantity,
                            status='pending'
                        )
                        messages.warning(request, 'Запрос создан локально. Будет отправлен при восстановлении соединения.')
                else:
                    messages.error(request, 'Не удалось определить ваш ПВЗ')
                    
            except Exception as e:
                LocalRequest.objects.create(
                    product_warehouse_id=product_id,
                    product_name=product.name,
                    quantity=quantity,
                    status='pending'
                )
                messages.warning(request, 'Запрос сохранен локально. Будет отправлен при восстановлении соединения.')
            
        except CachedProduct.DoesNotExist:
            messages.error(request, 'Товар не найден')
        except Exception as e:
            messages.error(request, f'Ошибка создания запроса: {e}')
        
        return redirect('pvz:requests_list')
    
    products = CachedProduct.objects.filter(quantity__gt=0)
    return render(request, 'pvz/create_request.html', {'products': products})


def sync_status(request):
    try:
        products_data = warehouse_api.get_available_products()
        online = True if products_data else False
    except Exception:
        online = False
    
    return JsonResponse({
        'online': online,
        'local_products': CachedProduct.objects.count(),
        'pending_requests': LocalRequest.objects.filter(status='pending').count()
    })


def _update_products_cache(products_data):
    try:
        if 'results' in products_data:
            products = products_data['results']
        else:
            products = products_data
            
        for product_data in products:
            CachedProduct.objects.update_or_create(
                warehouse_id=product_data['id'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data.get('description', ''),
                    'sector_name': product_data.get('sector_name', ''),
                    'quantity': product_data.get('quantity', 0),
                    'price': product_data.get('price', 0),
                }
            )
        
        SyncLog.objects.create(
            action='sync_products',
            status='success',
            message=f'Обновлено {len(products)} товаров'
        )
    except Exception as e:
        SyncLog.objects.create(
            action='sync_products',
            status='error',
            message=str(e)
        )


def _update_requests_cache(requests_data):
    try:
        if 'results' in requests_data:
            requests = requests_data['results']
        else:
            requests = requests_data
            
        for request_data in requests:
            LocalRequest.objects.update_or_create(
                warehouse_id=request_data['id'],
                defaults={
                    'product_warehouse_id': request_data['product'],
                    'product_name': request_data.get('product_name', ''),
                    'quantity': request_data.get('quantity', 0),
                    'status': request_data.get('status', 'pending'),
                    'notes': request_data.get('notes', ''),
                }
            )
        
        SyncLog.objects.create(
            action='sync_requests',
            status='success',
            message=f'Обновлено {len(requests)} запросов'
        )
    except Exception as e:
        SyncLog.objects.create(
            action='sync_requests',
            status='error',
            message=str(e)
        )
