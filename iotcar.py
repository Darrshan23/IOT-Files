import serial
import mysql.connector as mmariadb
import time

# Connect to Arduino
arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)
time.sleep(2)

# Connect to MariaDB
conn = mmariadb.connect(
    user="iotuser",
    password="iotpass",
    host="localhost",
    database="iot_car_data"
)
cursor = conn.cursor()

while True:
    try:
        raw_line = arduino.readline()
        print(f"Raw bytes: {raw_line}")  # print raw bytes for debugging
        line = raw_line.decode(errors='ignore').strip()  # ignore decode errors
        print(f"Decoded line: '{line}'")
        if line.startswith("Distance:"):
            parts = line.split(":")
            if len(parts) > 1:
                cm_value = parts[1].replace("cm", "").strip()
                print("Received Distance (cm):", cm_value)

                # Insert into distance_logs table with timestamp
                cursor.execute("INSERT INTO distance_logs (distance_cm) VALUES (%s)", (cm_value,))
                conn.commit()
    except Exception as e:
        print("Error:", e)
