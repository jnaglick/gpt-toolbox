# agent with the ability to search and access webpages
from console import console

from agents import relevence_summary_agent
from llm import chat_completion
from utils import duckduckgo, web_request

from .prompts import system, examples, user, user_context

SYSTEM = system()
EXAMPLES = examples()

class PromptBuilder:
    def __init__(self, agent):
        self.agent = agent

    def user_context(self):
        return user_context(self.agent.context_items[::-1])

    def __call__(self):
        return user(self.agent.query, self.user_context())

class WebAgent:
    def __init__(self, query):
        self.query = query
        self.context_items = []
        self.user_prompt = PromptBuilder(self)

    def clear_context(self):
        self.context_items = []
        return self

    def add_to_context(self, action, action_input, result):
        self.context_items.append((action, action_input, result))
        return self

    def prediction(self):
        console.log('(WebAgent) Getting prediction...')

        console.verbose([ (action, action_input, result) for (action, action_input, result) in self.context_items ])

        prediction = chat_completion(SYSTEM, EXAMPLES, self.user_prompt())

        if not prediction:
            console.error("(WebAgent) Fail: Couldn't get LLM prediction")
        else:
            console.log(prediction) # verbose?

        return prediction

def parse_output(output):
    lines = output.split("\n")
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

def run_agent(web_agent):
    # get prediction
    prediction = web_agent.prediction()

    if not prediction:
        return None # TODO try again if < max_iterations

    # parse
    action, action_input = parse_output(prediction)

    if not action:
        return None # TODO try again if < max_iterations

    console.log(f"[bold]Action: {action}[/] ({action_input})")

    # return answer if we have it
    if action == "Answer":
        return action_input

    # else, invoke action
    if action == "WebSearch":
        result = duckduckgo(action_input)
    elif action == "WebAccess":
        web_request_result = web_request(action_input)
        result = relevence_summary_agent(web_agent.query, web_request_result)
        if not result:
            return None # TODO try again (if < max_iterations) ?

    # take next step
    web_agent.add_to_context(action, action_input, result)
    return run_agent_with_status(web_agent)

def run_agent_with_status(web_agent):
    with console.status("[bold green]Executing Agent: WebInformed...[/]"):
        return run_agent(web_agent)

def agent(query):
    web_agent = WebAgent(query)
    return run_agent_with_status(web_agent)
