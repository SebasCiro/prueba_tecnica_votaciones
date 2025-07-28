# Sistema de Votaciones API

Una API RESTful completa para gestionar un sistema de votaciones desarrollada con FastAPI, SQLAlchemy y MySQL.

## Capturas de Pantalla

![Swagger UI - Documentación Interactiva](./screenshots/docs.png)
_Interfaz de documentación interactiva de la API_

![Estadísticas de Votación](./screenshots/stats.png)
_Ejemplo de estadísticas generadas por el sistema_

## Descripción del Proyecto

Esta API permite gestionar un sistema de votaciones completo donde los votantes pueden registrarse, los candidatos pueden ser registrados, y se pueden emitir votos únicos por votante. El sistema incluye validaciones de integridad y estadísticas en tiempo real.

**Características Principales:**

- Gestión de votantes (crear, listar, obtener por ID, eliminar)
- Gestión de candidatos (crear, listar, obtener por ID, eliminar)
- Sistema de votación con validaciones
- Estadísticas en tiempo real con porcentajes
- Documentación automática con Swagger UI
- Validación de datos con Pydantic
- Base de datos MySQL con SQLAlchemy ORM
- Manejo de errores

## Estructura del Proyecto

```
sistema-votaciones/
│
├── screenshots/        # Capturas de pantalla(evidencia en este README)
│   ├── docs.png
│   └── stats.png
├── .env                # Variables de entorno (configurar)
├── .gitignore          # Archivos a ignorar en Git
├── app.py              # Punto de entrada de FastAPI
├── crud.py             # Funciones CRUD para operaciones DB
├── database.py         # Configuración de SQLAlchemy y conexión DB
├── models.py           # Modelos ORM (Voter, Candidate, Vote)
└── README.md           # Documentación del proyecto
├── requirements.txt    # Dependencias del proyecto
├── routes.py           # Definición de rutas y endpoints
├── schemas.py          # Esquemas de Pydantic para validación
```

## Configuración y Ejecución Local

**Prerrequisitos**

- Python 3.8 o superior
- MySQL Server 5.7 o superior
- pip (gestor de paquetes de Python)

**Paso 1: Clonar el repositorio**

```bash
git clone https://github.com/SebasCiro/prueba_tecnica_votaciones.git
cd sistema-votaciones
```

**Paso 2: Crear y activar entorno virtual**

Es altamente recomendable usar un entorno virtual para evitar conflictos de dependencias:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

**Paso 3: Instalar dependencias**

```bash
pip install -r requirements.txt
```

**Paso 4: Configurar la base de datos**

1. Crear la base de datos en MySQL:

```sql
CREATE DATABASE sistema_votaciones;
```

2. Configurar variables de entorno:

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
# Configuración de Base de Datos - String de conexión
DATABASE_URL=mysql+pymysql://tu_usuario:tu_password@localhost:3306/sistema_votaciones

# Ejemplo real:
# DATABASE_URL=mysql+pymysql://root:mi_password123@localhost:3306/sistema_votaciones
```

**Importante:**

- Reemplaza `tu_usuario` y `tu_password` con tus credenciales reales de MySQL
- Asegúrate de que el usuario tenga permisos para crear y modificar tablas
- No necesitas crear las tablas manualmente, este proyecto las creará automáticamente

**Paso 5: Ejecutar la aplicación**

```bash
# Opción recomendada según la ultima documentación de FastAPI para desarrollo (con recarga automática)
fastapi dev app.py
```

**La API estará disponible en:**

- Aplicación principal: `http://localhost:8000`
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`
- Schema OpenAPI: `http://localhost:8000/openapi.json`

## Documentación Interactiva

Una vez ejecutando la aplicación, visita `http://localhost:8000/docs` para acceder a la documentación interactiva de Swagger UI, donde podrás ver todos los endpoints disponibles, probar los endpoints directamente desde el navegador, ver ejemplos de requests y responses, y consultar todos los modelos de datos.

## Endpoints Disponibles

**Votantes:**

- POST `/voters` - Registrar nuevo votante
- GET `/voters` - Obtener lista de votantes
- GET `/voters/{voter_id}` - Obtener detalles de un votante
- DELETE `/voters/{voter_id}` - Eliminar votante

**Candidatos:**

- POST `/candidates` - Registrar nuevo candidato
- GET `/candidates` - Obtener lista de candidatos
- GET `/candidates/{candidate_id}` - Obtener detalles de un candidato
- DELETE `/candidates/{candidate_id}` - Eliminar candidato

**Votos:**

- POST `/votes` - Emitir un voto
- GET `/votes` - Obtener todos los votos emitidos
- GET `/votes/statistics` - Obtener estadísticas de la votación

## Ejemplos de Uso

**1. Registrar un votante**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/voters' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Sebastián Jiménez Ciro",
  "email": "sebas.ciro@gmail.com"
}'
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Sebastián Jiménez Ciro",
  "email": "sebas.ciro@gmail.com",
  "has_voted": false
}
```

**2. Registrar un candidato**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/candidates' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Lucas Estrada Arrieta",
  "party": "Partido Derecha"
}'
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Lucas Estrada Arrieta",
  "party": "Partido Derecha",
  "votes": 0
}
```

**3. Emitir un voto**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/votes' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "voter_id": 1,
  "candidate_id": 1
}'
```

Respuesta esperada:

```json
{
  "id": 1,
  "voter_id": 1,
  "candidate_id": 1
}
```

**4. Obtener estadísticas completas**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/votes/statistics' \
  -H 'accept: application/json'
```

Respuesta esperada:

```json
{
  "candidates_stats": [
    {
      "candidate_name": "Lucas Estrada Arrieta",
      "total_votes": 3,
      "percentage": 42.86
    },
    {
      "candidate_name": "Juan Jaramillo Urrieta",
      "total_votes": 1,
      "percentage": 14.29
    },
    {
      "candidate_name": "Celeste Restrepo Hoyos",
      "total_votes": 0,
      "percentage": 0
    },
    {
      "candidate_name": "Marta Rojas Ruiz",
      "total_votes": 3,
      "percentage": 42.86
    }
  ],
  "total_voters_who_voted": 7
}
```

## Soporte

Si encuentras problemas, verifica que la base de datos(sistema_votaciones) esté ejecutándose, confirma que el archivo `.env` esté configurado correctamente, asegúrate de estar en el entorno virtual activado, revisa los logs en la consola donde ejecutas la aplicación y visita `http://localhost:8000/docs` para probar endpoints.

## Información Técnica

- **Lenguaje**: Python 3.8+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Base de Datos**: MySQL
- **Validación**: Pydantic
- **Documentación**: Swagger UI / ReDoc / OpenAPI
