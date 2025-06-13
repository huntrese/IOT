from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import socket

class StreamRequestHandler(SimpleHTTPRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except ConnectionAbortedError:
            print("Client disconnected, waiting for new connection...")
        except socket.error as e:
            print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        # Check specifically for stream.m3u8 request
        if self.path == '/stream.m3u8':
            stream_file = os.path.join(os.getcwd(), 'stream.m3u8')
            if not os.path.exists(stream_file):
                print(f"❌ Stream file not found at: {stream_file}")
                self.send_error(404, "Stream file not found")
                return
        super().do_GET()

def start_server(directory="stream", port=8000):
    # Ensure we're using absolute path
    abs_directory = os.path.abspath(directory)
    os.makedirs(abs_directory, exist_ok=True)
    os.chdir(abs_directory)
    
    handler = StreamRequestHandler
    server = HTTPServer(("0.0.0.0", port), handler)
    
    print(f"🌐 Serving HLS stream at port {port}")
    print(f"📂 Serving from directory: {abs_directory}")
    print(f"🔗 Stream URL: http://localhost:{port}/stream.m3u8")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
