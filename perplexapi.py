from flask import Flask, request, jsonify
from flask_cors import CORS
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import random
import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for development

# --- Cassandra connection setup (customize for your cluster) ---
CASSANDRA_HOSTS = ['127.0.0.1']
CASSANDRA_KEYSPACE = 'your_keyspace'

def get_cassandra_session():
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    return session

# --- Resource Utilization (Live Table) ---
@app.route("/api/resource_utilization", methods=["GET"])
def resource_utilization():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def status(): return "UP" if random.random() > 0.1 else "DOWN"
    data = [
        dict(node="Node1", cpu=random.randint(30, 90), ram=random.randint(28, 64), disk=random.randint(500, 900),
             read_ops=random.randint(800, 2000), write_ops=random.randint(700, 1900), status=status(), timestamp=now),
        dict(node="Node2", cpu=random.randint(40, 95), ram=random.randint(32, 64), disk=random.randint(600, 950),
             read_ops=random.randint(900, 2100), write_ops=random.randint(800, 2000), status=status(), timestamp=now),
        dict(node="Node3", cpu=random.randint(20, 85), ram=random.randint(16, 32), disk=random.randint(400, 700),
             read_ops=random.randint(600, 1800), write_ops=random.randint(500, 1500), status=status(), timestamp=now),
    ]
    return jsonify(data)

# --- Custom Query Execution (Safe) ---
@app.route("/api/run_query", methods=["POST"])
def run_query():
    data = request.get_json()
    q = data.get("query", "")
    params = data.get("params", {})
    # Only allow SELECT queries for safety
    if not q.strip().lower().startswith("select"):
        return jsonify({"error": "Only SELECT queries are allowed."}), 400
    try:
        session = get_cassandra_session()
        statement = SimpleStatement(q)
        result = session.execute(statement, params)
        rows = [dict(row._asdict()) for row in result]
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Dynamic Query Builder (optional, for UI filter sync) ---
@app.route("/api/dynamic_query", methods=["POST"])
def dynamic_query():
    f = request.get_json()
    query = "SELECT * FROM logs WHERE 1=1"
    params = {}
    if f.get("from_date"):
        query += " AND date >= %(from_date)s"
        params["from_date"] = f["from_date"]
    if f.get("to_date"):
        query += " AND date <= %(to_date)s"
        params["to_date"] = f["to_date"]
    if f.get("search"):
        query += " AND message LIKE %(search)s"
        params["search"] = f"%{f['search']}%"
    if f.get("filters"):
        for filt in f["filters"]:
            field = filt.get('field')
            terms = filt.get('terms', [])
            if len(terms) > 1:
                in_params = []
                for i, term in enumerate(terms):
                    pname = f"{field}_{i}"
                    in_params.append(f"%({pname})s")
                    params[pname] = term
                query += f" AND {field} IN ({', '.join(in_params)})"
            elif len(terms) == 1:
                pname = f"{field}"
                query += f" AND {field} = %({pname})s"
                params[pname] = terms[0]
    query += " ALLOW FILTERING"
    try:
        session = get_cassandra_session()
        statement = SimpleStatement(query)
        result = session.execute(statement, params)
        rows = [dict(row._asdict()) for row in result]
        return jsonify({"query": query, "params": params, "rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Root endpoint (optional for health check) ---
@app.route("/")
def root():
    return jsonify({"status": "ok", "message": "Cassandra Flask backend running"})

if __name__ == "__main__":
    app.run(debug=True)
