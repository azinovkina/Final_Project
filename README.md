Проект содержит UI тесты ЛК "Ростелеком": https://b2c.passport.rt.ru

В корневой папке лежит файл param.py с Тестовыми данными (ТД)

Папка Tests содержит файл для запуска автотестов:

tests_rtl_lk.py 

Папка Pages содержит следующие файлы:

base.py - содержит библиотеку Smart Page Object

auth_page.py - содержит класс для страницы "Авторизация"

elements.py - содержит класс для определения элементов на веб-страницах

register_page.py - содержит класс для страницы "Регистрация"


Запуск тестов:


1) Install all requirements:
   ```bash
    pip install -r requirements.txt
   ```
2) Run tests:

    ```bash
    python3 -m pytest -s -v tests_rtl_lk.py

    ```
   или
    ```bash
    python -m pytest -s -v tests_rtl_lk.py

    ```