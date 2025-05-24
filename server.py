from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.environ.get('SERVER')};"
        f"DATABASE={os.environ.get('DATABASE')};"
        f"UID={os.environ.get('UID')};"
        f"PWD={os.environ.get('PWD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )
    return conn

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    required_fields = ['num_cust', 'date', 'class', 'statmen', 'num_address', 'target', 'code_op']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"message": f"Missing required data: {', '.join(missing_fields)}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feild (num_cust, date, class, statmen, num_address, target, code_op)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['num_cust'], data['date'], data['class'], data['statmen'],
              data['num_address'], data['target'], data['code_op']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Data added successfully!"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'user' not in data or 'pass' not in data:
        return jsonify({"message": "Missing required data!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM enter WHERE name=? AND password=?", (data['user'], data['pass']))
        result = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    if result:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password!"}), 401

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT num_guid, subject_guid, date_guid, gold_guid, risk_guld, num_address, time_guld
            FROM guld
        """)
        rows = cursor.fetchall()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
