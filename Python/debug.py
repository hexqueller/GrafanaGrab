import config
import parse
import requests

dash = "edl434lyx3jswb"


headers = {
        "Authorization": f"Bearer {config.key}",
        "Content-Type": "application/json",
    }

response = requests.get(
        f"{config.url}/api/dashboards/uid/{dash}",
        headers=headers,
    )

dashboard_json = response.json()
print(parse.get_dashboard_update(dashboard_json))