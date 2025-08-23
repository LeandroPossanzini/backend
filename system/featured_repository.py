import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURED_FILE = os.path.join(BASE_DIR, "db", "featured_products.json")

def get_all_featured() -> list:
    try:
        with open(FEATURED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_featured(products: list):
    os.makedirs(os.path.dirname(FEATURED_FILE), exist_ok=True)
    with open(FEATURED_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)

def update_featured(article_id: str, new_data: dict) -> bool:
    featured = get_all_featured()
    updated = False
    for product in featured:
        if str(product.get("id")) == str(article_id):
            product.update(new_data)
            updated = True
            break
    if updated:
        save_featured(featured)
    return updated

def delete_featured_system(article_id: str) -> bool:
    featured = get_all_featured()
    new_featured = [p for p in featured if str(p.get("id")) != str(article_id)]

    if len(new_featured) == len(featured):
        return False 

    save_featured(new_featured)
    return True
