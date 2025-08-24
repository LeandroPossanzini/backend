import json
import os
import time
import logging

RECURRENCY = 2  # minutos entre ejecuciones

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
ARTICLES_PATH = os.path.join(BASE_DIR, "db", "articles.json")
FEATURED_PATH = os.path.join(BASE_DIR, "db", "featured_products.json")
PROCESSED_IDS_PATH = os.path.join(BASE_DIR, "db", "processed_ids.txt")
CATEGORIES_DIR = os.path.join(BASE_DIR, "db", "categories")
os.makedirs(CATEGORIES_DIR, exist_ok=True)

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"File not found: {path}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing {path}: {e}")
        return []

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Data saved to {path}")
    except Exception as e:
        logging.error(f"Error saving {path}: {e}")

def load_processed_ids():
    if not os.path.exists(PROCESSED_IDS_PATH):
        return set()
    try:
        with open(PROCESSED_IDS_PATH, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except Exception as e:
        logging.error(f"Error loading processed IDs: {e}")
        return set()

def save_processed_ids(ids):
    try:
        with open(PROCESSED_IDS_PATH, "a", encoding="utf-8") as f:
            for _id in ids:
                f.write(f"{_id}\n")
        logging.info(f"Processed IDs saved: {len(ids)}")
    except Exception as e:
        logging.error(f"Error saving processed IDs: {e}")

def save_featured(top5):
    if not top5:
        logging.info("No new Platinum products found. Featured products not updated.")
        return
    save_json(FEATURED_PATH, top5)
    logging.info(f"Featured products updated: {FEATURED_PATH}")

def generate_category_files(new_products):
    for product in new_products:
        category = product.get("additional_details", {}).get("category", "uncategorized").lower()
        category_file = os.path.join(CATEGORIES_DIR, f"{category}.json")

        existing = load_json(category_file)
        existing_dict = {p.get("id"): p for p in existing}
        existing_dict[product.get("id")] = product
        save_json(category_file, list(existing_dict.values()))

        logging.info(f"Product {product['id']} added to category '{category}'.")

def generate_featured_batch():
    logging.info("Starting featured products batch...")

    products = load_json(ARTICLES_PATH)
    if not products:
        logging.warning("No products found to process.")
        return

    processed_ids = load_processed_ids()
    new_products = [p for p in products if p.get("id") not in processed_ids]
    if not new_products:
        logging.info("No new products to process.")
        return

    featured_current = load_json(FEATURED_PATH)
    combined_dict = {p.get("id"): p for p in featured_current}
    for p in new_products:
        combined_dict[p.get("id")] = p

    combined = list(combined_dict.values())
    platinum = [
        p for p in combined
        if p.get("seller", {}).get("reputation") == "Platinum"
    ]
    platinum.sort(key=lambda x: x.get("additional_details", {}).get("reviews", 0), reverse=True)
    top5 = platinum[:5]

    save_featured(top5)
    generate_category_files(new_products)
    new_ids = [p.get("id") for p in new_products if p.get("id")]
    save_processed_ids(new_ids)

    logging.info(f"Batch completed. Processed {len(new_ids)} new products.")

if __name__ == "__main__":
    while True:
        try:
            generate_featured_batch()
        except Exception as e:
            logging.error(f"Error in batch execution: {e}")
        logging.info(f"Waiting {RECURRENCY} minutes for next run...\n")
        time.sleep(RECURRENCY * 60)