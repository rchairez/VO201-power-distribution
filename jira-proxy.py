
#!/usr/bin/env python3
"""
Tiny Jira CORS proxy for VO201 Power Distribution.
Usage: python3 jira-proxy.py
Then the browser calls http://localhost:8098/rest/api/3/...
Credentials are passed through from the browser — nothing is stored here.
"""

import http.server
import urllib.request
import urllib.error
import json

JIRA_BASE = "https://coreweave.atlassian.net"
PORT = 8098

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[jira-proxy] {args[0]} {args[1]}")

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Accept, Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        target = JIRA_BASE + self.path
        headers = {"Accept": "application/json"}

        # Forward Authorization header from the browser
        auth = self.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth

        req = urllib.request.Request(target, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors()
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_cors()
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    print(f"Jira proxy running on http://localhost:{PORT}")
    print(f"Forwarding to {JIRA_BASE}")
    print("Credentials are passed through from the browser — nothing stored here.")
    http.server.HTTPServer(("", PORT), ProxyHandler).serve_forever()
