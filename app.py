import base64
import os

from Crypto.Cipher import AES
from flask import Flask, jsonify, render_template_string, request

from src.analytics import platform_summary, top_destinations


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-secret")


def pad(value: str) -> str:
    return value + (AES.block_size - len(value) % AES.block_size) * chr(AES.block_size - len(value) % AES.block_size)


def encryption_key() -> bytes:
    raw = os.getenv("TRAVEL_VISTA_AES_KEY", "16byteSecretKey")
    return raw.encode("utf-8")[:16].ljust(16, b"0")


def encrypt(plain_text: str) -> str:
    cipher = AES.new(encryption_key(), AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(plain_text).encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


PAGE = """
<!doctype html>
<html>
<head>
  <title>Travel Vista Platform</title>
  <style>
    body {font-family: Segoe UI, sans-serif; margin: 36px; background: #f7faf9;}
    main {max-width: 1050px; margin: auto;}
    .grid {display:grid; grid-template-columns: repeat(4, 1fr); gap: 14px;}
    .card, section {background:white; border:1px solid #dce7e3; border-radius:8px; padding:18px;}
    code {background:#edf4f2; padding:2px 5px; border-radius:4px;}
  </style>
</head>
<body>
<main>
  <h1>Travel Vista AI Platform</h1>
  <p>Flask API and analytics layer for a secure travel-platform capstone.</p>
  <div class="grid">
    {% for label, value in summary.items() %}
      <div class="card"><h2>{{ value }}</h2><p>{{ label.replace("_", " ").title() }}</p></div>
    {% endfor %}
  </div>
  <section>
    <h2>API Endpoints</h2>
    <p><code>GET /api/summary</code> platform metrics</p>
    <p><code>GET /api/top-destinations</code> ranked destination records</p>
    <p><code>POST /api/secure-insert</code> demo AES encryption for sensitive payloads</p>
  </section>
</main>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, summary=platform_summary())


@app.get("/api/summary")
def summary():
    return jsonify(platform_summary())


@app.get("/api/top-destinations")
def destinations():
    limit = int(request.args.get("limit", 10))
    return jsonify(top_destinations(limit))


@app.post("/api/secure-insert")
def secure_insert():
    payload = request.get_json(force=True)
    sensitive = payload.get("sensitive_field", "")
    return jsonify({"status": "encrypted", "encrypted_data": encrypt(sensitive)})


if __name__ == "__main__":
    app.run(debug=True)
