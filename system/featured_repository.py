import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURED_PATH = os.path.join(BASE_DIR, "db", "featured_products.json")

def get_all_featured():
    try:
        with open(FEATURED_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
