### Дипломный проект TODOLIST

В данном проекте реализуем приложение для отслеживания выполнения задач и напоминаний.
___
Стек:
- python 3.10
- Django 4.1.1
- PostgreSQL

___
Для запуска проекта следует выполнить в терминале следующие команды:
```
docker-compose up -d
python manage.py migrate
python manage.py loaddata fixtures/ad.json fixtures/comments.json fixtures/users.json
```