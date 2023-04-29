# most basic agent: prompts the llm once with a few examples
from console import console
from llm import chat_completion

DEFAULT_SYSTEM = """
You're an expert assistant that gives formatted output exactly as specified.
""".strip()

# TODO "Think about the problem step by step..."

DEFAULT_EXAMPLES = []

class FewShotAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def system_prompt(self, *args, **kwargs):
        return DEFAULT_SYSTEM
    
    def examples_prompt(self, *args, **kwargs):
        return DEFAULT_EXAMPLES
    
    def user_prompt(self, query, *args, **kwargs):
        return query

    def prompt(self, *args, **kwargs):
        return (
            self.system_prompt(*args, **kwargs),
            self.examples_prompt(*args, **kwargs),
            self.user_prompt(*args, **kwargs)
        )
    
    def handle_completion(self, completion, *args, **kwargs):
        return completion

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

            prediction = self.handle_completion(completion, *args, **kwargs)

            if not prediction:
                console.error(f"({self.agent_name}) Fail: Couldn't parse LLM completion")
                # TODO retry
                return None

            return prediction
