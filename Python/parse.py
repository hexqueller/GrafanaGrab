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
    try:
        converted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S %d-%m-%Y")
    except ValueError:
        converted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M:%S %d-%m-%Y")
    return converted_date

def get_dashboard_update_all(dashboard_json):
    title = get_dashboard_title(dashboard_json)
    updated_by = get_dashboard_update_by(dashboard_json)
    updated_date = get_dashboard_update_date(dashboard_json)
    version = f"Версия: {get_dashboard_ver(dashboard_json)}"
    fmt = "{title:<50} {updated_by:<15} {updated_date:<20} {version:<10}"
    return fmt.format(title=title, updated_by=updated_by, updated_date=updated_date, version=version)
