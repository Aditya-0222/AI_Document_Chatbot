from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from upload import router as upload_router
from routes_query import router as query_router
from indexer import index_documents, get_index_stats
from models import IndexResponse

app = FastAPI(
    title="Document Research & Theme Identification Chatbot",
    description="Upload documents and ask questions to extract insights and themes",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, tags=["Upload"])
app.include_router(query_router, tags=["Query"])

@app.get("/")
async def root():
    """Health check and welcome message"""
    return {
        "message": "Document Research & Theme Identification API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    from vector_db import collection_exists, get_collection_info
    
    stats = get_index_stats()
    collection_info = get_collection_info()
    
    return {
        "status": "healthy",
        "database": {
            "connected": collection_exists(),
            "collection_info": collection_info
        },
        "indexing": stats
    }

@app.post("/index", response_model=IndexResponse)
async def index_endpoint():
    """Manual indexing endpoint"""
    try:
        success = index_documents()
        if success:
            stats = get_index_stats()
            return IndexResponse(
                message="Documents indexed successfully",
                indexed_documents=stats["documents"],
                total_paragraphs=stats["paragraphs"]
            )
        else:
            return IndexResponse(
                message="Indexing failed",
                indexed_documents=0,
                total_paragraphs=0
            )
    except Exception as e:
        return IndexResponse(
            message=f"Indexing error: {str(e)}",
            indexed_documents=0,
            total_paragraphs=0
        )

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    from config import PROCESSED_DIR, UPLOAD_DIR
    
    processed_files = len(list(PROCESSED_DIR.glob("*.json")))
    uploaded_files = len(list(UPLOAD_DIR.glob("*")))
    index_stats = get_index_stats()
    
    return {
        "files": {
            "uploaded": uploaded_files,
            "processed": processed_files
        },
        "indexing": index_stats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)