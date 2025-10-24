# Система управления складом и пунктами выдачи

## Описание проекта

Проект состоит из двух Django-приложений:
1. **Warehouse System** - основная система управления складом
2. **PVZ System** - система управления пунктами выдачи заказов

## 🔧 Требования

- Python 3.8+
- MySQL 5.7+ или MariaDB
- pip (менеджер пакетов Python)

## 📦 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd ggwpw
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/MacOS:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка базы данных

Создайте файл `.env` в корневой директории проекта со следующим содержимым:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=warehouse_system
DB_USER=root
DB_PASSWORD=ваш_пароль_mysql
DB_HOST=localhost
DB_PORT=3306
```

**Важно:** Замените `ваш_пароль_mysql` на реальный пароль от MySQL.

### 6. Создание базы данных

Подключитесь к MySQL и создайте базу данных:
```sql
CREATE DATABASE warehouse_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Применение миграций

**Для основной системы (warehouse_system):**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Для системы ПВЗ (pvz_system):**
```bash
cd pvz_system
python manage.py makemigrations
python manage.py migrate
cd ..
```

### 8. Создание суперпользователя (опционально)

**Для основной системы:**
```bash
python manage.py createsuperuser
```

**Для системы ПВЗ:**
```bash
cd pvz_system
python manage.py createsuperuser
cd ..
```

## 🚀 Запуск приложения

### Вариант 1: Ручный запуск двух серверов

**Терминал 1 - Основная система склада:**
```bash
python manage.py runserver 8000
```

**Терминал 2 - Система ПВЗ:**
```bash
cd pvz_system
python manage.py runserver 8001 --settings=pvz_system.settings
```

### Вариант 2: Запуск через PowerShell (рекомендуется для Windows)

Создайте файл `start_servers.ps1` в корне проекта:
```powershell
# Запуск основного сервера
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python manage.py runserver 8000"

# Запуск сервера ПВЗ
Start-Process powershell -ArgumentList "-Command", "cd '$PWD\pvz_system'; ..\.venv\Scripts\Activate.ps1; python manage.py runserver 8001 --settings=pvz_system.settings"

Write-Host "Серверы запущены:"
Write-Host "Основная система: http://127.0.0.1:8000/"
Write-Host "Система ПВЗ: http://127.0.0.1:8001/"
```

Затем запустите:
```powershell
.\start_servers.ps1
```

## 🌐 Доступ к приложениям

После успешного запуска приложения будут доступны по следующим адресам:

### Основная система управления складом
- **URL:** http://127.0.0.1:8000/
- **Админ-панель:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/v1/

**Основные разделы:**
- `/` - Главная страница (дашборд склада)
- `/products/` - Список товаров
- `/requests/` - Список заявок
- `/sectors/` - Управление секторами склада
- `/reports/` - Отчеты и аналитика
- `/pickup-dashboard/` - Дашборд пункта выдачи

### Система пунктов выдачи (ПВЗ)
- **URL:** http://127.0.0.1:8001/
- **Админ-панель:** http://127.0.0.1:8001/admin/

**Основные разделы:**
- `/` - Главная страница ПВЗ
- `/dashboard/` - Дашборд сотрудника ПВЗ
- `/create-request/` - Создание заявки на товар
- `/products/` - Каталог товаров
- `/requests/` - Список заявок

## 🔒 Аутентификация

Система использует встроенную аутентификацию Django:
- **Вход:** `/login/`
- **Выход:** `/logout/`

## 📊 Управление данными

### Создание тестовых данных

**Для основной системы:**
```bash
python manage.py setup_users
python manage.py create_test_data
```

**Для системы ПВЗ:**
```bash
cd pvz_system
python manage.py setup_users
python manage.py create_test_users
cd ..
```

### API эндпоинты (основная система)

- `GET /api/v1/products/` - Список товаров
- `POST /api/v1/products/` - Создание товара
- `GET /api/v1/requests/` - Список заявок
- `POST /api/v1/requests/` - Создание заявки
- `GET /api/v1/sectors/` - Список секторов
- `GET /api/v1/reports/` - Отчеты

## 🛠 Разработка

### Структура проекта
```
ggwpw/
├── warehouse_system/          # Основная Django-конфигурация
├── warehouse/                 # Приложение управления складом
├── pvz_system/               # Конфигурация системы ПВЗ
│   └── pvz/                  # Приложение ПВЗ
├── media/                    # Медиа файлы (отчеты, изображения)
├── requirements.txt          # Зависимости Python
├── .env                      # Переменные окружения
└── README.md                # Документация
```

### Полезные команды

**Просмотр логов сервера:**
```bash
python manage.py runserver --verbosity=2
```

**Проверка системы:**
```bash
python manage.py check
```

**Создание миграций:**
```bash
python manage.py makemigrations warehouse
```

**Откат миграций:**
```bash
python manage.py migrate warehouse 0001
```

**Запуск тестов:**
```bash
python manage.py test
```

## 🐛 Устранение неисправностей

### Проблема: Ошибка подключения к базе данных
**Решение:** 
1. Проверьте настройки в файле `.env`
2. Убедитесь, что MySQL сервер запущен
3. Проверьте права доступа пользователя к базе данных

### Проблема: Порт уже используется
**Решение:**
```bash
# Найти процесс, использующий порт
netstat -ano | findstr :8000
# Завершить процесс (Windows)
taskkill /PID <process_id> /F
```

### Проблема: Ошибка статических файлов
**Решение:**
```bash
python manage.py collectstatic
```

### Проблема: Миграции не применяются
**Решение:**
```bash
python manage.py migrate --fake-initial
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи сервера в терминале
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки базы данных в `.env`
4. Перезапустите серверы

## 📝 Лицензия

Проект разработан для внутреннего использования.
