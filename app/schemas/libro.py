from typing import List, Optional
from pydantic import BaseModel, Field


class UbicacionSchema(BaseModel):
    """Subdocumento para la localizacion fisica del libro."""
    sala: str = Field(..., description="Nombre o numero de la sala")
    estante: str = Field(..., description="Identificador del estante")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sala": "Sala Principal A",
                "estante": "E-12"
            }
        }
    }


class LibroBase(BaseModel):
    """Esquema base con los atributos del libro."""
    titulo: str = Field(..., min_length=1, description="Titulo de la obra")
    autor: str = Field(..., min_length=1, description="Nombre del autor")
    isbn: str = Field(..., description="Codigo ISBN unico")
    genero: str = Field(..., description="Genero literario")
    anio_publicacion: int = Field(..., ge=0, le=2100, description="Ano de publicacion")
    editorial: str = Field(..., description="Casa editorial")
    disponible: bool = Field(default=True, description="Indica si esta disponible para prestamo")
    etiquetas: List[str] = Field(default_factory=list, description="Lista de etiquetas descriptivas")
    ubicacion: UbicacionSchema = Field(..., description="Ubicacion fisica dentro de la biblioteca")


class LibroCreate(LibroBase):
    """Esquema utilizado para registrar un nuevo libro."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "titulo": "Cien anos de soledad",
                "autor": "Gabriel Garcia Marquez",
                "isbn": "978-0307474728",
                "genero": "Realismo Magico",
                "anio_publicacion": 1967,
                "editorial": "Editorial Sudamericana",
                "disponible": True,
                "etiquetas": ["clasico", "literatura latinoamericana", "premio nobel"],
                "ubicacion": {
                    "sala": "Sala 1",
                    "estante": "Estante B-4"
                }
            }
        }
    }


class LibroUpdate(BaseModel):
    """Esquema para modificar los datos de un libro existente (campos opcionales)."""
    titulo: Optional[str] = Field(None, min_length=1)
    autor: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = None
    genero: Optional[str] = None
    anio_publicacion: Optional[int] = Field(None, ge=0, le=2100)
    editorial: Optional[str] = None
    disponible: Optional[bool] = None
    etiquetas: Optional[List[str]] = None
    ubicacion: Optional[UbicacionSchema] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "disponible": False,
                "ubicacion": {
                    "sala": "Sala de Reserva",
                    "estante": "Estante R-1"
                }
            }
        }
    }


class LibroResponse(LibroBase):
    """Esquema devuelto por los endpoints que representa un libro con su ID."""
    id: str = Field(..., description="Identificador unico del libro (MongoDB ObjectId en formato string)")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "660c1d5f8a4e3c0012a4b891",
                "titulo": "Cien anos de soledad",
                "autor": "Gabriel Garcia Marquez",
                "isbn": "978-0307474728",
                "genero": "Realismo Magico",
                "anio_publicacion": 1967,
                "editorial": "Editorial Sudamericana",
                "disponible": True,
                "etiquetas": ["clasico", "literatura latinoamericana", "premio nobel"],
                "ubicacion": {
                    "sala": "Sala 1",
                    "estante": "Estante B-4"
                }
            }
        }
    }


class LibroEtiquetasResponse(BaseModel):
    """Esquema de respuesta para la consulta de etiquetas de un libro."""
    id: str
    titulo: str
    etiquetas: List[str]
