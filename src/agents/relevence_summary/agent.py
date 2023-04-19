from console import console
from llm import chat_completion

from .prompt import relevence_summary

# TODO also more context? (InternalThought(s)) ?

SYSTEM = """
You're a helpful summarizing agent.
""".strip()

EXAMPLES = []

class RelevenceSummaryAgent:
    def prediction(self, query, text_to_summarize):
        user_prompt = relevence_summary(query, text_to_summarize)

        console.log('(RelevenceSummaryAgent) Getting prediction...')
        console.verbose(user_prompt)

        prediction = chat_completion(SYSTEM, EXAMPLES, user_prompt)

        if not prediction:
            console.error("(WebAgent) Fail: Couldn't get LLM prediction")
        else:
            console.verbose(prediction)

        return prediction

def agent(query, text_to_summarize):
    summary_agent = RelevenceSummaryAgent()

    with console.status("[bold green]Executing Agent: RelevenceSummary...[/]"):
        return summary_agent.prediction(query, text_to_summarize)
