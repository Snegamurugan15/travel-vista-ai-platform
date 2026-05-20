import os

from flask import Flask, jsonify, render_template_string, request

from src.analytics import activity_mix, destination_performance, platform_summary, region_revenue
from src.recommender import recommend_destinations
from src.security import encrypt_text
from src.vr_model import predict_vr_engagement


try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "travel-vista-local-dev")


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Travel Vista AI Platform</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root { color-scheme: light; --ink:#17201d; --muted:#5c6f69; --line:#d7e2df; --accent:#0e7c66; --panel:#ffffff; --wash:#f3f7f5; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: "Segoe UI", Arial, sans-serif; background:var(--wash); color:var(--ink); }
    header { padding:32px 40px 20px; border-bottom:1px solid var(--line); background:#fff; }
    main { max-width:1200px; margin:0 auto; padding:28px 24px 44px; }
    h1 { margin:0 0 8px; font-size:32px; letter-spacing:0; }
    h2 { margin:0 0 14px; font-size:20px; }
    p { color:var(--muted); line-height:1.55; }
    .grid { display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:14px; margin-bottom:22px; }
    .metric, section { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:18px; }
    .metric strong { display:block; font-size:25px; margin-bottom:4px; }
    .split { display:grid; grid-template-columns:1.1fr .9fr; gap:18px; align-items:start; }
    table { width:100%; border-collapse:collapse; font-size:14px; }
    th, td { padding:10px 8px; border-bottom:1px solid #edf1ef; text-align:left; vertical-align:top; }
    th { color:#38514a; font-size:12px; text-transform:uppercase; }
    input, button { width:100%; padding:11px 12px; border:1px solid var(--line); border-radius:6px; font:inherit; }
    button { background:var(--accent); color:white; cursor:pointer; border-color:var(--accent); margin-top:10px; }
    pre { white-space:pre-wrap; background:#10231e; color:#e8fff8; padding:14px; border-radius:8px; min-height:88px; }
    @media (max-width: 900px) { .grid, .split { grid-template-columns:1fr; } header { padding:24px; } }
  </style>
</head>
<body>
  <header>
    <h1>Travel Vista AI Platform</h1>
    <p>Secure travel analytics, destination intelligence, recommendation APIs, and VR engagement scoring from the WIL capstone project.</p>
  </header>
  <main>
    <div class="grid">
      {% for label, value in summary.items() %}
        <div class="metric"><strong>{{ value }}</strong><span>{{ label.replace("_", " ").title() }}</span></div>
      {% endfor %}
    </div>
    <div class="split">
      <section>
        <h2>Top Destination Signals</h2>
        <table>
          <thead><tr><th>Destination</th><th>Wonder</th><th>Revenue</th><th>Rating</th></tr></thead>
          <tbody>
            {% for row in destinations %}
              <tr>
                <td>{{ row.name }}</td>
                <td>{{ row.world_wonder }}</td>
                <td>${{ "{:,.0f}".format(row.revenue) }}</td>
                <td>{{ row.average_rating }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </section>
      <section>
        <h2>Regional Revenue</h2>
        <canvas id="regionChart" height="245"></canvas>
      </section>
    </div>
    <div class="split" style="margin-top:18px">
      <section>
        <h2>Destination Recommender</h2>
        <input id="query" value="luxury scenic family trip by flight" aria-label="Recommendation query">
        <input id="budget" value="3500" type="number" aria-label="Budget">
        <button onclick="recommend()">Find Matches</button>
        <pre id="recommendationOutput">Ready.</pre>
      </section>
      <section>
        <h2>API Surface</h2>
        <table>
          <tr><td>GET</td><td>/api/summary</td></tr>
          <tr><td>GET</td><td>/api/destinations</td></tr>
          <tr><td>GET</td><td>/api/recommend?query=scenic&budget=3000</td></tr>
          <tr><td>POST</td><td>/api/secure-insert</td></tr>
          <tr><td>POST</td><td>/api/vr-engagement</td></tr>
        </table>
      </section>
    </div>
  </main>
  <script>
    const regionData = {{ regions|tojson }};
    new Chart(document.getElementById("regionChart"), {
      type: "bar",
      data: {
        labels: regionData.map(row => row.region),
        datasets: [{ label: "Revenue", data: regionData.map(row => row.revenue), backgroundColor: "#0e7c66" }]
      },
      options: { plugins: { legend: { display: false } }, scales: { y: { ticks: { callback: value => "$" + value.toLocaleString() } } } }
    });
    async function recommend() {
      const query = encodeURIComponent(document.getElementById("query").value);
      const budget = encodeURIComponent(document.getElementById("budget").value);
      const response = await fetch(`/api/recommend?query=${query}&budget=${budget}`);
      document.getElementById("recommendationOutput").textContent = JSON.stringify(await response.json(), null, 2);
    }
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(
        PAGE,
        summary=platform_summary(),
        destinations=destination_performance(8),
        regions=region_revenue(),
    )


@app.get("/api/summary")
def api_summary():
    return jsonify(platform_summary())


@app.get("/api/destinations")
def api_destinations():
    return jsonify(destination_performance(int(request.args.get("limit", 12))))


@app.get("/api/activity-mix")
def api_activity_mix():
    return jsonify(activity_mix())


@app.get("/api/regions")
def api_regions():
    return jsonify(region_revenue())


@app.get("/api/recommend")
def api_recommend():
    query = request.args.get("query", "scenic luxury family")
    budget = request.args.get("budget")
    return jsonify(recommend_destinations(query=query, budget=float(budget) if budget else None))


@app.post("/api/secure-insert")
def api_secure_insert():
    payload = request.get_json(force=True)
    sensitive = str(payload.get("sensitive_field", ""))
    return jsonify({"status": "encrypted", "encrypted_data": encrypt_text(sensitive)})


@app.post("/api/vr-engagement")
def api_vr_engagement():
    return jsonify(predict_vr_engagement(request.get_json(force=True)))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
