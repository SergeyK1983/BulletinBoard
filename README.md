## В разработке ...

### Финальный проект

## "ДОСКА ОБЪЯВЛЕНИЙ"
___

Python 3.10

Django 4.2

    superuser:
    username=admin
    password=admin

PostgreSQL 15.4

    POSTGRES_PASSWORD=root
    POSTGRES_USER=root
    POSTGRES_DB=pgdb
    ports:
      - "5437:5432"

---
## Развертывание

Перейти в директорию Adboard/pgdata/ и удалить файлы .gitkeep из следующих директорий:
  
    pg_commit_ts/
    pg_dynshmem/
    pg_logical/mappings/
    pg_logical/snapshots/
    pg_notify/
    pg_replslot/
    pg_serial/
    pg_snapshots/
    pg_stat_tmp/
    pg_tblspc/
    pg_twophase/
    pg_wal/archive_status/

В директории Adboard/ (в папке с manage.py) создать файл .env с содержимым:
    
    NAME='pgdb'
    USER='root'
    PASSWORD='root'
    HOST='localhost'
    PORT='5437'

    DEFAULT_FROM_EMAIL='почта'
    SERVER_EMAIL='почта'
    EMAIL_HOST_USER='почта без @что-то.ru'
    EMAIL_HOST_PASSWORD='пароль'

Перейти в директорию с yml, выполнить команду:

    docker-compose up