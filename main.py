import os
from fastapi import FastAPI, WebSocket

from agents.orchestrator import orchestrator_graph
from chains import create_assistant_chain, create_input_history_enricher_chain, create_detail_retriever, create_element_extractor_chain, router
from conversation.local.utils import init_local_history
from conversation.remote.utils import retrieve_remote_history, update_remote_history

from langchain_openai import ChatOpenAI


app = FastAPI()
llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

agent_tools = {
    'assistant_chain': create_assistant_chain(llm),
    'input_history_enricher_chain': create_input_history_enricher_chain(llm),
    'get_element_in_text': create_element_extractor_chain(llm),
    'detail_retriever': create_detail_retriever(llm),
    'router': router(llm)
}


@app.websocket("/")
async def main(websocket: WebSocket):
    await websocket.accept()
    user_id = '2'

    data = retrieve_remote_history(user_id)
    history = init_local_history(data, llm)

    constant_state = {
        'user_id': user_id,
        'agent_tools': agent_tools,
        'history': history,
        'llm': llm,
        'characteristics': dict(),
        'current_agent': None,
        'token_processor': {
            'is_async': True, 
            'fn': lambda output, token: websocket.send_text(output)},
    }

    state = {
        **constant_state,
        'input': None
    }

    while True:
        user_input = await websocket.receive_text()
        if user_input.lower() == 'bye':
            break
        elif user_input.lower() == 'r':
            state['current_agent'] = None
        
        state['input'] = user_input
        state = await orchestrator_graph.ainvoke(state)

        new_messages = {'input': state['input'], 'output': state['output']}

        update_remote_history(
            user_id=user_id, new_messages=new_messages,
        )

    update_remote_history(
        user_id=user_id, new_summary=history.moving_summary_buffer,
        new_last_message=len(history.chat_memory.messages),
    )
    
    await websocket.close()