import os
import requests
from prometheus_client import start_http_server, Gauge, Counter
import time

DUO_USER_ID = "626440950"
DUO_JWT = os.environ.get("DUO_JWT")

streak_metric_now = Gauge('duolingo_streak_now', 'Duolingo streak Now', unit='Days')
xp_metric_now = Gauge('duolingo_total_xp_now', 'Total Duolingo XP Now', unit='XP')

def fetch_duolingo_data():
    url = f"https://www.duolingo.com/2017-06-30/users/{DUO_USER_ID}?fields=streak,totalXp"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Adam",
        "Authorization": f"Bearer {DUO_JWT}",
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        streak_metric_now.set(data.get("streak", 0))
        xp_metric_now.set(data.get("totalXp", 0))
    except Exception as e:
        print(f"Error fetching Duolingo data: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        fetch_duolingo_data()
        time.sleep(3600)