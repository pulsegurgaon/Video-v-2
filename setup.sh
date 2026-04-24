#!/bin/bash

echo "🚀 Setting up AI Shorts Engine..."

apt update && apt upgrade -y
apt install -y python3 python3-pip git curl

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve &

sleep 5

# Pull model
ollama pull llama3

# Install backend
cd backend
pip install -r requirements.txt

echo "🔥 Starting backend..."
python3 main.py
