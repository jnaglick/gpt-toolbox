from .agent import FewShotAgent

def user(query, text_to_summarize):
    return f"""
Given this query:
{query}
Give a very brief summary of the relevant information from this result:
{text_to_summarize}
If the result is not relevant, only output "<NOT_RELEVANT>".
""".strip()

agent = FewShotAgent("RelevenceSummary")

def relevance_summary(query, text_to_summarize):
    return agent.prediction(user(query, text_to_summarize))
