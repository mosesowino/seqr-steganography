from flask import Flask, jsonify
import mysql.connector
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'seqr'

user_email = 'user3@gmail.com'

CHECK_EMAIL = 'select * from seqr.users where email = user_email'

def get_db_connection():
    return mysql.connector.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        database = app.config['MYSQL_DATABASE']
    )

@app.route('/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(CHECK_EMAIL)
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)
    # return str(rows)

if __name__ == '__main__':
    app.run(debug = True)