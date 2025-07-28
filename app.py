from fastapi import FastAPI
from database import create_tables
from routers import router

try:
    create_tables()
    print("Tablas de base de datos creadas exitosamente")
except Exception as e:
    print(f"Error al inicializar la base de datos: {str(e)}")
    print("Verifique la configuración de la base de datos en el archivo .env")


app = FastAPI(
    title="Sistema de Votaciones - API RESTful",
    description="""
    API RESTful para Sistema de Votaciones

    Esta API permite gestionar un sistema de votaciones con las siguientes funcionalidades:

    Funcionalidades Principales:
    - Gestión de Votantes: Registrar, consultar y eliminar votantes
    - Gestión de Candidatos: Registrar, consultar y eliminar candidatos  
    - Emisión de Votos: Permitir que los votantes emitan un único voto
    - Estadísticas: Obtener estadísticas completas de la votación

    Reglas de Negocio:
    - Un votante no puede ser registrado como candidato y viceversa
    - Cada votante puede emitir un único voto
    - Los votos deben ser contados correctamente en las estadísticas
    - Se mantiene la integridad de los datos en todo momento

    Tecnologías Utilizadas:
    - FastAPI: Framework web moderno 
    - SQLAlchemy: ORM para manejo de base de datos
    - MySQL: Sistema de gestión de base de datos
    - Pydantic: Validación de datos y serialización
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(router)

# Endpoint raíz
@app.get(
    "/",
    tags=["Sistema"],
    summary="Endpoint raíz",
    description="Información básica sobre la API"
)
async def root():
    """
    Endpoint raíz con información básica de la API
    """
    return {
        "message": "Bienvenido al Sistema de Votaciones API",
        "swagger": "/docs",
        "redoc": "/redoc"
    }