import os
import cv2
import shutil
import tempfile
import subprocess
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict, Any
import imageio_ffmpeg

logger = logging.getLogger(__name__)

class FrameExtractor:
    """FFmpeg + OpenCV 하이브리드 초고속 정밀 프레임 추출 및 전처리 모듈"""

    def __init__(self, output_dir: str = "data/keyframes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            self.ffmpeg_exe = "ffmpeg"

    def extract_sharp_keyframes(
        self,
        video_path: Path,
        max_keyframes: int = 6,
        sample_step_sec: float = 2.0,
        min_sharpness: float = 25.0
    ) -> List[Dict[str, Any]]:
        """빌드 쇼케이스가 집중된 초반 및 핵심 구간에서 고화질 프레임을 초고속 추출"""
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            out_pattern = str(temp_path / "f_%04d.jpg")

            # 딥위큰 빌드 소개가 집중되는 전반부(0~240초)를 1.5초 간격으로 초고속 캡처
            cmd = [
                self.ffmpeg_exe, "-y",
                "-ss", "0",
                "-t", "240",
                "-i", str(video_path),
                "-vf", "fps=0.66",
                "-q:v", "2",
                out_pattern
            ]

            logger.info("Extracting showcase frames via FFmpeg (0~240s)...")
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            extracted_files = sorted(list(temp_path.glob("f_*.jpg")))
            if not extracted_files:
                logger.warning("FFmpeg frame extraction yielded no frames.")
                return []

            candidates = []
            for idx, f_file in enumerate(extracted_files):
                sec = idx * 1.5
                img = cv2.imread(str(f_file))
                if img is None:
                    continue

                # 고속 처리를 위해 480p 해상도로 축소하여 선명도 및 에지 계산
                small = cv2.resize(img, (480, 270))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
                sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

                # Deepwoken 스탯 UI 영역:
                # 1) 우측 스탯 패널 (x: 60%~98%, y: 4%~96%)
                h, w = gray.shape
                right_crop = gray[int(h*0.04):int(h*0.96), int(w*0.60):int(w*0.98)]
                right_edges = cv2.Canny(right_crop, 50, 150)
                right_edge_density = float(np.mean(right_edges))

                # 2) 전체 중앙/빌더 에지 밀도
                center_crop = gray[int(h*0.05):int(h*0.90), int(w*0.20):int(w*0.80)]
                center_edges = cv2.Canny(center_crop, 50, 150)
                center_edge_density = float(np.mean(center_edges))

                # 우측 스탯창이 활성화된 경우 가중치를 대폭 부여
                ui_score = right_edge_density * 4.0 + center_edge_density * 1.5 + min(sharpness, 400.0) * 0.1

                if sharpness >= min_sharpness:
                    candidates.append({
                        "timestamp_sec": sec,
                        "sharpness": sharpness,
                        "ui_score": ui_score,
                        "file_path": f_file
                    })

            if not candidates:
                logger.warning("No candidate passed sharpness threshold.")
                return []

            # UI 점수 순 정렬 후 시간 간격 3초 이상으로 분산 선별
            candidates.sort(key=lambda x: x["ui_score"], reverse=True)
            selected = []
            min_time_gap = 3.0

            for cand in candidates:
                t = cand["timestamp_sec"]
                if not any(abs(t - s["timestamp_sec"]) < min_time_gap for s in selected):
                    selected.append(cand)
                    if len(selected) >= max_keyframes:
                        break

            selected.sort(key=lambda x: x["timestamp_sec"])

            video_stem = video_path.stem
            saved_keyframes = []

            for rank, item in enumerate(selected):
                sec = item["timestamp_sec"]
                raw_path = self.output_dir / f"{video_stem}_kf{rank+1}_{int(sec)}s_raw.jpg"
                enhanced_path = self.output_dir / f"{video_stem}_kf{rank+1}_{int(sec)}s_enhanced.jpg"
                stat_crop_path = self.output_dir / f"{video_stem}_kf{rank+1}_{int(sec)}s_stat_crop.jpg"
                inv_crop_path = self.output_dir / f"{video_stem}_kf{rank+1}_{int(sec)}s_inv_crop.jpg"

                shutil.copy(item["file_path"], raw_path)

                # 원본 1080p 로드 및 ROI 크롭 생성
                img = cv2.imread(str(raw_path))
                ih, iw, _ = img.shape

                # 1) 우측 스탯 패널 크롭 (x: 62%~99%, y: 3%~97%) 및 1.5배 업스케일
                stat_crop = img[int(ih*0.03):int(ih*0.97), int(iw*0.62):int(iw*0.99)]
                if stat_crop.size > 0:
                    stat_crop_up = cv2.resize(stat_crop, (int(stat_crop.shape[1] * 1.5), int(stat_crop.shape[0] * 1.5)), interpolation=cv2.INTER_LANCZOS4)
                    cv2.imwrite(str(stat_crop_path), stat_crop_up, [cv2.IMWRITE_JPEG_QUALITY, 95])

                # 2) 좌측 인벤토리 크롭 (x: 3%~45%, y: 5%~95%)
                inv_crop = img[int(ih*0.05):int(ih*0.95), int(iw*0.03):int(iw*0.48)]
                if inv_crop.size > 0:
                    cv2.imwrite(str(inv_crop_path), inv_crop, [cv2.IMWRITE_JPEG_QUALITY, 95])

                # 3) OpenCV CLAHE 고대비 전처리 이미지
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                cv2.imwrite(str(enhanced_path), enhanced, [cv2.IMWRITE_JPEG_QUALITY, 95])

                saved_keyframes.append({
                    "rank": rank + 1,
                    "timestamp_sec": sec,
                    "sharpness": item["sharpness"],
                    "raw_path": raw_path,
                    "enhanced_path": enhanced_path,
                    "stat_crop_path": stat_crop_path if stat_crop_path.exists() else raw_path,
                    "inv_crop_path": inv_crop_path if inv_crop_path.exists() else raw_path
                })
                logger.info(f"⭐ [Keyframe #{rank+1}] At {sec:.1f}s (Sharpness: {item['sharpness']:.1f}, UI Score: {item['ui_score']:.1f}) -> {raw_path.name}")

            return saved_keyframes