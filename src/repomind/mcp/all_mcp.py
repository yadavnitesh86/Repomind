import sys


mcp = {
    "retriever": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [
            "-m",
            "repomind.retriever.mcp",
        ],
    }
}