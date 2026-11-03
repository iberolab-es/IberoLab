"""The catalogue must reject data that could disguise undocumented analysis."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_academic_catalog import validate_data


class AcademicCatalogTest(unittest.TestCase):
    def setUp(self):
        self.seed = json.loads((ROOT / "data/corpus/attested-forms.v1.json").read_text())
        self.catalog = json.loads((ROOT / "data/corpus/academic-catalog.v1.json").read_text())

    def test_rejects_undocumented_segmentation(self):
        self.catalog["entries"][0]["linguistic_segmentation"]["segments"] = ["inventado"]
        with self.assertRaisesRegex(ValueError, "specialist review"):
            validate_data(self.seed, self.catalog)

    def test_rejects_fictitious_complete_text_count(self):
        self.catalog["complete_inscription_editions"] = 11
        with self.assertRaisesRegex(ValueError, "complete editions"):
            validate_data(self.seed, self.catalog)

    def test_rejects_invented_archaeological_identifier(self):
        self.catalog["entries"][0]["provenance"]["object_identifier"] = "fictional-id"
        with self.assertRaisesRegex(ValueError, "do not invent"):
            validate_data(self.seed, self.catalog)

    def test_rejects_duplicate_entry(self):
        self.catalog["entries"].append(copy.deepcopy(self.catalog["entries"][0]))
        with self.assertRaisesRegex(ValueError, "exactly once"):
            validate_data(self.seed, self.catalog)

    def test_rejects_missing_source_coverage(self):
        self.catalog["entries"].pop()
        with self.assertRaisesRegex(ValueError, "exactly once"):
            validate_data(self.seed, self.catalog)


if __name__ == "__main__":
    unittest.main()
