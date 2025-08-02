from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def create_collection():
    """Create or recreate Qdrant collection"""
    try:
        qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=rest.VectorParams(size=384, distance=rest.Distance.COSINE)
        )
        print(f"✓ Created collection: {QDRANT_COLLECTION}")
        return True
    except Exception as e:
        print(f"✗ Error creating collection: {e}")
        return False

def collection_exists():
    """Check if collection exists"""
    try:
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]
        return QDRANT_COLLECTION in collection_names
    except Exception as e:
        print(f"✗ Error checking collection: {e}")
        return False

def get_collection_info():
    """Get collection information"""
    try:
        if collection_exists():
            info = qdrant_client.get_collection(QDRANT_COLLECTION)
            return {
                "name": info.config.params.collection_name,
                "vectors_count": info.vectors_count,
                "status": info.status
            }
        return None
    except Exception as e:
        print(f"✗ Error getting collection info: {e}")
        return None