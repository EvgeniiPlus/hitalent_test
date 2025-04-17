# Restaurant Reservation API

## Описание
REST API сервис для бронирования столиков в ресторане с проверкой на пересекающиеся брони.

## Технологии
- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL
- Docker, docker-compose
- Alembic
- pytest

## Важно
Перед запуском необходимо создать файл .env в корне проекта с содержимым из .env.template

## Запуск
```bash
docker compose up -d --build
```

## Миграции:
```bash
docker compose exec web alembic upgrade head
```

## Эндпоинты:
- Столики:
  - GET http://localhost:8000/tables/
  - POST http://localhost:8000/tables/
    - payload: {"name": str, "seats": int, "location": str}
  - DELETE http://localhost:8000/tables/{table_id}
- Бронирование столиков:
  - GET http://localhost:8000/reservations/
  - POST http://localhost:8000/reservations/
    - payload: {"customer_name": str, "table_id": int, "reservation_time": datetime, "duration_minutes": int}
  - DELETE http://localhost:8000/reservations/{reservation_id}


## Запуск тестов
```bash
docker compose exec web pytest
```