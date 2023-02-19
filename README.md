# <h2 align="center">API YAMDB</h2>

## О проекте

Проект YaMDb собирает отзывы пользователей на произведения.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен.
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка
произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только
аутентифицированные пользователи.

Документацию к API можно найти  по адресу [<<ваш сервер или хостинг>>/redoc](http://localhost:8000/redoc/) после запуска проекта.

## Проект выполнялся в команде из 3 человек

- [Кирилл Насонкин](https://github.com/kirill-nasonkin)
- [Лев Алексеев](https://github.com/heroinboy)
- [Ростислав Рыманов](https://github.com/RostIiIslav)

## Технологии

Python 3.9, Django 3.2, DRF, Simplejwt, csv, sqlite3

## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/kirill-nasonkin/api_yamdb.git
cd api_yamdb
```

- Cоздать и активировать виртуальное окружение:

```bash
Unix
python3 -m venv env
source env/bin/activate
Windows
python -m venv env
source env/Scripts/activate
```

- Установить зависимости из файла requirements.txt:

```bash
Unix
python3 -m pip install --upgrade pip
Windows
python -m pip install --upgrade pip

pip install -r requirements.txt

```

- Выполнить миграции:

```bash
cd api_yamdb
Unix
python3 manage.py migrate
Windows
python manage.py migrate
```

- *Дополнительно* Для автоматического наполнения БД из csv файлов в папке
project_root/static/data применить команду:

```bash
Unix
python3 manage.py fill_my_db
Windows
python manage.py fill_my_db
```

- Запустить проект:

```bash
Unix
python3 manage.py runserver
Windows
python manage.py runserver
```

## Примеры запросов

### GET запросы

- `api/v1/posts/`
Список всех публикаций. При указании параметров **limit** и **offset** выдача работает с пагинацией.

- `api/v1/posts/{post_id}/`
Пост с id = 'post_id'.

- `/api/v1/posts/{post_id}/comments/`
Все комментарии к определённому посту.

- `api/v1/posts/{post_id}/comments/{id}/`
Определённый комментарий.

- `api/v1/groups/`
Все группы соцю сети.

- `api/v1/groups/{id}`
Определённая группа.

- `api/v1/follow/`
Все подписки пользователя, который запрашивает ресурс. При указании параметра **search** будет осуществляться поиск по подпискам пользователя.

### POST запросы

- `api/v1/posts/`
Создать новый пост.
- `/api/v1/posts/{post_id}/comments/`
Создать новый комментарий.
- `api/v1/follow/`
Подписаться на автора.

Информацию по другим запросам и примеры их выполнения вы можете найти в подробной документации к API, запустив проект и перейдя по адресу:

```bash
http://localhost:8000/redoc/
```
