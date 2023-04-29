# agent with the ability to search the web
from agents.few_shot import FewShotAgent, RelevenceSummaryAgent
from utils import duckduckgo, web_request

from .parse_completion import parse_completion
from .prompts import system, examples, user
from .prompts.special_tokens import SECTION_ANSWER, SECTION_WEB_SEARCH

def search_action(search_term, relevance_summary):
    search_results = duckduckgo(search_term, num_results=3)
    return [
        (title, url, relevance_summary(search_term, web_request(url)))
        for title, url in search_results 
    ]

class WebInformedAgent(FewShotAgent):
    def __init__(self, name):
        super().__init__(name)
        self.context_items = []
        self.relevance_summary_agent = RelevenceSummaryAgent(f"{name}/RelevanceSummary")

    def add_to_context(self, action, action_input, action_result):
        self.context_items.insert(0, (action, action_input, action_result))

    def prompt(self, query):
        return system(), examples(), user(query, self.context_items)

    def handle_completion(self, completion, query):
        parsed = parse_completion(completion)

        if not parsed:
            # TODO handle better
            return None

        if parsed[SECTION_ANSWER]:
            return parsed[SECTION_ANSWER]
        
        if parsed[SECTION_WEB_SEARCH]:
            search_term = parsed[SECTION_WEB_SEARCH]
            search_result = search_action(search_term, self.relevance_summary_agent.prediction)
            self.add_to_context(SECTION_WEB_SEARCH, search_term, search_result)
            return self.prediction(query)

        return None
