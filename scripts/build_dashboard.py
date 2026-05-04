import os
import json

DASHBOARD_DIR = "dashboards"
OUTPUT_FILE = "dashboard.json"


def load_charts():
    charts = []

    for file in os.listdir(DASHBOARD_DIR):
        if file.endswith(".json"):
            path = os.path.join(DASHBOARD_DIR, file)

            with open(path, "r") as f:
                data = json.load(f)

            charts.append({
                "id": file.replace(".json", ""),
                "metric": data["metric"],
                "title": data["chartTitle"]
            })

    return charts


def build_dashboard(charts):
    dashboard = {
        "name": "GitOps Infra Dashboard",
        "description": "Auto-generated via Observability as Code",
        "charts": []
    }

    for i, c in enumerate(charts):
        dashboard["charts"].append({
            "chartId": f"chart_{c['id']}_{i}",

            # ❗ NO "name" FIELD HERE

            "vizOptions": {
                "type": "timeSeries",
                "label": c["title"],
                "signalflow": f"data('{c['metric']}').publish(label='{c['title']}')"
            }
        })

    return dashboard


if __name__ == "__main__":
    charts = load_charts()
    dashboard = build_dashboard(charts)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("✅ dashboard.json generated successfully")
