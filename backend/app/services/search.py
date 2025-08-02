from vector_db import embedding_model, qdrant_client, QDRANT_COLLECTION, collection_exists

def search_documents(query: str, top_k: int = 10):
    """Search documents using vector similarity"""
    
    if not collection_exists():
        return []
    
    try:
        # Generate query embedding
        query_vector = embedding_model.encode(query).tolist()
        
        # Search in Qdrant
        results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        # Format results
        formatted_results = []
        for hit in results:
            payload = hit.payload
            formatted_results.append({
                "doc_id": payload.get("doc_id"),
                "filename": payload.get("filename"),
                "page": payload.get("page"),
                "para_num": payload.get("para_num"),
                "text": payload.get("text"),
                "score": hit.score
            })
        
        return formatted_results
    
    except Exception as e:
        print(f"Error searching documents: {e}")
        return []

def search_by_document_id(doc_id: str):
    """Get all paragraphs from a specific document"""
    
    if not collection_exists():
        return []
    
    try:
        # Search with filter for specific document
        results = qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION,
            scroll_filter=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="doc_id",
                        match=rest.MatchValue(value=doc_id)
                    )
                ]
            ),
            with_payload=True,
            limit=1000
        )
        
        # Format results
        formatted_results = []
        for hit in results[0]:  # results is tuple (points, next_page_offset)
            payload = hit.payload
            formatted_results.append({
                "doc_id": payload.get("doc_id"),
                "filename": payload.get("filename"),
                "page": payload.get("page"),
                "para_num": payload.get("para_num"),
                "text": payload.get("text")
            })
        
        # Sort by page and paragraph number
        formatted_results.sort(key=lambda x: (x["page"], x["para_num"]))
        return formatted_results
    
    except Exception as e:
        print(f"Error searching by document ID: {e}")
        return []