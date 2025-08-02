from openai import OpenAI
from search import search_documents
from config import OPENAI_API_KEY, LLM_MODEL
from models import QueryResponse, Citation

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def process_query(question: str) -> dict:
    """
    Process user query and return citations with theme analysis
    """
    # Step 1: Search for relevant documents
    search_results = search_documents(question, top_k=15)
    
    if not search_results:
        return {
            "citations": [],
            "themes": "No relevant documents found for your query. Please ensure documents are uploaded and indexed."
        }
    
    # Step 2: Format citations
    citations = []
    context_texts = []
    
    for result in search_results:
        # Truncate long text for display
        display_text = result['text']
        if len(display_text) > 300:
            display_text = display_text[:300] + "..."
        
        citations.append({
            "doc_id": result['doc_id'],
            "filename": result['filename'],
            "page": result['page'],
            "para_num": result['para_num'],
            "text": display_text
        })
        
        # Keep full text for theme analysis
        context_texts.append(result['text'])
    
    # Step 3: Generate theme analysis
    theme_analysis = generate_theme_analysis(question, context_texts, citations)
    
    return {
        "citations": citations,
        "themes": theme_analysis
    }

def generate_theme_analysis(question: str, contexts: list, citations: list) -> str:
    """
    Generate comprehensive theme analysis using OpenAI
    """
    if not contexts:
        return "No content available for theme analysis."
    
    # Limit context to avoid token limits
    limited_contexts = contexts[:8]  # Use top 8 results
    
    # Build context string with document references
    context_string = ""
    for i, text in enumerate(limited_contexts, 1):
        context_string += f"\\n\\n[Document {i}] {text[:500]}..."
    
    system_prompt = """You are an expert document analyst specializing in theme identification and synthesis. 

Your task is to:
1. Answer the user's question comprehensively
2. Identify 2-4 main themes from the provided document excerpts
3. Synthesize information across documents to show relationships and patterns
4. Reference specific documents when making claims
5. Provide actionable insights where possible

Format your response with clear sections:
- **Direct Answer**: Address the specific question
- **Key Themes**: List and explain main themes found
- **Cross-Document Analysis**: Show how different documents relate
- **Summary**: Provide key takeaways"""

    user_prompt = f"""Based on the following document excerpts, provide a comprehensive analysis for this question:

**Question:** {question}

**Document Excerpts:**{context_string}

Please provide a thorough theme-based analysis following the format specified in your instructions."""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"""**Analysis Error**: Unable to generate theme analysis due to: {str(e)}

**Basic Summary**: Found {len(citations)} relevant document sections that may help answer your question about: "{question}"

**Suggestions**: 
- Verify your OpenAI API key is configured correctly
- Check if you have sufficient API credits
- Try rephrasing your question for better results"""

def quick_answer(question: str) -> str:
    """
    Generate a quick answer without full theme analysis
    """
    search_results = search_documents(question, top_k=5)
    
    if not search_results:
        return "No relevant information found."
    
    # Combine top results
    combined_text = " ".join([result['text'][:200] for result in search_results[:3]])
    
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide a concise answer based on the given context."},
                {"role": "user", "content": f"Question: {question}\\n\\nContext: {combined_text}\\n\\nAnswer:"}
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to generate answer: {str(e)}"