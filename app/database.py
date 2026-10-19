from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

def get_database():
    """Obtiene la instancia de la base de datos MongoDB."""
    return db.client[settings.DATABASE_NAME]

def get_collection():
    """Obtiene la coleccion 'libros'."""
    database = get_database()
    return database[settings.COLLECTION_NAME]

async def connect_to_mongo():
    """Conecta el cliente asincrono de Motor a MongoDB y crea indices."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = db.client[settings.DATABASE_NAME]
    collection = database[settings.COLLECTION_NAME]
    
    # Crear indices para optimizacion de busquedas y garantizar unicidad de ISBN
    try:
        await collection.create_index("isbn", unique=True)
        await collection.create_index("titulo")
        await collection.create_index("autor")
        await collection.create_index("genero")
        await collection.create_index("anio_publicacion")
        print("Indices de coleccion 'libros' configurados correctamente.")
    except Exception as e:
        print(f"Advertencia al crear indices en MongoDB: {e}")
        
    print(f"Conectado exitosamente a MongoDB: {settings.MONGODB_URL}")

async def close_mongo_connection():
    """Cierra la conexion con MongoDB."""
    if db.client:
        db.client.close()
        print("Conexion con MongoDB cerrada.")
