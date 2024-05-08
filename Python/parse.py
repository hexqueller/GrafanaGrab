from datetime import datetime

def get_dashboard_title(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("title", "")

def get_dashboard_ver(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("version", "")

def convert_to_import_format(dashboard_json):
    if "meta" in dashboard_json:
        del dashboard_json["meta"]
    if "id" in dashboard_json["dashboard"]:
        del dashboard_json["dashboard"]["id"]
    return dashboard_json["dashboard"]

def get_dashboard_update(dashboard_json):
    date = dashboard_json.get("meta", {}).get("updated", "")
    converted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S %d-%m-%Y")
    return "Обновил: " + dashboard_json.get("meta", {}).get("updatedBy", "")+ " Дата: " + converted_date + " Версия: " + str(get_dashboard_ver(dashboard_json))