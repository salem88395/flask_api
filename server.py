
from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# إعداد الاتصال بقاعدة البيانات
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=myserver-int123.database.windows.net;"
        "DATABASE=Intelligence_cloud;"
        "UID=osk;"
        "PWD=int05420083@;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    return conn

# مسار لإضافة بيانات جديدة
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()  # الحصول على البيانات المرسلة كـ JSON
    
    # تحقق من وجود كافة البيانات المطلوبة
    required_fields = ['num_cust', 'date', 'class',  'statmen', 'num_address', 'target', 'code_op']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required data: {field}!"}), 400

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()
    cursor = conn.cursor()

    # إدخال البيانات
    cursor.execute("INSERT INTO feild (num_cust, date, class, statmen,num_address,target,code_op) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (data['num_cust'], data['date'], data['class'], data['statmen'], 
                    data['num_address'], data['target'], data['code_op']))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data added successfully!"}), 200

# مسار للتحقق من وجود بيانات معينة
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # الحصول على البيانات المرسلة كـ JSON

    # تحقق من وجود كافة البيانات المطلوبة
    if 'user' not in data or 'pass' not in data:
        return jsonify({"message": "Missing required data!"}), 400

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()
    cursor = conn.cursor()

    # التحقق من صحة بيانات الدخول
    cursor.execute("SELECT name, password FROM enter WHERE name=? AND password=?", 
                   (data['user'], data['pass']))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password!"}), 401


# مسار لعرض كافة البيانات في الجدول
@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT num_guid, subject_guid, date_guid, gold_guid, risk_guld, num_address, time_guld FROM guld")
        rows = cursor.fetchall()
        conn.close()
        data = [list(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

