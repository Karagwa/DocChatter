# Use a Python 3.11 slim image based on Debian Bookworm
FROM python:3.11-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install git and git-lfs. These are often required for downloading models from Hugging Face,
# especially if they use Git Large File Storage (LFS).
# `apt-get update` refreshes the package list, and `apt-get install -y` installs the packages.
# `rm -rf /var/lib/apt/lists/*` cleans up the apt cache to keep the image size down.
RUN apt-get update && apt-get install -y git git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies.
# `--no-cache-dir` prevents pip from storing cached downloads, reducing image size.
# `--timeout 300` sets a timeout for pip operations (already present, good to keep).
RUN pip install --no-cache-dir --timeout 300 -r requirements.txt

# --- Start: Add model pre-download steps ---
# Create a directory to store the pre-downloaded model.
# This path should be consistent with where your application code will look for the model.
# For sentence-transformers, a common pattern is to just clone it into a specific folder.
RUN mkdir -p /app/models/sentence-transformers/all-mpnet-base-v2

# Clone the sentence-transformers/all-mpnet-base-v2 model repository.
# This downloads all necessary model files directly into your Docker image during the build process.
# Replace this with the specific model your app needs if it's different.
RUN git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 /app/models/sentence-transformers/all-mpnet-base-v2
# --- End: Add model pre-download steps ---

# Copy the rest of your application code into the container.
# This should be done *after* installing dependencies and pre-downloading models
# to leverage Docker's layer caching effectively.
COPY . .

# Create additional directories needed by your application
RUN mkdir -p /app/chroma_langchain_db /app/temp_uploads

# Expose the port that Streamlit will run on.
# Cloud Run automatically sets the PORT environment variable.
EXPOSE $PORT

# Command to run your Streamlit application.
# `--server.port=$PORT` tells Streamlit to listen on the port provided by Cloud Run.
# `--server.address=0.0.0.0` makes Streamlit listen on all network interfaces.
# `--server.headless=true` prevents Streamlit from trying to open a browser, which is
# essential in a server environment like Cloud Run.
CMD ["streamlit", "run", "app/main.py", "--server.port=$PORT", "--server.address=0.0.0.0", "--server.headless=true"]