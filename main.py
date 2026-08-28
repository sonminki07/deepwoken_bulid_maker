import sys
import os

# Windows CP949 인코딩 호환성 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
import logging
import warnings
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

# Google GenAI 무해한 AFC 경고 필터링
warnings.filterwarnings("ignore")
logging.getLogger("google.genai").setLevel(logging.ERROR)
logging.getLogger("google_genai").setLevel(logging.ERROR)

# .env 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
)
logger = logging.getLogger("deepwoken_analyzer")

from pipeline.orchestrator import PipelineOrchestrator
from pipeline.web_orchestrator import WebPipelineOrchestrator
from pipeline.batch_processor import BatchProcessor
from agents.knowledge_builder import KnowledgeBuilder
from chatbot.build_advisor import BuildAdvisor

console = Console()

def check_gemini_key():
    if not os.getenv("GEMINI_API_KEY"):
        console.print("[bold red]❌ Error: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.[/bold red]")
        console.print("[yellow].env 파일에 GEMINI_API_KEY=your_key 를 입력하거나 시스템 환경 변수를 등록하세요.[/yellow]")
        sys.exit(1)

def handle_analyze(args):
    check_gemini_key()
    console.print(f"[bold cyan]🔍 Analyzing YouTube video:[/] {args.url}")
    orchestrator = PipelineOrchestrator(config_path=args.config)
    res = orchestrator.process_url(args.url)
    console.print(f"\n[bold green]✅ 분석 완료![/bold green]")
    console.print(f"- [bold]빌드명:[/] {res['build_name']}")
    console.print(f"- [bold]JSON 파일:[/] {res['json_path']}")
    console.print(f"- [bold]Markdown 파일:[/] {res['md_path']}")
    console.print(f"- [bold]소요 시간:[/] {res['elapsed_seconds']:.2f}초")

def handle_web(args):
    check_gemini_key()
    console.print(f"[bold cyan]🌐 Analyzing Web Page via Sub-Agents:[/] {args.url}")
    orchestrator = WebPipelineOrchestrator(config_path=args.config)
    res = orchestrator.process_url(args.url)
    console.print(f"\n[bold green]✅ 웹페이지 서브 에이전트 분석 완료![/bold green]")
    console.print(f"- [bold]빌드명:[/] {res['build_name']}")
    console.print(f"- [bold]문서 ID:[/] {res['doc_id']}")
    console.print(f"- [bold]JSON 파일:[/] {res['json_path']}")
    console.print(f"- [bold]Markdown 파일:[/] {res['md_path']}")
    console.print(f"- [bold]소요 시간:[/] {res['elapsed_seconds']:.2f}초")

