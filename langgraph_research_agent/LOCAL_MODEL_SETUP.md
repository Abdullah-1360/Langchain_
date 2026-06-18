# 🚀 Local Model Setup Guide

This guide explains how to set up and use the **Qwen2.5-1.5B-Instruct-Q4_K_** local model with the LangGraph Research Assistant.

## ✨ Benefits of Local Models

✅ **Privacy**: No API calls, all processing happens locally  
✅ **Cost**: No API fees, run unlimited queries  
✅ **Speed**: Instant responses without network latency  
✅ **Offline**: Works without internet connection  

## 📋 Requirements

- Python 3.8+
- 4GB+ RAM (recommended 8GB)
- 2GB disk space (for the model)
- Optional: GPU with CUDA support (for acceleration)

## 🛠️ Installation Steps

### 1. Install Dependencies

```bash
cd /home/ubuntu/Langchain_prc
pip install -r requirements.txt
```

Key packages installed:
- `llama-cpp-python`: Local LLM runtime
- `langchain-community`: LLM integrations
- `langgraph`: Workflow orchestration

### 2. Download the Qwen2.5 Model

Option A: **Automatic (Recommended)**
```bash
cd langgraph_research_agent
bash setup_model.sh
```

Option B: **Manual Download**
1. Download from [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
2. Save as: `langgraph_research_agent/models/qwen2.5-1.5b-instruct-q4_k.gguf`

### 3. Configure Environment

```bash
cd langgraph_research_agent
cp .env.example .env
```

Edit `.env` file (important settings):

```env
# Use local model
LLM_PROVIDER=local
LLM_MODEL=qwen2.5-1.5b

# Path to your model file
LOCAL_MODEL_PATH=./models/qwen2.5-1.5b-instruct-q4_k.gguf

# GPU Configuration
N_GPU_LAYERS=50          # -1 for full GPU, 0 for CPU only
N_THREADS=4              # Adjust based on your CPU cores
CONTEXT_WINDOW=2048      # Token context size
```

## ⚙️ Configuration Options

### GPU Acceleration (NVIDIA CUDA)

For faster inference with GPU:

```env
# Use GPU (requires CUDA setup)
N_GPU_LAYERS=-1          # Offload all layers to GPU
N_THREADS=1              # Can use fewer threads with GPU

# Alternative: Partial GPU offload
N_GPU_LAYERS=20          # Offload first 20 layers
```

**GPU Setup Requirements:**
1. NVIDIA GPU with CUDA Compute Capability 3.5+
2. CUDA Toolkit installed
3. cuDNN library
4. Reinstall llama-cpp-python with GPU support:
   ```bash
   pip install llama-cpp-python --force-reinstall --no-cache-dir --compile=cuda
   ```

### CPU-Only Configuration

```env
N_GPU_LAYERS=0           # No GPU acceleration
N_THREADS=8              # Use available CPU threads
CONTEXT_WINDOW=2048      # Adjust if running out of memory
```

## 🚀 Running the Application

### Standard Mode (Example Queries)
```bash
python main.py
```

### Interactive Mode (Your Queries)
```bash
python main.py --interactive
```

## 📊 Performance Expectations

### With CPU Only
- First response: 30-60 seconds (model loading)
- Subsequent responses: 20-40 seconds per query
- Memory usage: ~2GB

### With GPU Acceleration (NVIDIA)
- First response: 10-15 seconds
- Subsequent responses: 3-8 seconds per query
- Memory usage: ~2GB RAM + 2-3GB VRAM

## 🔧 Troubleshooting

### Issue: "Model not found"
```
Solution: Check LOCAL_MODEL_PATH in .env file
Make sure the file exists at: ./models/qwen2.5-1.5b-instruct-q4_k.gguf
```

### Issue: Out of Memory Error
```
Solution: Reduce CONTEXT_WINDOW in .env (try 1024 or 512)
         Or reduce MAX_SEARCH_RESULTS
```

### Issue: Very Slow Inference
```
Solution: Check N_GPU_LAYERS configuration
         Ensure you're using GPU acceleration if available
         Reduce CONTEXT_WINDOW
```

### Issue: CUDA Errors
```
Solution: Verify CUDA is installed: nvidia-smi
         Reinstall llama-cpp-python: 
         pip install llama-cpp-python --force-reinstall --no-cache-dir --compile=cuda
```

## 📈 Model Performance

**Qwen2.5-1.5B-Instruct** Characteristics:
- **Size**: 1.5 billion parameters
- **Quantization**: Q4_K_M (4-bit, ~1.2GB)
- **Context**: 32K token context window
- **Speed**: Fast inference on consumer hardware
- **Quality**: Good for most tasks, suitable for research assistant

## 🔄 Switching Between Local and OpenAI

To use OpenAI instead:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
OPENAI_API_KEY=your-key-here
```

To switch back to local:

```env
LLM_PROVIDER=local
```

## 📚 Additional Resources

- [Qwen2.5 Model Card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
- [llama-cpp-python Documentation](https://github.com/abetlen/llama-cpp-python)
- [LangChain Local Models](https://python.langchain.com/docs/guides/local_llms)

## 💡 Tips for Best Results

1. **Start with defaults**: The .env.example values are optimized for most systems
2. **Monitor memory**: Use `htop` or `top` to monitor RAM usage
3. **Adjust context**: Smaller context = faster, larger = more capable
4. **Test gradually**: Start with simple queries before complex research

---

**Happy local LLM experimenting! 🎉**
