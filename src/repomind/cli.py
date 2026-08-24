from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.types import Command
import os
from repomind.agents.welcome_message import show_welcome
import asyncio
from repomind.agents.print_intrupt import print_interrupt_summary
from langfuse.langchain import CallbackHandler
from repomind.utils.logger import get_logger
from repomind.retriever.factory import (
    get_thread_id,
    get_checkpointer_db_path,
)
from dotenv import load_dotenv
from repomind.agents.agent import build_graph
load_dotenv()

logger = get_logger(__name__)
langfuse_handler = None
if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
    langfuse_handler = CallbackHandler()


async def async_main():

    async with AsyncSqliteSaver.from_conn_string(
        get_checkpointer_db_path()
    ) as checkpointer:

        thread_id = get_thread_id()

        agent = await build_graph(checkpointer)

        config = {"configurable": {"thread_id": thread_id}}
        if langfuse_handler is not None:
            config["callbacks"] = [langfuse_handler]

        while True:

            query = input("\nYou: ")

            if query.lower() in {"exit", "quit"}:
                break

            # First agent call
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}, config=config
            )

            while "__interrupt__" in response:

                interrupt = response["__interrupt__"][0]

                print_interrupt_summary(interrupt)

                decision = (
                    input("\nApprove or reject? [approve/reject]: ").strip().lower()
                )

                if decision not in {"approve", "reject"}:
                    print("Please enter approve or reject.")
                    continue

                response = await agent.ainvoke(
                    Command(resume={"decisions": [{"type": decision}]}), config=config
                )

            if response.get("messages"):
                print(f"\nRepoMind: " f"{response['messages'][-1].content}")


def main():
    show_welcome()
    asyncio.run(async_main())
