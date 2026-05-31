import xml.etree.ElementTree as ET
from collections import Counter
import os

# Ruta al mapa maestro del backup de Moodle
XML_PATH = "DATA/raw/files.xml"

if not os.path.exists(XML_PATH):
    print(f"❌ No se encuentra el archivo en: {XML_PATH}")
else:
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    data = []
    for f in root.findall('file'):
        comp = f.find('component').text
        fname = f.find('filename').text
        # Si no tiene nombre es una carpeta
        ext = os.path.splitext(fname)[1].lower() if fname != "." else "folder"
        data.append((comp, ext))

    conteo_comp = Counter([d[0] for d in data])
    conteo_ext = Counter([d[1] for d in data])

    print("\n" + "="*30)
    print("📊 REPORTE DE COMPONENTES")
    print("="*30)
    for c, cant in conteo_comp.items(): 
        print(f"{c:20} | {cant} archivos")

    print("\n" + "="*30)
    print("📂 REPORTE DE EXTENSIONES")
    print("="*30)
    for e, cant in conteo_ext.items(): 
        if e != "folder":
            print(f"{e:10} | {cant} archivos")