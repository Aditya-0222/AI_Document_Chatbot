from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str

class Citation(BaseModel):
    doc_id: str
    filename: str
    page: int
    para_num: int
    text: str

class QueryResponse(BaseModel):
    citations: List[Citation]
    themes: str

class UploadedDocument(BaseModel):
    doc_id: str
    filename: str
    paragraph_count: int

class UploadResponse(BaseModel):
    uploaded_documents: List[UploadedDocument]
    message: str

class IndexResponse(BaseModel):
    message: str
    indexed_documents: int
    total_paragraphs: int