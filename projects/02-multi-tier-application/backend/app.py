import os
import psycopg
from flask import Flask, jsonify

app = Flask(__name__)
DSN = (f"host={os.environ['DB_HOST']} dbname={os.environ['DB_NAME']} "
       f"user={os.environ['DB_USER']} password={os.environ['DB_PASSWORD']} connect_timeout=3")


def db():
    return psycopg.connect(DSN)


@app.get("/healthz")  # liveness: process is alive; deliberately does NOT touch the DB
def healthz():
    return "ok"


@app.get("/ready")  # readiness: can we serve traffic? needs the DB
def ready():
    try:
        with db() as c:
            c.execute("SELECT 1")
        return "ready"
    except Exception as e:
        return str(e), 503


@app.get("/visits")
def visits():
    with db() as c:
        c.execute("CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, ts timestamptz DEFAULT now())")
        c.execute("INSERT INTO visits DEFAULT VALUES")
        n = c.execute("SELECT count(*) FROM visits").fetchone()[0]
    return jsonify(visits=n, pod=os.environ.get("HOSTNAME"))
