import gc
from machine import WDT, Pin
from network import STA_IF, WLAN
from time import sleep

# External Libraries
import dht
import urequests

from config import base_url, device, password, ssid

watchdog = WDT(timeout=8000)  # 8 Seconds
led = Pin("LED", Pin.OUT)
sensor = dht.DHT22(pin=Pin(16))
headers = {
    "User-Agent": f"Freyr-Device/v1.2/{device}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() is False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def collect_measurements():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        send_results(temperature=temperature, humidity=humidity)
    except Exception as err:
        print("Failed to read DHT22 sensor:", err)
        led.on()
        send_error(error=err)


def send_results(temperature, humidity):
    body = {"device": device, "temperature": temperature, "humidity": humidity}
    response = urequests.post(url=base_url + "/api/readings", json=body, headers=headers)
    if response.status_code != 204:
        print(f"Failed to connect: {response.text}")
        led.on()


def send_error(error):
    body = {"device": device, "error": str(error)}
    response = urequests.post(url=base_url + "/api/readings/error", json=body, headers=headers)
    if response.status_code != 204:
        print(f"Failed to connect: {response.text}")
        led.on()


ip = connect()
while True:
    led.off()
    collect_measurements()
    gc.collect()
    # Wait 5mins
    for _ in range(60):
        watchdog.feed()
        sleep(5)