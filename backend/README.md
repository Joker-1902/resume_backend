# API для управления резюме
## Это бэкенд-часть проекта по управлению резюме, построенная на фреймворке FastAPI.

### Используемые технологии
- FastAPI: Современный и быстрый веб-фреймворк для Python.

- SQLAlchemy: Инструмент для работы с базой данных (ORM).

- PostgreSQL: Система управления базами данных.

- alembic: Инструмент для миграций базы данных.

- python-jose & passlib: Для аутентификации и работы с JWT-токенами.

- uvicorn: ASGI-сервер для запуска FastAPI-приложения.

### Установка и запуск

Клонируйте репозиторий:
```bash
git clone https://github.com/Joker-1902/resume_project_backend.git
cd resume_project_backend
```

Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Установите зависимости:

```bash 
pip install -r requirements.txt
```

#### Настройте базу данных в PostgreSQL

#### Создайте файл .env в корневой папке бэкенда и добавьте в него переменные окружения для подключения к БД и JWT-секрета.

Выполните миграции для создания таблиц:

```bash 
alembic upgrade head
```

Запустите сервер:

```bash
uvicorn main:app --reload
```


## Эндпоинты API
### Аутентификация

* Получить JWT-токен:

```POST``` /users/token: 

* Зарегистрировать нового пользователя:

```POST``` /users/registration 


### Резюме

* Создать новое резюме:

```POST``` /resumes

* Получить список всех резюме текущего пользователя:

```GET``` /resumes/get_list 

* Получить одно резюме по ID:

```GET``` /resumes/{resume_id} 

* Обновить резюме по ID:

```PATCH``` /resumes/{resume_id} 

* Удалить резюме по ID:

```DELETE``` /resumes/{resume_id} 

* Удалить все резюме текущего пользователя:

```DELETE``` /resumes/delete_all 

## API будет доступно по адресу http://localhost:8000.