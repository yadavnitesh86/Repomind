import os
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from repomind.retriever.factory import get_embedder, get_collection_name
from repomind.utils.logger import get_logger
from repomind.retriever.file_loader import RepositoryLoader
from repomind.retriever.chunker import RepositoryChunker

logger = get_logger(__name__)
from repomind.retriever.repository_hash import (
    get_repository_hash,
    load_previous_hash,
    save_hash,
)

def index_codebase():

    embedder = get_embedder()
    collection_name = get_collection_name()

    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    try:
        client = QdrantClient(url=url, api_key=api_key)
        existing = [c.name for c in client.get_collections().collections]
    except Exception as e:
        logger.error(f"Cannot reach Qdrant at {url}: {e}")
        raise RuntimeError(
            "Vector store unavailable — check QDRANT_URL/QDRANT_API_KEY."
        ) from e

    

    # Load current repository
    repository_loader = RepositoryLoader()
    documents = repository_loader.load()

    # Calculate current repository hash
    current_hash = get_repository_hash(documents)

    # Load hash from the last indexing
    previous_hash = load_previous_hash()
    # Use existing index if repository has not changed
    if (
        collection_name in existing
        and previous_hash == current_hash
    ):
        info = client.get_collection(collection_name)

        if info.points_count > 0:
            logger.info(
                f"Repository unchanged. "
                f"Loaded existing index with {info.points_count} chunks"
            )

            return QdrantVectorStore.from_existing_collection(
                embedding=embedder,
                sparse_embedding=FastEmbedSparse(
                    model_name="Qdrant/bm25"
                ),
                retrieval_mode=RetrievalMode.HYBRID,
                url=url,
                api_key=api_key,
                collection_name=collection_name,
            )

    # Repository changed, remove old index
    if collection_name in existing:
        logger.info("Repository changed. Rebuilding index...")

        client.delete_collection(
            collection_name=collection_name
        )

    # Chunk latest repository
    repository_chunker = RepositoryChunker()
    chunks = repository_chunker.chunk(documents)

    # Create fresh vector store
    vector_store = QdrantVectorStore.from_documents(
        chunks,
        embedder,
        sparse_embedding=FastEmbedSparse(
            model_name="Qdrant/bm25"
        ),
        retrieval_mode=RetrievalMode.HYBRID,
        url=url,
        api_key=api_key,
        collection_name=collection_name,
        batch_size=50,
    )

    # Save hash of the repository that was just indexed
    save_hash(current_hash)

    logger.info(
        f"Repository indexed successfully with {len(chunks)} chunks"
    )

    return vector_store
