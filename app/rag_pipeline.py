from langchain import hub
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, TypedDict
import getpass
import os
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# the local path where the model is expected to be found inside the Docker container.

LOCAL_MODEL_PATH = "./models/sentence-transformers/all-mpnet-base-v2"

# Initialize HuggingFaceEmbeddings to load from the local path
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2", # Keep the model ID for internal logic
    cache_folder=LOCAL_MODEL_PATH, # Point to your pre-downloaded location
    model_kwargs={'device': 'cpu'} # Explicitly set device to CPU for Cloud Run
)

vector_store = Chroma(
    collection_name="rag_pipeline_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

prompt = hub.pull("rlm/rag-prompt")

def process_document(doc_path):
    loader = TextLoader(doc_path, encoding="utf-8", autodetect_encoding=True)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    split_docs = text_splitter.split_documents(docs)
    vector_store.add_documents(split_docs)

    return "Documents processed and stored successfully."

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"], k=3)
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join([doc.page_content for doc in state["context"]])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

def rag_pipeline(question: str) -> str:
    state = {"question": question}

    state.update(retrieve(state))

    result = generate(state)

    return result["answer"]