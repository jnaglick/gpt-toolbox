# most basic agent: prompts the llm once with a few examples
from console import console
from llm import chat_completion

from .prompts import DEFAULT_SYSTEM, DEFAULT_EXAMPLES

class FewShotAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def parse_completion(self, completion, *args, **kwargs):
        return completion

    def prompt(self, query, *args, **kwargs):
        return DEFAULT_SYSTEM, DEFAULT_EXAMPLES, query

    def prediction(self, *args, **kwargs):
        with console.status(f"[bold green]Executing Agent: {self.agent_name}...[/]"):
            console.log(f"({self.agent_name}) Getting prediction...")   

            system, examples, user = self.prompt(*args, **kwargs)

            console.verbose((system, examples, user))

            completion = chat_completion(system, examples, user)

            if not completion:
                console.error(f"({self.agent_name}) Fail: Couldn't get LLM completion")
                # TODO retry
                return None
            
            console.verbose(completion)

            prediction = self.parse_completion(completion, *args, **kwargs)

            if not prediction:
                console.error(f"({self.agent_name}) Fail: Couldn't parse LLM completion")
                # TODO retry
                return None

            return prediction
