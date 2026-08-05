FROM python:3.12-slim

# Install system dependencies required by OpenCV and Ultralytics
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create required directories
RUN mkdir -p logs screenshots

# Render sets PORT dynamically; default to 7860 for HuggingFace / local
ENV PORT=7860
EXPOSE $PORT

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1

# Start Streamlit using shell form so $PORT is expanded at runtime
CMD streamlit run streamlit_app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
