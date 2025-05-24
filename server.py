from flask import Flask, request, jsonify
import pymssql
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

def get_db_connection():
    conn = pymssql.connect(
        server=os.environ.get('SERVER'),
        user=os.environ.get('UID'),
        password=os.environ.get('PWD'),
        database=os.environ.get('DATABASE')
    )
    return conn

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    required_fields = ['num_cust', 'date', 'class', 'statmen', 'num_address', 'target', 'code_op']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required data: {field}!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feild (num_cust, date, class, statmen, num_address, target, code_op) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (data['num_cust'], data['date'], data['class'], data['statmen'], 
             data['num_address'], data['target'], data['code_op'])
        )
        conn.commit()
        return jsonify({"message": "Data added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'user' not in data or 'pass' not in data:
        return jsonify({"message": "Missing required data!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM enter WHERE name=%s AND password=%s", 
                       (data['user'], data['pass']))
        result = cursor.fetchone()
        if result:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT num_guid, subject_guid, date_guid, gold_guid, risk_guld, num_address, time_guld FROM guld")
        rows = cursor.fetchall()
        data = [list(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
