#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sonoripy.core import syllabify

class SyllabifyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/syllabify':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                text = data.get('text', '').strip()
                
                if not text:
                    response = {'success': False, 'error': 'No text provided'}
                else:
                    result = syllabify(text)
                    response = {'success': True, 'result': result}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                response = {'success': False, 'error': str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def get_html(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <textarea id="ipa-input" placeholder="tʃɛʃcɪna"></textarea>
    <div id="result"></div>
    <script>
        let debounceTimer;
        
        async function syllabifyText() {
            const input = document.getElementById('ipa-input').value.trim();
            const resultDiv = document.getElementById('result');
            
            if (!input) {
                resultDiv.innerHTML = '';
                return;
            }
            
            try {
                const response = await fetch('/syllabify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: input })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `${data.result}`;
                } else {
                    resultDiv.innerHTML = `Error: ${data.error}`;
                }
            } catch (error) {
                resultDiv.innerHTML = `Error: ${error.message}`;
            }
        }
        
        document.getElementById('ipa-input').addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(syllabifyText, 300); // Wait 300ms after user stops typing
        });
        
        document.getElementById('ipa-input').focus();
    </script>
</body>
</html>'''

def run_server(port=8000):
    with socketserver.TCPServer(("", port), SyllabifyHandler) as httpd:
        print(f"http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run web server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run server on (default: 8000)')
    args = parser.parse_args()
    
    run_server(args.port)