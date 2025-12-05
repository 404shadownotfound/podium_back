from bson import ObjectId
from datetime import datetime

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    
    # Rename _id to id for cleaner API
    if '_id' in serialized:
        serialized['id'] = serialized.pop('_id')
    
    return serialized