def handle_batch(args):
    check_gemini_key()
    orchestrator = PipelineOrchestrator(config_path=args.config)
    batch = BatchProcessor(orchestrator=orchestrator, delay_between_videos_sec=args.delay)

    if args.playlist:
        batch.process_playlist(args.target)
    else:
        # 파일 또는 쉼표 구분 URL 목록
        if Path(args.target).is_file():
            urls = [line.strip() for line in Path(args.target).read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
        else:
            urls = [u.strip() for u in args.target.split(",") if u.strip()]
        batch.process_urls(urls)

def handle_index(args):
    check_gemini_key()
    console.print("[bold cyan]🔄 Re-indexing analysis and knowledge base files into ChromaDB...[/bold cyan]")
    kb = KnowledgeBuilder(db_path=args.db_path)
    count = kb.ingest_all(analysis_dir=args.analysis_dir, kb_dir=args.kb_dir)
    console.print(f"[bold green]✅ 인덱싱 완료! 총 {count}개의 빌드가 인덱스되었습니다.[/bold green]")

def handle_chat(args):
    check_gemini_key()
    advisor = BuildAdvisor(
        model_name=args.model,
        db_path=args.db_path,
        top_k=args.top_k
    )
    advisor.interactive_cli()

def main():
    parser = argparse.ArgumentParser(
        description="Deepwoken Build Analyzer - 유튜브 기반 빌드 분석 및 RAG 어드바이저",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="실행 모드 선택")

    # analyze
    parser_analyze = subparsers.add_parser("analyze", help="단일 유튜브 영상 분석 및 RAG 인덱싱")
    parser_analyze.add_argument("url", type=str, help="유튜브 영상 URL")
    parser_analyze.add_argument("--config", type=str, default="config/settings.yaml", help="설정 파일 경로")

    # web (서브 에이전트 기반 웹페이지 분석)
    parser_web = subparsers.add_parser("web", help="웹사이트(위키/플래너/커뮤니티) 서브 에이전트 분석 및 RAG 인덱싱")
    parser_web.add_argument("url", type=str, help="웹페이지 URL")
    parser_web.add_argument("--config", type=str, default="config/settings.yaml", help="설정 파일 경로")

    # batch
    parser_batch = subparsers.add_parser("batch", help="복수 영상 또는 재생목록 일괄 분석")
    parser_batch.add_argument("target", type=str, help="재생목록 URL, URL 목록 파일 경로, 또는 쉼표로 구분된 URL")
    parser_batch.add_argument("--playlist", action="store_true", help="타겟이 유튜브 재생목록 URL인 경우 지정")
    parser_batch.add_argument("--delay", type=float, default=5.0, help="영상 간 딜레이(초)")
    parser_batch.add_argument("--config", type=str, default="config/settings.yaml", help="설정 파일 경로")

    # index
    parser_index = subparsers.add_parser("index", help="기존 Markdown/JSON 문서를 ChromaDB에 재인덱싱")
    parser_index.add_argument("--db-path", type=str, default="data/chromadb", help="ChromaDB 경로")
    parser_index.add_argument("--analysis-dir", type=str, default="data/analysis", help="JSON 디렉토리")
    parser_index.add_argument("--kb-dir", type=str, default="data/knowledge_base", help="MD 디렉토리")

    # chat
    parser_chat = subparsers.add_parser("chat", help="RAG 기반 AI 빌드 어드바이저 챗봇 실행")
    parser_chat.add_argument("--model", type=str, default="gemini-3.7-flash", help="Gemini 모델명")
    parser_chat.add_argument("--db-path", type=str, default="data/chromadb", help="ChromaDB 경로")
    parser_chat.add_argument("--top-k", type=int, default=4, help="참조할 유사 빌드 개수")

    # view (로컬 웹 뷰어 실행)
    parser_view = subparsers.add_parser("view", help="로컬 Deepwoken Build Viewer 웹 UI 실행")
    parser_view.add_argument("--port", type=int, default=8000, help="웹 서버 포트 번호 (기본: 8000)")

    # wiki (deepwoken.co 14개 카테고리 전체 전수 덤프)
    parser_wiki = subparsers.add_parser("wiki", help="deepwoken.co 위키의 모든 탤런트/무기/만트라/장비 전수 수집")

    # queue (예약 대기열 순차 처리 워커)
    parser_queue = subparsers.add_parser("queue", help="예약 대기열(Queue)에 있는 모든 링크 순차 분석 실행")
    parser_queue.add_argument("--interval", type=int, default=5, help="분석 간 대기 초 (기본: 5초)")
    parser_queue.add_argument("--loop", action="store_true", help="무한 대기 모드 (새 링크가 들어올 때까지 상시 대기)")

    # gdrive (구글 드라이브 동기화)
    parser_gdrive = subparsers.add_parser("gdrive", help="Google Drive(G: 또는 로컬) 데스크톱 폴더로 최신 NotebookLM 지식 베이스 동기화")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "analyze":
        handle_analyze(args)
    elif args.command == "web":
        handle_web(args)
    elif args.command == "batch":
        handle_batch(args)
    elif args.command == "index":
        handle_index(args)
    elif args.command == "chat":
        handle_chat(args)
    elif args.command == "view":
        from viewer.server import start_viewer
        start_viewer(port=args.port)
    elif args.command == "wiki":
        from agents.deepwoken_wiki_dumper import DeepwokenWikiDumper
        dumper = DeepwokenWikiDumper()
        dumper.dump_all()
    elif args.command == "queue":
        from agents.queue_manager import QueueManager
        qm = QueueManager()
        qm.run_worker(interval_seconds=args.interval, continuous=args.loop)
    elif args.command == "gdrive":
        from agents.gdrive_sync import sync_to_google_drive
        ok, msg, files = sync_to_google_drive()
        if ok:
            console.print(f"[bold green]✅ {msg}[/bold green]")
        else:
            console.print(f"[bold red]❌ {msg}[/bold red]")

if __name__ == "__main__":
    main()
