from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost', 
    'user': 'firewall_user',
    'password': 'password',
    'database': 'firewall_db'
}

@app.route('/data')
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
