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

## ☁️ Despliegue en Vercel con MongoDB Atlas / Storage

La API cuenta con configuración nativa para **Vercel Serverless Functions** (`vercel.json` y `api/index.py`).

### 1. Configurar MongoDB en la Nube (MongoDB Atlas o Vercel Storage)
1. Crea una cuenta gratuita en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Crea un clúster gratuito (M0 Sandbox).
3. En **Database Access**, crea un usuario con contraseña.
4. En **Network Access**, permite el acceso desde cualquier lugar (`0.0.0.0/0`) para que las funciones serverless de Vercel puedan conectarse.
5. En **Connect > Drivers (Python)**, copia tu cadena de conexión URI:
   ```text
   mongodb+srv://<usuario>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### 2. Desplegar en Vercel
#### Opción A: Desde el panel de Vercel (Recomendado)
1. Ve a [vercel.com](https://vercel.com/) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **Add New... > Project** e importa el repositorio `camacho-12345/book_catalogs`.
3. En la sección **Environment Variables**, añade:
   - `MONGODB_URL`: Tu cadena de conexión `mongodb+srv://...`
   - `DATABASE_NAME`: `catalogo_libros_db`
   - `COLLECTION_NAME`: `libros`
4. Haz clic en **Deploy**.

#### Opción B: Usando Vercel CLI
```bash
npx vercel
```
Sigue las indicaciones en consola y configura las variables de entorno con:
```bash
npx vercel env add MONGODB_URL
```

- **Swagger UI en Vercel:** `https://tu-proyecto.vercel.app/docs`
- **Health Check:** `https://tu-proyecto.vercel.app/`


