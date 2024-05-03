from sys import argv, exit
import requests
import json
import os
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

def main():
    error_count = 0
    headers = {
        "Authorization": f"Bearer {data.key}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{data.url}/api/search", headers=headers)

    if response.status_code == 200:
        uids = [dashboard["uid"] for dashboard in response.json()]
    elif response.status_code == 401:
        print(f"Неудачная авторизация ({response.status_code}).\nПроверьте ключ!")
        exit()
    else:
        print(f"Ошибка {response.status_code}")
        exit()

    output_folder = "/tmp/dashboards"
    os.makedirs(output_folder, exist_ok=True)

    for dashboard in uids:
        response = requests.get(
            f"{data.url}/api/dashboards/uid/{dashboard}",
            headers=headers,
        )

        if response.status_code == 200:
            dashboard_json = response.json()
            with open(os.path.join(output_folder, f"dashboard_{dashboard}.json"), "w") as outfile:
                json.dump(dashboard_json, outfile, indent=4)
                print(f"Дашборд {dashboard} успешно экспортирован.")
        else:
            print(f"Ошибка при экспорте дашборда: {response.status_code} {response.text}")
            error_count += 1

    print(f"\nДашборды успешно экспортированны!\nУспешно: {len(uids)}\nОшибок: {error_count}")

if __name__ == "__main__":
    main()