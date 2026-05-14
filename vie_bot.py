import requests
import time
import json
import os

TOKEN = "8675818877:AAEuWEf_9GJVnibFUPVu5_Xu46iH-EQt5q0"
CHAT_ID = "7912945095"

URL = "https://civiweb-api-prd.azurewebsites.net/api/Offers/search"

FILE = "seen.json"

if os.path.exists(FILE):
    seen = set(json.load(open(FILE)))
else:
    seen = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Telegram status:", r.status_code)
    print("Telegram response:", r.text)

def get_offers():
    r = requests.post(URL, json={"page": 1, "pageSize": 10})
    data = r.json()
    return data.get("result", [])

def format_offer(o):
    return f"""
🔥 NOUVELLE OFFRE

🏢 {o.get('organizationName')}
💼 {o.get('missionTitle')}
🌍 Pays: {o.get('country', 'N/A')}
🔗 https://mon-vie-via.businessfrance.fr/offres/{o.get('id')}
"""

print("BOT STARTED")

while True:
    offers = get_offers()

 for o in offers:
    oid = o.get("id")

    if oid in seen:
        continue

    seen.add(oid)

    with open(FILE, "w") as f:
        json.dump(list(seen), f)

    send_message(format_offer(o))
    print("Envoyé:", oid)

    time.sleep(60)
