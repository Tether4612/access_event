# Руководство администратора AccessEvent

## 1. Системные требования
- Python 3.11+
- PostgreSQL 15+
- Docker 24+ (для контейнерного запуска)

## 2. Развёртывание

### Локально
1. `python -m venv venv`, затем активируйте окружение
   (Windows: `venv\Scripts\activate`, macOS/Linux: `source venv/bin/activate`)
2. `pip install -r requirements.txt`
3. Создайте файл `.env` по образцу `.env.example` (см. раздел 3)
4. `python app.py`

### Контейнерно
- `docker compose up -d` — поднимет web и db
- `docker compose down` — остановит

## 3. Переменные окружения (.env)

| Переменная | Назначение | Пример |
|---|---|---|
| DATABASE_URL | Подключение к PostgreSQL | postgresql://postgres:пароль@localhost:5432/accessevent |
| SECRET_KEY | Ключ подписи JWT | произвольная длинная строка |
| USE_SQLITE | Принудительно использовать SQLite | 1 |
| DB_STRICT | В Docker: упасть с ошибкой, если нет PostgreSQL | 1 |
| DB_CONNECT_RETRIES | Число попыток подключения к БД | 10 |
| TESTING | Признак тестового запуска (выставляется в tests/conftest.py) | 1 |

## 4. Роли и права

| Роль | Права |
|---|---|
| guest | просмотр мероприятий |
| user | регистрация на мероприятия, чат, отзывы |
| organizer | всё user + создание/редактирование мероприятий |
| admin | всё organizer + модерация и блокировка |

## 5. Резервное копирование
- Создание копии: `pg_dump -U postgres accessevent > backup_2026-11-01.sql`
- Восстановление: `psql -U postgres accessevent < backup_2026-11-01.sql`

## 6. Типовые проблемы и решения
1. Password authentication failed — неверный пароль в .env.
2. Connection refused — не запущен сервис PostgreSQL.
3. Address already in use (порт 5000) — старый процесс не завершён.
4. Таблицы не создаются — проверьте, что app.py вызывает db.create_all().
5. Контейнер web падает сразу после старта — неверный DATABASE_URL внутри
   docker-compose.yml (должен указывать на хост db, а не localhost).
6. Приложение работает на SQLite вместо PostgreSQL — в терминале сообщение
   «НЕ УДАЛОСЬ подключиться к PostgreSQL»: проверьте пароль и службу.