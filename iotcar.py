import serial
import mysql.connector as mariadb  # ✅ Import with the correct alias
import time

# Connect to Arduino (you already confirmed ttyS0 works)
arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)
time.sleep(2)

# Connect to MariaDB
conn = mariadb.connect(
    user="root",
    password="root",
    host="localhost",
    database="iot_car_data"
)
cursor = conn.cursor()

while True:
    try:
        line = arduino.readline().decode().strip()
        if line.startswith("Distance:"):
            parts = line.split(":")
            if len(parts) > 1:
                cm_value = parts[1].replace("cm", "").strip()
                print("Received:", cm_value)

                # Use %s placeholder for mysql.connector
                cursor.execute("INSERT INTO distance_logs (distance_cm) VALUES (%s)", (cm_value,))
                conn.commit()
    except Exception as e:
        print("Error:", e)
