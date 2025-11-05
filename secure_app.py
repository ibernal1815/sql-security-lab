# secure_app.py
from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Database connection info
conn_info = "host=127.0.0.1 dbname=myappdb user=myappuser password=ChangeThisToAStrongOne!"

@app.route('/secure')
def secure():
    username = request.args.get('username', '')
    conn = psycopg2.connect(conn_info)
    cur = conn.cursor()
    # SAFE: parameterized query prevents SQL injection
    cur.execute("SELECT id, username, email, is_admin FROM users WHERE username = %s;", (username,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {'rows': rows}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
