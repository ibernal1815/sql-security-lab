from flask import Flask, request, render_template_string
import psycopg2

# This app is intentionally vulnerable – used for learning only!
app = Flask(__name__)

# Hard-coded DB config (not secure, just for testing)
def get_db_connection():
    return psycopg2.connect(
        dbname="sql_lab",
        user="sql_user",
        password="password123",
        host="localhost"
    )

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ❌ VULNERABLE: Direct string concatenation
        # This allows attackers to inject SQL
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        # Running the query unsafely
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()

        if result:
            # If a row is returned, we claim a login
            return f"Logged in as {username}"
        else:
            return "Invalid credentials"

    # super simple login form
    return render_template_string("""
        <form method="POST">
            <input name="username" placeholder="username"><br>
            <input name="password" placeholder="password"><br>
            <button>Login</button>
        </form>
    """)

# Run it
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
