# Учебный проект "Yatube"<br>
<b>Яндекс.Практикум   |   Python   |   Backend</b>
<br><br>

Пример развёрнут на [pythonanywhere](http://kuklin.pythonanywhere.com/ "http://kuklin.pythonanywhere.com/")<br>
<a href="http://kuklin.pythonanywhere.com/"><img src="https://i.ibb.co/dWJRGhd/ex.jpg" width="500" ></a>
<br>

Проект блога: 
- можно создавать / редактировать / комментировать посты с картинками, 
- присваивать постам заданные категории, 
- управлять подпиской на авторов.<br>

Реализовано кэширование:<br>
работает на главной странице и обновляется раз в 20 секунд.<br> 
Созданы unit-тесты.
<br><br>

## Технологический стек
Python, Django, Git, Bootstrap, SQLite
<br><br>

## Локальное развёртывание
Клонируем репозиторий на локальную машину:<br>
```$ git clone https://github.com/A-Kuklin/yatube.git```

Создаем виртуальное окружение:<br>
 ```$ python -m venv venv```

Запускаем виртуальное окружение<br>

Устанавливаем зависимости:<br>
```$ pip install -r requirements.txt```

Создание и применение миграций:<br>
```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:<br>
```$ python manage.py runserver```
