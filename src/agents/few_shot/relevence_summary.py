from .agent import FewShotAgent

agent = FewShotAgent("RelevenceSummary")

PROMPT = """
Given this query:
{}
Give a very brief summary of the relevant information from this result:
{}
If the result is not relevant, only output "<NOT_RELEVANT>".
"""

def relevence_summary(query, text_to_summarize):
    prompt = PROMPT.format(query, text_to_summarize).strip()
    return agent.prediction(prompt)
