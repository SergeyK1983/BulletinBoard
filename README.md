## "ДОСКА ОБЪЯВЛЕНИЙ"
___

    Python 3.10
    Django 4.2
    Django REST framework 3.14
    PostgreSQL 15.4    
    Celery 5.3
    Redis 5.0
    Docker

---

### Задача:

Необходимо разработать интернет-ресурс для фанатского сервера одной известной MMORPG — что-то вроде доски объявлений. 
Пользователи нашего ресурса должны иметь возможность:

1. Зарегистрироваться в нём. При регистрации пользователю должен получить e-mail с приветствием.
2. После регистрации им становится доступно создание и редактирование объявлений. Объявления состоят из заголовка и 
текста, внутри которого могут быть картинки.
3. Пользователи могут оставлять комментарии (отклики) на объявления других пользователей, состоящие из простого текста. 
Пользователь на чьё объявление бы оставлен комментарий должен получить e-mail с оповещением.
4. Пользователь может принять комментарий (отклик), после чего пользователь оставивший отклик должен получить e-mail с оповещением.
5. Также пользователю должна быть доступна приватная страница с его объявлениями, внутри которой он может фильтровать 
объявления, удалять их и принимать отклики.
6. Кроме того, пользователь обязательно должен определить объявление в одну из следующих категорий: Танки, Хилы, ДД, 
Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний.

---

### API endpoint-s:

#### ann

GET. Header: Content-Type = application/json.\
Вывод карточек всех объявлений на странице.\
Фильтры: author, category (DD, FR, GM, HL, MCH, PM, QG, SM, TK, TN), date_after, date_before

    /ann/v1/adboard/
    
    {
    "links": {
        "next": "http://api.example.org/ann/v1/adboard/?page=2",
        "previous": null
    },
    "context": null,
    "count": 14,
    "pages_count": 2,
    "board_list": [
        {
            "id": 39,
            "author": "Masha",
            "category": "QG",
            "title": "Моя первая публикация",
            "article": "Что-то очень интересное",
            "images": "http://api.example.org/media/announcement/5%20-%20Masha/2024/3/4/bloodelf1.jpg",
            "files": null,
            "date_create": "04.03.2024 14:11:29"
        },
        ...
      ]
    }

GET. Header: Content-Type = application/json.\
Вывод страницы с объявлением

    /ann/v1/adboard/page/<int:id>/

GET. Header: Content-Type = application/json. Authorization = Token ...\
Создание нового объявления

    /ann/v1/adboard/page/create/
    {"Detail": "Метод GET не разрешен"}

POST. Header: Content-Type = multipart/form-data. Authorization = Token ...\
Создание нового объявления

    /ann/v1/adboard/page/create/

    category = (DD, FR, GM, HL, MCH, PM, QG, SM, TK, TN), required
    title = string, required
    article = string, required
    images = file
    files = file

GET. Header: Content-Type = application/json. Authorization = Token ...\
Изменение объявления

    /ann/v1/adboard/page/<int:id>/update/

POST. Header: Content-Type = multipart/form-data. Authorization = Token ...\
Изменение объявления

    /ann/v1/adboard/page/<int:id>/update/

    category = (DD, FR, GM, HL, MCH, PM, QG, SM, TK, TN), required
    title = string, required
    article = string, required
    images = file
    files = file

    {
    "state": 1,
    "message": "Изменение прошло успешно"
    }

GET. Header: Content-Type = application/json. Authorization = Token ...\
Удаление объявления

    /ann/v1/adboard/page/<int:id>/destroy/
    {'msg': 'Удаление публикаций', 'method': 'POST'}

POST. Header: Content-Type = application/json. Authorization = Token ...\
Удаление объявления

    /ann/v1/adboard/page/<int:id>/destroy/
    {'status': 'Публикация удалена!'}

#### cab

GET. Header: Content-Type = application/json. Authorization = Token ...\
Страница пользователя
Фильтры: category (DD, FR, GM, HL, MCH, PM, QG, SM, TK, TN)-select, date_after, date_before

    /cab/v1/profile/<int:id>/

GET. Header: Content-Type = application/json. Authorization = Token ...\
Страница просмотра конкретной публикации пользователя

    /cab/v1/profile/<str:username>/<int:id>/

