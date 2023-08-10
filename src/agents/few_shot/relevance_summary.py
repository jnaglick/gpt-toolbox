from .agent import FewShotAgent

def user(query, text_to_summarize):
    return f"""
Given the following Query, extract all relevant or related information from the following Text.
If the text does not help answer the query in any way, say "<NOT_RELEVANT>".
Repeat relevant facts and figures exactly as they appear.
Query:
{query}
Text:
{text_to_summarize}
""".strip()

class RelevanceSummaryAgent(FewShotAgent):
    def user_prompt(self, query, text_to_summarize):
        return user(query, text_to_summarize)
