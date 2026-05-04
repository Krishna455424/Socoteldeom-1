import os
import json
import uuid

DASHBOARD_DIR = "dashboards"

def load_charts():
    charts = []
    for file in os.listdir(DASHBOARD_DIR):
        if file.endswith(".json"):
            with open(os.path.join(DASHBOARD_DIR, file)) as f:
                charts.append(json.load(f))
    return charts


def build_splunk_dashboard(charts):
    dashboard = {
        "name": "GitOps Infra Dashboard",
        "description": "Auto-created via pipeline",
        "charts": []
    }

    for c in charts:
        dashboard["charts"].append({
            "chartId": str(uuid.uuid4()),   # REQUIRED
            "name": c["chartTitle"],        # NOT "title"
            "programText": f"A = data('{c['metric']}').publish(label='{c['chartTitle']}')"
        })

    return dashboard


if __name__ == "__main__":
    charts = load_charts()
    dashboard = build_splunk_dashboard(charts)

    with open("dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)

    print("Dashboard generated successfully")
