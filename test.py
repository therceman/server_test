import http.server
import socketserver
import json
import socket
from urllib.parse import urlparse

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/latency-test':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Get the client's IP address
            if 'X-Forwarded-For' in self.headers:
                ip_address = self.headers['X-Forwarded-For'].split(',')[0]
            else:
                ip_address = self.client_address[0]

            if ':' in ip_address:
                ip_address = ip_address.split(':')[0]

            response = {
                'region': "Your Server Region",  # Replace with your actual region
                'user_ip': ip_address
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_GET()

handler = CustomHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
