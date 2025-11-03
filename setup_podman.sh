#!/bin/bash

# BakuDocs Podman Setup Script
# This script helps set up the Podman environment for BakuDocs
# Podman is a daemonless container engine for developing, managing, and running containers

set -e  # Exit on any error

echo "🚀 BakuDocs Podman Setup Script"
echo "================================"
echo "🐳 Using Podman (Docker-compatible alternative)"
echo ""

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "❌ Podman is not installed."
    echo ""
    echo "📦 Installation options:"
    echo "   • macOS: brew install podman"
    echo "   • Ubuntu/Debian: sudo apt-get install podman"
    echo "   • CentOS/RHEL: sudo yum install podman"
    echo "   • Fedora: sudo dnf install podman"
    echo ""
    echo "🌐 Visit: https://podman.io/getting-started/installation"
    exit 1
fi

# Check Podman version
PODMAN_VERSION=$(podman --version)
echo "✅ Podman found: $PODMAN_VERSION"

# Check if Podman Compose is available
if command -v podman-compose &> /dev/null; then
    echo "✅ Podman Compose found"
    COMPOSE_CMD="podman-compose"
elif command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose found (will work with Podman)"
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Neither podman-compose nor docker-compose found"
    echo ""
    echo "📦 Install podman-compose:"
    echo "   • pip install podman-compose"
    echo "   • or: sudo pip3 install podman-compose"
    exit 1
fi

echo "🔧 Using compose command: $COMPOSE_CMD"

# Check if Podman machine is running (macOS/Windows)
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "🖥️  Checking Podman machine status..."
    if ! podman machine list | grep -q "Running"; then
        echo "⚠️  Podman machine is not running. Starting it..."
        podman machine start
        echo "✅ Podman machine started"
    else
        echo "✅ Podman machine is running"
    fi
fi

# Create data directories with proper permissions
echo "📁 Creating data directories..."
mkdir -p data/{uploads,logs,databases}
echo "✅ Data directories created"

# Check if Google service account file exists
GOOGLE_CREDS_FILE="fileanalyzer-463911-e71c7f7288ad.json"
if [ ! -f "$GOOGLE_CREDS_FILE" ]; then
    echo "⚠️  Warning: Google service account file '$GOOGLE_CREDS_FILE' not found"
    echo "   Please ensure you have the Google service account JSON file in the project root"
    echo "   or update the path in docker-compose.podman.yml"
fi

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml not found. This file is required for the application to run."
    exit 1
fi

echo "✅ Configuration files checked"

# Build and start the containers using Podman-optimized compose file
echo "🔨 Building Podman images..."
$COMPOSE_CMD -f docker-compose.podman.yml build

echo "🚀 Starting BakuDocs with Podman..."
$COMPOSE_CMD -f docker-compose.podman.yml up -d

echo ""
echo "🎉 BakuDocs is starting up with Podman!"
echo ""
echo "📊 Container status:"
$COMPOSE_CMD -f docker-compose.podman.yml ps

echo ""
echo "📋 Next steps:"
echo "  1. Wait for the container to be healthy (may take 1-2 minutes)"
echo "  2. Open your browser and go to: http://localhost:5001"
echo "  3. Check logs if needed: $COMPOSE_CMD -f docker-compose.podman.yml logs -f bakudocs"
echo ""
echo "🔧 Useful Podman commands:"
echo "  • View logs: $COMPOSE_CMD -f docker-compose.podman.yml logs -f bakudocs"
echo "  • Stop: $COMPOSE_CMD -f docker-compose.podman.yml down"
echo "  • Restart: $COMPOSE_CMD -f docker-compose.podman.yml restart"
echo "  • Update: $COMPOSE_CMD -f docker-compose.podman.yml pull && $COMPOSE_CMD -f docker-compose.podman.yml up -d --build"
echo ""
echo "🐳 Podman-specific commands:"
echo "  • List containers: podman ps"
echo "  • List images: podman images"
echo "  • Shell access: podman exec -it bakudocs-app /bin/bash"
echo "  • View container info: podman inspect bakudocs-app"
echo ""

# Wait a moment and check if the container is running
sleep 5
if $COMPOSE_CMD -f docker-compose.podman.yml ps | grep -q "Up"; then
    echo "✅ Container is running successfully with Podman!"
else
    echo "❌ Container failed to start. Check logs with: $COMPOSE_CMD -f docker-compose.podman.yml logs bakudocs"
    exit 1
fi

echo ""
echo "🎯 Podman advantages for this deployment:"
echo "  • Daemonless architecture (no background service)"
echo "  • Rootless containers (better security)"
echo "  • Native systemd integration (Linux)"
echo "  • Kubernetes-ready (podman play kube)"
echo "  • Full Docker compatibility"
