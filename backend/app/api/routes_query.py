from fastapi import APIRouter, HTTPException
from models import QueryRequest, QueryResponse
from query_handler import process_query

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Handle user queries and return citations with theme analysis
    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        result = process_query(request.question)
        
        return QueryResponse(
            citations=result["citations"],
            themes=result["themes"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/search")
async def search_endpoint(q: str, top_k: int = 10):
    """
    Direct search endpoint for testing
    """
    try:
        from search import search_documents
        results = search_documents(q, top_k)
        return {"query": q, "results": results}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}"
        )