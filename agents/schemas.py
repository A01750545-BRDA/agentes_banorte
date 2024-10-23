from typing import TypedDict, Optional
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_core.runnables.base import Runnable

class AgentState(TypedDict):
    input: str
    history_enriched_input: Optional[str]
    output: Optional[str]
    history: ConversationSummaryBufferMemory
    agent_tools: dict
    llm: Runnable
    user_id: str
    characteristics: dict
    token_processor: dict
    current_agent: Optional[str]