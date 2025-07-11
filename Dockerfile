
FROM python:3.11-slim-bookworm


WORKDIR /app


RUN apt-get update && apt-get install -y git git-lfs \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir --timeout 300 -r requirements.txt


# Created a directory to store the pre-downloaded model. (This was used during deployment when the deployed container with making many requests to the Hugging Face model repository.)
# Comment them out if you are running the app locally.
RUN mkdir -p /app/models/sentence-transformers/all-mpnet-base-v2

# Cloned the sentence-transformers/all-mpnet-base-v2 model repository. (Used mainly in deployment)
# Comment this out if you are running the app locally.
RUN git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 /app/models/sentence-transformers/all-mpnet-base-v2

COPY . .


RUN mkdir -p /app/chroma_langchain_db /app/temp_uploads


EXPOSE $PORT
# Removed the square brackets around the port variable to ensure it is correctly interpreted on deployment
CMD streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true