📄 Document Research & Theme Identification Chatbot
An advanced AI-powered document analysis tool built during the Wasserstoff AI Internship. This chatbot allows users to upload documents (PDFs, scans, text), ask natural language questions, and receive answer citations with automated theme identification across all documents.

🚀 Features
✅ Multi-format Document Upload – Supports PDF, scanned images (OCR), and text files

🧠 AI-powered Semantic Search – Uses sentence-transformers + Qdrant for vector search

📚 Citation-Based QA – Returns accurate answers with doc ID, page, and paragraph

🧵 Theme Identification – Synthesizes key themes across documents using GPT

💬 Simple UI – Clean, Streamlit-based frontend with file upload & query interface

📦 Modular FastAPI Backend – With clearly separated services and API routes

📊 System Health Dashboard – Shows indexing status, document count, etc.

🧱 Tech Stack
Layer	Technology
Backend	FastAPI, Python
Frontend	Streamlit
OCR Engine	Tesseract
Document Parsing	PyMuPDF
Embeddings	Sentence Transformers (MiniLM)
Vector DB	Qdrant (Local or Cloud)
LLMs	OpenAI GPT-3.5 Turbo

📂 Project Structure
├── app.py                  # Streamlit Frontend
├── main.py                 # FastAPI Backend Entrypoint
├── config.py               # Centralized Configuration
├── models.py               # Pydantic Data Models
├── query_handler.py        # GPT Theme Analyzer
├── vector_db.py            # Qdrant Collection Helpers
├── upload.py               # File Upload + Text Extraction
├── indexer.py              # Document Indexing Logic
├── search.py               # Semantic Search Logic
├── routes_query.py         # FastAPI Query Endpoint
├── requirements.txt        # All dependencies
├── .env.example            # Sample Env Configuration
├── setup.sh                # Setup automation script
├── README.md               # This file
└── data/
    └── uploads/            # Uploaded raw files
    └── processed/          # JSONs with extracted paragraphs
⚙️ Installation Guide
1. Clone Repository
git clone https://github.com/yourusername/document-qa-chatbot.git
cd document-qa-chatbot
3. Install Dependencies

pip install -r requirements.txt
4. Install Tesseract OCR
Ubuntu/Debian:


sudo apt install tesseract-ocr
macOS (Homebrew):


brew install tesseract
Windows:
Download from: https://github.com/UB-Mannheim/tesseract/wiki

4. Start Qdrant (Choose One)
Local via Docker:


docker run -p 6333:6333 qdrant/qdrant
Or use Qdrant Cloud

🔐 Environment Setup
Copy and update your .env:


cp .env.example .env
Edit .env:

env

OPENAI_API_KEY=your-openai-api-key
LLM_MODEL=gpt-3.5-turbo
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
🧪 Quick Start
1. Run Backend (FastAPI)
python main.py
Available at: http://localhost:8000

3. Run Frontend (Streamlit)
streamlit run app.py
Available at: http://localhost:8501

💬 Example Queries
"Summarize the main findings across all research papers."

"What themes are common across the 2023 case studies?"

"What are the conclusions about healthcare AI?"

✅ Core API Endpoints
Method	Endpoint	Description
POST	/upload	Upload one or more documents
POST	/index	Index all processed documents
POST	/query	Ask natural language questions
GET	/health	System health check
GET	/search?q=...	Run direct semantic search query

🧠 How Theme Identification Works
User submits question

Top-matching paragraphs are retrieved via Qdrant

OpenAI GPT is prompted with top texts to summarize

Final response includes:

Individual citations with paragraph/page/doc info

Summary of themes extracted from context

📸 Screenshots
(Add Streamlit UI screenshots here to make it visually appealing)

🧰 Optional Enhancements
 Paragraph/sentence-level citation mapping

 Visual clickable themes → docs

 Metadata filters (date, author, tags)

 Export answers to PDF/CSV

🧑‍💻 Contributing
Pull requests are welcome. For significant changes, please open an issue first to discuss what you'd like to change.

📄 License
This project is for educational/research purposes under the Wasserstoff AI Internship. For any commercial use, please contact the project owner.

Let me know if you'd like this as a downloadable .md file or want to include deployment instructions for platforms like Render or Hugging Face Spaces.
