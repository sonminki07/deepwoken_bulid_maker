import os
import shutil
import logging
from pathlib import Path
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

# 기본 감지할 구글 드라이브 후보 경로들
CANDIDATE_GDRIVE_DIRS = [
    Path(r"G:\내 드라이브\Deepwoken"),
    Path(r"G:\My Drive\Deepwoken"),
    Path(r"G:\내 드라이브"),
    Path(r"G:\My Drive"),
    Path(os.path.expanduser(r"~\Google Drive\Deepwoken")),
    Path(os.path.expanduser(r"~\Google Drive")),
    Path(r"C:\Users\minki\Google Drive\Deepwoken"),
]

def find_gdrive_sync_dir() -> Optional[Path]:
    """시스템에서 Google Drive 폴더를 자동 감지하고 Deepwoken 하위 폴더를 반환합니다."""
    for p in CANDIDATE_GDRIVE_DIRS:
        try:
            if p.name == "Deepwoken" and p.parent.exists():
                p.mkdir(parents=True, exist_ok=True)
                return p
            elif p.exists():
                target = p / "Deepwoken" if p.name != "Deepwoken" else p
                target.mkdir(parents=True, exist_ok=True)
                return target
        except Exception:
            continue
    return None

def sync_to_google_drive(project_dir: Optional[Path] = None) -> Tuple[bool, str, List[Path]]:
    """프로젝트 내의 Master NotebookLM 소스 파일 및 최신 지식을 구글 드라이브로 자동 복사/동기화합니다."""
    if project_dir is None:
        project_dir = Path(__file__).resolve().parent.parent

    gdrive_dir = find_gdrive_sync_dir()
    if not gdrive_dir:
        return False, "Google Drive (G: 또는 로컬) 데스크톱 동기화 폴더를 찾을 수 없습니다.", []

    data_dir = project_dir / "data"
    synced_files = []

    # 복사할 주요 소스 파일들
    files_to_sync = [
        data_dir / "Deepwoken_Master_NotebookLM_Source.md",
        data_dir / "Deepwoken_Master_NotebookLM_Source.txt",
    ]

    # 개별 최신 빌드 MD 파일들도 추가 동기화
    builds_kb_dir = data_dir / "knowledge_base" / "builds"
    if builds_kb_dir.exists():
        gdrive_builds_dir = gdrive_dir / "builds"
        gdrive_builds_dir.mkdir(parents=True, exist_ok=True)
        for md_file in builds_kb_dir.glob("*.md"):
            try:
                dest = gdrive_builds_dir / md_file.name
                shutil.copy2(md_file, dest)
                synced_files.append(dest)
            except Exception as e:
                logger.warning(f"Failed to copy build {md_file.name}: {e}")

    # 마스터 파일들 동기화
    for src_file in files_to_sync:
        if src_file.exists():
            try:
                dest = gdrive_dir / src_file.name
                shutil.copy2(src_file, dest)
                synced_files.append(dest)
            except Exception as e:
                logger.error(f"Failed to copy {src_file.name}: {e}")

    msg = f"Google Drive ({gdrive_dir})에 총 {len(synced_files)}개 파일이 실시간 자동 동기화되었습니다."
    logger.info(msg)
    return True, msg, synced_files

if __name__ == "__main__":
    success, msg, files = sync_to_google_drive()
    print("Success:", success)
    print("Message:", msg)
    print("Files:", [f.name for f in files])