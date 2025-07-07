import streamlit as st
import os
from rag_pipeline import process_document, rag_pipeline

st.set_page_config(page_title="📄 Chat with Your Document")

st.title("🧠 RAG Chat App (Upload Your Own!)")


os.makedirs("app/temp_uploads", exist_ok=True)


uploaded_file = st.file_uploader("Upload a `.txt` document", type="txt")


if uploaded_file:
    file_path = f"app/temp_uploads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing document...")
    status = process_document(file_path)
    st.success(status)


question = st.text_input("Ask a question about the uploaded document:")

if question:
    answer = rag_pipeline(question)
    st.markdown("**💬 Answer:**")
    st.write(answer)


if st.button("🔄 Clear"):
    st.experimental_rerun()
