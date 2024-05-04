from sys import argv, exit
import requests
import json
import os
import shutil
import tarfile
from datetime import datetime
import data

def get_dashboard_title(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("title", "")

def convert_to_import_format(dashboard_json):
    if "meta" in dashboard_json:
        del dashboard_json["meta"]
    if "id" in dashboard_json["dashboard"]:
        del dashboard_json["dashboard"]["id"]
    return dashboard_json["dashboard"]

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
            dashboard_title = get_dashboard_title(dashboard_json)
            if not dashboard_title:
                print(f"Не удалось получить заголовок дашборда для {dashboard}. Будет использовано имя по умолчанию.")
                dashboard_title = "dashboard"
            filename = f"dashboard_{dashboard_title}.json"
            dashboard_json_converted = convert_to_import_format(dashboard_json)
            with open(os.path.join(output_folder, filename), "w") as outfile:
                json.dump(dashboard_json_converted, outfile, indent=4)
                print(f"Дашборд {dashboard} успешно экспортирован как {filename}.")
        else:
            print(f"Ошибка при экспорте дашборда: {response.status_code} {response.text}")
            error_count += 1

    print(f"\nДашборды успешно экспортированны!\nУспешно: {len(uids)}\nОшибок: {error_count}")

    script_dir = os.path.dirname(os.path.realpath(__file__))
    now = datetime.now()
    date_format = now.strftime("%d-%m-%Y")
    archive_name = f"dashboards_{date_format}.tar.gz"

    if data.save == "":
        data.save = os.path.join(script_dir, archive_name)
    else:
        data.save = data.save + "/" + archive_name

    with tarfile.open(data.save, "w:gz") as tar:
        tar.add(output_folder, arcname=os.path.basename(output_folder))

    print(f"\nАрхив {data.save} успешно создан.")

    shutil.rmtree(output_folder)
    print("Очистка завершена!")

if __name__ == "__main__":
    main()
