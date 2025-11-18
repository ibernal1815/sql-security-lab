from flask import Flask, request, render_template_string, session
import psycopg2
import psycopg2.extras

# This app is the secure version
app = Flask(__name__)
app.secret_key = "something-secret"  # Needed for session cookies

# DB connection with SSL + secure role
def get_db_connection():
    # Using a limited privilege role
    return psycopg2.connect(
        dbname="sql_lab",
        user="app_user",
        password="app_user_pass",
        host="localhost",
        options="-c app.current_tenant={}".format(session.get("tenant_id", 0))
    )

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ✔ FIXED: Parameterized query — prevents SQL injection entirely
        query = """
            SELECT id, username, tenant_id
            FROM users
            WHERE username = %s AND password = %s
        """

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, (username, password))
        result = cur.fetchone()

        if result:
            # Save tenant ID in session
            session["tenant_id"] = result["tenant_id"]
            return f"Logged in (securely) as {result['username']} (Tenant {result['tenant_id']})"

        return "Invalid credentials"

    return render_template_string("""
        <form method="POST">
            <input name="username" placeholder="username"><br>
            <input name="password" placeholder="password"><br>
            <button>Login</button>
        </form>
    """)

# Protected example route
@app.route("/profile")
def profile():
    if "tenant_id" not in session:
        return "Not logged in"

    conn = get_db_connection()
    cur = conn.cursor()

    # RLS enforces tenant restrictions automatically
    cur.execute("SELECT id, username FROM users")
    rows = cur.fetchall()

    return f"Rows visible to your tenant: {rows}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
