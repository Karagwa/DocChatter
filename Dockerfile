# Use a Python 3.11 slim image based on Debian Bookworm
FROM python:3.11-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install git and git-lfs. These are often required for downloading models from Hugging Face,
# especially if they use Git Large File Storage (LFS).
RUN apt-get update && apt-get install -y git git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir --timeout 300 -r requirements.txt

# --- Start: Add model pre-download steps ---
# Create a directory to store the pre-downloaded model.
RUN mkdir -p /app/models/sentence-transformers/all-mpnet-base-v2

# Clone the sentence-transformers/all-mpnet-base-v2 model repository.
RUN git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 /app/models/sentence-transformers/all-mpnet-base-v2
# --- End: Add model pre-download steps ---

# Copy the rest of your application code into the container.
COPY . .

# Create additional directories needed by your application
RUN mkdir -p /app/chroma_langchain_db /app/temp_uploads

# Expose the port that Streamlit will run on.
EXPOSE $PORT

# Command to run your Streamlit application.
CMD ["streamlit", "run", "app/main.py", "--server.port=$PORT", "--server.address=0.0.0.0", "--server.headless=true"]