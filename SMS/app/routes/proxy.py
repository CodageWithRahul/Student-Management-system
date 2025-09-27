from flask import Blueprint, request, Response, jsonify
import requests

proxy_bp = Blueprint("proxy", __name__)

CAPTCHA_BASE = "http://localhost:8080"   # inside Docker, Tomcat service

@proxy_bp.route("/captcha/generate", methods=["GET"])
def proxy_generate():
    print("calld proxy")
    resp = requests.get(f"{CAPTCHA_BASE}/generate", stream=True)
    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, headers)

@proxy_bp.route("/captcha/validate", methods=["POST"])
def proxy_validate():
    resp = requests.post(f"{CAPTCHA_BASE}/validate", json=request.json)
    return jsonify(resp.json())
