#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t password-manager-app-backend:local .

# Tag the Docker image
echo "Tagging Docker image..."
docker tag password-manager-app-backend:local maxnoragami/password-manager-app-backend:latest

# Push the Docker image
echo "Pushing Docker image to Docker Hub..."
docker push maxnoragami/password-manager-app-backend:latest

# Redeploy the Koyeb service
echo "Redeploying Koyeb service..."
koyeb service redeploy petite-danella/password-manager-app-backend
echo "Deployment complete!"
