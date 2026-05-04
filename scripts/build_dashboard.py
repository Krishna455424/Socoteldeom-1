import os
import json

DASHBOARD_DIR = "dashboards"
OUTPUT_FILE = "dashboard.json"


def load_charts():
    charts = []

    for file in os.listdir(DASHBOARD_DIR):
        if file.endswith(".json"):
            with open(os.path.join(DASHBOARD_DIR, file)) as f:
                data = json.load(f)

            charts.append({
                "id": file.replace(".json", ""),
                "metric": data["metric"],
                "title": data["chartTitle"]
            })

    return charts


def build_dashboard(charts):
    return {
        "name": "GitOps Infra Dashboard",
        "description": "Auto-generated via Observability as Code",
        "charts": [
            {
                "chartId": f"chart_{c['id']}_{i}",
                "programText": f"A = data('{c['metric']}').publish(label='{c['title']}')"
            }
            for i, c in enumerate(charts)
        ]
    }


if __name__ == "__main__":
    charts = load_charts()
    dashboard = build_dashboard(charts)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("✅ dashboard.json regenerated cleanly")
