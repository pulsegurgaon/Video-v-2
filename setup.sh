#!/bin/bash

echo "🚀 Starting AI Engine Setup..."

# Update system
apt update && apt upgrade -y

# Install python + pip
apt install python3 python3-pip git -y

# Install dependencies
pip3 install -r backend/requirements.txt

# Create outputs folder
mkdir -p backend/outputs

# Install Ollama (if needed)
curl -fsSL https://ollama.com/install.sh | sh

echo "✅ Setup complete!"