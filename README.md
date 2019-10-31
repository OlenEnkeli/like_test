# Like Test

Реализация тестового задания для приложения автоматизированного учета сбора урожая

## Развертывание приложения

Для развертывания приложения необходимы запушенные nginx, postgresql, redis

### Сборка backend

```bash
psql postgres
postgres=# create database liketest;
postgres=# \q

cd backend
python3 -m venv env
./env/bin/pip3 install - r requirements.txt
./env/bin/alembic upgrade head # запуск миграций
./init_data.py # запуск генерации тестовых значений

./dev.sh # запуск dev сервера (gunicorn)
```

### Сборка frontend

```bash
cd frontend
npm install install
npm run server
```

### Используемая конфигурация nginx

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ‘’ close;
}

upstream frontend {
    server 127.0.0.1:8080;
}

upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name moon.local;
    client_max_body_size 100M;

    location /api {
        proxy_pass http://backend/;
        proxy_set_header Host 127.0.0.1;
    }

    location / {
        proxy_pass http://frontend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection “upgrade”;
        proxy_set_header Host 127.0.0.1;
    }
}
```

## Описание API

[GET] /api/ - API Healthcheck

[POST] /login/manager - Вход менеджера

```json
{
    "login": "ivan666",
    "password: "qwerty"
}
```

[GET] /users/current - Получение текущего пользователя

[GET] /logout - Выход

[GET] /productivity?date=2018-01-01 - Получение выборки продуктивности за определенную дату (основной ресурс)

[GET] /workdate - Получение первого и последнего дня проведения работ

## Описание генерации данных

Скрипт `init_data.py` представляет собой простой генератор данных

Он проивзодит генерацию пользователей (коллекторов, ревьювера и менеджера) и имитирует проведение работ.

Содержит следующие параметры

```python
ACITIVITY_START_DATE = dt.date(year=2018, month=1, day=1) # Дата начала работ
ACITIVITY_END_DATE = dt.date(year=2018, month=1, day=10) # Дата конца работ
WORKDAY_START_TIME = dt.time(hour=8) # Дата начала рабочего дня
WORKDAY_END_TIME = dt.time(hour=20, minute=00) # Дата конца рабочего дня
BOX_COLLECT_TIME_MIN = dt.timedelta(minutes=10) # Минимальное время сборки ящика
BOX_COLLECT_TIME_MAX = dt.timedelta(minutes=50) # Максимальное время сборки ящика
BOX_REVIEW_TIME_MIN = dt.timedelta(minutes=5) # Минимальное время проверки ящика
BOX_REVIEW_TIME_MAX = dt.timedelta(minutes=7) # Максимальное время проверки ящика
BOX_PAYLOAD_MIN = 10000 # Минимальный вес коробки
BOX_PAYLOAD_MAX = 14000 # Максимальный вес коробки
```

Логи работы в выходные не генерируются.

Для генерации используются случайные значения (между минимальными и максимальными)

## Основные допущения

Тестовый архив не содержал модели `user.py` и основной логики, в связи с этим:

- Было сделано предположение, что пользователи делятся на менеджеров и два типа рабочих (коллекторов и ревьювера). Был реализована абстрактная модель пользователя и модель менеджера, реализован вход для менеджеров. Вход для рабочих реализован не был в виду отсутствия необходимости

- Было сделано предположение, что имеется некая админ-панель для менеджеров, был реализован ее прототип

- Было сделано предположение, что бизнес-логика является следующей: коллектор собирает урожая в ящик с опредленном номером и передает его ревьюверу, тот взвешивает ящики и вносит данные в систему. Связ ревьюверов и коллекторов предполагается через `box_code`

- Назначение таблицы `ContentType` было неясно, поэтому она была убрана
