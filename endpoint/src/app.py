from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost', 
    'user': 'firewall_user',
    'password': 'password',
    'database': 'firewall_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        raise

@app.route('/get_whitelisted', methods=['GET'])
def get_whitelisted():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Whitelist WHERE device_id = %s"
    cursor.execute(query, (device_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/get_logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Logs"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)
    
@app.route('/get_devices', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Devices"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/get_device', methods=['GET'])
def get_device():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Devices WHERE ip = %s"
    cursor.execute(query, (device_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/get_device_logs', methods=['GET'])
def get_device_logs():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Logs WHERE ip_src = %s OR ip_dst = %s"
    cursor.execute(query, (device_id, device_id))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
