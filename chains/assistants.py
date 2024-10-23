from langchain_core.runnables.base import RunnableSequence, Runnable

from templates import ASSISTANT_PROMPT, DETAIL_PROMPT


def create_assistant_chain(llm: Runnable) -> RunnableSequence:
    return ASSISTANT_PROMPT | llm

def create_detail_retriever(llm: Runnable) -> RunnableSequence:
    return DETAIL_PROMPT | llm