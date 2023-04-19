CONTEXT_ITEMS_SEPARATOR = "|||||"

def user(question, context=""): return f""" 
CONTEXT:
{context}
QUESTION: {question}
""".strip()

def user_context(context_items):
    return CONTEXT_ITEMS_SEPARATOR.join([
        f"{action}: {action_input}\nResults: {result}"
        for (action, action_input, result) in context_items
    ])
