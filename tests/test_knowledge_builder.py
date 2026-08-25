import os
import json
import shutil
import unittest
from pathlib import Path
from agents.knowledge_builder import KnowledgeBuilder

class TestKnowledgeBuilder(unittest.TestCase):

    def setUp(self):
        self.test_db_path = "data/test_chromadb"
        self.test_analysis_dir = Path("data/test_analysis")
        self.test_kb_dir = Path("data/test_kb")

        self.test_analysis_dir.mkdir(parents=True, exist_ok=True)
        self.test_kb_dir.mkdir(parents=True, exist_ok=True)

        self.sample_build = {
            "video_meta": {
                "title": "Flamecharm Voidwalker Test Build",
                "channel": "DeepwokenPro",
                "url": "https://www.youtube.com/watch?v=sample456",
                "upload_date": "20260201",
                "estimated_patch": "Verse 2"
            },
            "build_summary": {
                "build_name": "Flamecharm Voidwalker Burner",
                "build_type": "PvP",
                "difficulty": "Advanced",
                "creator_opinion": "High mobility fire combo.",
                "strengths": ["Burn damage", "Fast cast"],
                "weaknesses": ["Low defense"]
            },
            "oath": "Voidwalker",
            "stats": {"strength": 40, "fortitude": 40, "agility": 30, "intelligence": 0, "willpower": 20, "charisma": 0},
            "attunements": {"flamecharm": 80},
            "talents": [{"name": "Flame Within", "is_core": True}],
            "mantras": [{"name": "Fire Blade", "is_core": True}]
        }

        self.sample_md = """# ⚔️ Flamecharm Voidwalker Burner
> **출처 영상**: [Flamecharm Voidwalker Test Build](https://www.youtube.com/watch?v=sample456)
> **Oath**: Voidwalker | **타입**: PvP

## 📊 스탯 분배
| Stat | Value |
| Strength | 40 |
| Flamecharm | 80 |
"""
        self.json_path = self.test_analysis_dir / "sample456.json"
        self.json_path.write_text(json.dumps(self.sample_build), encoding="utf-8")
        self.md_path = self.test_kb_dir / "sample456.md"
        self.md_path.write_text(self.sample_md, encoding="utf-8")

    def test_chroma_ingest_and_query(self):
        # We test with use_gemini_embedding=False (fallback to default Chroma embedding function for offline test)
        kb = KnowledgeBuilder(
            db_path=self.test_db_path,
            collection_name="test_builds",
            use_gemini_embedding=False
        )

        kb.ingest_build("sample456", self.json_path, self.md_path)

        # Test query
        results = kb.query("Flamecharm PvP Voidwalker", n_results=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["metadata"]["build_name"], "Flamecharm Voidwalker Burner")
        self.assertEqual(results[0]["metadata"]["oath"], "Voidwalker")

    def tearDown(self):
        # Clean up test directories
        shutil.rmtree(self.test_db_path, ignore_errors=True)
        shutil.rmtree(str(self.test_analysis_dir), ignore_errors=True)
        shutil.rmtree(str(self.test_kb_dir), ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
