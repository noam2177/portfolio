import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from register import assert_admissible, render, upsert, upsert_tracker


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

    def test_tracker_block_refreshes_the_same_id(self) -> None:
        row = {"id": "hybrid-cloud-bus", "title": "אוטובוס", "stage": "שלב א", "next": "צעד א", "path": "D:\\hub"}
        first = upsert_tracker("# מעקב\n", row)
        second = upsert_tracker(first, {**row, "stage": "שלב ב", "next": "צעד ב"})
        self.assertEqual(second.count("<!-- project:hybrid-cloud-bus -->"), 1)
        self.assertIn("שלב ב", second)
        self.assertNotIn("שלב א", second)

    def test_office_paths_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            assert_admissible({"id": "notes", "path": r"C:\Desktop\sagole\client", "title": "x"})


if __name__ == "__main__":
    unittest.main()
