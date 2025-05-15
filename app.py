from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'iotuser',
    'password': 'iotpass',
    'database': 'iot_car_data'
}

def get_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM distance_logs ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.execute("SELECT MIN(distance_cm), MAX(distance_cm), AVG(distance_cm) FROM distance_logs")
    stats = cursor.fetchone()
    conn.close()
    return data[::-1], stats  # Reverse to show oldest-to-newest in chart

@app.route("/")
def index():
    data, stats = get_data()
    return render_template("index.html", data=data, stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
