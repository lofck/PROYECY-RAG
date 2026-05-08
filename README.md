# PROYECY-RAG
A Dockerized RAG (Retrieval-Augmented Generation) laboratory built with FastAPI and ChromaDB for secure document analysis and AI-driven retrieval

Laboratorio RAG: Análisis de Documentos con IA
Este proyecto establece un entorno de desarrollo portable y escalable para aplicaciones de Generación Aumentada por Recuperación (RAG). El objetivo principal es permitir el análisis de documentos locales mediante inteligencia artificial, garantizando la privacidad de los datos y la paridad del entorno entre todos los miembros del equipo.

🚀 Tecnologías Principales
Docker & Docker Compose: Virtualización de aplicaciones para asegurar que el sistema corra igual en cualquier PC.

Python 3.12 (Slim): Lenguaje base optimizado para alto rendimiento y bajo consumo de recursos.

FastAPI: Framework web moderno para la creación de la API del laboratorio.

ChromaDB: Base de datos vectorial de alto rendimiento para el almacenamiento y recuperación de documentos.

👥 Estructura del Equipo y Roles
Para el desarrollo de este laboratorio, hemos definido 5 áreas de responsabilidad:

Líder de Base de Datos (DB Lead): Responsable de la persistencia de datos en ChromaDB, gestión de volúmenes en Docker y optimización de la búsqueda vectorial.

Ingeniero de Datos (Ingesta): Encargado de la lógica de procesamiento de archivos (PDF/TXT), limpieza de texto y estrategias de segmentación (chunking).

Arquitecto de API: Desarrollador de los puntos de entrada en FastAPI y la comunicación entre el cliente y el servidor.

Orquestador de RAG: Integración con el modelo de lenguaje (LLM) y diseño del Prompt Engineering para respuestas precisas.

Analista de QA y Seguridad: Auditoría de seguridad del sistema, pruebas de estrés y mitigación de vulnerabilidades como el Prompt Injection.




