import serial
import mariadb
import time

# Connect to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

# Connect to MariaDB
conn = mariadb.connect(
    user="root",
    password="your_password_here",
    host="localhost",
    database="iotcar"
)
cursor = conn.cursor()

while True:
    try:
        line = arduino.readline().decode().strip()
        if line.startswith("Distance:"):
            # Extract numeric value
            parts = line.split(":")
            if len(parts) > 1:
                cm_value = parts[1].replace("cm", "").strip()
                print("Received:", cm_value)
                cursor.execute("INSERT INTO sensor_data (value) VALUES (?)", (cm_value,))
                conn.commit()
    except Exception as e:
        print("Error:", e)
