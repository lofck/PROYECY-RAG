from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_engine import procesar_consulta_rag

# 1. Definición única de la API con los metadatos institucionales
app = FastAPI(
    title="UNSO Cyber RAG - API de Inferencia",
    description="Backend del Sprint 3 con arquitectura modular de Mocking de contingencia.",
    version="1.0.0"
)

# 2. Estructura del JSON de entrada para las consultas de los alumnos
class ConsultaRequest(BaseModel):
    pregunta: str

# 3. Endpoint de verificación unificado (Mantiene tu estado de Docker y tu usuario)
@app.get("/")
def verificar_servidor():
    return {
        "status": "ONLINE", 
        "fase": "Sprint 3 - Inferencia Semántica",
        "docker": "Funcionando de diez",
        "user": "Emanuel"
    }

# 4. Endpoint principal del RAG para procesar las preguntas
@app.post("/api/v1/consultar")
def consultar_sistema(request: ConsultaRequest):
    resultado = procesar_consulta_rag(request.pregunta)
    return resultado