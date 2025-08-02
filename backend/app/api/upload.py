from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List
from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import uuid
import json
from config import UPLOAD_DIR, PROCESSED_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from models import UploadResponse, UploadedDocument

router = APIRouter()

def extract_text_from_pdf(file_path: Path) -> List[dict]:
    """Extract text from PDF using PyMuPDF with OCR fallback"""
    try:
        doc = fitz.open(str(file_path))
        paragraphs = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text").strip()
            
            # If no text found, use OCR
            if not text:
                try:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img).strip()
                except Exception as ocr_error:
                    print(f"OCR failed for page {page_num + 1}: {ocr_error}")
                    continue
            
            # Split into paragraphs
            para_list = [p.strip() for p in text.split('\\n') if p.strip() and len(p.strip()) > 20]
            
            for i, para_text in enumerate(para_list):
                paragraphs.append({
                    "page": page_num + 1,
                    "para_num": i + 1,
                    "text": para_text
                })
        
        doc.close()
        return paragraphs
    
    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return []

def extract_text_from_image(file_path: Path) -> List[dict]:
    """Extract text from image using OCR"""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img).strip()
        
        if text:
            return [{
                "page": 1,
                "para_num": 1,
                "text": text
            }]
        return []
    
    except Exception as e:
        print(f"Error processing image {file_path}: {e}")
        return []

def extract_text_from_txt(file_path: Path) -> List[dict]:
    """Extract text from plain text file"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Split by double newlines for paragraphs
        para_list = [p.strip() for p in content.split('\\n\\n') if p.strip() and len(p.strip()) > 20]
        
        paragraphs = []
        for i, para in enumerate(para_list):
            paragraphs.append({
                "page": 1,
                "para_num": i + 1,
                "text": para
            })
        
        return paragraphs
    
    except Exception as e:
        print(f"Error processing text file {file_path}: {e}")
        return []

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process multiple documents"""
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_docs = []
    
    for file in files:
        try:
            # Validate file
            if not file.filename:
                continue
            
            suffix = Path(file.filename).suffix.lower()
            if suffix not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=415, 
                    detail=f"Unsupported file type: {suffix}. Allowed: {ALLOWED_EXTENSIONS}"
                )
            
            # Check file size
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"File {file.filename} too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB"
                )
            
            # Save file
            unique_id = str(uuid.uuid4())[:8]
            safe_filename = f"{unique_id}_{file.filename}"
            save_path = UPLOAD_DIR / safe_filename
            
            with open(save_path, "wb") as buffer:
                buffer.write(content)
            
            # Extract text based on file type
            paragraphs = []
            if suffix == ".pdf":
                paragraphs = extract_text_from_pdf(save_path)
            elif suffix in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
                paragraphs = extract_text_from_image(save_path)
            elif suffix == ".txt":
                paragraphs = extract_text_from_txt(save_path)
            
            if not paragraphs:
                print(f"Warning: No text extracted from {file.filename}")
                continue
            
            # Save processed data as JSON
            doc_id = unique_id.upper()
            doc_json = {
                "doc_id": doc_id,
                "filename": file.filename,
                "original_path": str(save_path),
                "paragraphs": paragraphs
            }
            
            json_path = PROCESSED_DIR / f"{doc_id}.json"
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(doc_json, jf, indent=2, ensure_ascii=False)
            
            uploaded_docs.append(UploadedDocument(
                doc_id=doc_id,
                filename=file.filename,
                paragraph_count=len(paragraphs)
            ))
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process {file.filename}: {str(e)}"
            )
    
    if not uploaded_docs:
        raise HTTPException(
            status_code=400,
            detail="No documents were successfully processed"
        )
    
    return UploadResponse(
        uploaded_documents=uploaded_docs,
        message=f"Successfully uploaded and processed {len(uploaded_docs)} documents"
    )