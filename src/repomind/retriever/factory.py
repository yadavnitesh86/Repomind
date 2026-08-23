from repomind.utils.logger import get_logger
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

logger = get_logger(__name__)
from repomind.config.config import load_config
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from pathlib import Path
import hashlib
import uuid
from repomind.mcp_server.all_mcp import mcp

load_dotenv()

config = load_config()


logger = get_logger(__name__)


def get_embedder():
    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        provider="hf-inference",
    )


def get_collection_name() -> str:

    project_path = str(Path.cwd().resolve())

    project_hash = hashlib.sha256(project_path.encode("utf-8")).hexdigest()[:16]

    return f"repomind_{project_hash}"


def get_llm():
    provider = config["ChatGroq"]["provider"]
    model = config["ChatGroq"]["model"]

    if provider == "ChatGroq":
        from langchain_groq import ChatGroq

        
        return ChatGroq(model=model)

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        
        return ChatAnthropic(model=model)

    else:
        from langchain_openai import ChatOpenAI

        
        return ChatOpenAI(model=model)


async def get_mcp_tools() -> list:
    """Connect to all configured MCP servers and return their tools."""
    configs = mcp
    logger.info(f"Connecting to MCP servers: {list(configs.keys())}")
    client = MultiServerMCPClient(configs)
    tools = await client.get_tools()
    logger.info(f"Loaded {len(tools)} tools from MCP servers")
    return tools


def get_checkpointer_db_path() -> str:
    db_path = config["memory"]["db_path"]
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Using SQLite checkpointer at {db_path}")
    return db_path


def get_checkpointer() -> AsyncSqliteSaver:
    db_path = get_checkpointer_db_path()
    return AsyncSqliteSaver.from_conn_string(db_path)


def create_thread_id() -> str:
    """Create a unique thread ID for a new conversation."""
    return str(uuid.uuid4())


def get_thread_id() -> str:
    """Ask the user whether to resume or start a new conversation."""

    choice = (
        input("\nDo you want to resume an existing conversation? (yes/no): ")
        .strip()
        .lower()
    )

    if choice in ("yes", "y"):
        thread_id = input("Enter your existing thread ID: ").strip()

        if thread_id:
            print(f"\nResuming conversation: {thread_id}")
            return thread_id

        print("\nNo thread ID provided. Creating a new conversation.")

    elif choice in ("no", "n"):
        print("\nStarting a new conversation.")

    else:
        print("\nInvalid choice. Starting a new conversation.")

    thread_id = create_thread_id()

    print(
        f"\nNew conversation started. Please copy or save thread_id for future conversation \n"
    )
    print(f"Thread ID: {thread_id}")

    return thread_id
