from repomind.retriever.factory import (
    get_llm,
    get_mcp_tools,
    get_checkpointer,
    get_thread_id,
    get_checkpointer_db_path,
)
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain.agents import create_agent
from repomind.agents.all_middleware import middleware
SYSTEM_PROMPT = """You are RepoMind, a senior software engineer with deep knowledge of the codebase.

When answering questions about the repository:

- Use the available tools to inspect and gather information from the codebase before answering.
- Choose the most appropriate available tool based on its name, description, and input schema.
- Follow each tool's input schema exactly.
- Never invent tool parameters or capabilities that are not defined in the available tools.
- Do not assume a tool can read, edit, search, or execute code unless that capability is explicitly provided by the tool.
- If the available tools cannot provide the required information, say so clearly.
- Base your answers on information retrieved from the codebase.
- Reference relevant files, functions, classes, and line numbers when they are available from tool results."""


async def build_graph(checkpointer):
    llm = get_llm()

    mcp_tools = await get_mcp_tools()

    return create_agent(
        model=llm,
        tools=mcp_tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
        middleware=middleware,
    )
