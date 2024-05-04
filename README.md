# Grafana Dashboards Exporter

Этот репозиторий содержит простой скрипт Python для экспорта дашбордов Grafana с помощью их API. Скрипт сохраняет дашборды в формате JSON, архивирует их и удаляет исходную папку.

## Требования

- Python 3.x
- Модули: requests, json, os, shutil, datetime

## Установка

1. Скопируйте файлы `main.py` и `data.py` из папки `Python`.
2. Установите необходимые модули с помощью pip: `pip install requests`.

## Настройка

1. Откройте файл `data.py` и укажите значения для `url` (URL вашего экземпляра Grafana), `key` (API ключ вашего экземпляра Grafana) и `save` (Если хотите изменить путь сохранения архива)
2. Сохраните изменения.

## Использование

1. Запустите скрипт `main.py` из командной строки: `python3 main.py`. Если вы не указали ключ, то: `python3 main.py { key }`
2. Скрипт экспортирует все дашборды из вашего экземпляра Grafana в папку `/tmp/dashboards`.
3. После успешного экспорта скрипт архивирует папку `/tmp/dashboards` в формате `dashboards_DD-MM-YYYY.tar.gz` и сохраняет архив рядом со скриптом `main.py`.
4. Скрипт удаляет папку `/tmp/dashboards` после создания архива.

## Примечания

- Убедитесь, что у вас есть необходимые права на запись в папку `/tmp` и на удаление созданной папки.
- Если вы хотите изменить путь экспорта дашбордов, отредактируйте переменную `output_folder` в файле `main.py`.

## Автор

[TG: BesedinDV](https://t.me/BesedinDV)
