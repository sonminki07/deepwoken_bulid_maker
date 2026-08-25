import os
import json
import unittest
from pathlib import Path

from agents.structurer import BuildStructurer
from agents.collector import VideoMetadata
from pipeline.orchestrator import PipelineOrchestrator

class TestPipelineComponents(unittest.TestCase):

    def setUp(self):
        self.sample_build_data = {
            "video_meta": {
                "title": "Unstoppable Thundercall Greatsword PvP Build",
                "channel": "DeepwokenMaster",
                "url": "https://www.youtube.com/watch?v=sample123",
                "upload_date": "20260101",
                "estimated_patch": "Verse 2"
            },
            "build_summary": {
                "build_name": "Thundercall Greatsword Destroyer",
                "build_type": "PvP",
                "difficulty": "Advanced",
                "creator_opinion": "Extremely high posture damage with massive CC combo.",
                "strengths": ["Huge damage per hit", "Instant stun with lightning"],
                "weaknesses": ["Slow swing speed", "Requires precise timing"]
            },
            "race": "Vesperian",
            "origin": "Castaway",
            "oath": "Jetstriker",
            "resonance": "Wind Up",
            "murmur": "Ardour",
            "stats": {
                "strength": 80,
                "fortitude": 50,
                "agility": 40,
                "intelligence": 0,
                "willpower": 25,
                "charisma": 0,
                "heavy_wep": 100,
                "medium_wep": 0,
                "light_wep": 0
            },
            "attunements": {
                "thundercall": 80,
                "flamecharm": 0,
                "frostdraw": 0,
                "galebreathe": 0,
                "shadowcast": 0,
                "ironsing": 0
            },
            "weapons": [
                {
                    "name": "Enforcer's Blade",
                    "type": "Greatsword",
                    "enchant": "Grim",
                    "stars": 3
                }
            ],
            "talents": [
                {
                    "name": "Showstopper",
                    "category": "Strength",
                    "is_core": True
                },
                {
                    "name": "Exoskeleton",
                    "category": "Fortitude",
                    "is_core": True
                }
            ],
            "mantras": [
                {
                    "name": "Lightning Cloak",
                    "attunement": "Thundercall",
                    "is_core": True,
                    "modifications": "Vibrant Gem x2"
                }
            ],
            "shrine_of_order_path": "Invest 40 STR, 40 FORT pre-shrine, then distribute to Thundercall & Heavy post-shrine.",
            "equipment": [
                {
                    "name": "Black Diver",
                    "slot": "Chest",
                    "pip_summary": "+15 HP, +6% DRL"
                }
            ],
            "combo_guide": "M1 -> Lightning Cloak -> Greatsword Critical -> Grand Javelin"
        }

    def test_structurer_validation_and_markdown(self):
        structurer = BuildStructurer(
            schema_path="config/build_schema.json",
            analysis_dir="data/test_analysis",
            knowledge_base_dir="data/test_kb"
        )
        # 1. Validation test
        is_valid = structurer.validate(self.sample_build_data)
        self.assertTrue(is_valid, "Sample build data should pass JSON schema validation")

        # 2. Markdown rendering test
        md_text = structurer.to_markdown(self.sample_build_data)
        self.assertIn("Thundercall Greatsword Destroyer", md_text)
        self.assertIn("Jetstriker", md_text)
        self.assertIn("Showstopper", md_text)
        self.assertIn("Lightning Cloak", md_text)

        # 3. File saving test
        paths = structurer.process_and_save(self.sample_build_data, "sample123")
        self.assertTrue(Path(paths["json_path"]).exists())
        self.assertTrue(Path(paths["md_path"]).exists())

        # Cleanup test files
        Path(paths["json_path"]).unlink(missing_ok=True)
        Path(paths["md_path"]).unlink(missing_ok=True)
        Path("data/test_analysis").rmdir()
        Path("data/test_kb").rmdir()

if __name__ == "__main__":
    unittest.main()
