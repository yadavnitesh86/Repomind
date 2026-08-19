from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
)


class RepositoryChunker:
    LANGUAGE_MAP = {
        ".py": Language.PYTHON,
        ".js": Language.JS,
        ".ts": Language.TS,
        ".java": Language.JAVA,
        ".cpp": Language.CPP,
        ".c": Language.C,
        ".go": Language.GO,
        ".rs": Language.RUST,
        ".php": Language.PHP,
        ".rb": Language.RUBY,
        ".cs": Language.CSHARP,
        ".swift": Language.SWIFT,
        ".kt": Language.KOTLIN,
        ".scala": Language.SCALA,
        ".html": Language.HTML,
        ".md": Language.MARKDOWN,
    }

    def __init__(
        self,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _get_splitter(self, extension: str):

        language = self.LANGUAGE_MAP.get(extension.lower())

        if language:
            return RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
            )

        # Fallback for unknown/config files
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                " ",
                "",
            ],
        )

    def chunk(self, documents: list[Document]) -> list[Document]:

        all_chunks = []

        for document in documents:
            extension = document.metadata.get(
                "file_extension",
                "",
            )

            splitter = self._get_splitter(extension)

            chunks = splitter.split_documents([document])

            for index, chunk in enumerate(chunks):
                chunk.metadata["chunk_index"] = index

            all_chunks.extend(chunks)

        return all_chunks
