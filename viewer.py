import http.server
import socketserver
import webbrowser
import os

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress request logs

def launch():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        webbrowser.open(f"http://localhost:{PORT}/viewer.html")
        print(f"  Blockchain Viewer running at http://localhost:{PORT}/viewer.html")
        print("  Press Ctrl+C to stop the viewer and return to menu.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Viewer stopped.")

if __name__ == "__main__":
    launch()
