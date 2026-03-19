#!/usr/bin/env python3
"""
Tiny NetBox CORS proxy.
Usage: python3 netbox-proxy.py
Then set NB_BASE = 'http://localhost:8099' in VO201-dh2-phoenix.html
"""

import http.server
import urllib.request
import urllib.error
import json
import os

NETBOX_BASE = "https://coreweave.cloud.netboxapp.com"
NETBOX_TOKEN = "e7413999d0bf411278032ceebb770ad41a3550ab"
PORT = 8099

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[proxy] {args[0]} {args[1]}")

    def send_cors_headers(self):
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin if origin else "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Accept, Content-Type")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        target = NETBOX_BASE + self.path
        req = urllib.request.Request(target, headers={
            "Authorization": f"Token {NETBOX_TOKEN}",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    print(f"NetBox proxy running on http://localhost:{PORT}")
    print(f"Forwarding to {NETBOX_BASE}")
    http.server.HTTPServer(("", PORT), ProxyHandler).serve_forever()
