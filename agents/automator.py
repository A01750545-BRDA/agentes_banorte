from conversation.local.utils import pretty_format_history, update_local_history

from langgraph.graph import END, StateGraph
from agents.schemas import AgentState


REQUIRED_FIELDS = ['Tipo de movimiento (Ingresar / Egresar)', 'Frecuecia de transacción', 'Cantidad a mover']

def get_history_aware_input(state):
    history_str = pretty_format_history(
        state['history'], 
        last_k=2, 
        include_summary=False
    )
    state['history_enriched_input'] = state['agent_tools']['input_history_enricher_chain'].invoke(
        {
            'history': history_str, 
            'input': state['input']
        }
    )

    return state

def check_filled_details(state):
    for characteristic in REQUIRED_FIELDS:
        state['characteristics'][characteristic] = state['agent_tools']['get_element_in_text'].invoke(
            {
                'elemento': characteristic, 
                'input': state['input'],
            }
        )

    return state

async def get_remaining_details(state):
    history_str = pretty_format_history(state['history'])
    
    inputs = {
        'missing_characteristics': state['characteristics'],
        'input': state['input'],
        'history': history_str,
    }
    
    output = str()

    async for event in state['agent_tools']['detail_retriever'].astream_events(inputs, version='v2'):
        if event['event'] == 'on_chain_stream':
            token = event['data']['chunk'].content
            output += token

            if token:
                if state['token_processor']['is_async']:
                        await state['token_processor']['fn'](output, token)
                else:
                    state['token_processor']['fn'](output, token)

    print()
    
    state['output'] = output

    update_local_history(state['history'], state['input'], state['output'])
    return state

def funnel(state):
    return state

def details_fulfilled(state):
    if any(len(c) < 2 for c in state['characteristics'].values()):
        state['current_agent'] = 'automatizar'
    state['current_agent'] = None


workflow = StateGraph(AgentState)


workflow.add_node('history_aware_input', get_history_aware_input)
workflow.set_entry_point('history_aware_input')

workflow.add_node('check_filled_details', check_filled_details)
workflow.add_edge('history_aware_input', 'check_filled_details')

workflow.add_node('get_remaining_details', get_remaining_details)
workflow.add_edge('check_filled_details', 'get_remaining_details')

workflow.add_node('funnel', funnel)
workflow.add_edge('get_remaining_details', 'funnel')

workflow.add_node('details_fulfilled', details_fulfilled)
workflow.add_edge('funnel', 'details_fulfilled')

workflow.add_edge('details_fulfilled', END)


automator_graph = workflow.compile()

__all__ = [
    'automator_graph',
]