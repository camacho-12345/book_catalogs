# 📚 API Catálogo de Libros (FastAPI + MongoDB)

API REST desarrollada con **FastAPI** y **MongoDB** (driver asíncrono Motor) para administrar y consultar un catálogo de libros con operaciones de registro, actualización, consulta, eliminación, búsqueda y filtros avanzados.

---

## 🛠️ Tecnologías

- **Lenguaje:** Python 3.10+
- **Framework:** FastAPI
- **Base de Datos:** MongoDB
- **Driver Asíncrono:** Motor
- **Validación de Datos:** Pydantic v2
- **Contenedores:** Docker & Docker Compose

---

## 🗂️ Estructura del Proyecto

```text
catalogos-de-libros/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Inicialización de FastAPI, CORS y ciclo de vida
│   ├── config.py                   # Configuración con Pydantic Settings
│   ├── database.py                 # Conexión asíncrona a MongoDB con Motor
│   ├── models/
│   │   ├── __init__.py
│   │   └── libro.py                # Serializadores y utilidades BSON
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── libro.py                # Esquemas Pydantic (Validación y DTOs)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── libro_repository.py     # Acceso a base de datos y consultas MongoDB
│   ├── services/
│   │   ├── __init__.py
│   │   └── libro_service.py        # Capa de lógica de negocio
│   └── routers/
│       ├── __init__.py
│       └── libros.py               # Endpoints de la API (10 funcionalidades)
├── tests/
│   ├── __init__.py
│   └── test_libros.py              # Pruebas unitarias
├── .env.example                    # Ejemplo de variables de entorno
├── .gitignore                      # Reglas de exclusión para Git
├── Dockerfile                      # Imagen para desplegar la API
├── docker-compose.yml              # Orquestación de API + MongoDB
├── requirements.txt                # Dependencias de Python
└── README.md                       # Documentación del proyecto
```

---

## 📄 Estructura del Documento (`libros`)

Cada libro almacenado en la colección `libros` contiene la siguiente estructura:

```json
{
  "_id": "ObjectId('...')",
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "isbn": "978-0307474728",
  "genero": "Realismo Mágico",
  "anio_publicacion": 1967,
  "editorial": "Editorial Sudamericana",
  "disponible": true,
  "etiquetas": [
    "clasico",
    "literatura latinoamericana",
    "premio nobel"
  ],
  "ubicacion": {
    "sala": "Sala Principal",
    "estante": "Estante B-4"
  }
}
```

---

## 🚀 Endpoints de la API

| # | Método | Endpoint | Descripción |
|---|---|---|---|
| **1** | `POST` | `/api/v1/libros` | Registrar un nuevo libro |
| **2** | `GET` | `/api/v1/libros` | Listar todos los libros (paginado) |
| **3** | `GET` | `/api/v1/libros/{id}` | Consultar un libro por su identificador |
| **4** | `PUT` | `/api/v1/libros/{id}` | Modificar la información de un libro |
| **5** | `DELETE` | `/api/v1/libros/{id}` | Eliminar un libro por su ID |
| **6** | `GET` | `/api/v1/libros/buscar?q={texto}` | Buscar libros por título o autor |
| **7** | `GET` | `/api/v1/libros/filtrar/genero?genero={nombre}` | Filtrar libros por género literario |
| **8** | `GET` | `/api/v1/libros/filtrar/disponibilidad?disponible={true\|false}` | Filtrar libros por disponibilidad |
| **9** | `GET` | `/api/v1/libros/filtrar/anio?anio={año}` | Filtrar libros por año de publicación |
| **10** | `GET` | `/api/v1/libros/{id}/etiquetas` | Consultar etiquetas asociadas a un libro |

---

## ⚡ Ejecución del Proyecto

### Opción 1: Con Docker Compose (Recomendado)

Inicia automáticamente **MongoDB** y la **API**:

```bash
docker-compose up --build
```

- **API:** [http://localhost:8000](http://localhost:8000)
- **Documentación Interactiva (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Opción 2: Ejecución Local

1. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   ```

4. **Iniciar el servidor de desarrollo:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 🌿 Flujo Git

Este proyecto está configurado en la rama **`dev`**:
```bash
git branch
# * dev
```

<!-- CI status: passing -->

