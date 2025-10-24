import requests
import json
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class WarehouseAPIService:
    
    def __init__(self):
        self.base_url = settings.WAREHOUSE_API_BASE_URL
        self.username = settings.WAREHOUSE_API_USERNAME
        self.password = settings.WAREHOUSE_API_PASSWORD
        self.access_token = None
        self.refresh_token = None
    
    def _get_auth_headers(self):
        if not self.access_token:
            self._authenticate()
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _authenticate(self):
        try:
            cached_tokens = cache.get('warehouse_api_tokens')
            if cached_tokens:
                self.access_token = cached_tokens['access']
                self.refresh_token = cached_tokens['refresh']
                return
            
            auth_url = f"{self.base_url}auth/login/"
            data = {
                'username': self.username,
                'password': self.password
            }
            
            logger.info(f"Попытка аутентификации в {auth_url}")
            response = requests.post(auth_url, json=data, timeout=10)
            
            logger.info(f"Ответ аутентификации: {response.status_code}")
            
            if response.status_code == 200:
                tokens = response.json()
                self.access_token = tokens['access']
                self.refresh_token = tokens['refresh']
                
                cache.set('warehouse_api_tokens', {
                    'access': self.access_token,
                    'refresh': self.refresh_token
                }, timeout=3000)
                
                logger.info("Успешная аутентификация в API склада")
            else:
                logger.error(f"Ошибка аутентификации: {response.status_code} - {response.text}")
                raise Exception(f"Не удалось аутентифицироваться: {response.status_code}")
                
        except requests.RequestException as e:
            logger.error(f"Ошибка соединения с API склада: {e}")
            raise Exception(f"Нет соединения с системой склада: {e}")
    
    def _refresh_access_token(self):
        try:
            refresh_url = f"{self.base_url}auth/refresh/"
            data = {'refresh': self.refresh_token}
            
            response = requests.post(refresh_url, json=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access']
                
                cache.set('warehouse_api_tokens', {
                    'access': self.access_token,
                    'refresh': self.refresh_token
                }, timeout=3000)
                
                return True
            else:
                cache.delete('warehouse_api_tokens')
                self._authenticate()
                return True
                
        except requests.RequestException:
            cache.delete('warehouse_api_tokens')
            self._authenticate()
            return True
    
    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_auth_headers()
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Неподдерживаемый HTTP метод: {method}")
            
            if response.status_code == 401:
                if self._refresh_access_token():
                    headers = self._get_auth_headers()
                    if method.upper() == 'GET':
                        response = requests.get(url, headers=headers, params=params)
                    elif method.upper() == 'POST':
                        response = requests.post(url, headers=headers, json=data)
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса к API склада: {e}")
            raise Exception("Ошибка соединения с системой склада")
    
    def get_products(self, search=None, sector=None):
        params = {}
        if search:
            params['search'] = search
        if sector:
            params['sector'] = sector
            
        response = self._make_request('GET', 'products/', params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка получения товаров: {response.status_code}")
            return None
    
    def get_available_products(self):
        response = self._make_request('GET', 'products/available/')
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка получения доступных товаров: {response.status_code}")
            return None
    
    def get_sectors(self):
        response = self._make_request('GET', 'sectors/')
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка получения секторов: {response.status_code}")
            return None
    
    def get_pickup_points(self):
        response = self._make_request('GET', 'pickup-points/')
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка получения ПВЗ: {response.status_code}")
            return None
    
    def get_requests(self):
        response = self._make_request('GET', 'requests/')
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка получения запросов: {response.status_code}")
            return None
    
    def create_request(self, pickup_point_id, product_id, quantity):
        data = {
            'pickup_point': pickup_point_id,
            'product': product_id,
            'quantity': quantity
        }
        
        response = self._make_request('POST', 'requests/', data=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Ошибка создания запроса: {response.status_code}")
            return None

warehouse_api = WarehouseAPIService()