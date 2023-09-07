import random
import time
import requests

sonde_account = 2

while True:
    temperatures = []
    humiditys = []

    for x in range(sonde_account):
        random_temp = random.uniform(-20.0, 50.0)
        temperature = round(random_temp, 2)
        temperatures.append(temperature)

        # simulate the humidity (%)
        random_hum = random.uniform(0, 100.0)
        humidity = round(random_hum, 1)
        humiditys.append(humidity)

    url = "http://127.0.0.1:5000/addData"
    data = {
        "temperature": temperatures,
        "humidity": humiditys
    }
    response = requests.post(url, json=data)
    sonde_account = response.json()

    time.sleep(60)
