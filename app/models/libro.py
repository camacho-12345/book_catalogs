def libro_helper(libro: dict) -> dict:
    """Convierte un documento BSON de MongoDB a un diccionario compatible con LibroResponse."""
    if not libro:
        return None
    return {
        "id": str(libro["_id"]),
        "titulo": libro.get("titulo", ""),
        "autor": libro.get("autor", ""),
        "isbn": libro.get("isbn", ""),
        "genero": libro.get("genero", ""),
        "anio_publicacion": libro.get("anio_publicacion", 0),
        "editorial": libro.get("editorial", ""),
        "disponible": libro.get("disponible", True),
        "etiquetas": libro.get("etiquetas", []),
        "ubicacion": libro.get("ubicacion", {"sala": "", "estante": ""})
    }
