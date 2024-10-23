from conversation.local.utils import pretty_format_history
from agents.automator import automator_graph
from agents.investor import investor_graph
from agents.schemas import AgentState
from langgraph.graph import END, StateGraph

from conversation.local.utils import pretty_format_history, update_local_history


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


def chain_selection(state):
    if state['current_agent']:
        return state['current_agent']
    
    input = state['history_enriched_input']

    result = state['agent_tools']['router'].invoke(input)[:1]
    if result == '0':
        return 'asistente'
    elif result == '1':
        return 'invertir'
    else:
        return 'automatizar'


async def aasistente(state):
    history_str = pretty_format_history(state['history'])
    
    inputs = {
        'input': state['input'],
        'history': history_str,
    }
    
    output = str()

    async for event in state['agent_tools']['assistant_chain'].astream_events(inputs, version='v2'):
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


async def ainvertir(state):
    return await investor_graph.ainvoke(state)
    
async def aautomatizar(state):
    return await automator_graph.ainvoke(state) 


workflow = StateGraph(AgentState)

actions_map = {
    'asistente': aasistente,
    'invertir': ainvertir,
    'automatizar': aautomatizar,
}

for name, func in actions_map.items():
    workflow.add_node(name, func)
    workflow.add_edge(name, END)

workflow.add_node('history_aware_input', get_history_aware_input)
workflow.set_entry_point('history_aware_input')
workflow.add_conditional_edges('history_aware_input', chain_selection)

orchestrator_graph = workflow.compile()

__all__ = [
    'orchestrator_graph',
]