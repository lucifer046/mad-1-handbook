# Simple Python HTTP Server
# This is a built-in module to serve files from a directory

import http.server
import socketserver

PORT = 8000

# Handler for processing HTTP requests
# SimpleHTTPRequestHandler serves files from the current directory
Handler = http.server.SimpleHTTPRequestHandler

# Set up the server
# socketserver handles the underlying network communication
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print("Point your browser to http://localhost:8000")
    
    # Keep the server running until manually stopped
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
