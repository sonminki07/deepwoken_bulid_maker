import unittest
from agents.web_scraper import ScrapedWebContent
from agents.subagents.validator import CrossValidatorAgent

class TestWebPipeline(unittest.TestCase):

    def setUp(self):
        self.scraped = ScrapedWebContent(
            url="https://deepwoken.fandom.com/wiki/Builds/TestBuild",
            title="Thundercall Jetstriker Speedster Build",
            doc_id="web_123456789abc",
            meta_description="A fast-paced Thundercall PvP build utilizing Jetstriker oath.",
            cleaned_text="Deepwoken build guide for high mobility PvP.",
            tables_text="Stat | Value\nStrength | 80\nFortitude | 50\nThundercall | 80"
        )
        self.build_mechanics = {
            "stats": {"strength": 80, "fortitude": 50, "agility": 40, "intelligence": 0, "willpower": 25, "charisma": 0},
            "attunements": {"thundercall": 80},
            "oath": "Jetstriker",
            "weapons": [{"name": "Curved Blade of Winds", "type": "Medium", "enchant": "Storm", "stars": 2}],
            "talents": [{"name": "Showstopper", "is_core": True}],
            "mantras": [{"name": "Lightning Cloak", "attunement": "Thundercall", "is_core": True}]
        }
        self.context_data = {
            "build_name": "Thundercall Jetstriker Speedster",
            "build_type": "PvP",
            "difficulty": "Advanced",
            "creator_opinion": "Exceptional gap closer with fast combo reset.",
            "strengths": ["Extreme agility", "High pressure"],
            "weaknesses": ["Vulnerable to counter"],
            "combo_guide": "Slide -> M1 -> Lightning Cloak -> Mantra",
            "author": "Deepwoken Wiki Contributor",
            "estimated_patch": "Verse 2"
        }

    def test_cross_validator(self):
        validator = CrossValidatorAgent()
        merged = validator.validate_and_merge(self.scraped, self.build_mechanics, self.context_data)

        self.assertEqual(merged["build_summary"]["build_name"], "Thundercall Jetstriker Speedster")
        self.assertEqual(merged["build_summary"]["build_type"], "PvP")
        self.assertEqual(merged["oath"], "Jetstriker")
        self.assertEqual(merged["stats"]["strength"], 80)
        self.assertEqual(merged["attunements"]["thundercall"], 80)
        self.assertEqual(len(merged["talents"]), 1)
        self.assertEqual(len(merged["mantras"]), 1)
        self.assertEqual(merged["video_meta"]["channel"], "Deepwoken Wiki Contributor")

if __name__ == "__main__":
    unittest.main()
