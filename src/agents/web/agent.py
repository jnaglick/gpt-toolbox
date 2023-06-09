# agent with the ability to search the web
from agents.few_shot import FewShotAgent, RelevanceSummaryAgent
from utils import duckduckgo, web_request

from .parse_completion import parse_completion
from .prompts import system, examples, user
from .prompts.special_tokens import SECTION_ANSWER, SECTION_WEB_SEARCH

def search_action(search_term, relevance_summary_fn):
    search_results = duckduckgo(search_term, num_results=3)
    page_results = [web_request(url) for _, url in search_results]
    relevance_summaries = [relevance_summary_fn(search_term, content) for content in page_results]

    return [
        (title, url, summary)
        for (title, url), summary in zip(search_results, relevance_summaries)
    ]

class WebInformedAgent(FewShotAgent):
    def __init__(self, name, session):
        super().__init__(name, session)
        self.context_items = []
        self.relevance_summary_agent = RelevanceSummaryAgent(f"{name}/RelevanceSummary", session)

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
