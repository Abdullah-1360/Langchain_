#!/bin/bash
# Script to download and setup Qwen2.5-1.5B-Instruct model

set -e

echo "🚀 Setting up Qwen2.5-1.5B-Instruct-Q4_K_ model..."

# Create models directory
mkdir -p models
cd models

# Check if model already exists
if [ -f "qwen2.5-1.5b-instruct-q4_k.gguf" ]; then
    echo "✅ Model already exists at ./models/qwen2.5-1.5b-instruct-q4_k.gguf"
    exit 0
fi

echo ""
echo "📥 Downloading Qwen2.5-1.5B-Instruct-Q4_K_ model..."
echo "   Source: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF"
echo ""
echo "   Model: qwen2.5-1.5b-instruct-q4_k.gguf (~1.2 GB)"
echo ""

# Download using curl (you can replace with wget if needed)
if command -v curl &> /dev/null; then
    echo "Downloading using curl..."
    curl -L -o qwen2.5-1.5b-instruct-q4_k.gguf \
        "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k.gguf"
elif command -v wget &> /dev/null; then
    echo "Downloading using wget..."
    wget -O qwen2.5-1.5b-instruct-q4_k.gguf \
        "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k.gguf"
else
    echo "❌ Neither curl nor wget found. Please install one and try again."
    exit 1
fi

echo ""
echo "✅ Model downloaded successfully!"
echo "📁 Location: ./models/qwen2.5-1.5b-instruct-q4_k.gguf"
echo ""
echo "Next steps:"
echo "1. Configure .env file with LOCAL_MODEL_PATH settings"
echo "2. Run: python main.py"
