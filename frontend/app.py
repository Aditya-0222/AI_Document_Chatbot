import streamlit as st
import requests
import pandas as pd
import json

# Configuration
BACKEND_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Document Q&A Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Research & Theme Identification Chatbot")
st.markdown("Upload documents and ask questions to extract insights and themes from your content.")

# Sidebar for system status
with st.sidebar:
    st.header("🔧 System Status")
    
    try:
        health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ Backend Connected")
            
            # Display database status
            if health_data.get("database", {}).get("connected"):
                st.success("✅ Database Connected")
                
                # Show indexing stats
                indexing = health_data.get("indexing", {})
                if indexing.get("indexed"):
                    st.info(f"📊 {indexing.get('documents', 0)} documents indexed")
                    st.info(f"📝 {indexing.get('paragraphs', 0)} paragraphs searchable")
                else:
                    st.warning("⚠️ No documents indexed")
            else:
                st.error("❌ Database Issues")
        else:
            st.error("❌ Backend Issues")
    except requests.exceptions.RequestException:
        st.error("❌ Backend Offline")
    
    # Instructions
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload Documents**: Select PDFs, images, or text files
    2. **Wait for Processing**: Files are automatically processed
    3. **Index Documents**: Click to make documents searchable
    4. **Ask Questions**: Enter natural language questions
    5. **Review Results**: See citations and theme analysis
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'png', 'jpg', 'jpeg', 'txt', 'bmp', 'tiff'],
        accept_multiple_files=True,
        help="Upload PDFs, images, or text files for analysis"
    )
    
    if uploaded_files:
        st.info(f"Selected {len(uploaded_files)} files")
        
        if st.button("📤 Upload Files", type="primary"):
            # Prepare files for upload
            files_payload = []
            progress_bar = st.progress(0, text="Preparing files...")
            
            for i, file in enumerate(uploaded_files):
                files_payload.append(("files", (file.name, file.getvalue(), file.type)))
                progress_bar.progress((i + 1) / len(uploaded_files), text=f"Preparing {file.name}...")
            
            # Upload files
            try:
                with st.spinner("Uploading files..."):
                    response = requests.post(f"{BACKEND_URL}/upload", files=files_payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Successfully uploaded {len(result['uploaded_documents'])} documents!")
                    
                    # Display upload results
                    upload_df = pd.DataFrame(result['uploaded_documents'])
                    st.dataframe(upload_df, use_container_width=True)
                    
                    # Auto-index documents
                    with st.spinner("Indexing documents for search..."):
                        index_response = requests.post(f"{BACKEND_URL}/index")
                        if index_response.status_code == 200:
                            index_result = index_response.json()
                            st.success(f"✅ Indexed {index_result['total_paragraphs']} paragraphs from {index_result['indexed_documents']} documents")
                        else:
                            st.warning("⚠️ Upload successful, but indexing failed. Use manual indexing below.")
                
                else:
                    st.error(f"❌ Upload failed: {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
            
            progress_bar.empty()

with col2:
    st.header("🔍 Manual Operations")
    
    # Manual indexing
    st.subheader("Index Documents")
    st.write("Make uploaded documents searchable")
    
    if st.button("🔄 Index All Documents"):
        try:
            with st.spinner("Indexing documents..."):
                response = requests.post(f"{BACKEND_URL}/index")
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(result['message'])
                    st.info(f"📊 Indexed: {result['indexed_documents']} documents, {result['total_paragraphs']} paragraphs")
                else:
                    st.error("❌ Indexing failed")
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {str(e)}")
    
    # System stats
    st.subheader("System Statistics")
    if st.button("📊 Get Stats"):
        try:
            response = requests.get(f"{BACKEND_URL}/stats")
            if response.status_code == 200:
                stats = response.json()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Uploaded Files", stats['files']['uploaded'])
                    st.metric("Processed Files", stats['files']['processed'])
                
                with col_b:
                    st.metric("Indexed Documents", stats['indexing']['documents'])
                    st.metric("Searchable Paragraphs", stats['indexing']['paragraphs'])
        except:
            st.error("❌ Could not fetch statistics")

# Question and Answer Section
st.header("❓ Ask Questions")

question = st.text_input(
    "Enter your question about the documents:",
    placeholder="e.g., What are the main themes discussed in the documents?",
    help="Ask natural language questions about your uploaded documents"
)

if st.button("🔍 Ask Question", type="primary") and question:
    try:
        with st.spinner("Processing your question..."):
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"question": question}
            )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["📑 Citations", "🧠 Theme Analysis"])
            
            with tab1:
                st.subheader("Document Citations")
                
                if result.get("citations"):
                    citations_df = pd.DataFrame(result["citations"])
                    
                    # Rename columns for better display
                    display_df = citations_df.rename(columns={
                        "doc_id": "Doc ID",
                        "filename": "Filename",
                        "page": "Page",
                        "para_num": "Paragraph",
                        "text": "Relevant Text"
                    })
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Download option
                    csv = citations_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Citations as CSV",
                        data=csv,
                        file_name=f"citations_{question[:30]}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No citations found for your question.")
            
            with tab2:
                st.subheader("Theme Analysis & Synthesis")
                
                if result.get("themes"):
                    st.markdown(result["themes"])
                else:
                    st.info("No theme analysis available.")
        
        else:
            st.error(f"❌ Query failed: {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "💡 **Tip**: For best results, upload multiple related documents and ask specific questions about themes, patterns, or insights you want to discover."
)