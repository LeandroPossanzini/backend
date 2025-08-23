import json
import os
import time
import sys



RECURRENCY = 2  # minutos entre ejecuciones

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Subo dos niveles: batch -> process -> raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
ARTICULOS_PATH = os.path.join(BASE_DIR, "db", "articles.json")
DESTACADOS_PATH = os.path.join(BASE_DIR, "db", "featured_products.json")
DELTA_IDS_PATH = os.path.join(BASE_DIR, "db", "processed_ids.txt")
CATEGORIAS_DIR = os.path.join(BASE_DIR, "db", "categorias")
os.makedirs(CATEGORIAS_DIR, exist_ok=True)

# Funciones auxiliares
def leer_articulos():
    try:
        with open(ARTICULOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No se encontró {ARTICULOS_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parseando {ARTICULOS_PATH}: {e}")
        return []

def leer_ids_procesados():
    if not os.path.exists(DELTA_IDS_PATH):
        return set()
    with open(DELTA_IDS_PATH, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def guardar_ids_procesados(ids):
    with open(DELTA_IDS_PATH, "a", encoding="utf-8") as f:
        for _id in ids:
            f.write(f"{_id}\n")

def guardar_destacados(top5):
    if not top5:
        print("No se encontraron productos Platinum nuevos, no se sobrescribe productos_destacados.json")
        return
    with open(DESTACADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(top5, f, ensure_ascii=False, indent=2)
    print(f"Productos destacados actualizados en {DESTACADOS_PATH}")

def generar_archivos_categorias(nuevos_productos):
    for producto in nuevos_productos:
        categoria = producto["additional_details"].get("category", "sin_categoria").lower()
        categoria_file = os.path.join(CATEGORIAS_DIR, f"{categoria}.json")

        # Leer contenido existente
        if os.path.exists(categoria_file):
            try:
                with open(categoria_file, "r", encoding="utf-8") as f:
                    productos_existentes = json.load(f)
            except json.JSONDecodeError:
                productos_existentes = []
        else:
            productos_existentes = []

        productos_existentes.append(producto)

        # Guardar de nuevo
        with open(categoria_file, "w", encoding="utf-8") as f:
            json.dump(productos_existentes, f, ensure_ascii=False, indent=2)

        print(f"Producto {producto['id']} agregado a categoría '{categoria}' en {categoria_file}")

def generar_destacados_batch():
    print("Iniciando batch de generación de destacados")
    productos = leer_articulos()
    if not productos:
        return

    ids_procesados = leer_ids_procesados()

    # Buscar productos nuevos por ID
    nuevos_productos = [p for p in productos if p["id"] not in ids_procesados]

    if not nuevos_productos:
        print("No hay productos nuevos para procesar")
        return

    # Leer destacados actuales si existen
    if os.path.exists(DESTACADOS_PATH):
        try:
            with open(DESTACADOS_PATH, "r", encoding="utf-8") as f:
                destacados_actuales = json.load(f)
        except json.JSONDecodeError:
            destacados_actuales = []
    else:
        destacados_actuales = []

    # Combinar actuales + nuevos
    combinados = destacados_actuales + nuevos_productos

    # Filtrar solo vendedores Platinum
    platinum = [p for p in combinados if p["seller"]["reputation"] == "Platinum"]

    # Ordenar por reviews de mayor a menor
    platinum.sort(key=lambda x: x["additional_details"].get("reviews", 0), reverse=True)

    # Quedarse con los mejores 5
    top5 = platinum[:5]

    # Guardar los destacados
    guardar_destacados(top5)

    # Archivos por categoría
    generar_archivos_categorias(nuevos_productos)

    # Guardar IDs procesados
    nuevos_ids = [p["id"] for p in nuevos_productos]
    guardar_ids_procesados(nuevos_ids)

    print(f"Batch finalizado. Se procesaron {len(nuevos_ids)} productos nuevos")


if __name__ == "__main__":
    while True:
        generar_destacados_batch()
        print(f"Esperando {RECURRENCY} minutos para próxima ejecución...")
        time.sleep(RECURRENCY * 60)
