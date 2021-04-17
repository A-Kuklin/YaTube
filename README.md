# Учебный проект "Yatube"<br>
<b>Яндекс.Практикум   |   Python   |   Backend</b>
<br><br>

Пример развёрнут на [pythonanywhere](http://kuklin.pythonanywhere.com/ "http://kuklin.pythonanywhere.com/")<br>
<a href="http://kuklin.pythonanywhere.com/"><img src="https://lh3.googleusercontent.com/6m3tGE89nnedkMppz7OZknOAYlSIF3uPE4sqyEXm2Piwyo5qc15PiHD2dYdrjpIrFs_d_qDmIPnicjGQVRWwbatV8FYwLfE_SZJ4bmcUjmcxsWRYPxSDkvNt75vxrI-FseZMrTPdn5uoR3sjoSiHPuUMVOd-Bcep4KNFsI1AgZ9LIqTGeVkYqOh3XF09bhc2Hvs_skQOyLnpdCREUaCevHLOB7h2ReGLIMLOBShC796cG7_04m6kGVYcUHmeUObaKWnhUIiQirf72Blpov3SbrC1x7RmLk6OME2-Ahw5Qnz0UEkmUYuc3rUZeirO-pgxuXnVOZt2RzZ5JcvG1CwHD1aUZwVa8GO0UzUX9PKGm3FCmDwVY6-wzqLI-GQhfzG39t4Cp9yMlXHqbU5un_lBhs2oy4B4CU4EobmFxdiYme3mWEFGeeVblNbTDQ9vdfBUejPAnNAhyQnVfpD04cFklhADCmA4Jfuh1_NomelRQ80wpP9y1R5bDF4VW4qBTCUdhuOR5LfQchvzIyNbwpP8ipFaZHzD0s6EWi0y4aXNFeHfx0IXOKuHI1Zum35XdcvJ-_AlsNPIc6bGPzoHQvNNOu2I97b8KLxiyEm3qGSyR3uVxq5ULAxb0PQRzcpWXN7pIBLcX5rKCjO0cyXTvlrO1_gTR94h08VZ8QcshTLP6eNQJf2YSW0K2j236JP1esursgk92HpTnW_20Ykxg0JbMI_V=w770-h506-no?authuser=0?.jpg" width="500" ></a>
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
