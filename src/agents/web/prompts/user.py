from .special_tokens import CONTEXT_ITEMS_SEPARATOR

def context_section(context_items):
    return CONTEXT_ITEMS_SEPARATOR.join([
        f"{action}: {action_input}\nResults: {result}"
        for (action, action_input, result) in context_items
    ])

def user(question, context_items=[]): return f""" 
CONTEXT:
{context_section(context_items)}
QUESTION: {question}
""".strip()