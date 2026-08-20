from langchain.agents.middleware.types import AgentState


from typing import Any


from repomind.retriever.factory import get_llm
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.middleware import PIIMiddleware
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.middleware import HumanInTheLoopMiddleware

PASSWORD_SHARE_PATTERN = (
    r"(?i)\b(?:my\s+)?(?:password|passwrod|passwd|pwd)\s*(?:is|=|:)\s*\S+"
)
PASSWORD_IN_RESPONSE_PATTERN = (
    r'(?i)(?:password|passwrod|passwd|pwd)\s*["\']?[\w!@#$%^&*.-]{3,}["\']?'
)
API_KEY_SHARE_PATTERN = r"(?i)\b(?:api[_\s-]?key|apikey)\s*(?:is|=|:)\s*\S+"

middleware = [
    SummarizationMiddleware(model=get_llm(),trigger=("tokens", 6000),keep=("messages", 10)),
    PIIMiddleware("email", strategy="redact", apply_to_input=True),
    PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ToolCallLimitMiddleware(run_limit=15,),
    ModelCallLimitMiddleware(run_limit=10,),
    PIIMiddleware("api_key_share",detector=API_KEY_SHARE_PATTERN,strategy="redact",apply_to_input=True,apply_to_output=True,),
    PIIMiddleware("openai_api_key",detector=r"sk-[a-zA-Z0-9]{20,}",strategy="block", apply_to_input=True,),
    PIIMiddleware("password_share",detector=PASSWORD_SHARE_PATTERN,strategy="redact",apply_to_input=True,apply_to_output=True,),
    PIIMiddleware("password_output",detector=PASSWORD_IN_RESPONSE_PATTERN,strategy="redact",apply_to_output=True,apply_to_tool_results=True,),
    HumanInTheLoopMiddleware[AgentState[Any], None, Any](interrupt_on={
        "write_file": {
            "allowed_decisions": ["approve", "reject"]
        },
        "edit_file": {
            "allowed_decisions": ["approve", "reject"]
        },
        "move_file": {
            "allowed_decisions": ["approve", "reject"]
        },
        "create_directory": {
            "allowed_decisions": ["approve", "reject"]
         },
         }
       )
    
    

]