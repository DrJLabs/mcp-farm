FROM python:3.11-slim

WORKDIR /app

# Prevent .pyc and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install deps first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Default bind; override with env or compose
ENV BIND_HOST=0.0.0.0 \
    BIND_PORT=8000 \
    TRANSPORT=http

EXPOSE 8000

CMD ["python", "sample_mcp.py"]

