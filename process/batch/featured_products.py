import json
import os
import time

RECURRENCY = 2  # minutos entre ejecuciones

# Paths
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
        print(f"File not found: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {path}: {e}")
        return []


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_processed_ids():
    if not os.path.exists(PROCESSED_IDS_PATH):
        return set()
    with open(PROCESSED_IDS_PATH, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)


def save_processed_ids(ids):
    with open(PROCESSED_IDS_PATH, "a", encoding="utf-8") as f:
        for _id in ids:
            f.write(f"{_id}\n")


def save_featured(top5):
    if not top5:
        print("No new Platinum products found. Featured products not updated.")
        return
    save_json(FEATURED_PATH, top5)
    print(f"Featured products updated: {FEATURED_PATH}")


def generate_category_files(new_products):
    for product in new_products:
        category = product.get("additional_details", {}).get("category", "uncategorized").lower()
        category_file = os.path.join(CATEGORIES_DIR, f"{category}.json")

        existing = load_json(category_file)
        # Evitar duplicados por ID en categoría
        existing_dict = {p.get("id"): p for p in existing}
        existing_dict[product.get("id")] = product
        save_json(category_file, list(existing_dict.values()))

        print(f"Product {product['id']} added to category '{category}'.")



def generate_featured_batch():
    print("Starting featured products batch...")

    products = load_json(ARTICLES_PATH)
    if not products:
        return

    processed_ids = load_processed_ids()

    # Only new products
    new_products = [p for p in products if p.get("id") not in processed_ids]
    if not new_products:
        print("No new products to process.")
        return

    # Load current featured products
    featured_current = load_json(FEATURED_PATH)

    # Combine current + new but avoid duplicates by ID
    combined_dict = {p.get("id"): p for p in featured_current}  # start with current
    for p in new_products:
        combined_dict[p.get("id")] = p  # overwrite or add

    combined = list(combined_dict.values())

    # Filter Platinum sellers safely
    platinum = [
        p for p in combined
        if p.get("seller", {}).get("reputation") == "Platinum"
    ]

    # Sort by number of reviews descending
    platinum.sort(key=lambda x: x.get("additional_details", {}).get("reviews", 0), reverse=True)

    # Keep top 5
    top5 = platinum[:5]

    # Save featured
    save_featured(top5)

    # Save category files
    generate_category_files(new_products)

    # Save processed IDs
    new_ids = [p.get("id") for p in new_products if p.get("id")]
    save_processed_ids(new_ids)

    print(f"Batch completed. Processed {len(new_ids)} new products.")



if __name__ == "__main__":
    while True:
        generate_featured_batch()
        print(f"Waiting {RECURRENCY} minutes for next run...\n")
        time.sleep(RECURRENCY * 60)
