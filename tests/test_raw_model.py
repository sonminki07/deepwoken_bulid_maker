"""Unit tests for RawBuildData and BuildDataReconciler."""

import json
import unittest
from typing import Dict, Any

from agents.raw_build_model import RawBuildData, BuildDataReconciler
from agents.structurer import BuildStructurer


class TestRawBuildModel(unittest.TestCase):
    """RawBuildData 및 BuildDataReconciler 단위 테스트 모음"""

    def setUp(self):
        self.reconciler = BuildDataReconciler()
        self.structurer = BuildStructurer()

    def test_raw_build_data_creation_and_serialization(self):
        """RawBuildData 생성, to_dict, to_json, from_dict 라운드트립 검증"""
        raw = RawBuildData(
            video_id="test_vid_123",
            video_meta={
                "title": "Deepwoken PvE Boss Melter Build",
                "channel": "DeepwokenPro",
                "url": "https://www.youtube.com/watch?v=test_vid_123",
                "upload_date": "20260201",
                "estimated_patch": "Verse 3"
            },
            pre_shrine_raw={
                "stats": {"strength": 40, "fortitude": 50, "agility": 25, "willpower": 40, "charisma": 25},
                "traits": {"vitality": 6, "erudition": 6, "proficiency": 0, "songchant": 0},
            },
            post_shrine_raw={
                "stats": {"strength": 25, "fortitude": 30, "agility": 25, "willpower": 25, "charisma": 25, "heavy_wep": 100},
                "attunements": {"frostdraw": 100},
                "combat_stats": {"hp": 520, "posture": 35},
                "resistances": {"physical_blunt": "35.0%", "physical_slash": "35.0%"},
                "power": 20,
                "race": "Canor",
                "origin": "Castaway",
                "oath": "Silentheart"
            },
            builder_scraped={
                "talents": [{"name": "Brick Wall", "is_core": True}, "Conditioned Runner"],
                "mantras": []
            },
            vlm_narrative={
                "build_summary": {
                    "build_name": "Ultimate Frost Knight",
                    "build_type": "PvE",
                    "difficulty": "Intermediate",
                    "creator_opinion": "High survivability and boss shredding DPS.",
                    "strengths": ["Huge damage"],
                    "weaknesses": ["Slow startup"]
                },
                "combo_guide": "Use heavy slash then frost mantra."
            },
            captured_keyframes=[
                {"timestamp_sec": 42.5, "score": 98.2, "panel": "stat_sheet"},
                {"timestamp_sec": 115.0, "score": 95.0, "panel": "talents"}
            ]
        )

        # 1. to_dict 검증
        data_dict = raw.to_dict()
        self.assertEqual(data_dict["video_id"], "test_vid_123")
        self.assertEqual(data_dict["video_meta"]["channel"], "DeepwokenPro")
        self.assertEqual(len(data_dict["captured_keyframes"]), 2)
        self.assertEqual(data_dict["pre_shrine_raw"]["stats"]["strength"], 40)

        # 2. to_json 직렬화 검증
        json_str = raw.to_json()
        self.assertIsInstance(json_str, str)
        parsed_json = json.loads(json_str)
        self.assertEqual(parsed_json["video_id"], "test_vid_123")

        # 3. from_dict 역직렬화 라운드트립 검증
        restored = RawBuildData.from_dict(data_dict)
        self.assertEqual(restored.video_id, raw.video_id)
        self.assertEqual(restored.video_meta, raw.video_meta)
        self.assertEqual(restored.pre_shrine_raw, raw.pre_shrine_raw)
        self.assertEqual(restored.post_shrine_raw, raw.post_shrine_raw)
        self.assertEqual(restored.builder_scraped, raw.builder_scraped)
        self.assertEqual(restored.vlm_narrative, raw.vlm_narrative)
        self.assertEqual(len(restored.captured_keyframes), 2)

    def test_reconciler_priority_1_vision_overrides_all(self):
        """1순위 비전/OCR 실측 데이터가 빌더 및 VLM 데이터를 100% 오버라이드하는지 검증"""
        raw = RawBuildData(
            video_id="prio_test_1",
            video_meta={"title": "Priority Test Build", "channel": "DeepwokenHero", "url": "http://x"},
            post_shrine_raw={
                "stats": {"strength": 40, "fortitude": 50, "agility": 25, "intelligence": 0, "willpower": 40, "charisma": 25, "heavy_wep": 90},
                "attunements": {"ironsing": 60},
                "oath": "Starkindred",
                "race": "Gremor",
                "combat_stats": {"hp": 540, "posture": 32},
                "resistances": {"physical_blunt": "40.0%"}
            },
            builder_scraped={
                "stats": {"strength": 99, "fortitude": 99, "heavy_wep": 50},  # 왜곡 데이터
                "attunements": {"flamecharm": 80},
                "oath": "WrongOath"
            },
            vlm_narrative={
                "stats": {"strength": 10, "fortitude": 10},  # VLM 환각
                "oath": "AnotherWrongOath"
            }
        )

        reconciled = self.reconciler.reconcile(raw)

        # 비전 실측치가 최우선 적용되었는지 확인
        self.assertEqual(reconciled["_stats_source"], "vision_post_shrine")
        self.assertEqual(reconciled["stats"]["strength"], 40)
        self.assertEqual(reconciled["stats"]["fortitude"], 50)
        self.assertEqual(reconciled["stats"]["heavy_wep"], 90)
        self.assertEqual(reconciled["attunements"]["ironsing"], 60)
        self.assertEqual(reconciled["attunements"]["flamecharm"], 0)
        self.assertEqual(reconciled["oath"], "Starkindred")
        self.assertEqual(reconciled["race"], "Gremor")
        self.assertEqual(reconciled["combat_stats"]["hp"], 540)
        self.assertEqual(reconciled["resistances"]["physical_blunt"], "40.0%")

    def test_reconciler_priority_2_fallback_to_builder(self):
        """비전 데이터가 없을 때 2순위인 deepwoken.co 빌더 데이터가 채택되는지 검증"""
        raw = RawBuildData(
            video_id="prio_test_2",
            video_meta={"title": "Builder Fallback Build", "channel": "BuilderFan", "url": "http://x"},
            post_shrine_raw=None,  # 비전 데이터 없음
            builder_scraped={
                "stats": {"strength": 50, "fortitude": 50, "agility": 30, "intelligence": 0, "willpower": 40, "charisma": 20, "medium_wep": 100},
                "attunements": {"thundercall": 40},
                "oath": "Jetstriker",
                "talents": [{"name": "Speed Demon", "is_core": True}]
            },
            vlm_narrative={
                "stats": {"strength": 15, "fortitude": 15},  # 3순위 VLM
                "oath": "VLM_Oath"
            }
        )

        reconciled = self.reconciler.reconcile(raw)
        self.assertEqual(reconciled["_stats_source"], "builder_scraped")
        self.assertEqual(reconciled["stats"]["strength"], 50)
        self.assertEqual(reconciled["stats"]["medium_wep"], 100)
        self.assertEqual(reconciled["attunements"]["thundercall"], 40)
        self.assertEqual(reconciled["oath"], "Jetstriker")

    def test_reconciler_priority_3_fallback_to_vlm(self):
        """비전 및 빌더 데이터가 모두 없을 때 3순위 VLM 서술 데이터가 채택되는지 검증"""
        raw = RawBuildData(
            video_id="prio_test_3",
            video_meta={"title": "VLM Fallback Build", "channel": "VLMFan", "url": "http://x"},
            post_shrine_raw=None,
            builder_scraped=None,
            vlm_narrative={
                "stats": {"strength": 25, "fortitude": 40, "agility": 25, "intelligence": 40, "willpower": 20, "charisma": 20, "light_wep": 80},
                "attunements": {"shadowcast": 80},
                "oath": "Blindseer"
            }
        )

        reconciled = self.reconciler.reconcile(raw)
        self.assertEqual(reconciled["_stats_source"], "vlm_narrative")
        self.assertEqual(reconciled["stats"]["strength"], 25)
        self.assertEqual(reconciled["stats"]["light_wep"], 80)
        self.assertEqual(reconciled["attunements"]["shadowcast"], 80)
        self.assertEqual(reconciled["oath"], "Blindseer")

    def test_reconciler_330pt_integrity_exact(self):
        """330 포인트 무결성 검증 - 정확히 330pt인 경우 EXACT_330 확인"""
        # STR 40 + FTD 50 + AGL 25 + INT 0 + WLL 40 + CHA 25 = 180
        # Heavy 90
        # Ironsing 60
        # Total = 180 + 90 + 60 = 330
        raw = RawBuildData(
            video_id="cap_330_exact",
            video_meta={"title": "Exact 330 Build", "channel": "Pro", "url": "http://x"},
            post_shrine_raw={
                "stats": {
                    "strength": 40,
                    "fortitude": 50,
                    "agility": 25,
                    "intelligence": 0,
                    "willpower": 40,
                    "charisma": 25,
                    "heavy_wep": 90,
                    "medium_wep": 0,
                    "light_wep": 0
                },
                "attunements": {
                    "ironsing": 60,
                    "flamecharm": 0
                }
            }
        )

        reconciled = self.reconciler.reconcile(raw)
        val = reconciled["_stat_validation"]

        self.assertEqual(val["total_points"], 330)
        self.assertEqual(val["target_cap"], 330)
        self.assertEqual(val["difference"], 0)
        self.assertTrue(val["is_valid_330_cap"])
        self.assertEqual(val["status"], "EXACT_330")
        self.assertEqual(val["breakdown"]["core_attributes"], 180)
        self.assertEqual(val["breakdown"]["weapon_attributes"], 90)
        self.assertEqual(val["breakdown"]["attunements"], 60)

    def test_reconciler_330pt_integrity_below_and_over_cap(self):
        """330 포인트 상한 미달(BELOW_CAP) 및 초과(OVER_CAP) 상태 감지 검증"""
        # 1. 미달 케이스 (총 250pt)
        raw_below = RawBuildData(
            video_id="cap_below",
            video_meta={"title": "Below Cap", "channel": "X", "url": "http://x"},
            post_shrine_raw={
                "stats": {"strength": 25, "fortitude": 25, "agility": 25, "intelligence": 25, "willpower": 25, "charisma": 25, "medium_wep": 50},
                "attunements": {"galebreathe": 50}
            }
        )
        rec_below = self.reconciler.reconcile(raw_below)
        val_below = rec_below["_stat_validation"]
        self.assertEqual(val_below["total_points"], 250)
        self.assertEqual(val_below["difference"], -80)
        self.assertFalse(val_below["is_valid_330_cap"])
        self.assertEqual(val_below["status"], "BELOW_CAP")

        # 2. 초과 케이스 (총 350pt)
        raw_over = RawBuildData(
            video_id="cap_over",
            video_meta={"title": "Over Cap", "channel": "X", "url": "http://x"},
            post_shrine_raw={
                "stats": {"strength": 50, "fortitude": 50, "agility": 50, "intelligence": 50, "willpower": 50, "charisma": 50, "heavy_wep": 50},
                "attunements": {"shadowcast": 0}
            }
        )
        rec_over = self.reconciler.reconcile(raw_over)
        val_over = rec_over["_stat_validation"]
        self.assertEqual(val_over["total_points"], 350)
        self.assertEqual(val_over["difference"], 20)
        self.assertFalse(val_over["is_valid_330_cap"])
        self.assertEqual(val_over["status"], "OVER_CAP")

    def test_reconciler_shrine_build_detection_and_pre_post_separation(self):
        """Pre-Shrine과 Post-Shrine 스탯 분리 및 is_shrine_build True 판정 검증"""
        raw = RawBuildData(
            video_id="shrine_build_1",
            video_meta={"title": "Pre/Post Shrine Test Build", "channel": "ShrineMaster", "url": "http://x"},
            # 전반부 추출: 선행 탤런트(Brick Wall, Reinforce 등) 확보를 위한 Pre-Shrine 몰빵 스탯
            pre_shrine_raw={
                "stats": {
                    "strength": 40,
                    "fortitude": 90,
                    "agility": 25,
                    "intelligence": 0,
                    "willpower": 45,
                    "charisma": 0
                }
            },
            # 후반부 추출: 질서의 성소 이후 최종 완성 330pt 스탯
            post_shrine_raw={
                "stats": {
                    "strength": 25,
                    "fortitude": 30,
                    "agility": 25,
                    "intelligence": 0,
                    "willpower": 25,
                    "charisma": 25,
                    "heavy_wep": 100
                },
                "attunements": {
                    "frostdraw": 100
                }
            },
            vlm_narrative={
                "shrine_progression": {
                    "pre_shrine_talents": ["Brick Wall", "Reinforce", "Conditioned Runner"],
                    "post_shrine_priority": ["Frostdraw 100 마스터", "Heavy Weapon 100 달성"]
                }
            }
        )

        reconciled = self.reconciler.reconcile(raw)

        # 사원 빌드 플래그 검증
        self.assertTrue(reconciled["is_shrine_build"])
        sop = reconciled["shrine_progression"]
        self.assertTrue(sop["is_shrine_build"])

        # Pre-Shrine 스탯 분리 검증
        self.assertEqual(sop["pre_shrine"]["fortitude"], 90)
        self.assertEqual(sop["pre_shrine"]["willpower"], 45)
        self.assertEqual(len(sop["pre_shrine_talents"]), 3)
        self.assertIn("Brick Wall", sop["pre_shrine_talents"])

        # Post-Shrine 최종 완성 스탯 검증 (Fortitude는 30으로 정합)
        self.assertEqual(reconciled["stats"]["fortitude"], 30)
        self.assertEqual(reconciled["stats"]["heavy_wep"], 100)
        self.assertEqual(reconciled["attunements"]["frostdraw"], 100)

        # shrine_of_order_path 문자열 확인
        self.assertIn("Pre-Shrine", reconciled["shrine_of_order_path"])
        self.assertIn("Frostdraw 100 마스터", reconciled["shrine_of_order_path"])

    def test_reconciler_single_build_when_no_pre_shrine(self):
        """Pre-Shrine 스탯이 없을 때 is_shrine_build False 및 단일 빌드 처리 검증"""
        raw = RawBuildData(
            video_id="single_build_1",
            video_meta={"title": "Non-Shrine Straight Build", "channel": "PureBuilder", "url": "http://x"},
            pre_shrine_raw=None,
            post_shrine_raw={
                "stats": {"strength": 100, "fortitude": 100, "agility": 30, "heavy_wep": 100},
                "attunements": {}
            }
        )

        reconciled = self.reconciler.reconcile(raw)
        self.assertFalse(reconciled["is_shrine_build"])
        self.assertFalse(reconciled["shrine_progression"]["is_shrine_build"])
        self.assertEqual(reconciled["shrine_progression"]["pre_shrine"], {})
        self.assertEqual(reconciled["shrine_of_order_path"], "")

    def test_raw_source_data_complete_preservation(self):
        """원본 데이터가 _raw_source_data 키에 100% 무손실 보존되는지 검증"""
        keyframes = [
            {"timestamp_sec": 12.3, "sharpness": 88.5, "bbox": [10, 20, 100, 200]},
            {"timestamp_sec": 55.1, "sharpness": 91.2, "bbox": [50, 60, 300, 400]}
        ]
        raw = RawBuildData(
            video_id="audit_check_id",
            video_meta={"title": "Audit Test", "channel": "Auditor", "url": "http://youtube.com/audit"},
            captured_keyframes=keyframes,
            builder_scraped={"deepwoken_co_url": "https://deepwoken.co/builder?id=xyz123"}
        )

        reconciled = self.reconciler.reconcile(raw)

        # _raw_source_data 보존 확인
        self.assertIn("_raw_source_data", reconciled)
        raw_source = reconciled["_raw_source_data"]
        self.assertEqual(raw_source["video_id"], "audit_check_id")
        self.assertEqual(raw_source["video_meta"]["title"], "Audit Test")
        self.assertEqual(raw_source["captured_keyframes"], keyframes)
        self.assertEqual(raw_source["builder_scraped"]["deepwoken_co_url"], "https://deepwoken.co/builder?id=xyz123")

    def test_integration_with_build_structurer(self):
        """BuildDataReconciler의 출력 결과가 structurer.py의 sanitize 및 to_markdown과 완벽히 연동되는지 검증"""
        raw = RawBuildData(
            video_id="structurer_compat",
            video_meta={
                "title": "Silentheart Canor Heavy PvP Build",
                "channel": "PvpMaster",
                "url": "https://www.youtube.com/watch?v=structurer_compat",
                "upload_date": "20260210",
                "estimated_patch": "Verse 3"
            },
            pre_shrine_raw={
                "stats": {"strength": 40, "fortitude": 50, "agility": 25, "willpower": 40, "charisma": 25}
            },
            post_shrine_raw={
                "stats": {"strength": 40, "fortitude": 50, "agility": 25, "intelligence": 0, "willpower": 40, "charisma": 25, "heavy_wep": 90},
                "attunements": {"ironsing": 60},
                "power": 20,
                "oath": "Silentheart",
                "race": "Canor",
                "origin": "Castaway",
                "traits": {"vitality": 6, "erudition": 6, "proficiency": 0, "songchant": 0},
                "combat_stats": {"hp": 530, "posture": 32, "move_speed_pct": "-10.0%", "pve_dmg_pct": "+15.0%"},
                "resistances": {"physical_blunt": "45.0%", "physical_slash": "40.0%"}
            },
            builder_scraped={
                "weapons": [{"name": "Enforcer's Blade", "type": "Greatsword", "enchant": "Grim", "stars": 3}],
                "equipment": [{"slot": "Outfit", "name": "Deepwoken Cloak"}],
                "talents": [{"name": "Underdog", "category": "Willpower", "is_core": True}]
            },
            vlm_narrative={
                "build_summary": {
                    "build_name": "Canor Heavy Destroyer",
                    "build_type": "PvP",
                    "difficulty": "Advanced",
                    "creator_opinion": "Extremely tanky heavy build that shuts down mantras.",
                    "strengths": ["Huge damage resistance"],
                    "weaknesses": ["No mantras"]
                },
                "shrine_progression": {
                    "pre_shrine_talents": ["Reinforce", "Underdog"],
                    "post_shrine_priority": ["Heavy Weapon 90", "Ironsing 60"]
                },
                "combo_guide": "Catch with ankle cutter then heavy swing."
            }
        )

        reconciled = self.reconciler.reconcile(raw)

        # 1. structurer.py sanitize 검증
        sanitized = self.structurer.sanitize(reconciled)
        self.assertIsInstance(sanitized, dict)
        self.assertEqual(sanitized["stats"]["strength"], 40)
        self.assertEqual(sanitized["stats"]["heavy_wep"], 90)
        self.assertEqual(sanitized["attunements"]["ironsing"], 60)
        self.assertEqual(sanitized["oath"], "Silentheart")

        # 2. structurer.py to_markdown 검증
        markdown_text = self.structurer.to_markdown(sanitized)
        self.assertIsInstance(markdown_text, str)
        self.assertIn("# ⚔️ Canor Heavy Destroyer", markdown_text)
        self.assertIn("Silentheart", markdown_text)
        self.assertIn("질서의 성소 전", markdown_text)
        self.assertIn("질서의 성소 후", markdown_text)
        self.assertIn("100% 실측 원시 데이터", markdown_text)


if __name__ == "__main__":
    unittest.main()
