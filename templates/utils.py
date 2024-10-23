from langchain_core.prompts.prompt import PromptTemplate

MEMORY_TEMPLATE = '''Resume progresivamente las líneas de conversación proporcionadas, añadiendo a la resumen anterior y devolviendo un nuevo resumen. DEVUELVE SOLAMENTE el nuevo resumen.

EJEMPLO
Resumen actual:
El humano pregunta qué piensa la IA sobre la inteligencia artificial. La IA piensa que la inteligencia artificial es una fuerza para el bien.

Nuevas líneas de conversación:
Humano: ¿Por qué crees que la inteligencia artificial es una fuerza para el bien?
IA: Porque la inteligencia artificial ayudará a los humanos a alcanzar su máximo potencial.

Nuevo resumen (Lo que debes devolver):
El humano pregunta qué piensa la IA sobre la inteligencia artificial. La IA piensa que la inteligencia artificial es una fuerza para el bien porque ayudará a los humanos a alcanzar su máximo potencial.
FIN DEL EJEMPLO

Resumen actual:
{summary}

Nuevas líneas de conversación:
{new_lines}

Nuevo resumen:'''

MEMORY_PROMPT = PromptTemplate(input_variables=['summary', 'new_lines'], template=MEMORY_TEMPLATE)


HISTORY_ENRICHER_TEMPLATE = '''Dada una conversación, utiliza el contexto para reformular la ultima petición del usuario de manera que no necesite contexto adicional.
Solo usa el contexto en caso de ser necesario, caso contrario, regresa la misma petición tal cual como fue formulada.
SE LO MÁS ESPECIFICO POSIBLE, y para reformular la pregunta prioriza las peticiones del usuario sobre la respuesta del modelo.

Ejemplo 1:
Humano: Quien es el jefe?
AI: El jefe es Jeff Bezos
Humano: Cuéntame más
Reformulado: Cuéntame más del jefe

Ejemplo 2:
Humano: Como hago un cisne de origami
AI: Un cisne de origami lo puedes hacer ...
Humano: Y como hago una rana de origami
Reformulado: Y como hago una rana de origami

Ejemplo 3:
Humano: Con quien debo ir si mi mouse falla?
AI: Debes ir con ...
Humano: Y si mi compu falla?
Reformulado: Con quien debo ir si mi computadora falla?

Conversación actual:
{history}
Humano: {input}
Reformulado: '''

HISTORY_ENRICHER_PROMPT = PromptTemplate(
    input_variables=['history', 'input'], 
    template=HISTORY_ENRICHER_TEMPLATE)

ELEMENT_EXTRACTOR_TEMPLATE = '''Regresa el elemento {elemento} en caso de que se mencione en el siguiente parrafo:
{input}

En caso que no se mencione la característica, regresa un string vacío '' sin explicación extra.
En caso que si se mencione, regrese la característica sin explicaciones.
AI: '''

ELEMENT_EXTRACTOR_PROMPT = PromptTemplate(input_variables=['elemento', 'input'], template=ELEMENT_EXTRACTOR_TEMPLATE)

ROUTER_TEMPLATE = '''Dado un mensaje de un usuario, escoge cual de las siguientes acciones se deberian realizar.
Responde con solamente el número.

0. Platica normal
1. Hacer inversion
2. Automatizar un pago

Humano: {input}
Respuesta: '''

ROUTER_PROMPT = PromptTemplate(input_variables=['input'], template=ROUTER_TEMPLATE)