# RepoMind

> An AI-powered repository assistant that helps you understand, analyze, and interact with your codebase directly from the command line.

---

## 🚀 Quick Start

### Prerequisites

Before installing RepoMind, make sure you have:

- Python **3.12 or higher**
- Git
- UV
- An API key for your configured LLM provider

Verify your installation:

```bash
python --version
git --version
uv --version
```

---

## 1. Clone the Repository

```bash
git clone https://github.com/yadavnitesh86/Repomind.git
cd Repomind
```

---

## 2. Install Dependencies

RepoMind uses `uv` for dependency management.

```bash
uv sync
```

This installs the dependencies defined in `pyproject.toml` and `uv.lock`.

---

## 3. Configure RepoMind

The main configuration file is located at:

```text
Repomind/
└── src/
    └── repomind/
        └── config/
            └── config.yaml
```

You can modify `config.yaml` to change supported application settings, including:

- LLM provider
- Model
- Other supported model and application settings

> ⚠️ Make sure your API key matches the provider configured in `config.yaml`.

---

## 4. Create the `.env` File

RepoMind requires a `.env` file for API keys.

> ⚠️ **Important:** The `.env` file must be created at:

```text
Repomind/
└── src/
    └── repomind/
        └── .env
```

### Windows PowerShell

Create the file:

```powershell
New-Item -Path "src\repomind\.env" -ItemType File
```

Add the API key required by your configured provider.

Example for Groq:

```env
GROQ_API_KEY=your_api_key_here
```

If you select another provider in:

```text
src/repomind/config/config.yaml
```

add the corresponding API key required by that provider.

> 🔐 Never commit your `.env` file or API keys.

---

## 5. Optional: Configure Langfuse

Langfuse is optional and provides observability and tracing.

Add these variables to:

```text
src/repomind/.env
```

```env
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

If Langfuse credentials are not configured, RepoMind runs without Langfuse tracing.

---

## 6. Initialize Git

RepoMind works with Git repositories.

If the repository you want to analyze is not already initialized with Git, run:

```bash
git init
```

Verify Git:

```bash
git status
```

For an existing Git repository, you do not need to run `git init`.

---

## 7. Run RepoMind

From the RepoMind project directory:

```bash
uv run repomind
```

Example:

```text
You: Explain the architecture of this repository.

RepoMind: ...
```

To exit:

```text
exit
```

or:

```text
quit
```

---

# 📦 Complete Installation Flow

```bash
git clone https://github.com/yadavnitesh86/Repomind.git

cd Repomind

uv sync

# Create the required .env file at:
# src/repomind/.env

git init

