import os
import json

DASHBOARD_DIR = "dashboards"
OUTPUT_FILE = "dashboard.json"


def load_charts():
    charts = []

    if not os.path.exists(DASHBOARD_DIR):
        raise Exception(f"Directory {DASHBOARD_DIR} not found")

    for file in os.listdir(DASHBOARD_DIR):
        if file.endswith(".json"):
            path = os.path.join(DASHBOARD_DIR, file)

            try:
                with open(path, "r") as f:
                    data = json.load(f)

                # validate required fields
                if "chartTitle" not in data or "metric" not in data:
                    raise Exception(f"Missing keys in {file}")

                charts.append({
                    "id": file.replace(".json", ""),  # cpu, memory, etc.
                    "title": data["chartTitle"],
                    "metric": data["metric"]
                })

            except Exception as e:
                print(f"❌ Error parsing {file}: {e}")
                raise

    return charts


def build_dashboard(charts):
    dashboard = {
        "name": "GitOps Infra Dashboard",
        "description": "Auto-generated via Observability as Code",
        "charts": []
    }

    for c in charts:
        dashboard["charts"].append({
            "chartId": f"chart_{c['id']}_1",   # ✅ NO UUID, NO SPECIAL CHARS
            "name": c["title"],
            "programText": (
                f"A = data('{c['metric']}')"
                f".publish(label='{c['title']}')"
            )
        })

    return dashboard


def main():
    charts = load_charts()
    dashboard = build_dashboard(charts)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("✅ Dashboard generated successfully")
    print(f"📄 Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
