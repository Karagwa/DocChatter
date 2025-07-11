# 🤖 DocChatter - Chat with Your Documents

DocChatter is an AI-powered document chat application that allows you to upload documents and have intelligent conversations about their content using Google's Gemini AI and advanced RAG (Retrieval-Augmented Generation) technology.

## ✨ Features

- 📄 **Document Upload**: Support for text documents
- 🤖 **AI-Powered Chat**: Intelligent conversations using Google Gemini AI
- 🔍 **Smart Search**: Vector-based document search using ChromaDB
- 💬 **Chat History**: Persistent conversation history
- 🐳 **Dockerized**: Easy deployment with Docker


## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **AI Model**: Google Gemini AI via LangChain
- **Vector Database**: ChromaDB for document embeddings
- **Text Processing**: HuggingFace Sentence Transformers
- **Document Processing**: LangChain document loaders and text splitters

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Google AI API Key (Gemini)

### 1. Clone the Repository

```bash
git clone https://github.com/Karagwa/DocChatter
cd Build_A_Bot
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
PORT =
```

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app/main.py
```

Access the app at: http://localhost:8501

### 4. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t docchatter .
docker run -p 8081:8501 -e PORT=8501 --env-file .env docchatter
```

Access the app at: http://127.0.0.1:8081 when using docker incase the http://localhost:8501 has issues

### Deployed URL
https://docchatter-77068367626.europe-west1.run.app incase this doesn't work as expected stick to accessing the file locally via docker. There are issues with deployment.

### Important note
The dockerfile has these lines

``` bash
# Created a directory to store the pre-downloaded model. (This was used during deployment when the deployed container with making many requests to the Hugging Face model repository.)
# Comment them out if you are running the app locally.
RUN mkdir -p /app/models/sentence-transformers/all-mpnet-base-v2

# Cloned the sentence-transformers/all-mpnet-base-v2 model repository. (Used mainly in deployment)
# Comment this out if you are running the app locally.
RUN git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 /app/models/sentence-transformers/all-mpnet-base-v2
```

Comment them out as they are used mainly in deployment.
The container build perfectly without them.


## 📁 Project Structure

```
Build_A_Bot/
├── app/
│   ├── main.py              # Streamlit main application
│   ├── rag_pipeline.py      # RAG pipeline implementation
│   ├── chroma_langchain_db/ # Vector database storage
│   └── temp_uploads/        # Temporary file uploads
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yaml     # Docker Compose configuration
├── .env                    # Environment variables
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini | Yes |
| `PORT` | Application port (default: 8501) | No |



## 📋 Dependencies

### Core Dependencies

```
streamlit              # Web application framework
langchain             # LLM application framework
langchain-google-genai # Google AI integration
chromadb              # Vector database
sentence-transformers # Text embeddings
python-dotenv         # Environment management
```

### Full Dependencies

See `requirements.txt` 

## 🎯 Usage

1. **Start the Application**: Run locally or via Docker
2. **Upload Document**: Use the sidebar to upload a text document
3. **Ask Questions**: Type questions about your document
4. **View Responses**: Get AI-powered answers with context


### Supported File Types

- `.txt` - Plain text files
- More formats can be added by extending the document loaders

## 🛠️ Development

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app/main.py --server.runOnSave=true
```

### Code Structure

- `app/main.py`: Streamlit UI and application logic
- `app/rag_pipeline.py`: Document processing and RAG implementation
- Vector storage in `chroma_langchain_db/`
- Temporary uploads in `temp_uploads/`

## 🔍 Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify `GOOGLE_API_KEY` is set correctly
3. **Port Conflicts**: Change port mapping in docker-compose.yaml
4. **Memory Issues**: Increase Docker memory limits for large documents

### Docker Issues

```bash
# Rebuild container
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f

# Check container status
docker-compose ps
```

## 📊 Performance

- **Memory**: ~1-2GB recommended for typical usage
- **CPU**: Single core sufficient for small to medium documents
- **Storage**: Vector database grows with document size
- **Response Time**: 2-5 seconds depending on query complexity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [LangChain](https://langchain.com/) for LLM orchestration
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Google AI](https://ai.google.dev/) for Gemini API
- [HuggingFace](https://huggingface.co/) for embeddings

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Docker and Streamlit documentation

---

Built with ❤️ by me  using Streamlit, LangChain, and Google AI