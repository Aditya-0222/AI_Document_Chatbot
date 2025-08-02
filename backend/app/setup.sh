#!/bin/bash

# Setup script for Document Research & Theme Identification Chatbot

echo "🚀 Setting up Document Research & Theme Identification Chatbot..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p data/uploads
mkdir -p data/processed

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Tesseract is installed
echo "🔍 Checking Tesseract OCR installation..."
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR is installed"
    tesseract --version
else
    echo "❌ Tesseract OCR is not installed"
    echo "Please install Tesseract OCR:"
    echo "  - Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "  - macOS: brew install tesseract"
    echo "  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
fi

# Check if Docker is available for Qdrant
echo "🐳 Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
    
    # Check if Qdrant is already running
    if ! curl -s http://localhost:6333 > /dev/null; then
        echo "🔄 Starting Qdrant vector database..."
        docker run -d -p 6333:6333 -v $(pwd)/qdrant_data:/qdrant/storage qdrant/qdrant
        sleep 5
        
        if curl -s http://localhost:6333 > /dev/null; then
            echo "✅ Qdrant is running on port 6333"
        else
            echo "❌ Failed to start Qdrant"
        fi
    else
        echo "✅ Qdrant is already running on port 6333"
    fi
else
    echo "❌ Docker is not installed"
    echo "Please install Docker or use Qdrant Cloud"
fi

# Check environment configuration
echo "⚙️  Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found, copying from .env.example"
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Start the backend: python main.py"
echo "3. Start the frontend: streamlit run app.py"
echo ""
echo "📚 Documentation: See README.md for detailed instructions"