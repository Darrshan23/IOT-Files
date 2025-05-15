import serial
import datetime
import mysql.connector
from time import sleep

# Configuration
SERIAL_PORT = '/dev/ttyS0'  # Arduino serial port
BAUD_RATE = 9600
DB_CONFIG = {
    'host': 'localhost',
    'user': 'iotuser',
    'password': 'iotpass',
    'database': 'iot_car_data'
}

class DistanceLogger:
    def __init__(self):
        self.ser = None
        self.db_conn = None
        self.db_cursor = None

    def setup_serial_connection(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            sleep(2)
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to {SERIAL_PORT}: {e}")
            return False

    def setup_database_connection(self):
        try:
            self.db_conn = mysql.connector.connect(**DB_CONFIG)
            self.db_cursor = self.db_conn.cursor()
            print("Connected to MariaDB database")
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")

    def log_distance(self, distance_cm):
        try:
            query = "INSERT INTO distance_logs (distance_cm) VALUES (%s)"
            self.db_cursor.execute(query, (distance_cm,))
            self.db_conn.commit()
            print(f"Logged: {distance_cm} cm")
        except mysql.connector.Error as e:
            print(f"DB insert error: {e}")

    def monitor_serial(self):
        print("Monitoring serial data... Press Ctrl+C to exit")
        try:
            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    print("Raw line:", line)
                    if line.startswith("Distance:"):
                        parts = line.split(":")
                        if len(parts) > 1:
                            cm_value = parts[1].replace("cm", "").strip()
                            if cm_value.isdigit():
                                self.log_distance(int(cm_value))
                sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()
            if self.db_cursor:
                self.db_cursor.close()
            if self.db_conn:
                self.db_conn.close()

    def main(self):
        if self.setup_serial_connection():
            self.setup_database_connection()
            self.monitor_serial()

if __name__ == "__main__":
    logger = DistanceLogger()
    logger.main()
