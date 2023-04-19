from llm import chat_completion
from tasks import task_dictionary, task_prompt_segment

from .prompts import system, examples, user
from .verify_plan import verify_plan

def agent(query):
    plan = chat_completion(
        system(task_prompt_segment),
        examples(), 
        user(query)
    )

    print("Got Plan")
    print("========")
    print(plan)
    print("========")

    print("Is valid:", verify_plan(plan, task_dictionary))

    return plan