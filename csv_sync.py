import requests
import os

AIRTABLE_TOKEN = os.environ["AIRTABLE_TOKEN"]

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "text/csv",
}

# Upload outlets.csv
outlets_url = "https://api.airtable.com/v0/appztmwuhTzOT5AWH/tbltAGWHJNeLg0fJO/sync/SaDOnw7p"

with open("outlets.csv", "rb") as f:
    r = requests.post(
        outlets_url,
        headers=headers,
        data=f,
        timeout=30,
    )
    r.raise_for_status()

# Upload registers.csv
registers_url = "https://api.airtable.com/v0/appztmwuhTzOT5AWH/tblBzqR3ER3DAOVDE/sync/jWhUmPSL"

with open("registers.csv", "rb") as f:
    r = requests.post(
        registers_url,
        headers=headers,
        data=f,
        timeout=30,
    )
    r.raise_for_status()

print("Airtable sync completed successfully.")
