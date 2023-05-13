# API YaMDb

## Workflow status

![Workflow status badge](https://github.com/bvsvrvb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Ссылка на развёрнутый проект

http://84.201.134.185/redoc/

## О проекте

API YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Список технологий

- Python
- Django (DRF)
- Simple-JWT
- PostgreSQL
- nginx
- Docker

## Запуск проекта через Workflow

Workflow состоит из четырёх шагов:
    - Проверка кода тестами.
    - Сборка и публикация образа на DockerHub.
    - Автоматический деплой и запуск контейнеров на удаленном сервере.
    - Отправка уведомления в телеграм-чат.

- Склонировать репозиторий

```
git clone https://github.com/bvsvrvb/yamdb_final.git
```

- Выполнить вход на удаленный сервер

```
ssh <username>@<host>
```

- Установить docker на сервер:

```
sudo apt install docker.io 
```

- Установить docker-compose на сервер:

```b
sudo apt install docker-compose
```

- Скопировать файлы docker-compose.yaml и default.conf на сервер:

```
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp default.conf <username>@<host>:/home/<username>/nginx/
```

- Для работы с Workflow добавить в Secrets GitHub переменные окружения:

    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```

- После успешного выполнения Workflow выполнить следующие действия (только при первом деплое):

    * Создать миграции внутри контейнера:

    ```
    sudo docker-compose exec web python manage.py makemigrations
    ```

    * Выполнить миграции внутри контейнера:

    ```
    sudo docker-compose exec web python manage.py migrate
    ```

    * Собрать статику проекта:

    ```
    sudo docker-compose exec web python manage.py collectstatic --no-input
    ```  

    * Создать суперпользователя Django:
    ```
    sudo docker-compose exec web python manage.py createsuperuser
    ```

## Авторы

- [Ермолов Иван](https://www.youtube.com/watch?v=dQw4w9WgXcQ),

- [Башмаков Владислав](https://www.youtube.com/watch?v=dQw4w9WgXcQ),

- [Бессогонова Полина](https://www.youtube.com/watch?v=dQw4w9WgXcQ)