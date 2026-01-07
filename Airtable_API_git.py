import os
import json
import requests
import pandas as pd


BASE_ID = os.environ["AIRTABLE_BASE_ID"]
TABLE_ID = os.environ["AIRTABLE_TABLE_ID"]
VIEW_NAME = os.environ.get("AIRTABLE_VIEW_NAME", "").strip()  # optional
TOKEN = os.environ["AIRTABLE_TOKEN"]

OUTPUT_CSV = os.environ.get("OUTPUT_CSV", "data/events_list.csv")

URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def fetch_all_records(url: str, view: str | None, headers: dict) -> list[dict]:
    params = {"pageSize": 100}
    if view:
        params["view"] = view

    all_records: list[dict] = []

    while True:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if not response.ok:
            # Make Airtable errors visible in GitHub Actions logs
            print("Airtable request failed")
            print("URL:", response.url)
            print("Status:", response.status_code)
            print("Body:", response.text)
            response.raise_for_status()

        data = response.json()
        all_records.extend(data.get("records", []))

        offset = data.get("offset")
        if not offset:
            break
        params["offset"] = offset

    print(f"{len(all_records)} records fetched")
    return all_records


def flatten_cell(value):
    """Make Airtable cell values CSV-friendly."""
    if value is None:
        return None

    if isinstance(value, list):
        if len(value) == 0:
            return ""

        # list of dicts (attachments, etc.)
        if all(isinstance(x, dict) for x in value):
            # attachments: join URLs if present
            if all(("url" in x) for x in value):
                return ", ".join(x.get("url", "") for x in value if x.get("url"))
            # otherwise JSON each dict
            return "; ".join(json.dumps(x, ensure_ascii=False) for x in value)

        # list of primitives
        return ", ".join(str(x) for x in value)

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    return value


def main():
    records = fetch_all_records(URL, VIEW_NAME, HEADERS)

    rows = []
    for rec in records:
        row = dict(rec.get("fields", {}))
        row["_record_id"] = rec.get("id")
        rows.append(row)

    df = pd.DataFrame(rows)
    df_flat = df.applymap(flatten_cell)

    # Ensure output folder exists
    os.makedirs(os.path.dirname(OUTPUT_CSV) or ".", exist_ok=True)

    df_flat.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Exported {len(df_flat)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
