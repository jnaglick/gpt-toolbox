# agent with the ability to search and access webpages
from agents.few_shot.relevence_summary import relevence_summary
from console import console
from llm import chat_completion
from utils import duckduckgo, web_request

from .prompts import system, examples, user

SYSTEM = system()
EXAMPLES = examples()

class WebAgent:
    def __init__(self, query):
        self.query = query
        self.context_items = []

    def add_to_context(self, action, action_input, result):
        self.context_items.append((action, action_input, result))
        return self

    def prediction(self):
        console.log('(WebInformed) Getting prediction...')

        console.verbose(self.context_items)

        prompt = user(self.query, self.context_items[::-1])
        prediction = chat_completion(SYSTEM, EXAMPLES, prompt)

        if not prediction:
            console.error("(WebInformed) Fail: Couldn't get LLM prediction")
        else:
            console.log(prediction) # verbose?

        return prediction

def parse_prediction(prediction):
    lines = prediction.strip().split("\n")
    final = lines[-1]
    if final.startswith("Answer:"):
        return "Answer", final[len("Answer:"):].strip()
    elif final.startswith("WebSearch:"):
        return "WebSearch", final[len("WebSearch:"):].strip()
    elif final.startswith("WebAccess:"):
        return "WebAccess", final[len("WebAccess:"):].strip()
    else:
        console.error(f"Fail: Couldn't parse LLM output")
        return False, ""

def get_relevence_summary(query, url):
    web_request_result = web_request(url)
    return relevence_summary(query, web_request_result)

def exec_action(web_agent, action, action_input):
    if action == "WebSearch":
        results = duckduckgo(action_input)
        return [
            (result[0], result[1], get_relevence_summary(web_agent.query, result[1])) for result in results 
        ]

    if action == "WebAccess":
        return get_relevence_summary(web_agent.query, action_input)

def run_agent(web_agent):
    with console.status("[bold green]Executing Agent: WebInformed...[/]"): # TODO decorator
        # get prediction
        prediction = web_agent.prediction()

        if not prediction:
            return None # TODO try again if < max_iterations

        # parse
        action, action_input = parse_prediction(prediction)

        if not action:
            return None # TODO try again if < max_iterations

        console.log(f"[bold]Action: {action}[/] ({action_input})")

        # return answer if we have it
        if action == "Answer":
            return action_input

        # else, invoke action
        action_result = exec_action(web_agent, action, action_input)

        if not action_result:
            return None # TODO try again (if < max_iterations) ?

        # take next step (update context and iterate)
        web_agent.add_to_context(action, action_input, action_result)
        return run_agent(web_agent)

def agent(query):
    web_agent = WebAgent(query)
    return run_agent(web_agent)
