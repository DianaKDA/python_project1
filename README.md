# Мини-маркетплейс

## Описание
Мини-маркетплейс - это консольное приложение, реализующее базовый функционал торговой площадки с возможностью регистрации покупателей и продавцов. Проект разработан с использованием ООП и следует принципам SOLID.

## Структура проекта
python_project1/
├── src/ # Исходный код проекта
│ ├── init.py # Инициализация модуля
│ ├── models.py # Модели данных (User, Product)
│ ├── marketplace.py # Основная бизнес-логика
├── assets/ # Файлы данных и ресурсы
│ ├── users.json # База данных пользователей
│ └── products.json # База данных товаров
├── tests/ # Модульные тесты
│ ├── init.py
│ ├── test_marketplace.py
│ └── test_models.py
├── main.py # Точка входа в приложение
├── requirements.txt # Зависимости проекта
├── setup.sh # Скрипт установки
└── README.md # Документация

## Функционал

### Для покупателей (Buyer):
- Регистрация и авторизация
- Просмотр всех доступных товаров
- Добавление товаров в корзину
- Просмотр корзины
- Оформление покупок

### Для продавцов (Seller):
- Регистрация и авторизация
- Добавление новых товаров
- Редактирование существующих товаров
- Удаление товаров
- Просмотр списка своих товаров

## Системные требования
- Python 3.7+
- OS: Linux/MacOS (для автоматической установки через setup.sh)
- Поддерживаемые ОС: Linux, MacOS, Windows (для ручной установки)

## Установка и запуск

### Автоматическая установка (Linux/MacOS)
```bash
#Клонирование репозитория
git clone https://github.com/DianaKDA/python_project1.git
cd mini-marketplace
#Установка и запуск
chmod +x setup.sh
./setup.sh
```
### Ручная установка (Windows/Linux/MacOS)
1. Клонируйте репозиторий:

```bash
git clone https://github.com/DianaKDA/python_project1.git
cd mini-marketplace
```

2. Создайте виртуальное окружение:
```bash
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите проект:
```bash
python main.py
```

## Разработка

### Установка зависимостей для разработки
```bash
pip install -r requirements.txt
```

### Запуск тестов
```bash
# Запуск всех тестов
pytest tests/

# Запуск тестов с отчетом о покрытии
pytest --cov=src tests/
```
## Структура данных

### users.json
```json
[
    {
        "username": "string",
        "password": "string",
        "user_type": "buyer|seller",
        "cart": []
    }
]
```

### products.json
```json
[
    {
        "id": "integer",
        "name": "string",
        "price": "float",
        "description": "string",
        "seller": "string"
    }
]
```

## Принципы разработки
- Код написан в соответствии со стандартом PEP 8
- Использована объектно-ориентированная парадигма программирования
- Соблюдены принципы SOLID
- Все классы и методы имеют документацию (docstrings)
- Код покрыт модульными тестами

## Лицензия
MIT License

## Автор
Курницова Диана