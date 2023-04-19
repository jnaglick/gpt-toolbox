# agent with the ability to search and access webpages

from llm import chat_completion
from utils import duckduckgo, web_request

from .prompt import system, examples, user, user_context, refine_search

SYSTEM = system()
EXAMPLES = examples()

def send_completion(user_prompt):
    return chat_completion(SYSTEM, EXAMPLES, user_prompt)

class PromptBuilder:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self):
        query = self.agent.query
        context = user_context(self.agent.context_items[::-1])
        return user(query, context)

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
        return send_completion(self.prompt())

def parse_output(output):
    lines = output.split("\n")
    final = lines[-1]
    if final.startswith("Answer:"):
        return "Answer", final[len("Answer: "):].strip()
    elif final.startswith("WebSearch:"):
        return "WebSearch", final[len("WebSearch: "):].strip()
    elif final.startswith("WebAccess:"):
        return "WebAccess", final[len("WebAccess: "):].strip()
    else:
        return False

def run_agent(web_agent):
    # get prediction
    prediction = web_agent.prediction()
    
    print(prediction) # if verbose

    # parse
    action, action_input = parse_output(prediction)

    # return answer if we have it
    if action == "Answer":
        return action_input

    # else, take next step
    if action == "WebSearch":
        result = duckduckgo(action_input)
    elif action == "WebAccess":
        result = web_request(action_input)
        result = chat_completion(
            "You're a helpful summarizing agent.", 
            [], 
            refine_search(web_agent.query, result)
        )

    web_agent.add_to_context(action, action_input, result)
    return run_agent(web_agent)

def agent(query):
    agent = WebAgent(query)
    return run_agent(agent)
