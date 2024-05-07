#!/bin/bash

##################
### Переменные ###
API_URL="" # Ссылка на Grafana в формате http://grafana:3000/api
API_KEY="" # Ключ сервисного аккаунта
SAVE_PATH="." # Путь сохранения
##################

if [ ! -d "$SAVE_PATH" ]; then
  mkdir -p "$SAVE_PATH"
fi

TMP_DIR="/tmp/dashboards"
if [ ! -d "$TMP_DIR" ]; then
  mkdir -p "$TMP_DIR"
fi

convert_to_import_format() {
  DASHBOARD_JSON=$(echo "$1" | jq '.')
  DASHBOARD_JSON=$(echo "$DASHBOARD_JSON" | jq 'del(.meta)')
  DASHBOARD_JSON=$(echo "$DASHBOARD_JSON" | jq '.dashboard | del(.id)')
  echo "$DASHBOARD_JSON"
}

DASHBOARDS=$(curl -s -H "Authorization: Bearer ${API_KEY}" "${API_URL}/search?query=&type=dash-db" | jq -r '.[] | @base64')

for DASHBOARD_ENCODED in $DASHBOARDS; do
  _DASHBOARD_JSON=$(echo "$DASHBOARD_ENCODED" | base64 --decode)
  DASHBOARD_ID=$(echo "$_DASHBOARD_JSON" | jq -r '.uid')
  DASHBOARD_TITLE=$(echo "$_DASHBOARD_JSON" | jq -r '.title')

  if [ -z "$DASHBOARD_TITLE" ]; then
    echo "Пропуск Dashboard с пустым заголовком: ${DASHBOARD_ID}"
    continue
  fi

  DASHBOARD_URL="${API_URL}/dashboards/uid/${DASHBOARD_ID}"
  DASHBOARD_FILE="${TMP_DIR}/${DASHBOARD_TITLE}.json"

  echo "Скачивание Dashboard: ${DASHBOARD_TITLE}"
  DASHBOARD_JSON=$(curl -s -H "Authorization: Bearer ${API_KEY}" "${DASHBOARD_URL}")

  CONVERTED_DASHBOARD=$(convert_to_import_format "$DASHBOARD_JSON")

  echo "$CONVERTED_DASHBOARD" > "${DASHBOARD_FILE}"
done

echo "Все Dashboard скачаны и конвертированы"

# Создание архива
ARCHIVE_NAME="dashboards_$(date +%d-%m-%Y).tar.gz"
tar -czf "${SAVE_PATH}/${ARCHIVE_NAME}" -C "${TMP_DIR}" .

echo "Архив создан: ${ARCHIVE_NAME}"

# Удаление папки /tmp/dashboards
rm -rf "${TMP_DIR}"

echo "Очистка завершена!"
