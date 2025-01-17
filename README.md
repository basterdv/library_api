# Мини-проек на FastAPI с регистрацией, аутентификацией и авторизацией

Этот проект представляет собой управление библиотечным каталогом, разработанный на основе **FastAPI**, с реализацией
системы регистрации, аутентификации и авторизации пользователей. Проект включает модульную архитектуру, гибкое
логирование через **loguru**, и взаимодействие с базой данных с использованием **SQLAlchemy**. Для управления миграциями
используется **Alembic**.

## Основные возможности

1. **Управление пользователями:**
    - Регистрация и вход пользователей.
    - Безопасное хеширование паролей с использованием **bcrypt**.
    - Авторизация с использованием **JWT** токенов через библиотеку **python-jose**.
    - Защита эндпоинтов с помощью ролей и зависимостей.

2. **Функционал приложения:**
    - Добавление записей:
        - Добавление Авторов и Книг в каталог.
        - Удаление и изменение записей.
    - Удаление записей:
        - Администратор может удалить записи, поменять роль пользователя.
    - Пользователь может:
        - Получение списка всех книг из каталога.
        - Просматривать описание книги.
        - Фильтрация записей.

3. **Логирование:**
    - Использование **loguru** для удобного управления логами.

4. **Модульная архитектура:**
    - Проект разделен на модули для упрощения поддержки и масштабирования.

## Технологический стек

- **Веб-фреймворк:** FastAPI
- **ORM:** SQLAlchemy с асинхронной поддержкой через aiosqlite
- **База данных:** PostgreSQL (можно заменить на любую SQL-СУБД)
- **Миграции:** Alembic
- **Аутентификация:** bcrypt для хеширования паролей, python-jose для работы с JWT токенами
- **Фронтенд:** HTML + CSS + JS (с использованием Jinja2)

## Структура проекта

```

├── app/
│   ├── admin/                  # Модуль api админки
│   ├── auth/                   # Модуль авторизациии и аутентификации
│   ├── dao/                    # Общие DAO для приложения  
│   ├── labrary_api/            # Модуль api библиотеки
│   ├── pages/                  # Модуль фронтенд части
│   ├── static/                 # Статические файлы приложения
│   ├── templates/              # Шаблоны HTML страниц   
│   ├── users/                  # Модуль api пользователей  
│   ├── config.py               # Конфигурация приложения
│   └── main.py                 # Основной файл для запуска приложения  
├── migration/                  # Миграции базы данных
├── tests/                      # Модуль тестов приложения
├── .env                        # Конфигурация окружения
├── .gitignore                  # Файлы, игнорируемые в Git
├── alembic.ini                 # Конфигурация Alembic
├── exceptions.py               # Исключения для обработки ошибок
├── README.md                   # Документация проекта
└── requirements.txt            # Зависимости проекта
```

## Зависимости

- **Основные:** `fastapi`, `pydantic`, `uvicorn`
- **Для работы с базой данных:** `SQLAlchemy`,  `alembic`
- **Для аутентификации:** `bcrypt`, `passlib[bcrypt]`, `python-jose`
- **Шаблонизатор:** `jinja2`
- **Прочее:**  `loguru`

Установить зависимости можно командой:

```bash
pip install -r requirements.txt
```

## Настройка

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/basterdv/library_api .
   ```

2. Настройте файл `.env`:

   ```Настройки для подключения к базе данных PostgreSQL
   
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=librarydb 
   DB_USER=admin
   DB_PASSWORD=admin
   
   SECRET_KEY=supersecretkey
   ALGORITHM=HS256
   ```

3. Создайте и примените миграции базы данных:

   ```bash
   cd app
   alembic init -t async migration
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

4. Запустите приложение:

   ```bash
   uvicorn app.main:app --reload
   ```

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Ссылки на проект

- **Опубликованный проект:** [FastAPI Blog](https://library-api-baster.amvera.io/)  
  Перейдите по ссылке, чтобы ознакомиться с работающей версией. 

- **Документация API:** [FastAPI Docs](https://library-api-baster.amvera.io/docs)  
  Полная документация для всех эндпоинтов API, созданная с использованием встроенной системы OpenAPI от FastAPI.
  Позволяет тестировать API прямо в браузере и изучать входные/выходные данные.

