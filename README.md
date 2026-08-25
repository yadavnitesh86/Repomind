# RepoMind

> **An AI-powered CLI assistant for understanding and interacting with your codebase.** Ask questions about your repository in natural language, analyze code, use Git and filesystem tools, and extend RepoMind with your own MCP servers.

## ✨ Features

* 🤖 AI-powered repository assistant
* 💬 Natural language CLI interaction
* 🔍 RAG-based repository knowledge retrieval
* 🧠 Agent workflows powered by LangGraph
* 🛠️ Repository, Git, filesystem, and MCP tools
* 🔌 Add unlimited custom MCP servers
* 🛡️ Human-in-the-loop approval for sensitive actions
* 💾 SQLite conversation persistence
* 📊 Optional Langfuse tracing
* 🤖 Multiple LLM providers
* 🎨 Rich terminal interface
* ⚡ UV dependency management
* 🐳 Docker support
* 🔄 GitHub Actions CI

---

# 🚀 Quick Start

## Prerequisites

Make sure you have:

* Python **3.12+**
* Git
* UV
* An API key for your selected LLM provider

Verify:

```bash
python --version
git --version
uv --version
```

## 1. Clone and Install

```bash
git clone <RepoMind-repository-URL>
cd Repomind

uv sync
```

## 2. Configure Your LLM

Configure your LLM provider and model in:

```text
src/repomind/config/config.yaml
```

Create the `.env` file:

### Windows PowerShell

```powershell
New-Item -Path "src\repomind\.env" -ItemType File
```

Add the API key for your configured provider.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

> ⚠️ The API key must match the provider configured in `config.yaml`.

## 3. Initialize Git

RepoMind analyzes Git repositories.

If your target repository is not already a Git repository:

```bash
git init
```

You can verify it with:

```bash
git status
```

> Existing Git repositories do not need `git init`.

## 4. Run RepoMind

From the RepoMind project directory:

```bash
uv run repomind
```

Example:

```text
You: Explain the architecture of this repository.

RepoMind: ...
```

Exit with:

```text
exit
```

or:

```text
quit
```

---

# 🌍 Install as a Global CLI Tool

If you want to run RepoMind from anywhere:

```bash
repomind
```

install it as a UV tool:

```bash
uv tool install .
```

Then run:

```bash
repomind
```

---

# 🔌 Add Your Own MCP Servers

RepoMind is extensible with MCP servers.

You can configure and add your own MCP servers in:

```text
src/repomind/mcp_server/all_mcp.py
```

For example, RepoMind can connect to multiple MCP servers:

```python
mcp = {
    "retriever": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [
            "-m",
            "repomind.retriever.mcp_server",
        ],
    },
    "filesystem": {
        "transport": "stdio",
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(REPOSITORY_PATH),
        ],
    },
    "git": {
        "transport": "stdio",
        "command": "uvx",
        "args": [
            "mcp-server-git",
            "--repository",
            str(REPOSITORY_PATH),
        ],
    },
}
```

### Add as many MCP servers as you need

Simply add another server configuration to the `mcp` dictionary.

This allows you to extend RepoMind with your own tools and MCP integrations without changing the core agent architecture.

```text
all_mcp.py
    │
    ├── Retriever MCP
    ├── Filesystem MCP
    ├── Git MCP
    └── Your Custom MCP Servers...
```

---

# 📊 Optional: Langfuse Observability

Langfuse tracing is optional.

Add these variables to:

```text
src/repomind/.env
```

```env
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=<Langfuse-host>
```

If these variables are not configured, RepoMind will run normally without Langfuse tracing.

---

# 🧠 Tech Stack

**AI & Agents:** LangChain, LangGraph, FastMCP
**LLMs:** Groq, OpenAI, Anthropic, Hugging Face
**RAG:** Qdrant, FastEmbed
**Storage:** SQLite
**Developer Tools:** UV, Docker, GitHub Actions
**Observability:** Langfuse
**CLI:** Rich

---

# 📁 Important Configuration Files

```text
Repomind/
│
├── src/
│   └── repomind/
│       ├── config/
│       │   └── config.yaml       # LLM configuration
│       │
│       ├── mcp_server/
│       │   └── all_mcp.py        # Add custom MCP servers
│       │
│       └── .env                  # API keys and secrets
│
├── pyproject.toml
├── uv.lock
└── Dockerfile
```

---

# 🐛 Troubleshooting

Before reporting an issue, check:

* Python **3.12+** is installed
* UV is installed
* `uv sync` completed successfully
* `src/repomind/.env` exists
* Your API key is correct
* The API key matches the configured LLM provider
* The target repository is initialized with Git

> 🔐 Never commit API keys, tokens, secrets, or your `.env` file.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch
3. Make your changes
4. Test your changes
5. Open a Pull Request

GitHub Actions will run the configured checks automatically.

---

# 👨‍💻 Author

**Nitesh Yadav**

Aspiring Applied AI Engineer

**Python · Machine Learning · Deep Learning · Generative AI · RAG · LangChain · LangGraph · Agentic AI**
