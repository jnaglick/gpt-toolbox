# agent with the ability to search and access webpages
import re

from agents.few_shot import FewShotAgent, relevance_summary
from utils import duckduckgo, web_request

from .prompts import system, examples, user
from .prompts.special_tokens import *

def search_action(search_term):
    search_results = duckduckgo(search_term, num_results=1)
    return [
        (title, url, relevance_summary(search_term, web_request(url)))
        for title, url in search_results 
    ]

def completion_pattern():
    answer = f"{SECTION_ANSWER}:(?P<answer>[^\n]+)"
    web_search = f"{SECTION_WEB_SEARCH}:(?P<web_search>[^\n]+)"

    return re.compile(
        rf"{SECTION_PREVIOUS_ACTIONS}:(?P<previous_actions>[^\n]*)\n"
        rf"{SECTION_INTERNAL_THOUGHT}:(?P<internal_thought>[^\n]+)\n"
        rf"{SECTION_ENOUGH_INFO}:(?P<enough_info>yes|no)\n"
        rf"(?P<action_line>{'|'.join([answer, web_search])})\n?"
    )

COMPETION_PATTERN = completion_pattern()

def parse_completion(completion):
    match = COMPETION_PATTERN.match(completion)

    if match:
        return match.groupdict()
    else:
        return None

class WebAgent(FewShotAgent):
    def __init__(self):
        super().__init__("WebInformed")
        self.context_items = []

    def add_to_context(self, action, action_input, action_result):
        self.context_items.append((action, action_input, action_result))
        return self

    def prompt(self, query):
        return system(), examples(), user(query, self.context_items[::-1])

    def handle_completion(self, completion, query):
        parsed = parse_completion(completion)

        if not parsed:
            return None
        
        if parsed["answer"]:
            return parsed["answer"]
        
        if parsed["web_search"]:
            search_term = parsed["web_search"]
            search_result = search_action(search_term)
            self.add_to_context(SECTION_WEB_SEARCH, search_term, search_result)
            return self.prediction(query)

        return None

web_agent = WebAgent()

def agent(query):
    return web_agent.prediction(query)
