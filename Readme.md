# Запуск сервера FastAPI
1. установить **git**
2. клонировать репозиторий командой **git clone** ***адрес репозитория***
3. в папке с проектом создать виртуальное окружение python3.10 -m venv venv
4. установить зависимости (для *python версии 3.10*) командой **pip install -r requirements310.txt**
5. настроить переменные окружения в файле **.env**
6. провести миграции в базу данных командами 
   * **alembic revision --autogenerate -m "reorganise filesystem"**
   * **alembic upgrade head**
7. запустить сервер командой **uvicorn src.main:app --reload**
8. страницы: 
   * с документацией Swagger по адресу **http://127.0.0.1:8000/docs**
   * админка **http://127.0.0.1:8000/admin**

# Запуск сервера Scrapyd
1. перейти в папку parse_news (cd parse_news)
2. запустить сервер командой scrapyd
3. в файле scrapy.cfg изменить строку **deploy** на **deploy:local**
4. запустить конфигурирование командой **scrapyd-deploy local**
5. сервер доступен по адресу **http://127.0.0.1:8000/docs**
5. документация по API-scrapyd **https://scrapyd.readthedocs.io/en/latest/api.html**

# Запуск парсера по расписанию
1. в корневой папке проекта (src) выполнить команду **celery -A celery_tasks worker -l INFO -B**
2. изменение регулярности запуска спайдеров доступно в файле **src/celery_tasks.py** при помощи изменения параметров crontab