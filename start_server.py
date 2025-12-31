#!/usr/bin/env python3
"""
Simple HTTP Server for Product Recommendation Web Demo
Run this file to start the web server
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

def main():
    print("=" * 60)
    print("🛍️  Product Recommendation Web Demo Server")
    print("=" * 60)
    print(f"📂 Serving directory: {DIRECTORY}")
    print(f"🌐 Server running at: http://localhost:{PORT}")
    print(f"📱 Open in browser: http://localhost:{PORT}/web/index.html")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            # Auto-open browser
            webbrowser.open(f'http://localhost:{PORT}/web/index.html')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
