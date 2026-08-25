import os
import sys
import webbrowser
import http.server
import socketserver
from pathlib import Path

def start_viewer(port: int = 8000):
    viewer_dir = Path(__file__).parent.resolve()
    os.chdir(viewer_dir)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress normal GET logs for clean console
            pass

    url = f"http://localhost:{port}/index.html"
    print(f"🚀 Deepwoken Build Viewer 가 실행되었습니다: {url}")
    print("브라우저가 자동으로 열립니다. (종료하려면 Ctrl+C 를 누르세요)")

    webbrowser.open(url)

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n웹 뷰어 서버를 종료합니다.")

if __name__ == "__main__":
    start_viewer()
