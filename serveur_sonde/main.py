import random
import time
import requests

while True:
    # simulate the temperature (°C)
    random_temp = random.uniform(-20.0, 50.0)
    temperature = round(random_temp, 2)

    # simulate the humidity (%)
    random_hum = random.uniform(0, 100.0)
    humidity = round(random_hum, 1)

    url = "http://127.0.0.1:5000/addData"
    data = {
        "temperature": temperature,
        "humidity": humidity
    }
    requests.post(url, json=data)

    print(f"{temperature}°C and {humidity} % add to database")

    time.sleep(60)
