# praktikum_new_diplom
1) Я не понял момент с отпиской. Уже несколько раз переписал viewset. Намекни, плиз, что не так в реализации.
2) У меня скачивание рецептов работает корректно. Опиши, плиз, как воспроизвести проблему.

##########################################

«Фудграм» — сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект доступен по ссылке:
https://farrukh.zapto.org/

## Инструкция по работе с проектом:
Для начала необходимо склонировать репозиторий:
```yaml
git clone https://github.com/farrukhrus/foodgram-project-react.git
```
Необходимо в рабочей директории проекта создать файл .env со своими секретами
```yaml
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<ваш пароль для базы данных>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<ваш секретный ключ для django проекта>
```
## Запуск проекта в контейнерах:
Из рабочей директории с docker-compose файлом выполните команду:
```yaml
sudo docker-compose -f <имя файла> up -d 
```
Выполните миграции и соберите статические данные
```yaml
sudo docker-compose -f <имя файла> exec backend python manage.py makemigrations
sudo docker-compose -f <имя файла> exec backend python manage.py migrate
sudo docker compose -f <имя файла> exec backend python manage.py collectstatic
sudo docker compose -f <имя файла> exec backend cp -r /app/static_django/. /static_django/
```
Создайте администратора
```yaml
sudo docker compose -f <имя файла> exec backend python manage.py createsuperuser
```

admin/pass: admin2@d.ru/admin
