FROM python:3.11-slim-bookworm

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 -r requirements.txt


COPY . .


RUN mkdir -p /app/chroma_langchain_db /app/temp_uploads


EXPOSE $PORT

CMD streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true