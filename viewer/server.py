import os
import sys
import json
import logging
import subprocess
import webbrowser
import http.server
import socketserver
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).resolve().parent.parent
VIEWER_DIR = Path(__file__).resolve().parent

class DeepwokenAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Deepwoken 빌드 뷰어 및 AI 웹 챗봇 API 서버 핸들러"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(VIEWER_DIR), **kwargs)

    def log_message(self, format, *args):
        # 콘솔 로그 노이즈 억제
        pass

    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/builds":
            analysis_dir = PROJECT_DIR / "data" / "analysis"
            builds = []
            if analysis_dir.exists():
                for f in sorted(analysis_dir.rglob("*.json"), key=os.path.getmtime, reverse=True):
                    try:
                        content = json.loads(f.read_text(encoding="utf-8"))
                        summary = content.get("build_summary", {})
                        builds.append({
                            "id": f.stem,
                            "filename": f.name,
                            "category": f.parent.name,
                            "name": summary.get("build_name", f.stem),
                            "type": summary.get("build_type", "Unknown"),
                            "author": summary.get("author", "Unknown"),
                            "difficulty": summary.get("difficulty", "Intermediate"),
                            "data": content
                        })
                    except Exception as e:
                        logger.error(f"Error loading {f}: {e}")
            self._send_json({"builds": builds})
            return

        elif self.path == "/api/status":
            self._send_json({"status": "running", "project_dir": str(PROJECT_DIR)})
            return

        # 일반 정적 파일(index.html 등) 서빙
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}

        if self.path == "/api/chat":
            user_msg = req_data.get("message", "").strip()
            if not user_msg:
                self._send_json({"error": "메시지가 비어있습니다."}, status=400)
                return

            try:
                # RAG AI Advisor 실행
                sys.path.insert(0, str(PROJECT_DIR))
                from chatbot.build_advisor import DeepwokenBuildAdvisor
                advisor = DeepwokenBuildAdvisor(top_k=4)
                answer = advisor.answer_query(user_msg)
                self._send_json({"reply": answer})
            except Exception as e:
                logger.error(f"Chat error: {e}")
                self._send_json({"error": str(e)}, status=500)
            return

        elif self.path == "/api/sync":
            # GitHub 동기화 실행
            try:
                proc = subprocess.run(
                    ["git", "pull", "origin", "main"], 
                    cwd=str(PROJECT_DIR), 
                    capture_output=True, 
                    text=True
                )
                self._send_json({
                    "success": proc.returncode == 0,
                    "output": proc.stdout or proc.stderr
                })
            except Exception as e:
                self._send_json({"success": False, "output": str(e)}, status=500)
            return

        self._send_json({"error": "Not Found"}, status=404)

def start_viewer(port: int = 8000):
    url = f"http://localhost:{port}/index.html"
    print("\n" + "="*60)
    print(f"🚀 Deepwoken AI Web Chat & Build Viewer 서버 가동: {url}")
    print("웹 브라우저가 자동으로 열립니다. (종료하려면 Ctrl+C 를 누르세요)")
    print("="*60 + "\n")

    webbrowser.open(url)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), DeepwokenAPIHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")

if __name__ == "__main__":
    start_viewer()
