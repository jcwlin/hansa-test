#!/bin/bash

# BakuDocs Docker Setup Script
# This script helps set up the Docker environment for BakuDocs

set -e  # Exit on any error

echo "🚀 BakuDocs Docker Setup Script"
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{uploads,logs,databases}
echo "✅ Data directories created"

# Check if Google service account file exists
GOOGLE_CREDS_FILE="fileanalyzer-463911-e71c7f7288ad.json"
if [ ! -f "$GOOGLE_CREDS_FILE" ]; then
    echo "⚠️  Warning: Google service account file '$GOOGLE_CREDS_FILE' not found"
    echo "   Please ensure you have the Google service account JSON file in the project root"
    echo "   or update the path in docker-compose.yml"
fi

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml not found. This file is required for the application to run."
    exit 1
fi

echo "✅ Configuration files checked"

# Build and start the containers
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting BakuDocs..."
docker-compose up -d

echo ""
echo "🎉 BakuDocs is starting up!"
echo ""
echo "📊 Container status:"
docker-compose ps

echo ""
echo "📋 Next steps:"
echo "  1. Wait for the container to be healthy (may take 1-2 minutes)"
echo "  2. Open your browser and go to: http://localhost:5001"
echo "  3. Check logs if needed: docker-compose logs -f bakudocs"
echo ""
echo "🔧 Useful commands:"
echo "  • View logs: docker-compose logs -f bakudocs"
echo "  • Stop: docker-compose down"
echo "  • Restart: docker-compose restart"
echo "  • Update: docker-compose pull && docker-compose up -d --build"
echo ""

# Wait a moment and check if the container is running
sleep 5
if docker-compose ps | grep -q "Up"; then
    echo "✅ Container is running successfully!"
else
    echo "❌ Container failed to start. Check logs with: docker-compose logs bakudocs"
    exit 1
fi
