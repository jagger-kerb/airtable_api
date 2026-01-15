import requests

pat = os.environ["AIRTABLE_TOKEN"]
url = "https://api.airtable.com/v0/appztmwuhTzOT5AWH/tbltAGWHJNeLg0fJO/sync/SaDOnw7p"

headers = {"Authorization": f"Bearer {pat}",
           "Content-Type": "text/csv"}

with open('outlets.csv','rb') as f:
    r = requests.post(
        url,
        headers=headers,
        data=f,
        timeout=30
    )

url = "https://api.airtable.com/v0/appztmwuhTzOT5AWH/tblBzqR3ER3DAOVDE/sync/jWhUmPSL"

with open('registers.csv','rb') as f:
    r = requests.post(
        url,
        headers=headers,
        data=f,
        timeout=30
    )
