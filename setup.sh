#!/bin/bash

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Virtual environment already exists"
    source venv/bin/activate
fi

# Создание директории assets если её нет
if [ ! -d "assets" ]; then
    mkdir assets
fi

# Создание пустых JSON файлов если их нет
if [ ! -f "assets/users.json" ]; then
    echo "[]" > assets/users.json
fi

if [ ! -f "assets/products.json" ]; then
    echo "[]" > assets/products.json
fi

# Запуск тестов
echo "Running tests..."
pytest tests/

# Запуск проекта
echo "Starting marketplace..."
python main.py