uv run repomind
```

Before running RepoMind:

1. Create and configure:

```text
src/repomind/.env
```

2. Add the API key for your selected provider.

3. Configure your provider and model if needed at:

```text
src/repomind/config/config.yaml
```

---

# 🧪 Testing

After installation, start RepoMind:

```bash
uv run repomind
```

Recommended tests:

1. Start RepoMind successfully.
2. Ask a question about the repository.
3. Test repository and code analysis.
4. Test tool-based operations.
5. Test the approval/rejection workflow when applicable.
6. Verify conversation persistence.
7. Test the configured LLM provider.

If you find an error, check:

1. Is Python 3.12 or higher installed?
2. Is `uv` installed?
3. Did `uv sync` complete successfully?
4. Does `src/repomind/.env` exist?
5. Does the `.env` file contain the correct API key?
6. Does the API key match the provider configured in `config/config.yaml`?
7. Is the repository initialized with Git?

If you find a bug, please open an issue and include:

- Error message
- Steps to reproduce
- Operating system
- Python version
- Relevant configuration details

> 🔐 Never include API keys, secrets, tokens, or your `.env` file in an issue.

---

# 🤖 What is RepoMind?

RepoMind is an AI-powered CLI assistant designed to help developers understand and interact with code repositories.

Instead of manually searching through files and directories, users can ask questions about their codebase using natural language.

RepoMind analyzes repository information, retrieves relevant context, and uses an AI agent workflow to provide contextual answers and perform repository-related operations.

---

# ✨ Features

- 🤖 AI-powered repository assistant
- 💬 Natural language CLI interaction
- 📁 Repository and codebase analysis
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Agent-based workflows using LangGraph
- 🛠️ Tool-based repository interaction
- 🛡️ Human-in-the-loop approval for sensitive actions
- 💾 SQLite checkpointing and conversation persistence
- 🧵 Thread-based conversation state
- 📊 Optional Langfuse observability and tracing
- 🔌 Configurable LLM providers
- 🎨 Rich CLI interface
- ⚡ Dependency management with UV
- 🐳 Docker support
- 🔄 GitHub Actions CI

---

# 🏗️ Architecture

```text
                    User
                     │
                     ▼
               ┌───────────┐
               │    CLI    │
               └─────┬─────┘
                     │
                     ▼
               ┌───────────┐
               │ LangGraph │
               │   Agent   │
               └─────┬─────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     ┌─────────┐           ┌─────────┐
     │   LLM   │           │  Tools  │
     └─────────┘           └────┬────┘
                                │
                                ▼
                        Repository Analysis
                                │
                                ▼
                         Files / Git / Code
```

### Repository Knowledge Flow

```text
Repository
    ↓
Document Loading
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retriever
    ↓
Relevant Context
    ↓
LangGraph Agent
    ↓
Final Answer
```

---

# 🛡️ Human-in-the-Loop Safety

```text
Agent decides an action is required
            ↓
     Interrupt workflow
            ↓
   Show action summary
            ↓
User chooses:
Approve / Reject
            ↓
       Resume Agent
```

This adds an additional safety layer before sensitive operations are completed.

---

# 🧠 Tech Stack

- Python
- LangChain
- LangGraph
- FastMCP
- Qdrant
- FastEmbed
- SQLite
- Groq
- Anthropic
- OpenAI
- Hugging Face
- Langfuse
- Rich
- UV
- Docker
- GitHub Actions

---

# 🔐 Environment Variables

The required API key depends on the provider configured in:

```text
src/repomind/config/config.yaml
```

Example:

```env
GROQ_API_KEY=your_key_here

LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=https://cloud.langfuse.com
```

Langfuse variables are optional.

> Never commit real API keys to GitHub.

---

# 🔄 Continuous Integration

RepoMind uses GitHub Actions for Continuous Integration.

On pushes and pull requests, the workflow automatically performs project checks.

```text
Checkout Code
      ↓
Set Up Python
      ↓
Install UV
      ↓
Install Dependencies
      ↓
Run Project Checks
      ↓
Pass ✅ / Fail ❌
```

GitHub Actions validates repository changes. Cloning the repository does not trigger the workflow.

---

# 📁 Project Structure

```text
Repomind/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   └── repomind/
│       ├── agents/
│       ├── config/
│       │   └── config.yaml
│       ├── retriever/
│       ├── tools/
│       ├── utils/
│       ├── cli.py
│       └── .env
│
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── README.md
```



# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Clone your fork.
3. Create a new branch.
4. Make your changes.
5. Test your changes.
6. Push changes to your fork.
7. Create a Pull Request.

GitHub Actions will run configured checks on pull requests.

---

# 🐛 Found a Bug?

If you find an error or unexpected behavior, please open an issue.

Please include:

- A clear description of the problem
- Steps to reproduce it
- The error message
- Your operating system
- Python version
- Relevant configuration details

> 🔐 Do not include API keys, secrets, tokens, or the contents of your `.env` file.



# 👨‍💻 Author

**Nitesh Yadav**

Aspiring Applied AI Engineer

- Python
- Machine Learning
- Deep Learning
- Generative AI
- RAG
- LangChain
- LangGraph
- Agentic AI