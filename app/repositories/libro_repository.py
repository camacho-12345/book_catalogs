import re
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from app.database import get_collection
from app.models.libro import libro_helper


class LibroRepository:
    """Capa de acceso a datos para la coleccion 'libros' en MongoDB."""

    @property
    def collection(self):
        return get_collection()

    async def create(self, libro_data: dict) -> dict:
        """Inserta un nuevo libro en la base de datos."""
        result = await self.collection.insert_one(libro_data)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        return libro_helper(created_doc)

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Obtiene la lista de todos los libros paginada."""
        libros = []
        cursor = self.collection.find().skip(skip).limit(limit)
        async for doc in cursor:
            libros.append(libro_helper(doc))
        return libros

    async def find_by_id(self, libro_id: str) -> Optional[dict]:
        """Busca un libro por su identificador unico."""
        if not ObjectId.is_valid(libro_id):
            return None
        try:
            doc = await self.collection.find_one({"_id": ObjectId(libro_id)})
            return libro_helper(doc) if doc else None
        except InvalidId:
            return None

    async def find_by_isbn(self, isbn: str) -> Optional[dict]:
        """Busca un libro por su codigo ISBN exacto."""
        doc = await self.collection.find_one({"isbn": isbn})
        return libro_helper(doc) if doc else None

    async def update(self, libro_id: str, update_data: dict) -> Optional[dict]:
        """Actualiza la informacion de un libro existente con soporte de aplanado para subdocumentos."""
        if not ObjectId.is_valid(libro_id):
            return None
        try:
            obj_id = ObjectId(libro_id)
            
            # Aplanar claves para permitir actualizaciones parciales sin sobreescribir el objeto completo
            flattened_data = {}
            for key, value in update_data.items():
                if value is not None:
                    if key == "ubicacion" and isinstance(value, dict):
                        for sub_key, sub_val in value.items():
                            if sub_val is not None:
                                flattened_data[f"ubicacion.{sub_key}"] = sub_val
                    else:
                        flattened_data[key] = value

            if not flattened_data:
                return await self.find_by_id(libro_id)

            await self.collection.update_one({"_id": obj_id}, {"$set": flattened_data})
            doc = await self.collection.find_one({"_id": obj_id})
            return libro_helper(doc) if doc else None
        except InvalidId:
            return None

    async def delete(self, libro_id: str) -> bool:
        """Elimina un libro por su identificador."""
        if not ObjectId.is_valid(libro_id):
            return False
        try:
            result = await self.collection.delete_one({"_id": ObjectId(libro_id)})
            return result.deleted_count > 0
        except InvalidId:
            return False

    async def search_by_titulo_or_autor(self, query: str) -> List[dict]:
        """Busca libros cuyo titulo o autor coincida con la consulta (sanitizada e insensible a mayusculas)."""
        safe_query = re.escape(query.strip())
        regex = {"$regex": safe_query, "$options": "i"}
        filter_query = {
            "$or": [
                {"titulo": regex},
                {"autor": regex}
            ]
        }
        libros = []
        cursor = self.collection.find(filter_query)
        async for doc in cursor:
            libros.append(libro_helper(doc))
        return libros

    async def filter_by_genero(self, genero: str) -> List[dict]:
        """Filtra libros por su genero literario."""
        safe_genero = re.escape(genero.strip())
        libros = []
        cursor = self.collection.find({"genero": {"$regex": f"^{safe_genero}$", "$options": "i"}})
        async for doc in cursor:
            libros.append(libro_helper(doc))
        return libros

    async def filter_by_disponibilidad(self, disponible: bool) -> List[dict]:
        """Filtra libros segun su estado de disponibilidad."""
        libros = []
        cursor = self.collection.find({"disponible": disponible})
        async for doc in cursor:
            libros.append(libro_helper(doc))
        return libros

    async def filter_by_anio(self, anio: int) -> List[dict]:
        """Filtra libros por su ano de publicacion."""
        libros = []
        cursor = self.collection.find({"anio_publicacion": anio})
        async for doc in cursor:
            libros.append(libro_helper(doc))
        return libros

    async def get_etiquetas_by_id(self, libro_id: str) -> Optional[dict]:
        """Consulta las etiquetas asociadas a un libro especifico."""
        if not ObjectId.is_valid(libro_id):
            return None
        try:
            doc = await self.collection.find_one(
                {"_id": ObjectId(libro_id)},
                {"_id": 1, "titulo": 1, "etiquetas": 1}
            )
            if not doc:
                return None
            return {
                "id": str(doc["_id"]),
                "titulo": doc.get("titulo", ""),
                "etiquetas": doc.get("etiquetas", [])
            }
        except InvalidId:
            return None

# ReDoS prevention applied to all regex filters

