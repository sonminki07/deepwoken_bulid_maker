import os
import time
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
import yt_dlp

logger = logging.getLogger(__name__)

@dataclass
class VideoMetadata:
    video_id: str
    title: str
    channel: str
    url: str
    upload_date: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    view_count: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DownloadResult:
    video_id: str
    video_path: Path
    metadata: VideoMetadata
    from_cache: bool = False

class VideoCollector:
    """1단계: YouTube 영상 및 메타데이터 다운로드 수집기"""

    def __init__(self, output_dir: str = "data/videos", max_filesize_bytes: int = 2 * 1024 * 1024 * 1024):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_filesize_bytes = max_filesize_bytes

    def extract_metadata_only(self, url: str) -> VideoMetadata:
        """다운로드 없이 영상 메타데이터만 추출 (Cloudflare/Bot bypass)"""
        ydl_opts = {
            "extract_flat": False,
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._build_metadata(info, url)
        except Exception as e:
            logger.warning(f"Failed to extract full metadata ({e}), building minimal metadata...")
            import re
            vid_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
            vid = vid_match.group(1) if vid_match else "unknown_video"
            return VideoMetadata(
                video_id=vid,
                title=f"YouTube Video ({vid})",
                channel="YouTube Creator",
                url=url
            )

    def download(self, url: str, max_retries: int = 3) -> DownloadResult:
        """단일 영상 다운로드 (2GB 용량 제어 및 자동 폴백)"""
        # 먼저 메타데이터 및 video_id 확인
        metadata = self.extract_metadata_only(url)
        video_id = metadata.video_id

        # 기존 다운로드 파일 확인 (캐시 활용)
        existing_files = list(self.output_dir.glob(f"{video_id}.*"))
        for f in existing_files:
            if f.suffix.lower() in [".mp4", ".mkv", ".webm"] and f.stat().st_size > 0:
                logger.info(f"Existing video found: {f.name}")
                return DownloadResult(
                    video_id=video_id,
                    video_path=f,
                    metadata=metadata,
                    from_cache=True
                )

        target_template = str(self.output_dir / f"{video_id}.%(ext)s")

        # FFmpeg 경로 자동 탐지
        ffmpeg_location = None
        try:
            import imageio_ffmpeg
            ffmpeg_location = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

        # 다운로드 포맷 전략 (사용자 요청: 선명한 720p 고화질 우선 적용)
        format_strategies = [
            "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best[ext=mp4]/best",
            "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]/best",
            "best[filesize<?2G]",
        ]

        # 2시간(7200초)이 넘어가는 영상 필터링
        def duration_filter(info_dict, *, incomplete):
            duration = info_dict.get('duration')
            if duration and duration > 7200:
                return "영상 길이가 2시간을 초과하여 분석이 불가능합니다."
            return None

        last_err = None
        for attempt, fmt in enumerate(format_strategies):
            ydl_opts = {
                "format": fmt,
                "outtmpl": target_template,
                "merge_output_format": "mp4",
                "noplaylist": True,
                "quiet": False,
                "no_warnings": True,
                "retries": max_retries,
                "match_filter": duration_filter,
            }
            if ffmpeg_location:
                ydl_opts["ffmpeg_location"] = ffmpeg_location

            try:
                logger.info(f"Downloading {url} with format: {fmt}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    downloaded_file = Path(ydl.prepare_filename(info))
                    if not downloaded_file.exists():
                        # 확장자가 mp4로 병합되었을 수 있음
                        downloaded_file = downloaded_file.with_suffix(".mp4")

                    # 파일 크기 검증
                    if downloaded_file.exists() and downloaded_file.stat().st_size > self.max_filesize_bytes:
                        logger.warning(f"File size {downloaded_file.stat().st_size} exceeds max limit. Trying lower resolution...")
                        if downloaded_file.exists():
                            downloaded_file.unlink()
                        continue

                    if downloaded_file.exists():
                        return DownloadResult(
                            video_id=video_id,
                            video_path=downloaded_file,
                            metadata=self._build_metadata(info, url),
                            from_cache=False
                        )
            except Exception as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                last_err = e
                time.sleep(2)

        raise RuntimeError(f"Failed to download video {url} after multiple resolution attempts: {last_err}")

    def extract_playlist_urls(self, playlist_url: str) -> List[str]:
        """재생목록 URL에서 모든 영상 URL 목록 추출"""
        ydl_opts = {
            "extract_flat": "in_playlist",
            "quiet": True,
            "no_warnings": True,
        }
        urls = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if "entries" in info:
                for entry in info["entries"]:
                    if entry and "url" in entry:
                        video_url = entry["url"]
                        if not video_url.startswith("http"):
                            video_url = f"https://www.youtube.com/watch?v={entry.get('id', video_url)}"
                        urls.append(video_url)
            else:
                urls.append(playlist_url)
        return urls

    def _build_metadata(self, info: Dict[str, Any], original_url: str) -> VideoMetadata:
        return VideoMetadata(
            video_id=info.get("id", "unknown"),
            title=info.get("title", "Untitled Video"),
            channel=info.get("uploader", info.get("channel", "Unknown Channel")),
            url=info.get("webpage_url", original_url),
            upload_date=info.get("upload_date"),
            duration=info.get("duration"),
            description=info.get("description"),
            view_count=info.get("view_count"),
            extra={
                "tags": info.get("tags", []),
                "categories": info.get("categories", []),
            }
        )
