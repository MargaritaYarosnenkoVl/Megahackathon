# Запуск сервера FastAPI
1. установить **git**
2. клонировать репозиторий командой **git clone** ***адрес репозитория***
3. в папке с проектом создать виртуальное окружение python3.10 -m venv venv
4. установить зависимости (для *python версии 3.10*) командой **pip install -r requirements310.txt**
5. настроить переменные окружения в файле **.env**
   * прописать значения к базе данных PostgreSQL (у вас могут быть свои названия переменных): 
     * FSTR_DB_LOGIN, 
     * FSTR_DB_PASS, 
     * FSTR_DB_HOST, 
     * FSTR_DB_PORT, 
     * FSTR_DB_NAME
   * секретный ключ JWT: 
     * SECRET
   * также прописать экспорт переменных окружения для админки
     - export ADMIN_USER_MODEL=User
     - export ADMIN_USER_MODEL_USERNAME_FIELD=username
     - export ADMIN_SECRET_KEY=secret_key
6. провести миграции в базу данных командами 
   * **alembic revision --autogenerate -m "reorganise filesystem"**
   * **alembic upgrade head**
6. запустить сервер командой **uvicorn src.main:app --reload**
7. страницы: 
   * с документацией Swagger по адресу **http://127.0.0.1:8000/docs**
   * админка **http://127.0.0.1:8000/admin**