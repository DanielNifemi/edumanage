#!/usr/bin/env python
"""
Create a simple proxy server to test if the issue is with Vite
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
import threading
import time

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request('GET')
    
    def do_POST(self):
        self.proxy_request('POST')
    
    def proxy_request(self, method):
        # Get the request data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None
        
        # Build the target URL
        target_url = f"http://localhost:8000{self.path}"
        
        print(f"Proxying {method} {self.path} to {target_url}")
        
        try:
            # Forward the request
            headers = {key: value for key, value in self.headers.items() 
                      if key.lower() not in ['host', 'connection']}
            
            if method == 'GET':
                response = requests.get(target_url, headers=headers)
            else:
                response = requests.post(target_url, data=post_data, headers=headers)
            
            # Send response back
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                if header.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            print(f"Proxy error: {e}")
            self.send_error(500, f"Proxy Error: {e}")

def start_test_proxy():
    """Start a test proxy on port 9000"""
    server = HTTPServer(('localhost', 9000), ProxyHandler)
    print("🔧 Starting test proxy on http://localhost:9000")
    print("   Proxying to Django on http://localhost:8000")
    print("   Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping test proxy")
        server.shutdown()

def test_proxy():
    """Test the proxy after starting it"""
    print("⏳ Waiting for proxy to start...")
    time.sleep(2)
    
    test_data = {
        'username': f'proxytest_{int(time.time())}',
        'email': f'proxytest_{int(time.time())}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Proxy',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    print("🧪 Testing custom proxy...")
    try:
        response = requests.post(
            'http://localhost:9000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Custom proxy status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Custom proxy works!")
        else:
            print(f"❌ Custom proxy failed: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Custom proxy error: {e}")

if __name__ == "__main__":
    # Start test in a separate thread
    proxy_thread = threading.Thread(target=start_test_proxy, daemon=True)
    proxy_thread.start()
    
    # Test the proxy
    test_proxy()
    
    print("\nTest completed. Proxy still running for manual testing.")
