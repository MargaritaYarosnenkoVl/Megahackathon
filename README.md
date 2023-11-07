# Back сервер парсера для ThisIsХорошо

Добавлены:
Админ панель, таблицы к бд, возможность регистрироваться и авторизовываться, но возможность регистрации будет убрана.

Для запуска сервера:
1) Клонировать проект
2) Установить все библиотеки из requirements.txt
3) Создать файл .env и файл config.py
В .env добавить переменные DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS для работы БД, а также

export ADMIN_USER_MODEL=User

export ADMIN_USER_MODEL_USERNAME_FIELD=username

export ADMIN_SECRET_KEY=secret_key,
для работы Админ-панели.

А также создать и добавить JWT secret код.

Должно получится так:

![image](https://github.com/liveMusic13/Megahackathon_T17/assets/106066752/a44ad724-ea28-463d-aa53-b5bb09800145)

В файле config.py все это импортировать из файла .env для дальнейшего использования.
![image](https://github.com/liveMusic13/Megahackathon_T17/assets/106066752/ba2677d9-ae73-4b90-98b2-39c17d918e72)

4) Сервер запускается командой: uvicorn main:app --reload
