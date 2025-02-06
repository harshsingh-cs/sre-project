from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import platform
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Define metrics correctly using the metrics object
@metrics.counter('requests_total', 'Total requests')
def count_requests():
    return 1

@metrics.histogram('request_latency_seconds', 'Request latency in seconds')
def track_latency():
    return time.time() - request.start_time if hasattr(request, 'start_time') else 0

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    return response

@app.route('/health', methods=['GET', 'HEAD', 'POST'])
def health():
    if request.method in ['GET', 'HEAD']:
        return jsonify({
            'status': 'healthy',
            'hostname': platform.node(),
            'platform': platform.platform()
        }), 200
    elif request.method == 'POST':
        data = request.get_json(silent=True) or {}
        return jsonify({
            'status': 'received',
            'data': data
        }), 201

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({
            'message': 'Welcome to the web server'
        })
    elif request.method == 'POST':
        data = request.get_json(silent=True) or {}
        return jsonify({
            'message': 'Data received',
            'data': data
        }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7100, debug=True)