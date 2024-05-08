def get_dashboard_title(dashboard_json):
    return dashboard_json.get("dashboard", {}).get("title", "")

def convert_to_import_format(dashboard_json):
    if "meta" in dashboard_json:
        del dashboard_json["meta"]
    if "id" in dashboard_json["dashboard"]:
        del dashboard_json["dashboard"]["id"]
    return dashboard_json["dashboard"]