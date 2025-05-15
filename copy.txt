import serial
import mysql.connector as mmariadb
import time

# Connect to Arduino (adjust the port if needed)
arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)
time.sleep(2)

# Connect to MariaDB
conn = mmariadb.connect(
    user="root",              # root username
    password="root",          # your root password
    host="localhost",         # your MariaDB host
    database="iot_car_data"   # your database name
)
cursor = conn.cursor()

while True:
    try:
        line = arduino.readline().decode().strip()
        print("Raw line:", line)  # Debug: print the raw data from Arduino

        if line.startswith("Distance:"):
            # Extract numeric value
            parts = line.split(":")
            if len(parts) > 1:
                cm_value = parts[1].replace("cm", "").strip()
                print("Received:", cm_value)

                # Insert into distance_logs table with timestamp
                cursor.execute("INSERT INTO distance_logs (distance_cm) VALUES (%s)", (cm_value,))
                conn.commit()
    except Exception as e:
        print("Error:", e)
