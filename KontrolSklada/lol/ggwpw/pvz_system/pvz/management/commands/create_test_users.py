from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создает тестовых пользователей для ПВЗ системы'
    
    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых пользователей для ПВЗ системы...')
        
        # Создаем пользователей ПВЗ
        users_data = [
            {'username': 'pvz_user', 'password': 'pvz123', 'first_name': 'Анна', 'last_name': 'Иванова'},
            {'username': 'pvz_user2', 'password': 'pvz123', 'first_name': 'Петр', 'last_name': 'Петров'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Создан пользователь: {user_data["username"]}')
                )
            else:
                self.stdout.write(f'Пользователь уже существует: {user_data["username"]}')
        
        self.stdout.write('\nТестовые пользователи созданы!')
        self.stdout.write('Данные для входа в ПВЗ систему:')
        self.stdout.write('- ПВЗ Центр: pvz_user / pvz123')
        self.stdout.write('- ПВЗ Север: pvz_user2 / pvz123')