import hashlib
import json
from pathlib import Path


def get_repository_hash(documents):
    hasher = hashlib.sha256()

    documents = sorted(
        documents,
        key=lambda document: document.metadata.get(
            "relative_path",
            "",
        ),
    )

    for document in documents:
        path = document.metadata.get("relative_path", "")

        hasher.update(path.encode())
        hasher.update(document.page_content.encode())

    return hasher.hexdigest()


def get_state_path():
    state_dir = Path.cwd() / ".repomind"
    state_dir.mkdir(exist_ok=True)

    return state_dir / "index_state.json"


def load_previous_hash():
    state_path = get_state_path()

    if not state_path.exists():
        return None

    with open(state_path, "r") as file:
        data = json.load(file)

    return data.get("repository_hash")



def save_hash(repository_hash):
    state_path = get_state_path()

    with open(state_path, "w") as file:
        json.dump(
            {"repository_hash": repository_hash},
            file,
        )