from repomind.retriever.qdrant_store import index_codebase
from repomind.utils.logger import get_logger


logger = get_logger(__name__)


class RepositoryRetriever:
    def __init__(self):

        logger.info("Initializing repository hybrid retriever...")

        self.vector_store = index_codebase()

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})

    def search(self, query: str):

        logger.info(f"Searching repository for: {query}")

        results = self.retriever.invoke(query)

        logger.info(f"Retrieved {len(results)} relevant chunks.")

        return results
