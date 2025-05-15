from flask import Flask, render_template, jsonify
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_user',  # Update with your DB user
    'password': 'your_password',  # Update with your DB password
    'database': 'your_db'  # Update with your DB name
}

@app.route('/')
def dashboard():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM distance_logs ORDER BY timestamp DESC LIMIT 50")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Process data for JSON serialization
    for row in data:
        if isinstance(row['timestamp'], datetime):
            row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    # Prepare chart data (reversed to show chronological order)
    chart_data = list(reversed(data))
    chart_labels = [row['timestamp'] for row in chart_data]
    distance_values = [row['distance_cm'] for row in chart_data]
    speed_values = [row['car_speed'] for row in chart_data]

    return render_template('index.html', 
                           data=data,
                           labels=json.dumps(chart_labels),
                           distance_values=json.dumps(distance_values),
                           speed_values=json.dumps(speed_values))

@app.route('/api/data')
def get_data():
    """API endpoint to get the latest data without page refresh"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM distance_logs ORDER BY timestamp DESC LIMIT 50")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        # Process data for JSON serialization
        for row in data:
            if isinstance(row['timestamp'], datetime):
                row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare chart data (reversed to show chronological order)
        chart_data = list(reversed(data))
        chart_labels = [row['timestamp'] for row in chart_data]
        distance_values = [row['distance_cm'] for row in chart_data]
        speed_values = [row['car_speed'] for row in chart_data]

        return jsonify({
            'success': True,
            'data': data,
            'chart': {
                'labels': chart_labels,
                'distance_values': distance_values,
                'speed_values': speed_values
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')