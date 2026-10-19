from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status
from app.repositories.libro_repository import LibroRepository
from app.schemas.libro import LibroCreate, LibroUpdate


class LibroService:
    """Capa de logica de negocio para las operaciones con libros."""

    def __init__(self, repository: LibroRepository = None):
        self.repository = repository or LibroRepository()

    def _validar_object_id(self, libro_id: str) -> None:
        """Valida que la cadena corresponda a un ObjectId valido de MongoDB (24 hex chars)."""
        if not ObjectId.is_valid(libro_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El identificador '{libro_id}' no es un ObjectId valido de MongoDB (debe tener 24 caracteres hexadecimales)."
            )

    async def registrar_libro(self, libro_in: LibroCreate) -> dict:
        """1. Registrar un nuevo libro verificando unicidad de ISBN."""
        # Validar si ya existe un libro con el mismo ISBN
        existente = await self.repository.find_by_isbn(libro_in.isbn.strip())
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conflicto: Ya existe un libro registrado con el codigo ISBN '{libro_in.isbn}'."
            )
        libro_data = libro_in.model_dump()
        libro_data["isbn"] = libro_data["isbn"].strip()
        return await self.repository.create(libro_data)

    async def listar_libros(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """2. Listar todos los libros con paginacion."""
        return await self.repository.find_all(skip=skip, limit=limit)

    async def obtener_libro_por_id(self, libro_id: str) -> dict:
        """3. Consultar un libro mediante su identificador."""
        self._validar_object_id(libro_id)
        libro = await self.repository.find_by_id(libro_id)
        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontro ningun libro con el ID: {libro_id}"
            )
        return libro

    async def modificar_libro(self, libro_id: str, libro_update: LibroUpdate) -> dict:
        """4. Modificar la informacion de un libro."""
        self._validar_object_id(libro_id)
        # Verificar existencia
        libro_actual = await self.obtener_libro_por_id(libro_id)

        update_data = libro_update.model_dump(exclude_unset=True)

        # Si se desea actualizar el ISBN, validar que no pertenezca a otro libro
        if "isbn" in update_data and update_data["isbn"]:
            nuevo_isbn = update_data["isbn"].strip()
            libro_con_mismo_isbn = await self.repository.find_by_isbn(nuevo_isbn)
            if libro_con_mismo_isbn and libro_con_mismo_isbn["id"] != libro_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"No se puede actualizar el ISBN a '{nuevo_isbn}' porque ya pertenece a otro libro."
                )
            update_data["isbn"] = nuevo_isbn

        updated_libro = await self.repository.update(libro_id, update_data)
        if not updated_libro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo actualizar el libro proporcionado."
            )
        return updated_libro

    async def eliminar_libro(self, libro_id: str) -> dict:
        """5. Eliminar un libro."""
        self._validar_object_id(libro_id)
        # Verificar existencia
        await self.obtener_libro_por_id(libro_id)
        eliminado = await self.repository.delete(libro_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al intentar eliminar el libro."
            )
        return {"mensaje": f"Libro con ID {libro_id} eliminado exitosamente"}

    async def buscar_libros(self, query: str) -> List[dict]:
        """6. Buscar libros por titulo o autor."""
        if not query or not query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parametro de busqueda 'q' no puede estar vacio."
            )
        return await self.repository.search_by_titulo_or_autor(query.strip())

    async def filtrar_por_genero(self, genero: str) -> List[dict]:
        """7. Filtrar libros por genero."""
        if not genero or not genero.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El genero no puede estar vacio."
            )
        return await self.repository.filter_by_genero(genero.strip())

    async def filtrar_por_disponibilidad(self, disponible: bool) -> List[dict]:
        """8. Filtrar libros por disponibilidad."""
        return await self.repository.filter_by_disponibilidad(disponible)

    async def filtrar_por_anio(self, anio: int) -> List[dict]:
        """9. Filtrar libros por ano de publicacion."""
        return await self.repository.filter_by_anio(anio)

    async def consultar_etiquetas(self, libro_id: str) -> dict:
        """10. Consultar las etiquetas asociadas a un libro."""
        self._validar_object_id(libro_id)
        etiquetas_info = await self.repository.get_etiquetas_by_id(libro_id)
        if not etiquetas_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontro ningun libro con el ID: {libro_id}"
            )
        return etiquetas_info

# Validated ObjectId and ISBN uniqueness constraint

