import RPi.GPIO as GPIO
import time
import os
import Adafruit_DHT
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder


# Tentukan pin GPIO untuk sensor ultrasonik
TRIG_PIN = 13
ECHO_PIN = 8

# Tentukan pin GPIO untuk LED
LED_PIN = 11

# pin dht22
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 22

#setting camera
time.sleep(2)
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(10000000)
picam2.start_recording(encoder, 'test.mp4')
picam2.start_preview(Preview.QTGL)
time.sleep(3600)
picam2.stop_preview()
picam2.stop_recording()

# Inisialisasi GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

def measure_distance():
    # Kirim sinyal ultrasonik
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Waktu mulai dan berhenti
    start_time = time.time()
    stop_time = time.time()

    # Rekam waktu mulai
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Rekam waktu berhenti
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Hitung jarak
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return distance

try:
    f = open('./data-Temp/humidity.csv', 'a+')
    if os.stat('./data-Temp/humidity.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity\r\n')
    while True:


        # Baca suhu dan kelembaban dari sensor DHT22
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity))
        else:
            print("Failed to retrieve data from humidity sensor")

        distance = measure_distance()

        # Tentukan rentang jarak yang diizinkan
        rentang_min = 10
        rentang_max = 100

        # Cek apakah jarak di luar rentang yang ditentukan
        if distance < rentang_min or distance > rentang_max:
            # Nyalakan LED jika jarak di luar rentang
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            # Matikan LED jika jarak dalam rentang
            GPIO.output(LED_PIN, GPIO.LOW)

        time.sleep(0.1)

except KeyboardInterrupt:
    # Matikan GPIO dan keluar saat keyboard interrupt (Ctrl+C)
    GPIO.cleanup()

