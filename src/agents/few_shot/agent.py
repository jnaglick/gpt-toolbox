# most basic agent: prompts the llm once with a few examples
from console import console
from llm import chat_completion

DEFAULT_SYSTEM = """
You're an expert assistant that gives formatted output exactly as specified
""".strip()

DEFAULT_EXAMPLES = []

class FewShotAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def parse_prediction(self, prediction):
        return prediction

    def prediction(self, user, system=DEFAULT_SYSTEM, examples=DEFAULT_EXAMPLES):
        with console.status(f"[bold green]Executing Agent: {self.agent_name} (Few Shot)...[/]"):
            console.log(f"({self.agent_name}) Getting prediction...")
            console.verbose((system, examples, user))

            prediction = chat_completion(system, examples, user)

            if not prediction:
                console.error(f"({self.agent_name}) Fail: Couldn't get LLM output")
                # TODO retry
                return None

            parsed_prediction = self.parse_prediction(prediction)

            if not parsed_prediction:
                console.error(f"({self.agent_name}) Fail: Couldn't parse LLM output")
                # TODO retry
                return None

            console.verbose(prediction)

            return parsed_prediction
