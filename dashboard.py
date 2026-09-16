from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"



def get_logs():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, severity, message
        FROM security_logs
        ORDER BY id DESC
        LIMIT 30
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows



@app.route("/")
def index():

    logs = get_logs()

    # STATS CALCULATION
    stats = {
        "total": len(logs),
        "critical": sum(1 for r in logs if r[1] == "CRITICAL"),
        "high": sum(1 for r in logs if r[1] == "HIGH"),
        "medium": sum(1 for r in logs if r[1] == "MEDIUM"),
        "low": sum(1 for r in logs if r[1] == "LOW"),
    }

    return render_template("dashboard.html", stats=stats)



@app.route("/api/logs")
def api_logs():

    logs = get_logs()

    return jsonify([
        {
            "time": r[0],
            "severity": r[1],
            "message": r[2]
        }
        for r in logs
    ])



if __name__ == "__main__":
    app.run(debug=True, port=5000)