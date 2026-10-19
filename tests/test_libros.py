import pytest
from bson import ObjectId
from app.schemas.libro import LibroCreate, LibroUpdate, UbicacionSchema
from app.services.libro_service import LibroService
from fastapi import HTTPException


def test_libro_create_schema_validation():
    """Valida que el esquema de creacion de libro funcione correctamente con datos validos."""
    datos_libro = {
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "isbn": "978-8424116286",
        "genero": "Novela clasica",
        "anio_publicacion": 1605,
        "editorial": "Francisco de Robles",
        "disponible": True,
        "etiquetas": ["clasico", "literatura espanola", "siglo de oro"],
        "ubicacion": {
            "sala": "Sala A",
            "estante": "E-01"
        }
    }
    libro = LibroCreate(**datos_libro)
    assert libro.titulo == "Don Quijote de la Mancha"
    assert libro.autor == "Miguel de Cervantes"
    assert libro.ubicacion.sala == "Sala A"
    assert libro.ubicacion.estante == "E-01"
    assert len(libro.etiquetas) == 3


def test_invalid_object_id_validation():
    """Valida que el servicio lance HTTPException 400 cuando se le pasa un ObjectId invalido."""
    service = LibroService()
    invalid_id = "123-id-invalido"

    with pytest.raises(HTTPException) as exc_info:
        service._validar_object_id(invalid_id)

    assert exc_info.value.status_code == 400
    assert "no es un ObjectId valido" in exc_info.value.detail


def test_valid_object_id_validation():
    """Valida que un ObjectId valido de 24 caracteres hex sea aceptado sin excepcion."""
    service = LibroService()
    valid_id = str(ObjectId())
    # No debe levantar ninguna excepcion
    service._validar_object_id(valid_id)


def test_libro_update_partial_schema():
    """Valida que LibroUpdate permita campos opcionales."""
    update = LibroUpdate(disponible=False)
    assert update.disponible is False
    assert update.titulo is None
    assert update.ubicacion is None

