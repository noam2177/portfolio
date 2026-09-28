import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from register import render, upsert


class RegisterTests(unittest.TestCase):
    def test_new_id_is_appended_once(self) -> None:
        rows = upsert({"id": "burrow-sniper", "title": "בור-צלף", "stage": "פתוח"}, [])
        again = upsert({"id": "burrow-sniper", "title": "בור-צלף", "stage": "שלב 2"}, rows)
        self.assertEqual(len(again), 1)
        self.assertEqual(again[0]["stage"], "שלב 2")

    def test_table_names_the_project(self) -> None:
        text = render([{"id": "burrow-sniper", "title": "בור-צלף", "stage": "ירי", "next": "סיבוב"}])
        self.assertIn("burrow-sniper", text)
        self.assertIn("בור-צלף", text)


if __name__ == "__main__":
    unittest.main()
