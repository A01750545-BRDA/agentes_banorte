from langchain_core.runnables.base import Runnable, RunnableSequence

from templates import (
    HISTORY_ENRICHER_PROMPT,
    ELEMENT_EXTRACTOR_PROMPT,
    ROUTER_PROMPT,
    )

from langchain_core.output_parsers import StrOutputParser


def create_input_history_enricher_chain(llm: Runnable) -> RunnableSequence:
    return HISTORY_ENRICHER_PROMPT | llm | StrOutputParser()

def create_element_extractor_chain(llm: Runnable) -> RunnableSequence:
    return ELEMENT_EXTRACTOR_PROMPT | llm | StrOutputParser()

def router(llm: Runnable) -> RunnableSequence:
    return ROUTER_PROMPT | llm | StrOutputParser()