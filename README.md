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

## 🛠️ Стек технологий

### Основные технологии
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-3.14-ff1709?logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)

### Тестирование
![Pytest](https://img.shields.io/badge/Pytest-8.4.0-0A9EDC)
![Pytest Django](https://img.shields.io/badge/Pytest_Django-4.11.1-4B32C3)

- Бэкенд: Python 3.7+, Django 5.1+
- API: Django REST Framework 3.12+
- Фронтенд: Bootstrap


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

3. Установить зависимости из файла requirements.txt:
```bash
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
