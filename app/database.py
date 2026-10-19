import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

def get_client() -> AsyncIOMotorClient:
    """Obtiene o inicializa el cliente asincrono de MongoDB optimizado para Serverless (Vercel)."""
    if db.client is None:
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=20000
        )
    return db.client

def get_database():
    """Obtiene la instancia de la base de datos MongoDB."""
    client = get_client()
    return client[settings.DATABASE_NAME]

def get_collection():
    """Obtiene la coleccion 'libros'."""
    database = get_database()
    return database[settings.COLLECTION_NAME]

async def connect_to_mongo():
    """Conecta a MongoDB y crea indices de optimizacion."""
    try:
        client = get_client()
        database = client[settings.DATABASE_NAME]
        collection = database[settings.COLLECTION_NAME]
        
        # Crear indices para acelerar consultas y garantizar unicidad
        await collection.create_index("isbn", unique=True)
        await collection.create_index("titulo")
        await collection.create_index("autor")
        await collection.create_index("genero")
        await collection.create_index("anio_publicacion")
        print(f"Indices de coleccion 'libros' verificados en MongoDB.")
    except Exception as e:
        print(f"Aviso al inicializar indices (comportamiento normal en serverless cold start): {e}")

async def close_mongo_connection():
    """Cierra la conexion con MongoDB."""
    if db.client:
        db.client.close()
        db.client = None
        print("Conexion con MongoDB cerrada.")
