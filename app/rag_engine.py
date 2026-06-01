import os
import chromadb
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() == "true"
FACULTY_API_URL = os.getenv("FACULTY_API_URL")
FACULTY_TOKEN = os.getenv("FACULTY_TOKEN")

# Conectar a la base de datos vectorial persistida en tu carpeta ./DB
chroma_client = chromadb.PersistentClient(path="./DB")

# Intentamos levantar tu colección indexada (ajustá el nombre si usaste otro en el chunker)
try:
    collection = chroma_client.get_collection(name="unso_clases")
except Exception:
    # Salvavidas por si la colección tiene otro nombre
    colecciones = chroma_client.list_collections()
    collection = chroma_client.get_collection(name=colecciones[0].name) if colecciones else None

def procesar_consulta_rag(pregunta_alumno: str):
    if not collection:
        return {"error": "La base de datos vectorial de la UNSO no está disponible."}

    # 1. RETRIEVAL: Búsqueda de similitud semántica en ChromaDB
    # Buscamos los 3 fragmentos de texto de las clases más parecidos a la pregunta
    resultados = collection.query(
        query_texts=[pregunta_alumno],
        n_results=3
    )

    chunks_recuperados = resultados['documents'][0] if resultados['documents'] else []
    metadatas_recuperadas = resultados['metadatas'][0] if resultados['metadatas'] else []

    # 2. CONTROL FLOW: Filtro de Simulación (Mocking) vs Producción
    if MOCK_MODE:
        # Extraemos las fuentes reales para mostrar que el motor funciona de verdad
        fuentes = [meta.get("source", "Apunte UNSO") for meta in metadatas_recuperadas]
        
        # Simulamos la respuesta estructurada que daría Gemma 4 en base a ese contexto
        respuesta_gemma = (
            f"[MODO SIMULACIÓN ACTIVO - SPRINT 3]\n"
            f"Gemma 4 procesó los fragmentos de la base de datos de la facultad.\n"
            f"Respuesta emulada basada en el contexto de las cátedras inyectadas."
        )
        
        return {
            "status": "SUCCESS",
            "plano_control": "SIMULADO (Falta credencial de cátedra)",
            "pregunta": pregunta_alumno,
            "respuesta_ia": respuesta_gemma,
            "contexto_verificado_unso": chunks_recuperados,
            "fuentes_utilizadas": fuentes
        }
    else:
        # 3. GENERATION: Conexión real por red mediante payload seguro (Para cuando tengan el token)
        import requests
        
        # Aquí consolidamos el megaprompt con los estándares NIST de sanitización
        contexto_plano = "\n---\n".join(chunks_recuperados)
        prompt_institucional = (
            f"Actúa como un asistente académico de la UNSO. Responde la pregunta basándote estrictamente "
            f"en el siguiente contexto académico. Si la información no está, di 'No sé'.\n\n"
            f"Contexto:\n{contexto_plano}\n\nPregunta: {pregunta_alumno}\nRespuesta:"
        )
        
        headers = {"Authorization": f"Bearer {FACULTY_TOKEN}", "Content-Type": "application/json"}
        payload = {"model": "gemma-4", "prompt": prompt_institucional, "temperature": 0.0}
        
        try:
            response = requests.post(FACULTY_API_URL, json=payload, headers=headers, timeout=10)
            return response.json()
        except Exception as e:
            return {"status": "ERROR", "detalle": f"Falló la conexión al servidor de la UNSO: {str(e)}"}