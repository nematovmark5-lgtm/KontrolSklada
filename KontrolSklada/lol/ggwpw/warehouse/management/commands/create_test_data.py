from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from warehouse.models import Sector, Product, PickupPoint, ProductRequest


class Command(BaseCommand):
    help = 'Создает тестовые данные для демонстрации системы'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создаем пользователей для ПВЗ
        pvz_user, created = User.objects.get_or_create(
            username='pvz_user',
            defaults={
                'email': 'pvz@example.com',
                'first_name': 'Менеджер',
                'last_name': 'ПВЗ Центр'
            }
        )
        if created:
            pvz_user.set_password('pvz123')
            pvz_user.save()
            self.stdout.write(f'Создан пользователь: {pvz_user.username}')

        # Создаем второго пользователя для второго ПВЗ
        pvz_user2, created = User.objects.get_or_create(
            username='pvz_user2',
            defaults={
                'email': 'pvz2@example.com',
                'first_name': 'Менеджер',
                'last_name': 'ПВЗ Север'
            }
        )
        if created:
            pvz_user2.set_password('pvz123')
            pvz_user2.save()
            self.stdout.write(f'Создан пользователь: {pvz_user2.username}')

        # Создаем секторы
        sectors_data = [
            {'name': 'Электроника', 'description': 'Телефоны, планшеты, аксессуары'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Дом и сад', 'description': 'Товары для дома и дачи'},
            {'name': 'Спорт', 'description': 'Спортивные товары и инвентарь'},
        ]

        sectors = []
        for sector_data in sectors_data:
            sector, created = Sector.objects.get_or_create(
                name=sector_data['name'],
                defaults={'description': sector_data['description']}
            )
            sectors.append(sector)
            if created:
                self.stdout.write(f'Создан сектор: {sector.name}')

        # Создаем товары
        products_data = [
            {'name': 'iPhone 15', 'article': 'IP15-128', 'quantity': 25, 'sector': 0, 'description': 'Смартфон Apple iPhone 15 128GB'},
            {'name': 'Samsung Galaxy S24', 'article': 'SGS24-256', 'quantity': 15, 'sector': 0, 'description': 'Смартфон Samsung Galaxy S24 256GB'},
            {'name': 'Беспроводные наушники', 'article': 'WH-001', 'quantity': 50, 'sector': 0, 'description': 'Bluetooth наушники TWS'},
            {'name': 'Зарядное устройство', 'article': 'CHG-USB-C', 'quantity': 100, 'sector': 0, 'description': 'USB-C зарядное устройство 20W'},
            
            {'name': 'Футболка мужская', 'article': 'TSHIRT-M-001', 'quantity': 80, 'sector': 1, 'description': 'Хлопковая футболка размер M'},
            {'name': 'Джинсы женские', 'article': 'JEANS-W-002', 'quantity': 30, 'sector': 1, 'description': 'Джинсы классического кроя'},
            {'name': 'Кроссовки', 'article': 'SNEAK-001', 'quantity': 20, 'sector': 1, 'description': 'Спортивные кроссовки унисекс'},
            
            {'name': 'Чайник электрический', 'article': 'KETTLE-001', 'quantity': 12, 'sector': 2, 'description': 'Электрический чайник 1.7л'},
            {'name': 'Пылесос', 'article': 'VAC-001', 'quantity': 5, 'sector': 2, 'description': 'Пылесос с мешком для сбора пыли'},
            {'name': 'Лампа настольная', 'article': 'LAMP-001', 'quantity': 35, 'sector': 2, 'description': 'LED настольная лампа'},
            
            {'name': 'Мяч футбольный', 'article': 'BALL-001', 'quantity': 18, 'sector': 3, 'description': 'Профессиональный футбольный мяч'},
            {'name': 'Гантели', 'article': 'DUMB-001', 'quantity': 8, 'sector': 3, 'description': 'Разборные гантели 2х10кг'},
            {'name': 'Йога-мат', 'article': 'YOGA-001', 'quantity': 25, 'sector': 3, 'description': 'Коврик для йоги и фитнеса'},
        ]

        products = []
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                article=product_data['article'],
                defaults={
                    'name': product_data['name'],
                    'quantity': product_data['quantity'],
                    'sector': sectors[product_data['sector']],
                    'description': product_data['description']
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f'Создан товар: {product.name}')

        # Создаем ПВЗ
        pickup_points_data = [
            {'name': 'ПВЗ Центр', 'address': 'ул. Ленина, 15', 'manager': pvz_user},
            {'name': 'ПВЗ Север', 'address': 'пр. Мира, 42', 'manager': pvz_user2},
        ]

        pickup_points = []
        for pvz_data in pickup_points_data:
            pvz, created = PickupPoint.objects.get_or_create(
                name=pvz_data['name'],
                defaults={
                    'address': pvz_data['address'],
                    'manager': pvz_data['manager']
                }
            )
            pickup_points.append(pvz)
            if created:
                self.stdout.write(f'Создан ПВЗ: {pvz.name}')

        # Создаем несколько тестовых запросов
        if pickup_points and products:
            requests_data = [
                {'pickup_point': pickup_points[0], 'product': products[0], 'quantity': 2, 'requested_by': pvz_user},
                {'pickup_point': pickup_points[0], 'product': products[2], 'quantity': 10, 'requested_by': pvz_user},
                {'pickup_point': pickup_points[1], 'product': products[4], 'quantity': 5, 'requested_by': pvz_user},
            ]

            requests_data = [
                {'pickup_point': pickup_points[0], 'product': products[0], 'quantity': 2, 'requested_by': pvz_user},
                {'pickup_point': pickup_points[0], 'product': products[2], 'quantity': 10, 'requested_by': pvz_user},
                {'pickup_point': pickup_points[1], 'product': products[4], 'quantity': 5, 'requested_by': pvz_user2},
            ]

            for req_data in requests_data:
                request_obj, created = ProductRequest.objects.get_or_create(
                    pickup_point=req_data['pickup_point'],
                    product=req_data['product'],
                    quantity=req_data['quantity'],
                    requested_by=req_data['requested_by'],
                    defaults={'status': 'pending'}
                )
                if created:
                    self.stdout.write(f'Создан запрос: {request_obj}')

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )
        self.stdout.write('Данные для входа:')
        self.stdout.write('- Администратор: admin / admin123')
        self.stdout.write('- Сотрудник ПВЗ Центр: pvz_user / pvz123')
        self.stdout.write('- Сотрудник ПВЗ Север: pvz_user2 / pvz123')