import os
import xml.etree.ElementTree as ET
import shutil

# Aquí es donde se definen las rutas que mencionamos
# Coinciden exactamente con tu estructura de carpetas
RAW_PATH = "DATA/raw"
OUTPUT_PATH = "DATA/processed"
FILES_XML = os.path.join(RAW_PATH, "files.xml")
FILES_DIR = os.path.join(RAW_PATH, "files")

def procesar_moodle_files():
    # Creamos la carpeta de salida si no existe
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    print("--- Iniciando recuperación de archivos académicos ---")
    
    # Verificamos que el archivo de índice exista
    if not os.path.exists(FILES_XML):
        print(f"Error: No se encontró {FILES_XML}. Revisá la ubicación.")
        return

    tree = ET.parse(FILES_XML)
    root = tree.getroot()

    count = 0
    for file in root.findall('file'):
        filename = file.find('filename').text
        contenthash = file.find('contenthash').text
        component = file.find('component').text 

        # Filtro de seguridad: Solo archivos de recursos (evitamos datos de usuarios)
        if filename == "." or component != "mod_resource":
            continue

        # Moodle organiza los archivos por los primeros 2 caracteres del hash
        hash_subdir = contenthash[:2]
        source = os.path.join(FILES_DIR, hash_subdir, contenthash)
        
        # Nombre final del archivo recuperado
        destination = os.path.join(OUTPUT_PATH, filename)

        if os.path.exists(source):
            shutil.copy(source, destination)
            count += 1
            if count % 50 == 0:
                print(f"Archivos procesados: {count}...")

    print(f"--- Proceso finalizado. {count} archivos están listos en {OUTPUT_PATH} ---")

if __name__ == "__main__":
    procesar_moodle_files()