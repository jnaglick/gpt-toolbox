from utils import console

from .chat_completion import (
    chat_completion,
    chat_completion_token_counts,
)
from .model_specs import get_model_spec, ModelType

def cost_of_call(usage, model):    
    model_spec = get_model_spec(model)
    
    prompt_tokens, completion_tokens = usage.prompt_tokens, usage.completion_tokens
    usd_per_prompt_token, usd_per_completion_token = model_spec["usd_per_prompt_token"], model_spec["usd_per_completion_token"]
    
    return prompt_tokens * usd_per_prompt_token + completion_tokens * usd_per_completion_token

def sum_total_tokens(successful_calls):
    return sum(call["usage"].total_tokens for call in successful_calls)

def sum_total_cost(successful_calls):
    return sum(cost_of_call(call["usage"], call["model"]) for call in successful_calls)

def usage_report(successful_calls, failed_calls_count):
    report = [
        f"[bold]Chat Session Report[/]",
        f"Completions: {len(successful_calls)} ({failed_calls_count} failed)",
        f"Total Tokens: {sum_total_tokens(successful_calls)} [bold yellow](${sum_total_cost(successful_calls)})[/]",
    ]

    return '\n'.join(report)

class ChatSession:
    def __init__(self):
        self.failed_calls_count = 0
        self.successful_calls = []

    def token_counts(self, system, examples, user, model: ModelType):
        return chat_completion_token_counts(system, examples, user, model)

    def precheck_completion(self, system, examples, user, model: ModelType, completion_size=0):
        counts = self.token_counts(system, examples, user, model)
        return counts["total_prompt"] <= counts["model_max"] - completion_size

    def completion(self, system, examples, user, model: ModelType):
        completion = chat_completion(system, examples, user, model)

        if not completion:
            self.handle_failed_completion()
            return completion

        self.handle_successful_completion(completion, model)

        return completion.choices[0].message.content

    def handle_failed_completion(self):
        self.failed_calls_count += 1

    def handle_successful_completion(self, completion, model):
        self.successful_calls.append(dict(model=model, usage=completion.usage))

    def current_token_usage(self):
        return sum_total_tokens(self.successful_calls)

    def current_cost_usage(self):
        return sum_total_cost(self.successful_calls)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        console.log(usage_report(self.successful_calls, self.failed_calls_count))

        return False
