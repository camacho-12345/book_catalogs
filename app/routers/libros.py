from typing import List
from fastapi import APIRouter, Depends, Query, status
from app.schemas.libro import (
    LibroCreate,
    LibroUpdate,
    LibroResponse,
    LibroEtiquetasResponse,
)
from app.services.libro_service import LibroService

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)

def get_service() -> LibroService:
    return LibroService()


# -------------------------------------------------------------
# 1. Registrar un nuevo libro
# -------------------------------------------------------------
@router.post(
    "",
    response_model=LibroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="1. Registrar un nuevo libro",
    description="Inserta un nuevo documento de libro en la coleccion con su ubicacion y etiquetas."
)
async def registrar_libro(
    libro_in: LibroCreate,
    service: LibroService = Depends(get_service)
):
    return await service.registrar_libro(libro_in)


# -------------------------------------------------------------
# 2. Listar todos los libros
# -------------------------------------------------------------
@router.get(
    "",
    response_model=List[LibroResponse],
    status_code=status.HTTP_200_OK,
    summary="2. Listar todos los libros",
    description="Obtiene el listado completo de libros con soporte para paginacion."
)
async def listar_libros(
    skip: int = Query(0, ge=0, description="Numero de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Limite maximo de registros a devolver"),
    service: LibroService = Depends(get_service)
):
    return await service.listar_libros(skip=skip, limit=limit)


# -------------------------------------------------------------
# 6. Buscar libros por titulo o autor
# (Definido antes de /{id} para evitar colisiones de rutas)
# -------------------------------------------------------------
@router.get(
    "/buscar",
    response_model=List[LibroResponse],
    status_code=status.HTTP_200_OK,
    summary="6. Buscar libros por titulo o autor",
    description="Realiza una busqueda parcial e insensible a mayusculas en los campos 'titulo' y 'autor'."
)
async def buscar_libros(
    q: str = Query(..., min_length=1, description="Texto a buscar en titulo o autor"),
    service: LibroService = Depends(get_service)
):
    return await service.buscar_libros(query=q)


# -------------------------------------------------------------
# 7. Filtrar libros por genero
# -------------------------------------------------------------
@router.get(
    "/filtrar/genero",
    response_model=List[LibroResponse],
    status_code=status.HTTP_200_OK,
    summary="7. Filtrar libros por genero",
    description="Devuelve todos los libros pertenecientes al genero especificado."
)
async def filtrar_por_genero(
    genero: str = Query(..., min_length=1, description="Genero literario (ej: Novela, Ficcion, etc.)"),
    service: LibroService = Depends(get_service)
):
    return await service.filtrar_por_genero(genero=genero)


# -------------------------------------------------------------
# 8. Filtrar libros por disponibilidad
# -------------------------------------------------------------
@router.get(
    "/filtrar/disponibilidad",
    response_model=List[LibroResponse],
    status_code=status.HTTP_200_OK,
    summary="8. Filtrar libros por disponibilidad",
    description="Filtra los libros segun esten disponibles para prestamo (true) o no (false)."
)
async def filtrar_por_disponibilidad(
    disponible: bool = Query(..., description="Estado de disponibilidad (true/false)"),
    service: LibroService = Depends(get_service)
):
    return await service.filtrar_por_disponibilidad(disponible=disponible)


# -------------------------------------------------------------
# 9. Filtrar libros por ano de publicacion
# -------------------------------------------------------------
@router.get(
    "/filtrar/anio",
    response_model=List[LibroResponse],
    status_code=status.HTTP_200_OK,
    summary="9. Filtrar libros por ano de publicacion",
    description="Filtra los libros publicados en un ano especifico."
)
async def filtrar_por_anio(
    anio: int = Query(..., ge=0, le=2100, description="Ano de publicacion"),
    service: LibroService = Depends(get_service)
):
    return await service.filtrar_por_anio(anio=anio)


# -------------------------------------------------------------
# 3. Consultar un libro mediante su identificador
# -------------------------------------------------------------
@router.get(
    "/{id}",
    response_model=LibroResponse,
    status_code=status.HTTP_200_OK,
    summary="3. Consultar un libro mediante su identificador",
    description="Busca y obtiene el detalle completo de un libro a partir de su ID de MongoDB."
)
async def obtener_libro(
    id: str,
    service: LibroService = Depends(get_service)
):
    return await service.obtener_libro_por_id(libro_id=id)


# -------------------------------------------------------------
# 4. Modificar la informacion de un libro (PUT / PATCH)
# -------------------------------------------------------------
@router.put(
    "/{id}",
    response_model=LibroResponse,
    status_code=status.HTTP_200_OK,
    summary="4. Modificar la informacion de un libro (Reemplazo / Actualizacion)",
    description="Actualiza la informacion de un libro existente especificado por su ID."
)
async def modificar_libro(
    id: str,
    libro_update: LibroUpdate,
    service: LibroService = Depends(get_service)
):
    return await service.modificar_libro(libro_id=id, libro_update=libro_update)


@router.patch(
    "/{id}",
    response_model=LibroResponse,
    status_code=status.HTTP_200_OK,
    summary="4b. Modificar parcialmente la informacion de un libro",
    description="Actualiza unicamente los campos provistos de un libro existente (ej. disponibilidad, ubicacion)."
)
async def modificar_libro_parcial(
    id: str,
    libro_update: LibroUpdate,
    service: LibroService = Depends(get_service)
):
    return await service.modificar_libro(libro_id=id, libro_update=libro_update)


# -------------------------------------------------------------
# 5. Eliminar un libro
# -------------------------------------------------------------
@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="5. Eliminar un libro",
    description="Elimina permanentemente un libro de la coleccion."
)
async def eliminar_libro(
    id: str,
    service: LibroService = Depends(get_service)
):
    return await service.eliminar_libro(libro_id=id)


# -------------------------------------------------------------
# 10. Consultar las etiquetas asociadas a un libro
# -------------------------------------------------------------
@router.get(
    "/{id}/etiquetas",
    response_model=LibroEtiquetasResponse,
    status_code=status.HTTP_200_OK,
    summary="10. Consultar las etiquetas asociadas a un libro",
    description="Retorna el listado de etiquetas asignadas al libro especificado."
)
async def consultar_etiquetas(
    id: str,
    service: LibroService = Depends(get_service)
):
    return await service.consultar_etiquetas(libro_id=id)
