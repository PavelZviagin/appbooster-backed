# Тестовое задание appbooster-backed

## Задача

Задание находится в файле task.md в корне репозитория.

## Технологии
 - #### Framework: FastAPI
 - #### ORM: SqlAlchemy
 - #### Database: SQLite
 - #### Tests: Pytest

## Запуск
Для запуска приложения локально необходимо выполнить следующие команды:
```bash
git clone
cd appbooster-backend
pip install -r requirements.txt
make run
```

## Тесты
Для запуска тестов необходимо выполнить следующие команды:
```bash
make test
```

## Переменные окружения
Для запуска приложения необходимо создать файл .env в корне проекта и заполнить его следующими переменными:
```bash
DB_URL=sqlite:///database.db
TEST_DB_URL=sqlite:///test_database.db
MODE=DEV
```
