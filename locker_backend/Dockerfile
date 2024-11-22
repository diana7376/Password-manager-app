# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    build-essential \
    nginx \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && npm install -g npm@latest

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Delete existing frontend files (if any) and clone the frontend repository
RUN rm -rf /Password-manager-app-frontend && \
    git clone --single-branch --branch main https://github.com/diana7376/Password-manager-app-frontend ../Password-manager-app-frontend

# Navigate to the frontend directory, set up the environment, and build
WORKDIR /Password-manager-app-frontend
RUN echo "REACT_APP_API_BASE_URL=https://petite-danella-lockr-b5f8b6cb.koyeb.app/api" > .env && \
    npm install && \
    npm run build

# Copy the built frontend to the static directory
WORKDIR /app
RUN rm -rf static/* && mkdir -p static/build && \
    cp -r /Password-manager-app-frontend/build/* static/build/

# Copy backend requirements and code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port 80 for Nginx
EXPOSE 80

# Run both Nginx and Gunicorn
CMD service nginx start && gunicorn locker_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
