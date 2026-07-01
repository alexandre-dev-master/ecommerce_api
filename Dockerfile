# Use the official lightweight Python 3.12 image based on Debian Linux
FROM python:3.12-slim

# Set environment variables to optimize Python behavior inside the container:
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED: Forces the stdout and stderr streams to be unbuffered (real-time logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define the working directory inside the container's isolated filesystem
WORKDIR /app

# Install system dependencies required for compiling certain Python packages (like database drivers)
# Clean up the apt cache afterwards to keep the image size as small as possible
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies without caching the index packages
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your local project files into the container's /app directory
COPY . /app/