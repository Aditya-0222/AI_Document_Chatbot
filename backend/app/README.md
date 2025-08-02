# Document Research & Theme Identification Chatbot

A powerful AI-powered document analysis system that allows users to upload multiple documents, extract insights, and perform theme-based analysis through natural language queries.

## Features

- **Multi-format Document Support**: PDF, images (PNG, JPG, JPEG, BMP, TIFF), and text files
- **Advanced Text Extraction**: OCR for scanned documents and images
- **Vector-based Search**: Semantic search using sentence transformers and Qdrant vector database
- **Theme Analysis**: AI-powered synthesis of information across multiple documents
- **Web Interface**: User-friendly Streamlit frontend
- **RESTful API**: FastAPI backend with comprehensive endpoints

## Architecture

- **Frontend**: Streamlit web application
- **Backend**: FastAPI with async support
- **Vector Database**: Qdrant for semantic search
- **Text Processing**: PyMuPDF for PDFs, Tesseract OCR for images
- **AI**: OpenAI GPT for theme analysis and synthesis
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)

## Prerequisites

- Python 3.8+
- Docker (for Qdrant)
- Tesseract OCR
- OpenAI API key

## Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd document-qa-chatbot
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 3. Setup Qdrant Vector Database

**Option A: Local Docker**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Qdrant Cloud**
1. Sign up at https://cloud.qdrant.io/
2. Create a cluster
3. Get API key and cluster URL

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

Required environment variables:
```
OPENAI_API_KEY=your-openai-api-key
LLM_MODEL=gpt-3.5-turbo
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
```

## Usage

### 1. Start the Backend

```bash
python main.py
```

The API will be available at http://localhost:8000

### 2. Start the Frontend

```bash
streamlit run app.py
```

The web interface will be available at http://localhost:8501

### 3. Using the System

1. **Upload Documents**: Use the web interface to upload PDF, image, or text files
2. **Wait for Processing**: Files are automatically processed and text extracted
3. **Index Documents**: Documents are automatically indexed for search
4. **Ask Questions**: Enter natural language questions about your documents
5. **Review Results**: See individual document citations and synthesized theme analysis

## API Endpoints

### Document Upload
```http
POST /upload
Content-Type: multipart/form-data

Upload multiple files for processing
```

### Query Documents
```http
POST /query
Content-Type: application/json

{
  "question": "What are the main themes in the documents?"
}
```

### Index Documents
```http
POST /index

Manually trigger document indexing
```

### Health Check
```http
GET /health

Get system status and statistics
```

## File Structure

```
project/
├── main.py              # FastAPI application
├── app.py               # Streamlit frontend
├── config.py            # Configuration settings
├── models.py            # Pydantic models
├── vector_db.py         # Qdrant database operations
├── upload.py            # File upload and processing
├── search.py            # Document search functionality
├── query_handler.py     # Query processing and AI analysis
├── routes_query.py      # Query API endpoints
├── indexer.py           # Document indexing utilities
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── data/
    ├── uploads/         # Raw uploaded files
    └── processed/       # Processed JSON documents
```

## Key Features Explained

### Document Processing
- **PDF**: Text extraction with OCR fallback for scanned pages
- **Images**: Full OCR text extraction
- **Text Files**: Paragraph-based splitting
- **Metadata**: Page and paragraph numbering for precise citations

### Vector Search
- Uses sentence-transformers for embedding generation
- Qdrant vector database for fast similarity search
- Cosine similarity for semantic matching

### Theme Analysis
- OpenAI GPT models for intelligent synthesis
- Cross-document pattern recognition
- Structured theme identification
- Citation-backed analysis

### Error Handling
- Comprehensive error handling and logging
- Graceful degradation for missing services
- User-friendly error messages

## Deployment

### Production Considerations

1. **Security**: Configure CORS origins, add authentication
2. **Database**: Use persistent Qdrant storage
3. **Scaling**: Consider horizontal scaling for high loads
4. **Monitoring**: Add logging and monitoring systems

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **OCR Not Working**: Ensure Tesseract is installed and in PATH
2. **Qdrant Connection**: Check if Qdrant is running on the correct port
3. **OpenAI API**: Verify API key and sufficient credits
4. **File Upload Fails**: Check file size limits and supported formats

### Performance Optimization

- Use GPU-enabled embeddings for faster processing
- Implement batch processing for large document sets
- Cache embeddings to avoid recomputation
- Use async processing for file uploads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Create an issue on GitHub