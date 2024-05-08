import config
import parse

from sys import argv, exit
import requests
import json
import os
import shutil
import tarfile
from datetime import datetime

if config.url == "":
    print("Не указан { url } в config.py")
    exit()

if config.key == "":
    try:
        config.key = argv[1]
    except IndexError:
        print("Ключ не прописан в config.py или не указан в качестве аргумента")
        exit()

def main():
    error_count = 0
    headers = {
        "Authorization": f"Bearer {config.key}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{config.url}/api/search", headers=headers)

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
            f"{config.url}/api/dashboards/uid/{dashboard}",
            headers=headers,
        )

        if response.status_code == 200:
            dashboard_json = response.json()
            dashboard_title = parse.get_dashboard_title(dashboard_json) + "_ver_" + str(parse.get_dashboard_ver(dashboard_json))
            if not dashboard_title:
                print(f"Не удалось получить заголовок дашборда для {dashboard}. Будет использовано имя по умолчанию.")
                dashboard_title = "dashboard"
            filename = f"dashboard_{dashboard_title}.json"
            dashboard_json_converted = parse.convert_to_import_format(dashboard_json)
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

    if config.save == "":
        config.save = os.path.join(script_dir, archive_name)
    else:
        config.save = config.save + "/" + archive_name

    with tarfile.open(config.save, "w:gz") as tar:
        tar.add(output_folder, arcname=os.path.basename(output_folder))

    print(f"\nАрхив {config.save} успешно создан.")

    shutil.rmtree(output_folder)
    print("Очистка завершена!")

if __name__ == "__main__":
    main()
