from sys import argv, exit
import requests
import json
import data

if data.url == "":
    print("Не указан { url } в data.py")
    exit()

if data.key == "":
    try:
        data.key = argv[1]
    except IndexError:
        print("Ключ не прописан в data.py или не указан в качестве аргумента")
        exit()

headers = {
    "Authorization": f"Bearer {data.key}",
    "Content-Type": "application/json",
}

response = requests.get(f"{data.url}/api/search", headers=headers)

if response.status_code == 200:
    uids = [dashboard["uid"] for dashboard in response.json()]
else:
    print(f"Ошибка при получении дашборда: {response.status_code}")
    exit()


for dashboard in uids:
    response = requests.get(
        f"{data.url}/api/dashboards/uid/{dashboard}",
        headers=headers,
    )

    if response.status_code == 200:
        dashboard_json = response.json()
        with open(f"dashboard_{dashboard}.json", "w") as outfile:
            json.dump(dashboard_json, outfile, indent=4)
            print(f"Дашборд {dashboard} успешно экспортирован.")
    else:
        print(f"Ошибка при экспорте дашборда: {response.status_code} {response.text}")


print(f"Дашборды успешно экспортированны!\nКоличество: {len(uids)}")