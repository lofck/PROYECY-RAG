import os
import fitz  # PyMuPDF
from docx import Document

# Rutas
INPUT_DIR = "DATA/processed"
OUTPUT_DIR = "DATA/vault"

# Lista de archivos corruptos a ignorar automáticamente
ARCHIVOS_CORRUPTOS = [
    "e6b1e_Convenio de Budapest .pdf",  # Con espacio al final
    "e6b1e_Convenio de Budapest.pdf",   # Pegado
    "Convenio de Budapest .pdf",        # Con espacio al final
    "Convenio de Budapest.pdf"          # Pegado
]

def convert_to_markdown():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"--- Iniciando conversión a Markdown (NIST 800-218) ---")

    for filename in os.listdir(INPUT_DIR):
        # Filtro de seguridad: si el archivo está en la lista negra, lo saltea de una
        if filename in ARCHIVOS_CORRUPTOS:
            print(f"⚠️ LOG NIST: '{filename}' omitido. Motivo: Archivo corrupto de origen (ToUnicode roto).")
            continue

        file_path = os.path.join(INPUT_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.md")

        text = ""
        print(f"Procesando: {filename}...")

        try:
            # Procesar PDF
            if filename.lower().endswith(".pdf"):
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                doc.close()

            # Procesar Word
            elif filename.lower().endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])

            # Guardar como Markdown
            if text:
                with open(output_path, "w", encoding="utf-8") as f:
                    # Aquí es donde podrías agregar metadatos o tags automáticos
                    f.write(f"# {base_name}\n\n")
                    f.write(text)
                print(f"✅ Convertido: {base_name}.md")

        except Exception as e:
            print(f"❌ Error en {filename}: {e}")

    print(f"--- Proceso finalizado. Archivos listos en {OUTPUT_DIR} ---")

if __name__ == "__main__":
    convert_to_markdown()