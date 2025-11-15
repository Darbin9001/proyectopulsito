from bson import ObjectId

def serialize_mongo(document):
    """
    Convierte ObjectId y otros tipos no serializables a formatos JSON válidos.
    """
    if isinstance(document, list):
        return [serialize_mongo(doc) for doc in document]
    if isinstance(document, dict):
        return {k: serialize_mongo(v) for k, v in document.items()}
    if isinstance(document, ObjectId):
        return str(document)
    return document
