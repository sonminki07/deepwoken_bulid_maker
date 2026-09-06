import os
import cv2
import shutil
import subprocess
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import imageio_ffmpeg

logger = logging.getLogger(__name__)

class MultiUIStatDetector:
    """인게임 Stat Sheet, deepwoken.co 웹 빌더, 커스텀 스탯 요약 카드 다중 UI 정밀 감지기"""

    @staticmethod
    def detect_ingame_hud(img: np.ndarray) -> float:
        """1. 인게임 기본 스탯창: 우측 중앙 스탯 원형 아이콘(BODY/MIND/ELEMENTS), Traits 및 Power 20 엠블럼"""
        try:
            h, w = img.shape[:2]

            # 1) 필수 게이트: 우측 상단 Power 20 엠블럼 (x: 70%~85%, y: 5%~25%)
            top_icon_area = img[int(h * 0.05):int(h * 0.25), int(w * 0.70):int(w * 0.85)]
            tia_hsv = cv2.cvtColor(top_icon_area, cv2.COLOR_BGR2HSV)
            blue_mask = cv2.inRange(tia_hsv, np.array([90, 70, 70]), np.array([130, 255, 255]))
            blue_pixels = int(np.count_nonzero(blue_mask))

            # 파란 픽셀이 딱 엠블럼 크기(250 ~ 8000)여야만 진짜 스탯창으로 인정 (없거나 너무 많으면 탈락)
            if not (250 <= blue_pixels <= 8000):
                return 0.0

            # 2) 우측 중앙 핵심 스탯 영역 (x: 70%~96%, y: 15%~60%) - BODY, WEAPONS, ELEMENTS
            stat_area = img[int(h * 0.15):int(h * 0.60), int(w * 0.70):int(w * 0.96)]
            sa_hsv = cv2.cvtColor(stat_area, cv2.COLOR_BGR2HSV)
            sa_gray = cv2.cvtColor(stat_area, cv2.COLOR_BGR2GRAY)

            # 스탯 원형 테두리 골드/황동 픽셀 (아이콘 적정 범위: 2,500 ~ 25,000)
            gold_mask = cv2.inRange(sa_hsv, np.array([12, 50, 50]), np.array([35, 255, 255]))
            gold_pixels = int(np.count_nonzero(gold_mask))
            if not (2000 <= gold_pixels <= 25000):
                return 0.0

            # 스탯 수치 및 라벨 텍스트 에지 밀도
            sa_edges = cv2.Canny(sa_gray, 50, 150)
            sa_edge_density = float(np.mean(sa_edges))
            if sa_edge_density < 16.0:
                return 0.0

            # 3) 우측 하단 STATS/RESISTANCES 세부 스탯 밀도 (x: 68%~99%, y: 70%~98%)
            bottom_right = img[int(h * 0.70):int(h * 0.98), int(w * 0.68):int(w * 0.99)]
            br_gray = cv2.cvtColor(bottom_right, cv2.COLOR_BGR2GRAY)
            br_edges = cv2.Canny(br_gray, 50, 150)
            br_edge_density = float(np.mean(br_edges))

            total_score = (blue_pixels * 10.0) + (gold_pixels * 2.0) + (sa_edge_density * 200.0) + (br_edge_density * 100.0)
            return float(total_score)
        except Exception:
            return 0.0

    @staticmethod
    def detect_builder_web(img: np.ndarray) -> float:
        """2. deepwoken.co 웹 빌더 화면: 다크 테마 배경(#0d0d12 ~ #1a1a24) + 중앙/전체 격자 구조 + 높은 텍스트 밀도"""
        try:
            h, w = img.shape[:2]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 다크 모드 특성 (평균 밝기가 어두움: 10 ~ 80)
            mean_brightness = float(np.mean(gray))
            if not (10 <= mean_brightness <= 80):
                return 0.0

            # 중앙/우측 스탯 박스들의 격자선 및 테이블 에지 검출
            center_area = gray[int(h * 0.15):int(h * 0.85), int(w * 0.15):int(w * 0.85)]
            edges = cv2.Canny(center_area, 40, 120)
            edge_density = float(np.mean(edges))

            # 수직/수평 선형 구조 검출 (웹 컴포넌트 박스)
            sobelx = cv2.Sobel(center_area, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(center_area, cv2.CV_64F, 0, 1, ksize=3)
            grid_score = float(np.mean(np.abs(sobelx)) + np.mean(np.abs(sobely)))

            if edge_density > 15.0 and grid_score > 25.0:
                return (edge_density * 3.5) + (grid_score * 1.5)
            return 0.0
        except Exception:
            return 0.0

    @staticmethod
    def detect_text_card(img: np.ndarray) -> float:
        """3. 편집자 커스텀 스탯 자막/카드 (중앙 반투명 박스 및 굵은 스탯 텍스트)"""
        try:
            h, w = img.shape[:2]
            center_rect = img[int(h * 0.20):int(h * 0.80), int(w * 0.20):int(w * 0.80)]
            cr_gray = cv2.cvtColor(center_rect, cv2.COLOR_BGR2GRAY)
            
            # 높은 선명도 및 텍스트 외곽선
            sharpness = float(cv2.Laplacian(cr_gray, cv2.CV_64F).var())
            edges = cv2.Canny(cr_gray, 50, 150)
            edge_density = float(np.mean(edges))

            if sharpness > 180.0 and edge_density > 12.0:
                return min(sharpness, 400.0) * 0.25 + (edge_density * 2.0)
            return 0.0
        except Exception:
            return 0.0

    @classmethod
    def evaluate_frame(cls, img: np.ndarray) -> Tuple[float, str]:
        """세 가지 UI 형태 중 가장 높은 점수와 UI 유형 반환"""
        s_hud = cls.detect_ingame_hud(img)
        s_builder = cls.detect_builder_web(img)
        s_card = cls.detect_text_card(img)

        best_score = max(s_hud, s_builder, s_card)
        if best_score == s_hud and s_hud > 0:
            return s_hud, "ingame_hud"
        elif best_score == s_builder and s_builder > 0:
            return s_builder, "builder_web"
        elif s_card > 0:
            return s_card, "text_card"
        return 0.0, "unknown"


class FrameExtractor:
    """FFmpeg + OpenCV 하이브리드 고밀도 2단계(Pre/Post) 스마트 프레임 추출기"""

    def __init__(self, output_dir: str = "data/keyframes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            self.ffmpeg_exe = "ffmpeg"

    def _get_video_duration(self, video_path: Path) -> float:
        """OpenCV로 비디오 총 길이 측정"""
        try:
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
            cap.release()
            if count > 0 and fps > 0:
                return count / fps
        except Exception:
            pass
        return 300.0

    def extract_dual_stage_keyframes(
        self,
        video_path: Path,
        max_pre_frames: int = 3,
        max_post_frames: int = 3,
        sample_interval_sec: float = 0.5,
        **kwargs
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        영상 전 구간을 1-Pass 고속 순차 스트리밍(Sequential Streaming)으로 스캔하여
        시킹(seeking) 데드락 없이 초고속으로
        영상 초반(0~45% Pre-Shrine)과 후반(55~100% Post-Shrine)의 최적 빌드 프레임을 독립 선별
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            logger.error(f"Cannot open video with OpenCV: {video_path}")
            return {"pre_shrine": [], "post_shrine": []}

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_dur = (total_frames / fps) if (fps > 0 and total_frames > 0) else self._get_video_duration(video_path)
        logger.info(f"🚀 [1-Pass Smart Stream Scan] Video: {video_path.name} ({total_dur:.1f}s, {fps:.0f}fps)")

        # 0.5초 간격 = fps * 0.5 프레임마다 retrieve 및 평가 (시킹 0회)
        step_frames = max(1, int(fps * sample_interval_sec))
        frame_idx = 0
        all_scored = []

        while True:
            ret = cap.grab()
            if not ret:
                break
            if frame_idx % step_frames == 0:
                ret, frame = cap.retrieve()
                if ret and frame is not None:
                    score, ui_type = MultiUIStatDetector.evaluate_frame(frame)
                    if score > 8.0:
                        t_sec = frame_idx / fps
                        all_scored.append({
                            "timestamp_sec": t_sec,
                            "score": score,
                            "ui_type": ui_type,
                            "frame": frame
                        })
            frame_idx += 1

        cap.release()
        logger.info(f"📊 [Stream Scan Complete] Evaluated {frame_idx} frames, found {len(all_scored)} candidate UI points.")

        # ----------------------------------------------------
        # Pre-Shrine(0~45%) vs Post-Shrine(55~100%) 버킷 분리
        # ----------------------------------------------------
        split_pre_boundary = total_dur * 0.45
        split_post_boundary = total_dur * 0.55

        pre_candidates = [f for f in all_scored if f["timestamp_sec"] <= split_pre_boundary]
        post_candidates = [f for f in all_scored if f["timestamp_sec"] >= split_post_boundary]

        # 점수 내림차순 정렬
        pre_candidates.sort(key=lambda x: x["score"], reverse=True)
        post_candidates.sort(key=lambda x: x["score"], reverse=True)

        def _select_top_distinct(candidates: List[Dict[str, Any]], max_count: int, stage_tag: str) -> List[Dict[str, Any]]:
            selected = []
            for item in candidates:
                if len(selected) >= max_count:
                    break
                # 시간 중복 방지 (최소 1.5초 간격)
                if any(abs(item["timestamp_sec"] - s["timestamp_sec"]) < 1.5 for s in selected):
                    continue

                t_sec = item["timestamp_sec"]
                img = item["frame"]
                h, w = img.shape[:2]

                # 1) 원본 프레임 저장
                raw_filename = f"{video_path.stem}_{stage_tag}_{int(t_sec)}s_raw.jpg"
                raw_path = self.output_dir / raw_filename
                cv2.imwrite(str(raw_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])

                # 2) 우측 스탯창 또는 중앙 패널 크롭 저장
                if item["ui_type"] == "ingame_hud":
                    # 우측 35% 영역 크롭
                    stat_crop = img[:, int(w * 0.65):]
                else:
                    # 중앙 80% 영역 크롭
                    stat_crop = img[int(h * 0.10):int(h * 0.90), int(w * 0.10):int(w * 0.90)]

                crop_filename = f"{video_path.stem}_{stage_tag}_{int(t_sec)}s_crop.jpg"
                crop_path = self.output_dir / crop_filename
                cv2.imwrite(str(crop_path), stat_crop, [cv2.IMWRITE_JPEG_QUALITY, 95])

                selected.append({
                    "timestamp_sec": t_sec,
                    "hud_score": item["score"],
                    "ui_type": item["ui_type"],
                    "stage": stage_tag,
                    "path": str(raw_path),
                    "raw_path": str(raw_path),
                    "stat_crop_path": str(crop_path)
                })
            return selected

        pre_selected = _select_top_distinct(pre_candidates, max_pre_frames, "pre_shrine")
        post_selected = _select_top_distinct(post_candidates, max_post_frames, "post_shrine")

        logger.info(f"🎯 [Selection Done] Pre-Shrine Frames: {len(pre_selected)} | Post-Shrine Frames: {len(post_selected)}")
        return {
            "pre_shrine": pre_selected,
            "post_shrine": post_selected
        }

    def extract_sharp_keyframes(
        self,
        video_path: Path,
        max_keyframes: int = 6,
        fps_step: float = 1.0,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """기존 파이프라인 호환용 (sample_step_sec 포함 모든 kwargs 지원 및 Pre/Post 프레임 종합 반환)"""
        coarse_step = kwargs.get("sample_step_sec", fps_step)
        dual = self.extract_dual_stage_keyframes(
            video_path=video_path,
            max_pre_frames=max(1, max_keyframes // 2),
            max_post_frames=max(1, max_keyframes // 2),
            coarse_step_sec=coarse_step
        )
        combined = dual.get("post_shrine", []) + dual.get("pre_shrine", [])
        combined.sort(key=lambda x: x.get("hud_score", 0), reverse=True)
        return combined[:max_keyframes]