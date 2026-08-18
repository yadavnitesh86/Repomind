from pathlib import Path

from langchain_core.documents import Document


class RepositoryLoader:
    """Loads supported files from the current repository."""

    # Directories we should not scan
    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".idea",
        ".vscode",
        ".pytest_cache",
        ".mypy_cache",
    }

    # File types supported by RepoMind
    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".go",
        ".rs",
        ".cs",
        ".md",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
    }

    def __init__(self):
        """Initialize loader with the user's current directory."""

        self.project_path = Path.cwd().resolve()

    def _should_ignore(self, file_path: Path) -> bool:
        """
        Check whether a file is inside an ignored directory.
        """

        relative_path = file_path.relative_to(self.project_path)

        return any(
            part in self.IGNORED_DIRECTORIES
            for part in relative_path.parts
        )

    def _is_supported(self, file_path: Path) -> bool:
        """
        Check whether the file extension is supported.
        """

        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def _read_file(self, file_path: Path) -> str | None:
        """
        Read a file safely.

        Returns None if the file cannot be decoded as text.
        """

        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except OSError:
            return None

    def load(self) -> list[Document]:
        """
        Load supported repository files as LangChain Documents.
        """

        documents = []

        for file_path in self.project_path.rglob("*"):

            # Skip directories
            if not file_path.is_file():
                continue

            # Skip ignored directories
            if self._should_ignore(file_path):
                continue

            # Skip unsupported files
            if not self._is_supported(file_path):
                continue

            # Read file content
            content = self._read_file(file_path)

            # Skip unreadable or empty files
            if not content or not content.strip():
                continue

            # Get path relative to project root
            relative_path = file_path.relative_to(
                self.project_path
            )

            # Create LangChain Document
            document = Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "project_path": str(self.project_path),
                    "relative_path": str(relative_path),
                    "file_name": file_path.name,
                    "file_extension": file_path.suffix.lower(),
                },
            )

            documents.append(document)

        return documents