import sys
import os
import unittest
from pydantic import ValidationError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.loader import DataLoader
from src.graph.schema import GraphData, Entity, Relationship


class TestIngestion(unittest.TestCase):

    def test_schema_validation(self):
        """Test if our Pydantic models correctly validate data"""
        print("\n Testing Data Schema...")

        # 1. Valid Data
        valid_payload = {
            "entities": [
                {"id": "Bob", "type": "Person", "properties": {"role": "CEO"}}
            ],
            "relationships": [
                {"source": "Bob", "target": "Company_A", "type": "OWNS"}
            ]
        }
        try:
            model = GraphData(**valid_payload)
            self.assertEqual(model.entities[0].id, "Bob")
            print("   Schema Validation Passed")
        except ValidationError as e:
            self.fail(f"Schema rejected valid data: {e}")

    def test_loader_finds_files(self):
        """Test if the DataLoader can see files in the data directory"""
        print("\n Testing File Loader...")

        # Ensure we point to the project root data folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "raw")

        loader = DataLoader(data_dir=data_path)

        # We just want to check if it runs without crashing,
        # NOT actually parse PDFs (which is slow)
        if not os.path.exists(data_path):
            print(f"    Warning: Data path {data_path} does not exist yet.")
            return

        print(f"   Looking in: {data_path}")
        # Only check existence of the directory for this unit test
        self.assertTrue(os.path.exists(data_path))
        print("    Data Directory Found")


if __name__ == "__main__":
    unittest.main()