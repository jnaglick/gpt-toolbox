from console import console
from llm import chat_completion, ChatSession, get_model_spec, ModelType

DEFAULT_SYSTEM = """
You're an expert assistant that gives formatted output exactly as specified.
""".strip()

DEFAULT_EXAMPLES = []

class BasicFewShotAgent:
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

    def completion(self, system, examples, user, model):
        return chat_completion(system, examples, user, model)

    def handle_completion(self, completion, *args, **kwargs):
        return completion

    def prediction(self, *args, model=ModelType.GPT_3_5_TURBO, **kwargs):
        with console.status(self.prediction_status_msg()):
            console.log(f"({self.agent_name}) Getting prediction...")

            system, examples, user = self.prompt(*args, **kwargs)
            console.verbose((system, examples, user))

            completion = self.completion(system, examples, user, model)

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

    def prediction_status_msg(self):
        return f"[bold green]Executing Agent: {self.agent_name}[/]"

class FewShotAgent(BasicFewShotAgent):
    def __init__(self, agent_name, session=None):
        super().__init__(agent_name)
        self.session = session or ChatSession()

    def completion(self, system, examples, user, model):
        system, examples, user = self.check_and_downsize(system, examples, user, model)

        return self.session.completion(system, examples, user, model)

    def check_and_downsize(self, system, examples, user, model):
        if self.session.precheck_completion(system, examples, user, model):
            return system, examples, user

        console.verbose("({self.agent_name}) Completion precheck failed, downsizing prompt...")

        return self.downsize_prompt(system, examples, user, model)

    def downsize_prompt(self, system, examples, user, model):
        token_counts = self.session.token_counts(system, examples, user, model)
        model_spec = get_model_spec(model)

        console.error(f"({self.agent_name}) Fail: Prompt token count ({token_counts['total_prompt']}) exceeds max tokens ({model_spec['max_tokens']}) of model ({model_spec['name']}). Failure incoming...")
        console.verbose(token_counts)

        return system, examples, user
    
    def prediction_status_msg(self):
        return f"[bold green]Executing Agent: {self.agent_name} (tks: {self.session.current_token_usage()}, usd: ${self.session.current_cost_usage()})[/]"
