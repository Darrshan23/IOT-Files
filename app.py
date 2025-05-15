from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'iotuser',
    'password': 'iotpass',
    'database': 'iot_car_data'
}

@app.route('/')
def dashboard():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM distance_logs ORDER BY timestamp DESC LIMIT 50")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Prepare data for chart (reverse for time order)
    chart_labels = [row['timestamp'].strftime('%H:%M:%S') for row in reversed(data)]
    chart_values = [row['distance_cm'] for row in reversed(data)]

    return render_template('dashboard.html', data=data, labels=chart_labels, values=chart_values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
