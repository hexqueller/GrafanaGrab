from datetime import datetime

def convert_to_import_format(dashboard_json):
    if "meta" in dashboard_json:
        del dashboard_json["meta"]
    if "id" in dashboard_json["dashboard"]:
        del dashboard_json["dashboard"]["id"]
    return dashboard_json["dashboard"]

def get_dashboard_title(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("title", "")

def get_dashboard_ver(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("version", "")

def get_dashboard_update_by(dashboard_json):
    return dashboard_json.get("meta", {}).get("updatedBy", "")

def get_dashboard_update_date(dashboard_json):
    date = dashboard_json.get("meta", {}).get("updated", "")
    converted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S %d-%m-%Y")
    return converted_date

def get_dashboard_update_all(dashboard_json):
    return "Дашборд: " + get_dashboard_title(dashboard_json) + " Обновил: " + get_dashboard_update_by(dashboard_json) + " Дата: " + get_dashboard_update_date(dashboard_json) + " Версия: " + str(get_dashboard_ver(dashboard_json))