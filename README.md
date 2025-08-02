# 📄 Document Research & Theme Identification Chatbot

> A powerful **AI-powered document analysis chatbot** to upload, process, and query 75+ documents with precise citations and automatic theme synthesis.

![Chatbot Banner]([https://via.placeholder.com/800x200?text=Document+QA+Chatbot](https://www.shutterstock.com/image-vector/engaging-image-robot-ai-assistant-600nw-2442410769.jpg))


---

## 🎯 Features

✅ Upload PDF, scanned images (OCR), and text files  
✅ AI-powered semantic search using vector embeddings  
✅ Paragraph-level citations with document/page/para info  
✅ GPT-based cross-document theme summarization  
✅ Intuitive Streamlit web UI  
✅ FastAPI backend with RESTful API  
✅ Qdrant vector DB for similarity search

---

## 🧱 Tech Stack

| Layer         | Tech Stack                            |
|--------------|----------------------------------------|
| 🧠 LLM        | OpenAI GPT-3.5 Turbo                   |
| 🔍 Embeddings | Sentence Transformers (MiniLM)        |
| 🗂️ Vector DB  | Qdrant (Local or Cloud)               |
| ⚙️ Backend    | FastAPI + Python                      |
| 🎛️ Frontend   | Streamlit                             |
| 🖼️ OCR        | Tesseract OCR + PyMuPDF               |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

├── app.py # Streamlit Frontend
├── main.py # FastAPI Backend Entrypoint
├── config.py # Centralized Configuration
├── models.py # Pydantic Data Models
├── query_handler.py # GPT Theme Analyzer
├── vector_db.py # Qdrant Collection Helpers
├── upload.py # File Upload + Text Extraction
├── indexer.py # Document Indexing Logic
├── search.py # Semantic Search Logic
├── routes_query.py # FastAPI Query Endpoint
├── requirements.txt # All dependencies
├── .env.example # Sample Env Configuration
├── setup.sh # Setup automation script
├── README.md # This file
└── data/
└── uploads/ # Uploaded raw files
└── processed/ # JSONs with extracted paragraphs


</details>

---

## ⚙️ Installation Guide

### 1. 📦 Clone Repository

```bash
git clone https://github.com/yourusername/document-qa-chatbot.git
cd document-qa-chatbot
```

2. 🧪 Install Dependencies
```bash
pip install -r requirements.txt
```

3. 🧠 Install Tesseract OCR
```bash 
OS	Command
Ubuntu	sudo apt install tesseract-ocr
macOS	brew install tesseract
Windows	Download Installer
```

4. 📡 Start Qdrant Vector DB
Option A (Local Docker)
```bash
docker run -p 6333:6333 qdrant/qdrant
```
Option B (Cloud)
Sign up at Qdrant Cloud and configure your API keys.

🔐 Environment Variables
```bash
cp .env.example .env
```

Update .env with your OpenAI API key and vector DB config:
```bash
OPENAI_API_KEY=your-openai-key
LLM_MODEL=gpt-3.5-turbo
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
```
🚀 Getting Started
Start Backend (FastAPI)
```bash
python main.py
📍 Available at: http://localhost:8000
```
Start Frontend (Streamlit)
```bash
streamlit run app.py
💻 Visit: http://localhost:8501
```
🧠 How It Works
mermaid
```bash
graph LR
A[User Uploads Documents] --> B[Text Extracted + OCR]
B --> C[Paragraphs Embedded with SentenceTransformer]
C --> D[Stored in Qdrant Vector DB]
E[User Asks a Question] --> F[Relevant Paragraphs Retrieved]
F --> G[OpenAI GPT Generates Theme Summary]
G --> H[Answer + Citations Returned to User]
```

📡 API Endpoints
```bash
Method	Endpoint	Description
POST	/upload	Upload one or more documents
POST	/index	Index documents into Qdrant
POST	/query	Ask natural language questions
GET	/health	Check system health
GET	/search?q=...	Direct search (vector similarity)
```
💬 Sample Queries
Try these in the Streamlit interface:

"What are the main findings across all documents?"

"Summarize the healthcare trends discussed."

"Which documents mention AI in education?"

"What themes emerge from 2023 whitepapers?"

📸 Screenshots
![Alt Text](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/6876d204-51c9-4561-878b-d554a94af980.png)
![Alt Text](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/6998a351-4e02-4121-98d4-74e3575bb27b.png)
![Alt Text](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/c5048e45-00bf-4674-ba8a-b1fafffcf4b2.png)



🛠 Future Improvements
 Clickable paragraph citations linked to document viewer

 Metadata filtering by author, type, date

 Export results to CSV/PDF

 Summarization with confidence scores

🧑‍💻 Contributing
Pull requests are welcome! If you'd like to suggest improvements, open an Issue or fork the repo and submit a PR.

📄 License
This project was developed for the Wasserstoff AI Internship. For research and educational use only.
For commercial usage, contact the project owner.

🙌 Acknowledgements
Wasserstoff

Qdrant

OpenAI

Streamlit

Tesseract OCR


---

### ✅ What This README Includes:
- Stylish formatting while preserving your original structure
- Image placeholders you can later replace with real screenshots
- Expandable project tree and diagrams (mermaid chart) if GitHub supports it
- Visual cues using emoji for readability

Let me know if you want:
- A downloadable `.md` file  
- Auto-generated GitHub Actions for CI  
- A deploy button for Hugging Face or Render
