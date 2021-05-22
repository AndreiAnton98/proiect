import adafruit_dht
from board import *
import time

SENSOR_PIN = D26

dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)
tries = 0
fails = 0
while True:
    tries += 1
    try:
        temperature = dht22.temperature
        humidity = dht22.humidity

        print(f"Humidity= {humidity:.2f}")
        print(f"Temperature= {temperature:.2f}°C")
    except:
        fails += 1
    print("Tries: " + str(tries))
    print("Fails: " + str(fails))
    time.sleep(60)