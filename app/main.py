import streamlit as st
import os
from rag_pipeline import process_document, rag_pipeline

st.set_page_config(
    page_title="DocChatter - Chat with Your Document", 
    page_icon="🤖",
    layout="wide"
)


if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("🤖 DocChatter")
st.markdown("### Chat with your documents using AI")


col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 📄 Document Upload")
    
    
    if st.session_state.document_processed:
        st.success(f"✅ Document loaded: {st.session_state.document_name}")
        if st.button("🔄 Upload New Document"):
            st.session_state.document_processed = False
            st.session_state.document_name = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.info("📁 Please upload a document to get started")
    
    
    if not st.session_state.document_processed:
        os.makedirs("app/temp_uploads", exist_ok=True)
        uploaded_file = st.file_uploader(
            "Choose a text file", 
            type="txt",
            help="Upload a .txt document to chat with its content"
        )
        
        if uploaded_file:
            file_path = f"app/temp_uploads/{uploaded_file.name}"
            
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            
            with st.spinner("🔄 Processing document..."):
                status = process_document(file_path)
            
            
            st.session_state.document_processed = True
            st.session_state.document_name = uploaded_file.name
            st.success("✅ Document processed successfully!")
            st.rerun()

with col2:
    st.markdown("#### 💬 Chat Interface")
    
    if st.session_state.document_processed:
       
        chat_container = st.container()
        
        
        with chat_container:
            for i, (q, a) in enumerate(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**🙋‍♀️ You:** {q}")
                    st.markdown(f"**🤖 DocChatter:** {a}")
                    st.divider()
        
                
        with st.form("question_form", clear_on_submit=True):
            question = st.text_input(
                "Ask a question about your document:",
                placeholder="e.g., What is the main theme of this document?"
            )
            
            
            
            
            ask_button = st.form_submit_button("🚀 Ask Question", type="primary", use_container_width=True)
            
        
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
        
       
        if ask_button and question:
            with st.spinner("🤔 Thinking..."):
                answer = rag_pipeline(question)
            
            
            st.session_state.chat_history.append((question, answer))
            st.rerun()
        
       
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
    
    else:
        st.markdown("👆 Upload a document first to start chatting!")


with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Upload** a `.txt` document
    2. **Wait** for processing to complete
    3. **Ask** questions about te content
    4. **Chat** and explore your document!
    
    ### ✨ Anything else?
    - 🚀 Well...nothing. 
    """)
    
    if st.session_state.document_processed:
        st.markdown("### 📊 Document Stats")
        st.info(f"**File:** {st.session_state.document_name}")
        st.info(f"**Questions Asked:** {len(st.session_state.chat_history)}")