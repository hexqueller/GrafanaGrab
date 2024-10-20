# Grafana Dashboards Exporter
![Image alt](https://github.com/V1RUSnya/GrafanaGrab/blob/main/image/screenshot.png)


Dockerhub image: hexqueller/grafanagrab:latest


Этот репозиторий содержит два скрипта для экспорта дашбордов Grafana с помощью их API: Python-версию и bash-версию. Скрипты сохраняют дашборды в формате JSON и архивируют их.

## Требования

### Python-версия

- Python 3.x
- Модули: requests, json, os, datetime (server: http.server urllib.parse)

### Bash-версия

- bash 4.x
- jq (для работы с JSON)
- curl (для запросов к API Grafana)

## Установка

### Python-версия

1. Скопируйте файлы из папки `Python`.
2. Установите необходимые модули с помощью pip: `pip install requests`.

### Bash-версия

1. Скопируйте файл `main.sh` из репозитория.
2. Установите права на выполнение скрипта: `chmod +x main.sh`.

## Настройка

### Python-версия

1. Откройте файл `config.py` и укажите значения для `url` (URL вашего экземпляра Grafana), `key` (API ключ вашего экземпляра Grafana), `port` (порт сервера) и `save` (Если хотите изменить путь сохранения архива)
2. Сохраните изменения.

### Bash-версия

1. Откройте файл `main.sh` и укажите значения для `API_URL` (URL вашего экземпляра Grafana), `API_KEY` (API ключ вашего экземпляра Grafana) и `SAVE_PATH` (Если хотите изменить путь сохранения архива)
2. Сохраните изменения.

## Использование

### Python-версия

1. Запустите скрипт `main.py` из командной строки: `python3 main.py`. Если вы не указали ключ, то: `python3 main.py { key }`
2. Скрипт экспортирует все дашборды из вашего экземпляра Grafana в папку `$save/data`.
3. Каждое изменение после предыдущего использования будет отражено в файле `/data/log.txt`.
4. После успешного экспорта скрипт архивирует папку `/data` в формате `dashboards_DD-MM-YYYY.tar.gz` и сохраняет архив в `$save`.

### Server-версия

1. Запустите скрипт `sever.py` из командной строки: `python3 main.py` или создайте сервис.
2. Откройте браузер и введите http:localhost:8000 (порт по умолчанию).
3. Для экспорта используется кнопка `Обновить`.
4. Доступ к открытой части можно регулировать используя стандартные инструменты (напр. `iptables`).

### Bash-версия

1. Запустите скрипт `main.sh` из командной строки: `./main.sh`
2. Скрипт экспортирует все дашборды из вашего экземпляра Grafana в папку `/tmp/dashboards`.
3. После успешного экспорта скрипт архивирует папку `/tmp/dashboards` в формате `dashboards_DD-MM-YYYY.tar.gz` и сохраняет архив в указанной директории `SAVE_PATH`.
4. Скрипт удаляет папку `/tmp/dashboards` после создания архива.
