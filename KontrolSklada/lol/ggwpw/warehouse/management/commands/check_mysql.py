from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management.color import make_style

class Command(BaseCommand):
    help = 'Проверяет подключение к базе данных MySQL'
    
    def handle(self, *args, **options):
        style = make_style()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()
                
                cursor.execute("SELECT DATABASE()")
                database = cursor.fetchone()
                
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE()")
                tables_count = cursor.fetchone()
                
            self.stdout.write(
                style.SUCCESS('✅ Подключение к MySQL успешно!')
            )
            self.stdout.write(f"📋 Версия MySQL: {result[0]}")
            self.stdout.write(f"🗄️ База данных: {database[0]}")
            self.stdout.write(f"📊 Количество таблиц: {tables_count[0]}")
            
        except Exception as e:
            self.stdout.write(
                style.ERROR(f'❌ Ошибка подключения к MySQL: {e}')
            )