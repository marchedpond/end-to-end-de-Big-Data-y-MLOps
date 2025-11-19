"""
Dashboard simple para visualizar métricas
"""

from flask import Flask, jsonify, render_template_string
from src.monitoring.metrics_collector import MetricsCollector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ML Pipeline Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; }
        .metric-value { font-size: 2em; font-weight: bold; color: #333; }
        .metric-label { color: #666; margin-top: 5px; }
        .refresh-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
    </style>
    <script>
        function refreshMetrics() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('tweets').textContent = data.summary.tweets_processed;
                    document.getElementById('predictions').textContent = data.summary.predictions_made;
                    document.getElementById('errors').textContent = data.summary.errors;
                    document.getElementById('latency').textContent = data.summary.average_latency_seconds + 's';
                });
        }
        setInterval(refreshMetrics, 5000);
        window.onload = refreshMetrics;
    </script>
</head>
<body>
    <div class="container">
        <h1>ML Pipeline - Dashboard</h1>
        <button class="refresh-btn" onclick="refreshMetrics()">Actualizar</button>
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value" id="tweets">0</div>
                <div class="metric-label">Tweets Procesados</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="predictions">0</div>
                <div class="metric-label">Predicciones</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="errors">0</div>
                <div class="metric-label">Errores</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="latency">0s</div>
                <div class="metric-label">Latencia Promedio</div>
            </div>
        </div>
    </div>
</body>
</html>
"""


def create_dashboard_app(metrics_collector: MetricsCollector, port: int = 8080):
    """Crea la app Flask del dashboard"""
    app = Flask(__name__)
    
    @app.route("/")
    def dashboard():
        return render_template_string(DASHBOARD_TEMPLATE)
    
    @app.route("/api/metrics")
    def api_metrics():
        return jsonify({
            "summary": metrics_collector.get_metrics_summary(),
            "recent_predictions": list(metrics_collector.recent_predictions)[-10:],
            "recent_errors": list(metrics_collector.recent_errors)[-10:]
        })
    
    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy"})
    
    return app


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dashboard")
    parser.add_argument("--port", type=int, default=8080)
    
    args = parser.parse_args()
    
    metrics = MetricsCollector()
    app = create_dashboard_app(metrics, args.port)
    logger.info(f"Dashboard en http://localhost:{args.port}")
    app.run(host="0.0.0.0", port=args.port, debug=True)

