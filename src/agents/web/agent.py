# agent with the ability to search and access webpages
from agents.few_shot.relevence_summary import relevence_summary
from console import console
from llm import chat_completion
from utils import duckduckgo, web_request

from .prompts import system, examples, user

SYSTEM = system()
EXAMPLES = examples()

class PromptBuilder:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self):
        return user(self.agent.query, self.agent.context_items[::-1])

class WebAgent:
    def __init__(self, query):
        self.query = query
        self.context_items = []
        self.prompt = PromptBuilder(self)

    def clear_context(self):
        self.context_items = []
        return self

    def add_to_context(self, action, action_input, result):
        self.context_items.append((action, action_input, result))
        return self

    def prediction(self):
        console.log('(WebInformed) Getting prediction...')

        console.verbose([ (action, action_input, result) for (action, action_input, result) in self.context_items ])

        prediction = chat_completion(SYSTEM, EXAMPLES, self.prompt())

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

def exec_action(web_agent, action, action_input):
    if action == "WebSearch":
        return duckduckgo(action_input)

    if action == "WebAccess":
        web_request_result = web_request(action_input)
        return relevence_summary(web_agent.query, web_request_result)

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
