import bs4
from langchain import hub
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="rag_pipeline_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)


def process_document(doc_path):
    # Load the document
    loader = TextLoader(doc_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    split_docs = text_splitter.split_documents(docs)
    vector_store.add_documents(split_docs)
    
prompt = hub.pull("rlm/rag-prompt")
    
    
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"], k=3)
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content= "\n\n".join([doc.page_content for doc in state["context"]])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

def rag_pipeline(question: str) -> str:
    state = {
        "question": question,
        "context": [],
        "answer": ""
    }
    
    graph = StateGraph(
        states={
            START: state,
            "retrieve": retrieve,
            "generate": generate
        },
        transitions={
            START: "retrieve",
            "retrieve": "generate"
        }
    )
    
    final_state = graph.run(START)
    return final_state["answer"]
    
    
        
    
        
    