#!/bin/bash

# URL и ключ для Grafana API
API_URL=""
API_KEY=""

# Путь для сохранения Dashboard
SAVE_PATH="."

# Проверка и создание папки для сохранения, если она не существует
if [ ! -d "$SAVE_PATH" ]; then
  mkdir -p "$SAVE_PATH"
fi

# Получение списка всех Dashboard
DASHBOARDS=$(curl -s -H "Authorization: Bearer ${API_KEY}" "${API_URL}/search?query=&type=dash-db" | jq -r '.[] | @base64')

# Скачивание Dashboard
for DASHBOARD_ENCODED in $DASHBOARDS; do
  _DASHBOARD_JSON=$(echo "$DASHBOARD_ENCODED" | base64 --decode)
  DASHBOARD_ID=$(echo "$_DASHBOARD_JSON" | jq -r '.uid')
  DASHBOARD_TITLE=$(echo "$_DASHBOARD_JSON" | jq -r '.title')

  if [ -z "$DASHBOARD_TITLE" ]; then
    echo "Пропуск Dashboard с пустым заголовком: ${DASHBOARD_ID}"
    continue
  fi

  DASHBOARD_URL="${API_URL}/dashboards/uid/${DASHBOARD_ID}"
  DASHBOARD_FILE="${SAVE_PATH}/${DASHBOARD_TITLE}.json"

  echo "Скачивание Dashboard: ${DASHBOARD_TITLE}"
  curl -s -H "Authorization: Bearer ${API_KEY}" "${DASHBOARD_URL}" > "${DASHBOARD_FILE}"
done

echo "Все Dashboard скачаны"