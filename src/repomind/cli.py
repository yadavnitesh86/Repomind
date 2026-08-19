from repomind.retriever.file_loader import RepositoryLoader


def main():
    print("\nRepoMind started!\n")

    repository_loader = RepositoryLoader()

    print(f"Current project: {repository_loader.project_path}")

    documents = repository_loader.load()

    print(f"Documents loaded: {len(documents)}")

    for i, document in enumerate(documents, start=1):
        print("\n" + "=" * 60)
        print(f"DOCUMENT {i}")
        print("=" * 60)

        print("Metadata:")
        print(document.metadata)

        print("\nContent:")
        print(document.page_content)
