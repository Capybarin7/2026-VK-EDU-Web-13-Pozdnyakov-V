## Локальный запуск

1. Создайте виртуальное окружение и активируйте его:
   python -m venv .venv
   .venv\Scripts\activate

2. Установите зависимости:
   pip install -r requirements.txt

3. Запустите сервер:
   python manage.py runserver

4. Откройте в браузере: http://127.0.0.1:8000

## Запуск через Docker Compose

1. Выполните команду:
   docker compose up --build

2. Откройте в браузере: http://127.0.0.1:8000