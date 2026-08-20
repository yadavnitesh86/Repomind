import sys
from pathlib import Path
import os
from dotenv import load_dotenv
REPOSITORY_PATH = Path.cwd().resolve()
load_dotenv()

import logging
logger = logging.getLogger(__name__)
logger.info("Repository path: %s", REPOSITORY_PATH)

mcp = {
    "retriever": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [
            "-m",
            "repomind.retriever.mcp_server",
        ],
    },
    "filesystem": {
        "transport": "stdio",
        "command": "cmd",
        "args": [
            "/c",
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(REPOSITORY_PATH),
        ],
    },
    "git": {
        "transport": "stdio",
        "command": "uvx",
        "args": [
            "mcp-server-git",
            "--repository",
            str(REPOSITORY_PATH),
        ],
    },
    
}
