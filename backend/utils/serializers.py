from bson import ObjectId


def serialize_doc(doc):
    """
    Serialize MongoDB document for JSON response.
    - Converts ObjectId to string
    - Renames _id to id for frontend compatibility
    - Recursively serializes nested objects and arrays
    """
    if not doc:
        return None
    result = {}
    for key, value in doc.items():
        # Rename _id to id for frontend compatibility
        output_key = "id" if key == "_id" else key
        
        if isinstance(value, ObjectId):
            result[output_key] = str(value)
        elif isinstance(value, list):
            result[output_key] = [serialize_doc(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, dict):
            result[output_key] = serialize_doc(value)
        else:
            result[output_key] = value
    return result
