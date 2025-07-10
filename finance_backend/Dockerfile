# Dockerfile for FastAPI backend — robust src/api import handling

FROM python:3.11-slim

# Set workdir to backend directory so src/** is available at expected import path
WORKDIR /app/finance_backend

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set robust PYTHONPATH for src importability from WORKDIR and subdirs
ENV PYTHONPATH="/app/finance_backend/src:/app/finance_backend"

# Expose FastAPI port
EXPOSE 8000

# Entrypoint: use robust start.sh
CMD ["/bin/bash", "start.sh"]
