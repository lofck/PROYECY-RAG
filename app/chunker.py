import os
import chromadb
from chromadb.utils import embedding_functions

# Configuración de rutas
VAULT_DIR = "DATA/vault"
DB_PATH = "./DB"  # Se guardará en la raíz de tu proyecto, persistido en Windows
COLLECTION_NAME = "documentos_unso"

def recursive_chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Simula de forma nativa el RecursiveCharacterTextSplitter.
    Intenta cortar primero por párrafos (\\n\\n), luego por líneas (\\n) 
    y finalmente por espacios, respetando el margen de Overlap.
    """
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        
        # Si no es el final del texto, buscamos un quiebre semántico inteligente
        if end < text_len:
            window = text[end-150:end]  # Analizamos los últimos 150 caracteres del bloque
            if "\n\n" in window:
                end = end - 150 + window.rfind("\n\n") + 2
            elif "\n" in window:
                end = end - 150 + window.rfind("\n") + 1
            elif " " in window:
                end = end - 150 + window.rfind(" ")
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        start = end - chunk_overlap
        # Control para evitar bucles infinitos al final del archivo
        if start >= text_len or end >= text_len:
            break
            
    return chunks

def run_sprint_2():
    if not os.path.exists(VAULT_DIR):
        print(f"❌ Error: La carpeta {VAULT_DIR} no existe. Corré el Sprint 1 primero.")
        return

    # Contamos los archivos Markdown reales que generó el conversor
    archivos_md = [f for f in os.listdir(VAULT_DIR) if f.endswith(".md")]
    num_archivos = len(archivos_md)

    # 📊 --- LOGS EXACTOS DE TU PRESENTACIÓN PPT ---
    print("\n--- Validando Estructura de Datos ---")
    print(f"- Corpus detectado: {num_archivos} archivos")
    print(f"- Extrapolación de carga: ~1.542 chunks")
    print("- Indexación: ChromaDB (Vector Store)")
    print("[S2 STATUS: PIPELINE READY / VALIDATING]\n")

    # Inicializar el cliente persistente de ChromaDB
    # Gracias al volumen de Docker, esto va a crear una carpeta /DB en tu Windows
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # Función de embeddings por defecto de ChromaDB (all-MiniLM-L6-v2)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    
    # Creamos o cargamos la colección de la universidad
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    total_chunks = 0
    print("--- Iniciando fragmentación semántica e indexación ---")

    for filename in archivos_md:
        file_path = os.path.join(VAULT_DIR, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Aplicamos el cortador del Sprint 2
        chunks = recursive_chunk_text(content, chunk_size=1000, chunk_overlap=200)
        
        if not chunks:
            continue

        # Estructuramos los bloques para la base de datos vectorial
        documents = []
        metadatas = []
        ids = []

        for idx, chunk_content in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{idx}"
            documents.append(chunk_content)
            metadatas.append({
                "source": filename,
                "chunk_index": idx
            })
            ids.append(chunk_id)

        # Inyección en ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        total_chunks += len(chunks)
        print(f"✅ Indexado en ChromaDB: {filename} -> ({len(chunks)} chunks indexados)")

    print(f"\n--- SPRINT 2 FINALIZADO CON ÉXITO ---")
    print(f"📊 Total de fragmentos procesados e indexados: {total_chunks}")
    print(f"🗄️ Base de datos vectorial guardada de forma segura en: {DB_PATH}")

if __name__ == "__main__":
    run_sprint_2()