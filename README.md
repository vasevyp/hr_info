# Приложение по учету персонала

### Приложение позволяет получить следующую информацию:
  
- Данные по персоналу на текущий рабочий день текущего месяца и за прошедшие месяцы по выбору:
-       - отработано человеко-дней
-       - отработано человеко-часов
-       - начислено зарплаты
- Список персонала с основными данными  
- Персональные данные сотрудника с текущими результатами:
-       - отработано часов, 
-       - начислено зарплаты
-       - информация по отпускам, больничным и т.п.
- Табель текущего месяца и табель за прошедшие месяцы по выбору  
- Зарплата текущего месяца и зарплата за прошедшие месяцы по выбору  
- Табель отсутствия на работе (Отпуска/больничные и др.)  

### Загрузка данных в приложение и выгрузка резудьтатов

 - Заргузка данных в приложение производится через административную панель, через форму загрузки, из файлов csv или xlsx.
 - Вывод/скачивание данных по сотрудникам зарплате и табелю возможен в формате pdf или csv/xlsx.

### Порядок запуска проекта

#### Шаг 1: Создайте виртуальную среду:

Обязательно использовать версию Python 3.10 (в оригинале используется Python 3.10.14)

Пользователи Unix / Linux / macOS выполняют следующую команду

python3 -m venv env

Пользователи Windows запускают следующую команду

py -m venv env

#### Шаг 2: Активируйте виртуальную среду и проверьте ее:

Пользователи Unix / Linux / macOS выполняют следующую команду

source env/bin/activate

Пользователи Windows запускают следующую команду

.\env\Scripts\activate

#### Шаг 3:Устанавливаем необходимые пакеты из requirements.txt:

pip3 install -r requirements.txt

#### Шаг 4:Создание миграции для БД:

python manage.py makemigrations

#### Шаг 5:Миграция данных для таблиц:

python manage.py migrate

#### Шаг 6:Создать суперпользователя:

python manage.py createsuperuser

#### Шаг 7:Запуск локального сервера:

python manage.py runserver

#### Шаг 8: Открытие проекта в браузере:

Запуск сервера разработки в браузере по адресу http://127.0.0.1:8000/




