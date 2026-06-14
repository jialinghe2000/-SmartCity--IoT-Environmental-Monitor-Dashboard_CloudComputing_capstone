import requests
import random
import time
from datetime import datetime, timezone

###need to change URL (from API Gateway endpoint)
API_URL = "https://********.amazonaws.com"

sensors = [
    {
        "sensor_id": "S001",
        "district": "Downtown"
    },
    {
        "sensor_id": "S002",
        "district": "Industrial Zone"
    },
    {
        "sensor_id": "S003",
        "district": "Residential Area"
    }
]

while True:

    sensor = random.choice(sensors)

    data = {
        "sensor_id": sensor["sensor_id"],
        "district": sensor["district"],
        "temperature": random.randint(25, 42),
        "co2": random.randint(400, 1200),
        "no2": random.randint(20, 100),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(API_URL, json=data)

        print("=" * 60)
        print("Sent Data:")
        print(data)
        print("Response:", response.status_code)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)