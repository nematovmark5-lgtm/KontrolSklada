from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from warehouse.models import PickupPoint


class Command(BaseCommand):
    help = 'Создает или обновляет всех пользователей системы'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Настройка пользователей системы...')
        
        # Создаем суперпользователя admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        
        status = 'создан' if created else 'обновлен'
        self.stdout.write(f'✅ Суперпользователь admin {status}')

        # Создаем пользователей ПВЗ
        pvz_users = [
            ('pvz_user', 'pvz@example.com'),
            ('pvz_user2', 'pvz2@example.com')
        ]
        
        for username, email in pvz_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            user.set_password('pvz123')
            user.save()
            
            status = 'создан' if created else 'обновлен'
            self.stdout.write(f'✅ Пользователь {username} {status}')

        # Создаем пункты выдачи
        pvz_data = [
            ('ПВЗ Центр', 'ул. Центральная, 1', 'pvz_user'),
            ('ПВЗ Север', 'ул. Северная, 15', 'pvz_user2')
        ]
        
        for name, address, manager_username in pvz_data:
            manager = User.objects.get(username=manager_username)
            pvz, created = PickupPoint.objects.get_or_create(
                name=name,
                defaults={
                    'address': address,
                    'manager': manager
                }
            )
            if not created:
                pvz.manager = manager
                pvz.address = address
                pvz.save()
            
            status = 'создан' if created else 'обновлен'
            self.stdout.write(f'✅ {name} {status} (менеджер: {manager_username})')

        self.stdout.write()
        self.stdout.write(self.style.SUCCESS('🎉 Все пользователи и ПВЗ настроены!'))
        self.stdout.write()
        self.stdout.write('👤 Доступные аккаунты:')
        self.stdout.write('   admin / admin123 (суперпользователь)')
        self.stdout.write('   pvz_user / pvz123 (ПВЗ Центр)')
        self.stdout.write('   pvz_user2 / pvz123 (ПВЗ Север)')