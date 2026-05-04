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

            # validate input schema
            if "chartTitle" not in data or "metric" not in data:
                raise Exception(f"Invalid file: {file}")

            charts.append({
                "id": file.replace(".json", ""),
                "title": data["chartTitle"],
                "metric": data["metric"]
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
            "chartId": f"chart_{c['id']}_{i}",   # ✅ safe ID
            "name": c["title"],                 # allowed at chart level in O11y dashboard API
            "chartConfig": {
                "type": "TimeSeriesChart",
                "programOptions": {
                    "signalflowProgram": (
                        f"data('{c['metric']}')"
                        f".publish(label='{c['title']}')"
                    )
                }
            }
        })

    return dashboard


def main():
    charts = load_charts()
    dashboard = build_dashboard(charts)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("✅ dashboard.json generated successfully")


if __name__ == "__main__":
    main()
