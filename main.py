import requests
import json
import data

GRAFANA_URL = data.url
API_KEY = data.key
DASHBOARD_UID = data.uid

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

response = requests.get(
    f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}",
    headers=headers,
)

if response.status_code == 200:
    dashboard_json = response.json()
    with open(f"dashboard_{DASHBOARD_UID}.json", "w") as outfile:
        json.dump(dashboard_json, outfile, indent=4)
        print(f"Дашборд {DASHBOARD_UID} успешно экспортирован.")
else:
    print(f"Ошибка при экспорте дашборда: {response.status_code} {response.text}")



# Первая версия
# Экспорт сработал. Нужен сервисный аккаунт с привелегиями Viewer и ключ от него