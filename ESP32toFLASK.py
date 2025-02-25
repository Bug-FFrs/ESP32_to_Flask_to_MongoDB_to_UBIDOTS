from machine import Pin
import dht
import time
import network
import urequests

# Inisialisasi sensor
sensor = dht.DHT11(Pin(26))  # DHT11 di GPIO 26
pir = Pin(25, Pin.IN)  # PIR Motion Sensor di GPIO 25

# WiFi Credentials
SSID = "BAGAS"
PASSWORD = "rotibakar"

# Inisialisasi WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Menghubungkan ke WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("Terhubung ke WiFi! IP:", wifi.ifconfig()[0])

# API Flask
FLASK_URL = "http://192.168.1.3:5000/sensor" 

while True:
    try:
        sensor.measure()  # Baca sensor
        data = {
            "temperature": sensor.temperature(),
            "humidity": sensor.humidity(),
            "motion": pir.value()
        }
        
        print("Mengirim data ke Flask:", data)
        response = urequests.post(FLASK_URL, json=data)
        print("Response:", response.text)
        response.close()

    except OSError as e:
        print("Gagal membaca sensor atau mengirim data:", e)

    time.sleep(5)  # Kirim data setiap 5 detik
