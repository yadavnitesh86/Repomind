from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import asyncio
from repomind.utils.logger import get_logger
from repomind.retriever.factory import (
    get_thread_id,
    get_checkpointer_db_path,
)
from repomind.agents.agent import build_graph

logger = get_logger(__name__)


async def async_main():

    async with AsyncSqliteSaver.from_conn_string(
        get_checkpointer_db_path()
    ) as checkpointer:
        thread_id = get_thread_id()

        agent = await build_graph(checkpointer)

        config = {"configurable": {"thread_id": thread_id}}

        while True:
            query = input("\nYou: ")

            if query.lower() in {"exit", "quit"}:
                break

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}, config=config
            )
            print(f"\nRepoMind: {response['messages'][-1].content}")

def main():
    asyncio.run(async_main())
