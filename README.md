![foodgram_workflow](https://github.com/netshy/foodgram-project/workflows/foodgram_workflow/badge.svg?branch=master)

# Foodgram-project
http://foodgram.tk/ 
## Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.
## Стек технологий
- Python
- Django
- PostgreSQL
- Docker
- Nginx
- Gunicorn
- Git / GitHub actions

## Как запустить проект, используя Docker (база данных PostgreSQL):
1) Клонируйте репозиторий с проектом:
```
git clone https://github.com/netshy/foodgram-project.git
```
2) В директории проекта создайте файл .env, по пути `<project_name>/foodgram/.env`, в котором пропишите следующие переменные окружения:
- ALLOWED_HOSTS="127.0.0.1 localhost 0.0.0.0"
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- SECRET_KEY=
- YANDEX_USERNAME=
- YANDEX_PASSWORD=

##### Для локального использования DB_HOST=127.0.0.1
##### Для включения дебага DEBUG=True


3) С помощью Dockerfile и docker-compose.yaml разверните проект:
```
docker-compose up --build
```
Автоматически были созданы миграции для приложения и произошла миграция в БД. В БД загружены ингредиенты и теги.
###### Проект запустился на http://127.0.0.1/
###### Аккаунт суперпользователя после деплоя
http://127.0.0.1/admin/panel/
Login: admin
Password: admin

## Над проектом трудились
- Безымянные выпускники фронтенда - шаблоны, JS, css
- Лундак Иван - все остальное