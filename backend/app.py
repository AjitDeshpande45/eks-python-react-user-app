from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL connection settings
DB_CONFIG = {
    "dbname": "postgres",
    "user": "myuser",
    "password": "admin",
    "host": "postgres-container",  # Use "localhost" if not in Docker
    "port": "5432"
}

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Create users table if it doesn't exist
def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                );
            """)
        conn.commit()

@app.route("/api/addusers", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and Email are required."}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
            conn.commit()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email FROM users;")
                rows = cur.fetchall()
                users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
