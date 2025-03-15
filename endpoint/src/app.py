from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost', 
    'user': 'firewall_user',
    'password': 'password',
    'database': 'firewall_db'
}

conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
cursor = conn.cursor()

@app.route('/get_whitelisted', methods=['POST'])
def get_whitelisted(device_ip):
    try:
        cursor.execute("SELECT * FROM Whitelist WHERE ip = {device_ip}")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return str(e)

@app.route('/get_logs', methods=['POST'])
def get_logs():
    try:
        cursor.execute("SELECT * FROM Logs")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return str(e)
    
@app.route('/get_devices', methods=['POST'])
def get_devices():
    try:
        cursor.execute("SELECT * FROM Devices")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return str(e)

@app.route('/get_device', methods=['POST'])
def get_device(device_ip):
    try:
        cursor.execute("SELECT * FROM Devices WHERE ip = {device_ip}")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return str(e)

@app.route('/get_device_logs', methods=['POST'])
def get_device_logs(device_ip):
    try:
        cursor.execute("SELECT * FROM Logs WHERE ip_src = {device_ip} OR ip_dst = {device_ip}")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
