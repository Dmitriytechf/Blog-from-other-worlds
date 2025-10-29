# Project: 🌌 *Blog-From-Other-Worlds*

**Проект представляет собой многофункциональный сайт в формате блога.**  Название отсылает на рассказ *«Цвет из иных миров»* (англ. The Colour Out of Space) **Говарда Филлипса Лавкрафта**, написанный в марте *1927* года. 


## Описание

### 🚀 Возможности и развитие
✅ Блог с упором на **бэкенд-функциональность**  
✅ Постепенное развитие **фронтенд-части**  
✅ Подключенное **API** с документацией (см. ниже)  
✅ Расширение функционала по мере развития проекта 

### 📊 Основной функционал для пользователя
- Полный CRUD (создание, чтение, обновление, удаление) для ваших постов
- Возможность оставлять комменатрии к постам
- Удобная авторизация и аутентификация
- Капча от ботов во время авторизации
- Возможность ставить лайки к постам и комментариям
- Работа с API
- Пагинация на сайте

### ⚙️ Основной функционал работы с проектом для разработчика и администратора
- Работа с API
- Удобная панель администратора
- Настройки тестов
- Настройки flake8 для оформления проекта
- Docker контейнеры

## 🛠️ Стек технологий

### Основные технологии
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-3.14-ff1709?logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

### Тестирование
![Pytest](https://img.shields.io/badge/Pytest-8.4.0-0A9EDC)
![Pytest Django](https://img.shields.io/badge/Pytest_Django-4.11.1-4B32C3)

- Бэкенд: Python 3.7+, Django 5.1+
- API: Django REST Framework 3.12+
- Фронтенд: Bootstrap

## Внешний вид

### Главная
<img width="1268" height="939" alt="image" src="https://github.com/user-attachments/assets/4ae3470f-91ea-45e6-8a32-3ba9b91405e4" />
<img width="1394" height="901" alt="image" src="https://github.com/user-attachments/assets/d9ac1f5d-6266-4e11-83e3-4e8e1055894c" />
<img width="1290" height="774" alt="image" src="https://github.com/user-attachments/assets/2907e70e-3b9e-476e-a355-b82141af7687" />

### Отдельный пост
<img width="1238" height="912" alt="image" src="https://github.com/user-attachments/assets/9de8962b-e8e8-4e12-976e-e8991ccf7208" />
<img width="1404" height="908" alt="image" src="https://github.com/user-attachments/assets/15b86ba6-2e47-4b05-8ece-ed020e46c229" />

### Регистрация
<img width="1041" height="919" alt="image" src="https://github.com/user-attachments/assets/2f26e574-cb9f-40d3-b477-473a4ed2d150" />


## 🚀 Установка
1. Клонируйте репозиторий:
```bash
git clone <название-репозитория>
cd <название-репозитория>
```

2. Создать и активировать виртуальную среду:
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Перейдите в backend и установить зависимости из файла requirements.txt:
```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
python manage.py migrate
```

5. Запустить проект:
```bash
python manage.py runserver
```

## Работа с API. Примеры запросов

### GET запросы:
#### 📄 Получение списка публикаций
```http://127.0.0.1:8000/api/v1/post/``` - запрос по адресу
```
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {...}
  ]
}
```
Можно задать параметры *limit* и *offset* при запросе

#### 📄 Получение конкретной публикации
```http://127.0.0.1:8000/api/v1/post/{id}/``` - запрос по адресу
```
{
  "id": 0,
  "title": "string",
  "content": "string",
  "author": 0,
  "created_date": "2019-08-24T14:15:22Z",
  "image": "http://example.com"
}
```

## 📚 Документация к API
После применения миграций `python manage.py migrate `  и запуска проекта командной `python manage.py runserver` можно перейти на локальный сервер. Там Вам будет доступна документация проекта по ссылке
`http://127.0.0.1:8000/redoc/`. В ней **более подробно** расипсаны все способы запросов к API.

## 👨‍💻 Автор
[Дмитрий] - [https://github.com/Dmitriytechf]
