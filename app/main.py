import streamlit as st
import os
from rag_pipeline import process_document, rag_pipeline

st.set_page_config(page_title="Chat with Your Document")

st.title("DocChatter 🤖")
st.write("Step 1. Upload a `.txt` document to chat with its content.")
st.write("Step 2. Ask questions about the document, and the bot will respond based on its content.")
st.write("That's all you need to do! No need to configure anything else. Just upload your document and start chatting.")


st.write("Are you ready to chat? Let's go! 😊")                


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
