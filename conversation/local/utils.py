from typing import Optional
from templates import MEMORY_PROMPT

from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langchain_core.runnables.base import Runnable


key_map = {
        'summary': 'summary',
        'human': 'human',
        'AI': 'AI',
        'messages': 'messages',
        'last_message': 'last_message',
        'tokens': 'tokens',
    }

MAX_MEMORY_TOKENS = 2048

def load_from_json(d: dict) -> tuple[str, list]:
    summary = d[key_map['summary']]
    messages = d[key_map['messages']][-d[key_map['last_message']]//2:]

    messages = [
        HumanMessage(content=message) if remitent == key_map['human'] else AIMessage(content=message) 
        for interaction in messages 
        for remitent, message in interaction.items()
        ]
    
    return summary, messages

def init_local_history(d: dict, 
                       llm: Runnable, 
                       prompt=MEMORY_PROMPT, 
                       max_token_limit=MAX_MEMORY_TOKENS,
                       ):
    
    summary, messages = load_from_json(d)
    
    return ConversationSummaryBufferMemory(
        llm=llm,
        prompt=prompt,
        max_token_limit=max_token_limit,
        chat_memory=InMemoryChatMessageHistory(messages=messages),
        moving_summary_buffer=summary,
        )


def update_local_history(history: ConversationSummaryBufferMemory, input: str, output: str) -> None:
    history.chat_memory.add_messages([HumanMessage(content=input), AIMessage(content=output)])
    history.prune()


def pretty_format_history(history: ConversationSummaryBufferMemory, 
                  human_prefix: str = 'Humano', ai_prefix: str = 'AI',
                  last_k: Optional[int] = None, include_summary: bool = True) -> str:
    
    summary = history.moving_summary_buffer + '\n' if include_summary else ''
    messages = history.chat_memory.messages if last_k is None else history.chat_memory.messages[-last_k:]
    
    return (summary + 
            get_buffer_string(messages, 
                             human_prefix=human_prefix,
                             ai_prefix=ai_prefix))