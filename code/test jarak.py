import RPi.GPIO as GPIO
import time
import os

# Tentukan pin GPIO untuk sensor ultrasonik
TRIG_PIN = 13
ECHO_PIN = 8

# Tentukan pin GPIO untuk LED
LED_PIN = 11

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
    while True:
        # Hitung jarak lalu tampilkan ke serial monitor
        distance = measure_distance()
        min = 10
        max = 20

        # Jika jarak kurang dari 20 cm, LED akan menyala
        if distance < min or distance > max:
            GPIO.output(LED_PIN, True)
        else:
            GPIO.output(LED_PIN, False)

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
