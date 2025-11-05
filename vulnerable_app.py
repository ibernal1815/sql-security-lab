# WARNING: This file is intentionally insecure and only for local/lab use.
# Do NOT run this app on any public network. Use in an isolated VM or Codespace only.

# vulnerable_app.py
from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn_info = "host=127.0.0.1 dbname=myappdb user=myappuser password=ChangeThisToAStrongOne!"

@app.route('/vuln')
def vuln():
    username = request.args.get('username', '')
    conn = psycopg2.connect(conn_info)
    cur = conn.cursor()
    # DANGEROUS: concatenating user input into SQL
    query = "SELECT id, username, email, is_admin FROM users WHERE username = '%s';" % username
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {'rows': rows}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
