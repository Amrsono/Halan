#!/bin/bash
# Quick Start Script for Halan Invest

echo "🚀 Halan Invest - Quick Start"
echo "=============================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker Compose found"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created"
else
    echo "✅ .env already exists"
fi

# Start services
echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo ""
echo "🔍 Checking services..."
docker-compose ps

# Print access information
echo ""
echo "✅ All services started!"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "📡 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "View logs with: docker-compose logs -f"
echo "Stop services with: docker-compose down"
