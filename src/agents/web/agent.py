# agent with the ability to search and access webpages
from agents.few_shot import FewShotAgent, RelevenceSummaryAgent
from utils import duckduckgo, web_request

from .prompts import system, examples, user
from .prompts.special_tokens import *

relevence_summary_agent = RelevenceSummaryAgent("RelevenceSummary")

def get_relevence_summary(query, url):
    web_request_result = web_request(url)
    return relevence_summary_agent.prediction(query, web_request_result)

def handle_search_action(search_term):
    search_results = duckduckgo(search_term, num_results=1)
    return [
        (title, url, get_relevence_summary(search_term, url)) for title, url in search_results 
    ]

class WebAgent(FewShotAgent):
    def __init__(self):
        super().__init__("WebInformed")
        self.context_items = []

    def add_to_context(self, action, action_input, action_result):
        self.context_items.append((action, action_input, action_result))
        return self

    def prompt(self, query):
        return system(), examples(), user(query, self.context_items[::-1])

    def parse_completion(self, completion, query):
        lines = completion.strip().split("\n")
        final = lines[-1]

        if final.startswith(f"{SECTION_ANSWER}:"):
            return final[len(f"{SECTION_ANSWER}:"):].strip()

        elif final.startswith(f"{SECTION_WEB_SEARCH}:"):
            search_term = final[len(f"{SECTION_WEB_SEARCH}:"):].strip()
            action_result = handle_search_action(search_term)
            self.add_to_context(SECTION_WEB_SEARCH, search_term, action_result)
            return self.prediction(query)

        else:
            return None

web_agent = WebAgent()

def agent(query):
    return web_agent.prediction(query)
