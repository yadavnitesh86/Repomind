import os
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from repomind.retriever.factory import get_embedder, get_collection_name
from repomind.utils.logger import get_logger
from repomind.retriever.file_loader import RepositoryLoader
from repomind.retriever.chunker import RepositoryChunker

logger = get_logger(__name__)


def index_codebase():
    embedder = get_embedder()
    collection_name = get_collection_name()
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    client = QdrantClient(url=url, api_key=api_key)
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        info = client.get_collection(collection_name)
        if info.points_count > 0:
            logger.info(f"Loaded existing index with {info.points_count} chunks")
            return QdrantVectorStore.from_existing_collection(
                embedding=embedder,
                sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
                retrieval_mode=RetrievalMode.HYBRID,
                url=url,
                api_key=api_key,
                collection_name=collection_name,
            )
    repository_loader = RepositoryLoader()
    documents = repository_loader.load()
    repository_chunker = RepositoryChunker()
    chunks = repository_chunker.chunk(documents)
    vector_store = QdrantVectorStore.from_documents(
        chunks,
        embedder,
        sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
        retrieval_mode=RetrievalMode.HYBRID,
        url=url,
        api_key=api_key,
        collection_name=collection_name,
        batch_size=50,
    )
    return vector_store
