# Заготовка кода для хранения заказов пользователей

## Приступая к работе

Следуя этим инструкциям, вы получите копию проекта, которая будет запущена на вашем локальном компьютере для целей разработки и тестирования. Примечания о том, как развернуть проект в действующей системе, см. в разделе Развертывание.

### Предпосылки

Клонируйте проект на локальный компьютер

```commandline
git clone https://github.com/s-klimov/simple_market.git
```

Для работы сервиса у вас должны быть установлены:
* python версии 3.10 и выше
* poetry версии 1.4.x 

### Развертывание

1. Установите зависимости
```commandline
poetry install
```
2. Активируйте локальное окружение
```commandline
poetry shell
```

## Запуск проекта

### Запустите сервер
> Проект запускается из папки moex_fastapi
```commandline
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Выполните тестирование
> Модульные тесты запускаются из корневой папки проекта  
```commandline
pytest -v -p no:warnings
```

### Ознакомьтесь в автодокументацией
Документация разработанных методов доступна по урлу [/docs](http://0.0.0.0:5000/docs)