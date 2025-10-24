from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создает или обновляет пользователей PVZ системы'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Настройка пользователей PVZ системы...')
        
        # Создаем администратора ПВЗ
        pvz_admin, created = User.objects.get_or_create(
            username='pvz_admin',
            defaults={
                'email': 'pvz_admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        pvz_admin.set_password('pvz123')
        pvz_admin.is_superuser = True
        pvz_admin.is_staff = True
        pvz_admin.save()
        
        status = 'создан' if created else 'обновлен'
        self.stdout.write(f'✅ Администратор pvz_admin {status}')

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

        self.stdout.write()
        self.stdout.write(self.style.SUCCESS('🎉 Все пользователи PVZ системы настроены!'))
        self.stdout.write()
        self.stdout.write('👤 Доступные аккаунты:')
        self.stdout.write('   pvz_admin / pvz123 (администратор)')
        self.stdout.write('   pvz_user / pvz123 (ПВЗ Центр)')
        self.stdout.write('   pvz_user2 / pvz123 (ПВЗ Север)')