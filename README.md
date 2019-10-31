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