GET. Header: Content-Type = application/json\
Аутентификация (dj_rest_auth)

    /cab/v1/profile/login/

    {
    "username": "",
    "email": "",
    "password": "",
    "content-type": "multipart/form-data"
    }

POST. Header: Content-Type = multipart/form-data\
Аутентификация (dj_rest_auth)

    /cab/v1/profile/login/

    username = ""
    email = ""
    password = ""

    {"key": "99b830f2be4f456d25b966f441bd5d009e1f0517"}

POST. Header: Content-Type = application/json. Authorization = Token ...\
Выход (dj_rest_auth)

    /cab/v1/profile/logout/
    {"detail": "Успешно вышли."}

GET. Header: Content-Type = application/json\
Регистрация (dj_rest_auth)

    /cab/v1/profile/register/

    {
    "username": "",
    "email": "",
    "password1": "",
    "password2": "",
    "content-type": "multipart/form-data"
    }

POST. Header: Content-Type = multipart/form-data\
Регистрация (dj_rest_auth)

    /cab/v1/profile/register/

    {
    "id": 58,
    "username": "Vasya",
    "email": "examp4@yandex.ru"
    }

GET. Header: Content-Type = application/json. Authorization = Token ...\
Удаление пользователя (dj_rest_auth)

    /cab/v1/profile/destroy/
    {'msg': 'Удаление аккаунта', 'method': 'POST'}

POST. Header: Content-Type = application/json. Authorization = Token ...\
Удаление пользователя (dj_rest_auth)

    /cab/v1/profile/destroy/
    {'status': 'Аккаунт пользователя удален'}

GET. Header: Content-Type = application/json. Authorization = Token ...\
Изменение данных пользователя

    /cab/v1/profile/update/

    {
    "data": {
        "username": "serg",
        "first_name": "Сергей",
        "last_name": "Карачаров",
        "email": "examp@gmail.com",
        "photo": "/media/cabinet/3-serg/2024/3/3/Master_Yoda.jpg",
        "date_birth": null
    },
    "content-type": "multipart/form-data"
    }

POST. Header: Content-Type = multipart/form-data. Authorization = Token ...\
Изменение данных пользователя

    /cab/v1/profile/update/

    username = "serg"
    first_name = "Сергей"
    last_name = "Карачаров"
    email = "examp@gmail.com"
    photo = file.jpg
    date_birth = 2000-01-01
    
    {
    "state": 1,
    "message": "Изменение прошло успешно"
    }

GET. Header: Content-Type = application/json. Authorization = Token ...\
Изменение пароля (dj_rest_auth)

    /cab/v1/profile/change-pass/

    {
    "data": {
        "new_password1": "",
        "new_password2": ""
    },
    "content-type": "application/json"
    }

POST. Header: Content-Type = application/json. Authorization = Token ...\
Изменение пароля (dj_rest_auth)

    /cab/v1/profile/change-pass/

    {
    "new_password1": "secret",
    "new_password2": "secret"
    }

    {
    "detail": "Новый пароль сохранён."
    }

#### com

GET. Header: Content-Type = application/json. Authorization = Token ...\
Создание комментария к объявлению

    /com/v1/add-comment/<int:id>/
    {"Detail": "Метод GET не разрешен"}

POST. Header: Content-Type = application/json. Authorization = Token ...\
Создание комментария к объявлению

    /com/v1/add-comment/<int:id>/
    {
    "comment": "Новый комментарий"
    }
    Response:
    {
    "to_post": "Объявление",
    "comment": "Новый комментарий"
    }

GET. Header: Content-Type = application/json. Authorization = Token ...\
Просмотр своих комментариев к объявлениям других авторов на своей странице
Фильтры: author, category (DD, FR, GM, HL, MCH, PM, QG, SM, TK, TN), date_after, date_before

    /com/v1/<str:username>/my-comment/

GET. Header: Content-Type = application/json. Authorization = Token ...\
Просмотр комментариев к своему объявлению
    
    /com/v1/<str:username>/<int:id>/comments-to-post/

POST. Header: Content-Type = application/json. Authorization = Token ...\
Изменение статуса комментария на принято (accepted).
    
    /com/v1/comments-to-accepted/<int:id>/
    {
    "accepted": "True"
    }
    Response:
    {
    "accepted": true
    }

