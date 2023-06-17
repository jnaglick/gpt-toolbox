from .duckduckgo import duckduckgo
from .web_request import web_request

def web_search(search_term, num_results=3, relevance_summary_fn=None):
    search_results = duckduckgo(search_term, num_results)
    results = [web_request(url) for _, url in search_results]

    if relevance_summary_fn:
        results = [relevance_summary_fn(search_term, content) for content in results]

    return [
        (title, url, content)
        for (title, url), content in zip(search_results, results)
    ]
