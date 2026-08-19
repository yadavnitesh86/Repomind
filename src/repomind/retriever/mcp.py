from fastmcp import FastMCP

from repomind.retriever.retriever import RepositoryRetriever
from repomind.utils.logger import get_logger


logger = get_logger(__name__)


mcp = FastMCP(name="retriever")


repository_retriever = None


def get_repository_retriever() -> RepositoryRetriever:
    global repository_retriever

    if repository_retriever is None:
        logger.info("Initializing repository retriever...")

        repository_retriever = RepositoryRetriever()

    return repository_retriever


@mcp.tool(description="Search the repository for code and documents relevant to a natural-language query. Input: query only. Does not read arbitrary files by path.")
def search_repository(query: str) -> list[dict]:
    """
    Search the current repository using hybrid retrieval.

    Use this tool to find relevant source code, functions,
    classes, configurations, documentation, and implementation
    details inside the repository.

    Args:
        query: A natural-language or code-related search query.

    """

    logger.info(
        "MCP search request: %s",
        query,
    )

    retriever = get_repository_retriever()
    results = retriever.search(query)

    return [
        {
            "content": document.page_content,
            "relative_path": document.metadata.get("relative_path"),
            "file_name": document.metadata.get("file_name"),
            "file_extension": document.metadata.get("file_extension"),
            "chunk_index": document.metadata.get("chunk_index"),
        }
        for document in results
    ]


if __name__ == "__main__":
    logger.info("Starting RepoMind FastMCP server...")

    mcp.run(transport="stdio")
