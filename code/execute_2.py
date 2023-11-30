import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder


# Konfigurasi GPIO untuk HC-SR04
TRIG_PIN = 13
ECHO_PIN = 8

# Konfigurasi GPIO untuk LED
LED_PIN = 11

# Konfigurasi sensor DHT22
DHT_PIN = 22
DHT_SENSOR = Adafruit_DHT.DHT22

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

def get_distance():
    # Mengirimkan sinyal ultrasonik
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Mendapatkan waktu tiba pulsa pantulan
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Menghitung jarak
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def get_dht_data():
    # Membaca data dari sensor DHT22
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def record():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    encoder = H264Encoder(10000000)
    picam2.start_recording(encoder, 'record.h264')

def main():
    try:
        while True:
            #record 
            record()

            # Mendapatkan data dari sensor HC-SR04
            distance = get_distance()
            
            # Memeriksa apakah jarak di luar rentang yang ditentukan
            max = 30
            min = 20
            if distance > max or distance < min:  # Ganti nilai ini sesuai dengan rentang yang diinginkan
                GPIO.output(LED_PIN, GPIO.HIGH)
            else:
                GPIO.output(LED_PIN, GPIO.LOW)

            # Mendapatkan data dari sensor DHT22
            humidity, temperature = get_dht_data()

            # Menyimpan data ke file
            with open("sensor_data.csv", "a") as file:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{current_time}, {temperature}, {humidity}\n")

            time.sleep(1)  # Jeda 2 detik antara setiap pembacaan

    except KeyboardInterrupt:
        # Menangani penekanan Ctrl+C untuk menghentikan program
        GPIO.cleanup()

if __name__ == "__main__":
    main()
