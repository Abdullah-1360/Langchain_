# 🤖 Multi-Agent Research Assistant with LangGraph

A sophisticated multi-agent system built with **LangGraph** that solves the real-world problem of automated research and analysis. The system uses the **Qwen2.5-1.5B-Instruct-Q4_K_** local model running on a local API server.

## 🎯 Real-World Problem

**Challenge**: Manually researching complex topics is time-consuming and often results in fragmented information from multiple sources.

**Solution**: An automated multi-agent system that:
- 🔍 **Researches** information on any topic
- 📊 **Synthesizes** findings into coherent summaries
- 💡 **Analyzes** data for insights and patterns
- 📈 **Generates** actionable recommendations

## 🏗️ Project Structure

```
langgraph_research_agent/
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration and environment variables
├── agents/
│   ├── __init__.py
│   ├── base_agent.py            # Base class for all agents
│   ├── researcher.py            # Information gathering agent
│   └── analyst.py               # Analysis and insights agent
├── graph/
│   ├── __init__.py
│   └── research_graph.py        # LangGraph workflow definition
├── utils/
│   ├── __init__.py
│   ├── search_tools.py          # Search functionality
│   └── output_formatting.py     # Output formatting utilities
├── main.py                      # Main entry point
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Local API Server

The system requires a local API server running on `http://127.0.0.1:8080/v1` with the Qwen2.5-1.5B model.

You can start it using one of these methods:

**Option A: Using Ollama (Recommended)**
```bash
# Install Ollama from https://ollama.ai
# Then run:
ollama run qwen2.5:1.5b
```

**Option B: Using LM Studio**
1. Download [LM Studio](https://lmstudio.ai/)
2. Load the Qwen2.5-1.5B-Instruct-Q4_K_M model
3. Start the local API server on port 8080

**Option C: Using vLLM**
```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct-GGUF \
  --port 8080
```

### 3. Configure Environment

```bash
cp .env.example .env
```

The default `.env` is already configured to use `http://127.0.0.1:8080/v1`. No changes needed!

### 4. Run the Application

**Standard mode** (with example queries):
```bash
python main.py
```

**Interactive mode** (enter your own queries):
```bash
python main.py --interactive
```

## 🤖 System Architecture

### Workflow Flow

```
START
  ↓
[Research Phase] → Query → Search → Synthesize
  ↓
[Analysis Phase] → Analyze Findings → Generate Insights
  ↓
[Review Phase] → Generate Report
  ↓
END
```

### Agents

#### 1. **ResearcherAgent** 🔍
- Receives research queries
- Creates research plans
- Performs web searches
- Synthesizes findings into coherent summaries

#### 2. **AnalystAgent** 📊
- Receives synthesized research data
- Identifies key insights and patterns
- Highlights gaps and areas for further research
- Provides recommendations

## 📝 Example Usage

```python
from graph.research_graph import ResearchGraph

# Initialize the graph
research_graph = ResearchGraph()

# Run a query
result = research_graph.run("What are AI trends in 2024?")

# Access results
print(result["research"])      # Research data
print(result["analysis"])      # Analysis data
```

## 🔧 Configuration Options

Edit `.env` to customize settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `LOCAL_API_URL` | http://127.0.0.1:8080/v1 | Local API server URL |
| `LOCAL_MODEL` | Qwen2.5-1.5B-Instruct-Q4_K_M | Model name |
| `LLM_TEMPERATURE` | 0.7 | Model temperature (0-1) |
| `MAX_TOKENS` | 2048 | Maximum response tokens |
| `MAX_SEARCH_RESULTS` | 5 | Number of search results |

## 🎨 Key Features

✅ **Multi-Agent Architecture**: Specialized agents for different tasks
✅ **LangGraph Workflow**: Conditional routing and state management  
✅ **Local Model**: Uses Qwen2.5-1.5B with no API costs
✅ **Real-time Search**: Integration with DuckDuckGo for current information
✅ **Structured Output**: Well-organized analysis and insights
✅ **Error Handling**: Graceful error management and fallbacks
✅ **Extensible Design**: Easy to add new agents or modify workflows

## 🔌 Extending the System

### Add a New Agent

1. Create a new file in `agents/`:
```python
from .base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__("NewAgent")
    
    def execute(self, input_data):
        # Your logic here
        return {"result": "..."}
```

2. Add it to the graph in `research_graph.py`:
```python
graph.add_node("new_phase", self._new_phase_node)
```

### Modify the Workflow

Edit `graph/research_graph.py` to:
- Add new nodes (agents)
- Change routing logic
- Adjust state transitions

## 🛠️ Troubleshooting

**Connection Error - "Failed to connect to http://127.0.0.1:8080"**
- Make sure the local API server is running
- Check if Ollama/LM Studio/vLLM is started
- Verify the server is listening on port 8080

**Slow Response Times**
- Local models are slower than cloud APIs
- This is normal for 1.5B parameter models on consumer hardware
- Consider using GPU acceleration if available

**Out of Memory Error**
- Reduce `MAX_TOKENS` in `.env`
- Reduce `MAX_SEARCH_RESULTS`
- Close other applications to free up memory

## 📚 Technologies Used

- **LangGraph**: Agentic workflow orchestration
- **LangChain**: LLM framework and utilities
- **Qwen2.5**: Local language model (1.5B parameters)
- **Pydantic**: Data validation and state management
- **DuckDuckGo**: Web search integration

## 📖 Additional Resources

- [LangGraph Documentation](https://python.langchain.com/langgraph)
- [LangChain Documentation](https://python.langchain.com)
- [Qwen Model Card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- [Ollama](https://ollama.ai/)
- [LM Studio](https://lmstudio.ai/)

## ⚡ Performance Tips

1. **Use GPU acceleration** if your system supports it (NVIDIA CUDA)
2. **Start with simple queries** to test the setup
3. **Monitor memory usage** with `htop` or `top`
4. **Batch process** multiple queries for better efficiency

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Happy Researching with Local LLMs! 🚀**
