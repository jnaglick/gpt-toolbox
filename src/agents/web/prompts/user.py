from .special_tokens import *

def context_section(context_items):
    return INPUT_SECTION_CONTEXT_ITEMS_SEPARATOR.join([
        f"{action}: {action_input}\n{INPUT_SECTION_CONTEXT_ITEM_RESULT}: {result}"
        for (action, action_input, result) in context_items
    ])

def user(question, context_items=[]): return f""" 
{INPUT_SECTION_CONTEXT}:
{context_section(context_items)}
{INPUT_SECTION_QUESTION}: {question}
""".strip()