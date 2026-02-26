# AgenticCharbot

Streamlit-based LangGraph app with multiple agentic AI use cases powered by Groq and Tavily.

## Features

- `Basic Chatbot`: simple LLM chat using a LangGraph flow
- `Chatbot with Tools`: Groq model with Tavily web search tool via LangGraph `ToolNode`
- `AI News`: fetches AI news with Tavily, summarizes with Groq, and saves a markdown report
- Streamlit sidebar UI for model selection, API keys, and use-case selection
- Tool-call fallback: if Groq tool calling fails, the app retries with `Basic Chatbot`

## Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Groq (`langchain_groq`)
- Tavily (`tavily-python`)

## Project Structure

```text
AgenticCharbot/
├── app.py
├── requirements.txt
├── pyproject.toml
├── AINews/                       # generated AI news markdown files
└── src/langgraphagenticai/
    ├── main.py                   # app orchestration
    ├── graph/graph_builder.py    # LangGraph graph setup for each use case
    ├── LLMS/groqllm.py           # Groq model configuration
    ├── tools/search_tools.py     # Tavily search tool setup
    ├── nodes/
    │   ├── basic_chatbot_node.py
    │   ├── chatbot_with_tool_node.py
    │   └── ai_news_node.py
    └── ui/
        ├── uiconfigfile.ini
        └── streamlitui/
            ├── loadui.py
            └── display_result.py
```

## Requirements

- Python `3.13+` (as declared in `pyproject.toml`)
- Groq API key
- Tavily API key (required for `Chatbot with Tools` and `AI News`)

## Installation

1. Clone the repository and move into it.

```bash
git clone <your-repo-url>
cd AgenticCharbot
```

2. Create and activate a virtual environment.

```bash
python3.13 -m venv venv
source venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How to Use

### 1) Select LLM and Model

- Choose `Groq` in the sidebar
- Select a Groq model (configured in `src/langgraphagenticai/ui/uiconfigfile.ini`)
- Enter your `GROQ API KEY`

### 2) Select Use Case

- `Basic Chatbot`
- `Chatbot with Tools` (requires `TAVILY_API_KEY`)
- `AI News` (requires `TAVILY_API_KEY`)

### 3) Provide Input

- For `Basic Chatbot` / `Chatbot with Tools`: type a message in chat input
- For `AI News`: choose `Daily`, `Weekly`, or `Monthly` and click `Latest News`

## API Keys

The UI collects keys from the sidebar and also sets environment variables at runtime.

- `GROQ_API_KEY`
- `TAVILY_API_KEY`

You can also export them in your shell before running:

```bash
export GROQ_API_KEY="your_groq_key"
export TAVILY_API_KEY="your_tavily_key"
```

## AI News Output

The `AI News` flow saves a markdown summary file to:

```text
./AINews/<frequency>_summary.md
```

Examples:

- `AINews/daily_summary.md`
- `AINews/weekly_summary.md`
- `AINews/monthly_summary.md`

If the `AINews/` folder does not exist, create it first:

```bash
mkdir -p AINews
```

## Common Errors and Fixes

### `invalid_api_key` (Groq)

- Make sure the Groq API key is valid and active
- Paste the key without extra spaces
- Regenerate a key from the Groq console if needed

### `model_not_found`

- Check the selected Groq model name in `src/langgraphagenticai/ui/uiconfigfile.ini`
- Ensure your Groq account has access to that model

### `tool_use_failed` / `Failed to call a function`

- This happens in `Chatbot with Tools` when the model fails to generate a valid tool call
- The app now retries automatically using `Basic Chatbot`
- For simple prompts (e.g., definitions), use `Basic Chatbot` directly

### `Graph must have an entrypoint`

- Usually caused by a use-case string mismatch in config (extra spaces/typos)
- Check `USECASE_OPTIONS` in `src/langgraphagenticai/ui/uiconfigfile.ini`

## Notes

- `pyproject.toml` is present but dependencies are currently maintained in `requirements.txt`
- Tool rendering in the UI is formatted separately so raw Tavily results are easier to read

## Future Improvements (Optional)

- Add pinned dependency versions
- Improve Groq API key fallback logic in `src/langgraphagenticai/LLMS/groqllm.py`
- Add tests for graph setup and node behavior
- Add `.env` support (`python-dotenv`)
