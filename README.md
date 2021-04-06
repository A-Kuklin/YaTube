# Учебный проект "yatube"<br>
<b>Яндекс.Практикум   |   Python   |   Backend</b>

Пример развёрнут на [pythonanywhere](http://kuklin.pythonanywhere.com/ "http://kuklin.pythonanywhere.com/")<br>
<a href="http://kuklin.pythonanywhere.com/"><img src="https://lh3.googleusercontent.com/x97A5Yh8X-KNHbmX7HMHB9PptxWA1UJ4e-66YQnXsG30cNwCNn2URklW1F-IWNAARE4RchJ6LcTsZqDPIZJkpdIIqxn-tmLA2ZYG0kZA09KD9rgMAJk7JaeeQk21QG6QStCTyvdrlEKLIcegfhwGNNpoXVN8x8CxhhaSkOodNLH6Zllk0eBm3PE8eHZzV62Gw0SlI8YJJaH_S8s25lqySXDNfdEMJtPCvWMrj64at7vmpfmPOn7IDqwlW4ui_T4LZXr9MN9DLq7zsvBOOTYmV-ITH28NBWoEAkhFhvJap1H7nYoOv79GHc-4NxKYWqYrodFG9JZxNUtahse55_2OLHRvik7B76xmDe7svuZuEqejx6Ax9IDuhWWO7_4MklVayKFpIjH8bX0Ce7M85_fb0IW5weF8DZLGP3sijEsCMeiGZU2-_hlVzFwZZKH_kClEW79P72rYzxWVwnDteMrY3aWMR9EzhrzTrXIS9v0J4XowGGhQttsNMoTKfN_9eEtTJPUFG9Vi0q6I7aFAfRf7R3Q6teKx4qfkDsHDYjt8cPKe6AJo7P6PCYA8UVUYEpoHNlMVZLNTk11CWtoObHjLFV0RkD0xxw6dZeKEErfhGRdQq4exsZjPEj_lamoGWFN2VnxVDoBY9RppmltozKDAQBFMDctgkSTbPGOnfW3pMeMb2L8fwjtmF7dDKXRCknbYJABV3392_GoDvREK7XDK9mPg=w770-h506-no?authuser=0?.jpg" width="500" ></a>
<br>

Проект блога: 
- можно создавать / редактировать /  посты с картинками, 
- присваивать постам заданные категории, 
- управлять подпиской на авторов.<br>

Реализовано кэширование:<br>
работает на главной странице и обновляется раз в 20 секунд.<br> 
Созданы unit-тесты.

## Технологический стек
Python, Django, Git, Bootstrap, SQLite

## Локальное развёртывание
Клонируем репозиторий на локальную машину:<br>
```$ git clone https://github.com/A-Kuklin/yatube.git```

 Создаем виртуальное окружение:<br>
 ```$ python -m venv venv```
 
 Устанавливаем зависимости:<br>
```$ pip install -r requirements.txt```

Создание и применение миграций:<br>
```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:<br>
```$ python manage.py runserver```
