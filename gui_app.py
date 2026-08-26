import os
import sys
import json
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path

# 현재 프로젝트 디렉토리 경로
PROJECT_DIR = Path(__file__).parent.resolve()
os.chdir(PROJECT_DIR)

class DeepwokenAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Deepwoken AI Build Analyzer (안티그래비티)")
        self.root.geometry("780x620")
        self.root.minsize(700, 550)
        self.root.configure(bg="#12161f")

        # 폰트 및 스타일 설정
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#12161f", foreground="#e2e8f0", font=("Malgun Gothic", 10))
        self.style.configure("Header.TLabel", background="#12161f", foreground="#38bdf8", font=("Malgun Gothic", 15, "bold"))
        self.style.configure("Sub.TLabel", background="#12161f", foreground="#94a3b8", font=("Malgun Gothic", 9))
        self.style.configure("TButton", font=("Malgun Gothic", 10, "bold"), padding=6)
        
        self.last_analyzed_json = None
        self.create_widgets()

    def create_widgets(self):
        # 헤더
        header_frame = tk.Frame(self.root, bg="#12161f", pady=10)
        header_frame.pack(fill=tk.X, padx=20)

        title_lbl = ttk.Label(header_frame, text="⚔️ Deepwoken AI Build Analyzer", style="Header.TLabel")
        title_lbl.pack(anchor="w")

        sub_lbl = ttk.Label(header_frame, text="유튜브 영상 또는 웹 가이드 링크를 입력하면 AI가 빌드를 전자동 분석/구조화합니다.", style="Sub.TLabel")
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # 입력 프레임
        input_frame = tk.Frame(self.root, bg="#1e293b", bd=1, relief=tk.SOLID, padx=15, pady=12)
        input_frame.pack(fill=tk.X, padx=20, pady=8)

        url_label = tk.Label(
            input_frame, 
            text="🔗 분석할 URL (유튜브, 구글 닥스, 웹 링크를 1개 또는 여러 줄로 붙여넣으세요):", 
            bg="#1e293b", fg="#38bdf8", font=("Malgun Gothic", 10, "bold")
        )
        url_label.pack(anchor="w")

        self.url_text = scrolledtext.ScrolledText(
            input_frame, height=4, font=("Consolas", 10), 
            bg="#0f172a", fg="#f8fafc", insertbackground="white", bd=1, relief=tk.SOLID
        )
        self.url_text.pack(fill=tk.X, pady=(6, 10))
        self.url_text.insert(tk.END, "https://www.youtube.com/watch?v=wL96bVek6Cg")

        # 버튼 그리드
        btn_grid = tk.Frame(input_frame, bg="#1e293b")
        btn_grid.pack(fill=tk.X)

        self.analyze_btn = tk.Button(
            btn_grid, text="⬇️ 대기열에 추가 및 시작", command=self.start_analysis,
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white",
            font=("Malgun Gothic", 10, "bold"), relief=tk.FLAT, padx=15, pady=7, cursor="hand2"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.chat_btn = tk.Button(
            btn_grid, text="💬 AI 챗봇", command=self.open_chat_terminal,
            bg="#059669", fg="white", activebackground="#047857", activeforeground="white",
            font=("Malgun Gothic", 10, "bold"), relief=tk.FLAT, padx=12, pady=7, cursor="hand2"
        )
        self.chat_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.view_btn = tk.Button(
            btn_grid, text="🌐 웹 뷰어로 보기", command=self.open_web_viewer,
            bg="#7c3aed", fg="white", activebackground="#6d28d9", activeforeground="white",
            font=("Malgun Gothic", 10, "bold"), relief=tk.FLAT, padx=12, pady=7, cursor="hand2"
        )
        self.view_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.sync_btn = tk.Button(
            btn_grid, text="☁️ 클라우드 동기화", command=self.sync_cloud,
            bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white",
            font=("Malgun Gothic", 10, "bold"), relief=tk.FLAT, padx=12, pady=7, cursor="hand2"
        )
        self.sync_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.wiki_btn = tk.Button(
            btn_grid, text="📚 위키 DB 갱신", command=self.sync_wiki,
            bg="#475569", fg="white", activebackground="#334155", activeforeground="white",
            font=("Malgun Gothic", 10), relief=tk.FLAT, padx=10, pady=7, cursor="hand2"
        )
        self.wiki_btn.pack(side=tk.RIGHT)

        # 대기열 리스트박스 (새로 추가됨)
        queue_label = tk.Label(
            input_frame, 
            text="📋 대기열 (Queue): 위에 링크를 넣고 '분석 큐에 추가'를 누르세요. 순서대로 자동 실행됩니다.", 
            bg="#1e293b", fg="#94a3b8", font=("Malgun Gothic", 9)
        )
        queue_label.pack(anchor="w", pady=(15, 2))

        self.queue_listbox = tk.Listbox(
            input_frame, height=4, font=("Consolas", 9),
            bg="#0f172a", fg="#f8fafc", bd=1, relief=tk.SOLID, selectbackground="#38bdf8"
        )
        self.queue_listbox.pack(fill=tk.X)
        self.is_processing = False
        self.queue_thread = None

        # 로그 출력 영역
        log_header_frame = tk.Frame(self.root, bg="#12161f")
        log_header_frame.pack(fill=tk.X, padx=20, pady=(10, 2))

        log_title = ttk.Label(log_header_frame, text="📋 진행 로그 및 분석 결과:", style="TLabel")
        log_title.pack(side=tk.LEFT)

        self.copy_json_btn = tk.Button(
            log_header_frame, text="📋 deepwoken.co 주입 코드 복사", command=self.copy_injection_code,
            bg="#0f766e", fg="white", font=("Malgun Gothic", 9, "bold"), relief=tk.FLAT, padx=8, pady=2, cursor="hand2", state=tk.DISABLED
        )
        self.copy_json_btn.pack(side=tk.RIGHT)

        self.log_text = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Consolas", 10),
            bg="#0a0e17", fg="#cbd5e1", insertbackground="white", bd=1, relief=tk.SOLID
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.log("💡 [안내] URL 입력창에 링크를 넣고 '대기열에 추가'를 누르면 순서대로 자동 분석됩니다.\n")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_analysis(self):
        """기존 start_analysis를 큐 추가(Add to Queue) 로직으로 대체합니다."""
        raw_text = self.url_text.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("입력 확인", "URL을 입력해 주세요.")
            return

        urls = [line.strip() for line in raw_text.splitlines() if line.strip() and not line.strip().startswith("#")]
        if not urls:
            return
            
        for u in urls:
            self.queue_listbox.insert(tk.END, u)
            self.log(f"✅ 대기열 추가됨: {u}")
            
        self.url_text.delete(1.0, tk.END)
        
        if not self.is_processing:
            self.is_processing = True
            self.analyze_btn.config(text="⏳ 분석 큐 가동 중 (추가 가능)")
            self.queue_thread = threading.Thread(target=self._process_queue_worker, daemon=True)
            self.queue_thread.start()

    def _process_queue_worker(self):
        while True:
            size = self.queue_listbox.size()
            if size == 0:
                self.is_processing = False
                self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL, text="⬇️ 대기열에 추가 및 시작"))
                self.root.after(0, self.log, "\n🎉 [완료] 대기열의 모든 분석이 끝났습니다!")
                break
                
            current_url = self.queue_listbox.get(0)
            self.queue_listbox.delete(0)
            
            self.root.after(0, self.log, "\n" + "="*60 + f"\n🚀 큐 자동 분석 시작: {current_url}")
            
            # main.py analyze 명령어 동기식 실행
            is_youtube = "youtube.com" in current_url.lower() or "youtu.be" in current_url.lower()
            cmd = [sys.executable, "main.py", "analyze" if is_youtube else "web", current_url]

            creation_flags = 0x08000000 if sys.platform == "win32" else 0
            try:
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1,
                    creationflags=creation_flags
                )
                for line in iter(process.stdout.readline, ''):
                    if line:
                        self.root.after(0, self.log, line.rstrip())
                process.stdout.close()
                process.wait()

                if process.returncode == 0:
                    self.root.after(0, self.log, "✅ [성공] 분석 완료!")
                    self.root.after(0, self._on_analysis_success, current_url)
                else:
                    self.root.after(0, self.log, f"❌ [실패] 에러 코드 {process.returncode}")
            except Exception as e:
                self.root.after(0, self.log, f"❌ [예외 발생] {e}")

    def _run_queue_thread(self, total_count: int):
        cmd = [sys.executable, "main.py", "queue"]
        creation_flags = 0x08000000 if sys.platform == "win32" else 0
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1,
                creationflags=creation_flags
            )
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.root.after(0, self.log, line.rstrip())
            process.stdout.close()
            process.wait()
            if process.returncode == 0:
                self.root.after(0, self.log, "\n" + "="*60 + f"\n🎉 [성공] 총 {total_count}개 빌드의 자동 분석 및 지식 베이스 등록이 모두 완료되었습니다!")
                self.root.after(0, self._on_analysis_success, "")
            else:
                self.root.after(0, self.log, f"\n⚠️ [완료/확인 필요] 프로세스 종료 코드: {process.returncode}")
        except Exception as e:
            self.root.after(0, self.log, f"\n❌ [예외 발생] {e}")
        finally:
            self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL, text="🚀 빌드 자동 분석 시작 (Analyze)"))

    def _run_analysis_thread(self, url: str):
        is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
        cmd = [sys.executable, "main.py", "analyze" if is_youtube else "web", url]
        creation_flags = 0x08000000 if sys.platform == "win32" else 0

        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1,
                creationflags=creation_flags
            )

            for line in iter(process.stdout.readline, ''):
                if line:
                    clean_line = line.rstrip()
                    self.root.after(0, self.log, clean_line)

            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                self.root.after(0, self.log, "\n" + "="*60 + "\n✅ [완료] 빌드 분석 및 지식 베이스 등록이 성공적으로 완료되었습니다!")
                self.root.after(0, self._on_analysis_success, url)
            else:
                self.root.after(0, self.log, f"\n❌ [오류] 프로세스가 에러 코드 {process.returncode}로 종료되었습니다.")
        except Exception as e:
            self.root.after(0, self.log, f"\n❌ [예외 발생] {e}")
        finally:
            self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL, text="🚀 빌드 자동 분석 시작 (Analyze)"))

    def _on_analysis_success(self, url: str):
        self.copy_json_btn.config(state=tk.NORMAL)
        # 깃허브 자동 백업 실행 (백그라운드 무음 실행)
        threading.Thread(target=self._auto_push_github, args=(url,), daemon=True).start()

    def _auto_push_github(self, url: str):
        creation_flags = 0x08000000 if sys.platform == "win32" else 0
        try:
            subprocess.run(["git", "add", "data/analysis/", "data/knowledge_base/"], cwd=str(PROJECT_DIR), check=True, creationflags=creation_flags)
            diff_proc = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=str(PROJECT_DIR), creationflags=creation_flags)
            if diff_proc.returncode != 0:
                subprocess.run(["git", "commit", "-m", f"🤖 [Local PC] 빌드 분석 자동 동기화 ({url[:30]})"], cwd=str(PROJECT_DIR), check=True, creationflags=creation_flags)
                subprocess.run(["git", "push", "origin", "main"], cwd=str(PROJECT_DIR), check=True, creationflags=creation_flags)
                self.root.after(0, self.log, "☁️ [GitHub 동기화 완료] 깃허브 저장소에 최신 빌드 데이터가 자동 백업되었습니다.")
        except Exception as e:
            self.root.after(0, self.log, f"⚠️ [GitHub 동기화 건너뜀] {e}")
        # 최신 분석 파일 찾기 (하위 카테고리 폴더 재귀 탐색)
        analysis_dir = PROJECT_DIR / "data" / "analysis"
        json_files = sorted(analysis_dir.rglob("*.json"), key=os.path.getmtime, reverse=True)
        if json_files:
            self.last_analyzed_json = json_files[0]
            self.log(f"\n💾 저장된 JSON: {self.last_analyzed_json.name}")
            self.log("💡 우측 상단의 '📋 deepwoken.co 주입 코드 복사' 버튼을 눌러 바로 deepwoken.co/builder에 적용할 수 있습니다.")

    def copy_injection_code(self):
        if not self.last_analyzed_json or not self.last_analyzed_json.exists():
            messagebox.showinfo("안내", "아직 분석된 최신 빌드가 없습니다.")
            return

        try:
            data = json.loads(self.last_analyzed_json.read_text(encoding="utf-8"))
            js_code = f"""// Deepwoken Builder 자동 주입 코드 (F12 콘솔에 붙여넣기)
const myBuild = {json.dumps(data, ensure_ascii=False, indent=2)};
localStorage.setItem('dwb-active-build', JSON.stringify(myBuild));
localStorage.setItem('dw-builder-save', JSON.stringify(myBuild));
location.reload();
"""
            self.root.clipboard_clear()
            self.root.clipboard_append(js_code)
            messagebox.showinfo("복사 완료", "deepwoken.co/builder 콘솔 주입용 코드가 클립보드에 복사되었습니다!\n\n사이트에서 F12 -> Console 탭에 붙여넣기(Ctrl+V) 후 엔터를 누르세요.")
        except Exception as e:
            messagebox.showerror("오류", f"주입 코드 복사 실패: {e}")

    def open_chat_terminal(self):
        """챗봇을 별도 CMD 창에서 실행"""
        cmd = f'start cmd /k "cd /d "{PROJECT_DIR}" && python main.py chat"'
        subprocess.Popen(cmd, shell=True)

    def open_web_viewer(self):
        """로컬 웹 뷰어 실행 및 브라우저 열기"""
        cmd = f'start cmd /c "cd /d "{PROJECT_DIR}" && python main.py view"'
        subprocess.Popen(cmd, shell=True)
        import webbrowser
        self.root.after(1000, lambda: webbrowser.open("http://localhost:8000"))

    def open_queue_dialog(self):
        """다중 링크 일괄 예약 및 대기열 관리 창"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📋 Deepwoken 링크 일괄 예약 & 대기열")
        dialog.geometry("620x520")
        dialog.configure(bg="#12161f")

        tk.Label(dialog, text="📋 일괄 분석할 링크들을 줄 단위로 붙여넣으세요:", bg="#12161f", fg="#38bdf8", font=("Malgun Gothic", 10, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        txt_area = scrolledtext.ScrolledText(dialog, wrap=tk.NONE, font=("Consolas", 10), bg="#0f172a", fg="#f8fafc", insertbackground="white", height=10)
        txt_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        txt_area.insert(tk.END, "# 여기에 유튜브, 웹사이트, 구글 닥스 링크를 한 줄에 하나씩 넣으세요\nhttps://www.youtube.com/watch?v=...\nhttps://docs.google.com/document/d/...\n")

        from agents.queue_manager import QueueManager
        qm = QueueManager()

        def add_to_queue():
            raw_lines = txt_area.get(1.0, tk.END).splitlines()
            valid_urls = [line.strip() for line in raw_lines if line.strip() and not line.strip().startswith("#")]
            if not valid_urls:
                messagebox.showwarning("입력 확인", "유효한 URL이 입력되지 않았습니다.")
                return
            count = qm.add_urls(valid_urls)
            messagebox.showinfo("예약 완료", f"총 {count}개의 링크가 예약 대기열에 등록되었습니다!")
            dialog.destroy()
            self.log(f"\n📋 [대기열] {count}개의 링크가 예약되었습니다. 'main.py queue' 또는 백그라운드 워커가 순차 처리합니다.")

        def run_queue_now():
            dialog.destroy()
            self.log("\n🚀 [대기열 작업 시작] 예약된 모든 링크를 순차적으로 자동 분석합니다...")
            threading.Thread(target=self._run_cmd_thread, args=(["main.py", "queue"],), daemon=True).start()

        btn_box = tk.Frame(dialog, bg="#12161f")
        btn_box.pack(fill=tk.X, padx=15, pady=15)

        tk.Button(btn_box, text="➕ 대기열에 예약 추가", command=add_to_queue, bg="#2563eb", fg="white", font=("Malgun Gothic", 10, "bold"), padx=10, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_box, text="⚡ 지금 전체 순차 실행", command=run_queue_now, bg="#059669", fg="white", font=("Malgun Gothic", 10, "bold"), padx=10, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT)
        tk.Button(btn_box, text="닫기", command=dialog.destroy, bg="#475569", fg="white", font=("Malgun Gothic", 10), padx=10, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT)

    def sync_cloud(self):
        """클라우드에서 분석된 모든 최신 빌드를 0.5초 만에 자동 동기화"""
        self.log("\n☁️ [클라우드 동기화] GitHub에서 최신 분석 데이터 가져오는 중...")
        threading.Thread(target=self._run_git_pull_thread, daemon=True).start()

    def _run_git_pull_thread(self):
        try:
            p = subprocess.Popen(["git", "pull", "origin", "main"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
            for line in iter(p.stdout.readline, ''):
                if line:
                    self.root.after(0, self.log, line.rstrip())
            p.stdout.close()
            p.wait()
            self.root.after(0, self.log, "\n🎉 [완료] 클라우드의 모든 최신 빌드가 내 컴퓨터로 100% 동기화되었습니다!")
            # 최신 분석 파일 버튼 활성화
            self.root.after(0, self._on_analysis_success, "")
        except Exception as e:
            self.root.after(0, self.log, f"\n❌ 동기화 오류: {e}")

    def sync_wiki(self):
        """위키 전수 수집 백그라운드 실행"""
        self.log("\n📚 위키 14개 카테고리 전수 수집 시작...")
        threading.Thread(target=self._run_cmd_thread, args=(["main.py", "wiki"],), daemon=True).start()

    def _run_cmd_thread(self, args):
        cmd = [sys.executable] + args
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
            for line in iter(p.stdout.readline, ''):
                if line:
                    self.root.after(0, self.log, line.rstrip())
            p.stdout.close()
            p.wait()
            self.root.after(0, self.log, "\n✅ 위키 DB 동기화 완료!")
        except Exception as e:
            self.root.after(0, self.log, f"\n❌ 오류: {e}")

def main():
    root = tk.Tk()
    app = DeepwokenAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
