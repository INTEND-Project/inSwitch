FROM python:3.12-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs are sent straight to stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Install system deps first (only if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# 2) Install Python dependencies
# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3) Copy application code
COPY . .

# # 4) Run the app
# CMD ["python", "app.py"]