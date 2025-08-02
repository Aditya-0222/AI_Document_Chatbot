import os
import json
from pathlib import Path
from vector_db import embedding_model, qdrant_client, QDRANT_COLLECTION, create_collection, collection_exists
from qdrant_client.http import models as rest
from config import PROCESSED_DIR

def load_documents():
    """Load all processed JSON documents"""
    json_files = list(PROCESSED_DIR.glob("*.json"))
    documents = []
    
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
                documents.append(doc)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return documents

def index_documents():
    """Index all documents into Qdrant vector database"""
    print("Starting document indexing...")
    
    # Ensure collection exists
    if not collection_exists():
        if not create_collection():
            return False
    
    # Load documents
    documents = load_documents()
    if not documents:
        print("No documents found to index")
        return False
    
    total_points = 0
    
    for doc in documents:
        try:
            doc_id = doc["doc_id"]
            filename = doc["filename"]
            paragraphs = doc["paragraphs"]
            
            # Create vectors and payloads for each paragraph
            points = []
            
            for i, para in enumerate(paragraphs):
                text = para["text"]
                if len(text.strip()) < 10:  # Skip very short texts
                    continue
                
                # Generate embedding
                vector = embedding_model.encode(text).tolist()
                
                # Create point
                point = rest.PointStruct(
                    id=f"{doc_id}_{i}",
                    vector=vector,
                    payload={
                        "doc_id": doc_id,
                        "filename": filename,
                        "page": para["page"],
                        "para_num": para["para_num"],
                        "text": text
                    }
                )
                points.append(point)
            
            # Upsert points to Qdrant
            if points:
                qdrant_client.upsert(
                    collection_name=QDRANT_COLLECTION,
                    points=points
                )
                total_points += len(points)
                print(f"✓ Indexed {len(points)} paragraphs from {filename}")
        
        except Exception as e:
            print(f"✗ Error indexing document {doc.get('filename', 'unknown')}: {e}")
    
    print(f"✅ Indexing complete! Total points indexed: {total_points}")
    return True

def get_index_stats():
    """Get indexing statistics"""
    try:
        if not collection_exists():
            return {"indexed": False, "documents": 0, "paragraphs": 0}
        
        info = qdrant_client.get_collection(QDRANT_COLLECTION)
        documents = load_documents()
        
        return {
            "indexed": True,
            "documents": len(documents),
            "paragraphs": info.vectors_count or 0
        }
    except Exception as e:
        print(f"Error getting index stats: {e}")
        return {"indexed": False, "documents": 0, "paragraphs": 0}

if __name__ == "__main__":
    success = index_documents()
    if success:
        stats = get_index_stats()
        print(f"Final stats: {stats}")
    else:
        print("Indexing failed!")