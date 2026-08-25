import os
import sys
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console

logger = logging.getLogger(__name__)

class QueueManager:
    """배치/예약 대기열(Queue) 관리자: 링크들을 예약 등록하고 순차적으로 자동 처리"""

    def __init__(self, queue_file: str = "data/queue.json", history_file: str = "data/queue_history.json"):
        self.queue_file = Path(queue_file)
        self.history_file = Path(history_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.queue_file.exists():
            self.queue_file.write_text("[]", encoding="utf-8")
        if not self.history_file.exists():
            self.history_file.write_text("[]", encoding="utf-8")

    def get_queue(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.queue_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def save_queue(self, queue: List[Dict[str, Any]]):
        self.queue_file.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_urls(self, urls: List[str]) -> int:
        """대기열에 신규 URL 목록 추가 (중복 방지)"""
        current_queue = self.get_queue()
        existing_urls = {item["url"] for item in current_queue}
        
        added_count = 0
        for u in urls:
            cleaned = u.strip()
            if cleaned and cleaned not in existing_urls:
                current_queue.append({
                    "url": cleaned,
                    "added_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "pending",
                    "retries": 0
                })
                existing_urls.add(cleaned)
                added_count += 1

        self.save_queue(current_queue)
        logger.info(f"Added {added_count} URLs to queue. (Total pending: {len(current_queue)})")
        return added_count

    def run_worker(self, interval_seconds: int = 5, continuous: bool = False):
        """대기열 작업자: pending 상태인 URL을 순차적으로 분석"""
        from pipeline.orchestrator import BuildPipelineOrchestrator
        from pipeline.web_orchestrator import WebPipelineOrchestrator

        console = Console()
        video_orc = BuildPipelineOrchestrator()
        web_orc = WebPipelineOrchestrator()

        console.print("[bold cyan]🚀 Deepwoken AI 예약 대기열 작업자(Worker) 가동 시작...[/bold cyan]\n")

        while True:
            queue = self.get_queue()
            pending_items = [item for item in queue if item["status"] == "pending"]

            if not pending_items:
                if not continuous:
                    console.print("[green]✅ 대기열의 모든 예약 작업 처리가 완료되었습니다.[/green]")
                    break
                else:
                    time.sleep(interval_seconds)
                    continue

            item = pending_items[0]
            url = item["url"]
            console.print(f"\n[bold yellow]⚡ [처리 중 ({len(pending_items)}개 남음)][/bold yellow] {url}")

            is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
            try:
                if is_youtube:
                    video_orc.process_url(url)
                else:
                    web_orc.process_url(url)

                item["status"] = "completed"
                item["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                console.print(f"[bold green]✓ 성공:[/] {url}")
            except Exception as e:
                item["retries"] += 1
                if item["retries"] >= 3:
                    item["status"] = "failed"
                    item["error"] = str(e)
                    console.print(f"[bold red]✗ 3회 실패로 건너뜀:[/] {url} ({e})")
                else:
                    item["last_error"] = str(e)
                    console.print(f"[yellow]⚠️ 재시도 예정 (시도 {item['retries']}/3):[/yellow] {e}")

            self.save_queue(queue)
            time.sleep(interval_seconds)
