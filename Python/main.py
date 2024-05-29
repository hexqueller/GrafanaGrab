import config
import parse
import logging0

from sys import argv, exit
import requests
import json
import os
import tarfile
from datetime import datetime

def fix_path_error(text):
    return text.replace("/", "-")

if config.url == "":
    print("Не указан { url } в config.py")
    exit()

if config.key == "":
    try:
        config.key = argv[1]
    except IndexError:
        print("Ключ не прописан в config.py или не указан в качестве аргумента")
        exit()

now = datetime.now()
date_format = now.strftime("%d-%m-%Y")
archive_name = "dashboards_{0}.tar.gz".format(date_format)

config.save = "{0}/{1}".format(config.save, archive_name)

def main():
    error_count = 0
    headers = {
        "Authorization": "Bearer {0}".format(config.key),
        "Content-Type": "application/json",
    }

    response = requests.get("{0}/api/search".format(config.url), headers=headers)

    if response.status_code == 200:
        uids = [dashboard["uid"] for dashboard in response.json()]
    elif response.status_code == 401:
        print("Неудачная авторизация ({0}).\nПроверьте ключ!".format(response.status_code))
        exit()
    else:
        print("Ошибка {0}".format(response.status_code))
        exit()

    output_folder, log_file = logging0.create_dir(config.save[:-len(archive_name)])

    for dashboard in uids:
        response = requests.get(
            "{0}/api/dashboards/uid/{1}".format(config.url, dashboard),
            headers=headers,
        )

        if response.status_code == 200:
            dashboard_json = response.json()
            dashboard_title = "{0}_ver_{1}".format(fix_path_error(parse.get_dashboard_title(dashboard_json)), parse.get_dashboard_ver(dashboard_json))
            logging0.logging(log_file, parse.get_dashboard_update_all(dashboard_json))
            if not dashboard_title:
                print("Не удалось получить заголовок дашборда для {0}. Будет использовано имя по умолчанию.".format(dashboard))
                dashboard_title = "dashboard"
            filename = "{0}.json".format(dashboard_title)
            dashboard_json_converted = parse.convert_to_import_format(dashboard_json)
            with open(os.path.join(output_folder, filename), "w") as outfile:
                json.dump(dashboard_json_converted, outfile, indent=4)
                print("Дашборд {0} успешно экспортирован как {1}.".format(dashboard, filename))
        else:
            print("Ошибка при экспорте дашборда: {0} {1}".format(response.status_code, response.text))
            error_count += 1

    print("\nДашборды успешно экспортированны!\nУспешно: {0}\nОшибок: {1}".format(len(uids), error_count))

    with tarfile.open(config.save, "w:gz") as tar:
        tar.add(output_folder, arcname=os.path.basename(output_folder))

    print("\nАрхив {0} успешно создан.".format(config.save))

if __name__ == "__main__":
    main()
