import time
import logging
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

from pipeline.orchestrator import PipelineOrchestrator

logger = logging.getLogger(__name__)

class BatchProcessor:
    """대량 영상 및 재생목록 일괄 처리기"""

    def __init__(self, orchestrator: PipelineOrchestrator, delay_between_videos_sec: float = 5.0):
        self.orchestrator = orchestrator
        self.delay_between_videos_sec = delay_between_videos_sec

    def process_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """복수 영상 URL 목록 순차 처리"""
        results = []
        total = len(urls)
        console = Console()

        console.print(f"\n[bold cyan]🚀 Starting Batch Processing for {total} video(s)...[/bold cyan]\n")

        for idx, url in enumerate(urls, 1):
            console.print(f"[bold yellow]▶ [{idx}/{total}] Processing:[/] {url}")
            try:
                res = self.orchestrator.process_url(url)
                results.append(res)
                console.print(f"[bold green]✔ [{idx}/{total}] Success:[/] {res['build_name']} (ID: {res['video_id']})\n")
            except Exception as e:
                logger.error(f"Failed to process video {url}: {e}", exc_info=True)
                results.append({
                    "status": "failed",
                    "url": url,
                    "error": str(e)
                })
                console.print(f"[bold red]✖ [{idx}/{total}] Failed:[/] {e}\n")

            if idx < total and self.delay_between_videos_sec > 0:
                time.sleep(self.delay_between_videos_sec)

        self._print_summary_table(results)
        return results

    def process_playlist(self, playlist_url: str) -> List[Dict[str, Any]]:
        """재생목록 URL에서 모든 영상 추출 후 일괄 처리"""
        console = Console()
        console.print(f"[bold blue]🔍 Extracting video URLs from playlist:[/] {playlist_url}")
        urls = self.orchestrator.collector.extract_playlist_urls(playlist_url)
        console.print(f"[green]Found {len(urls)} video(s) in playlist.[/green]")
        return self.process_urls(urls)

    def _print_summary_table(self, results: List[Dict[str, Any]]):
        console = Console()
        table = Table(title="📊 Batch Processing Summary", header_style="bold magenta")
        table.add_column("No.", style="dim", width=4)
        table.add_column("Video ID / URL", style="cyan")
        table.add_column("Build Name", style="bold green")
        table.add_column("Status", style="bold")
        table.add_column("Time (s)", justify="right")

        for idx, r in enumerate(results, 1):
            status = "[green]SUCCESS[/green]" if r.get("status") == "success" else "[red]FAILED[/red]"
            vid = r.get("video_id", r.get("url", "N/A"))
            name = r.get("build_name", r.get("error", "N/A"))[:30]
            elapsed = f"{r.get('elapsed_seconds', 0):.1f}s" if "elapsed_seconds" in r else "-"
            table.add_row(str(idx), vid, name, status, elapsed)

        console.print("\n")
        console.print(table)
        console.print("\n")
