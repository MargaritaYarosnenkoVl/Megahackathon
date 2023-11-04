# Запуск сервера FastAPI
1. установить пакетный менеджер pip
2. установить зависимости командой **pip install -r requirements.txt**
3. настроить переменные виртуального окружения в файле **config.py**
* к базе данных PostgreSQL: 
  * FSTR_DB_LOGIN, 
  * FSTR_DB_PASS, 
  * FSTR_DB_HOST, 
  * FSTR_DB_PORT, 
  * DB_NAME
* секретный ключ JWT: 
  * SECRET
* у вас свои названия переменных  
4. запустить сервер командой **uvicorn main:app --reload**
5. страница с документацией Swagger по адресу **http://127.0.0.1:8000/docs**