import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURED_FILE = os.path.join(BASE_DIR, "db", "featured_products.json")

def get_all_featured() -> list:
    try:
        with open(FEATURED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Error leyendo productos destacados: {e}")
        return []

def save_featured(products: list):
    os.makedirs(os.path.dirname(FEATURED_FILE), exist_ok=True)
    try:
        with open(FEATURED_FILE, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)
    except Exception as e:
        logging.error(f"Error guardando productos destacados: {e}")

def update_featured(article_id: str, new_data: dict) -> bool:
    try:
        featured = get_all_featured()
        updated = False
        for product in featured:
            if str(product.get("id")) == str(article_id):
                product.update(new_data)
                updated = True
                break
        if updated:
            save_featured(featured)
            logging.info(f"Producto destacado actualizado: {article_id}")
        else:
            logging.warning(f"Producto destacado no encontrado para actualizar: {article_id}")
        return updated
    except Exception as e:
        logging.error(f"Error actualizando producto destacado {article_id}: {e}")
        return False

def delete_featured_system(article_id: str) -> bool:
    try:
        featured = get_all_featured()
        new_featured = [p for p in featured if str(p.get("id")) != str(article_id)]

        if len(new_featured) == len(featured):
            logging.warning(f"Producto destacado no encontrado para eliminar: {article_id}")
            return False 

        save_featured(new_featured)
        logging.info(f"Producto destacado eliminado: {article_id}")
        return True
    except Exception as e:
        logging.error(f"Error eliminando producto destacado {article_id}: {e}")
        return False