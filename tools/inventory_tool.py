import json
from pathlib import Path
from typing import Optional, Dict

MOCK_PATH = Path(__file__).parent.parent / "data" / "mock_inventory.json"

def load_mock_inventory() -> list[Dict]:
    with open(MOCK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def check_inventory(product_name: str) -> Optional[Dict]:
    inventory = load_mock_inventory()
    for item in inventory:
        if item["name"].lower() == product_name.lower():
            return item
    return None
