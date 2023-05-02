import openai

from console import console
from utils import env

from .count_tokens import count_tokens
from .model_specs import get_model_spec, ModelType

def setup():
    openai_api_key = env["OPENAI_API_KEY"]
    if not openai_api_key:
        raise ValueError("Put your OpenAI API key in the OPENAI_API_KEY environment variable.")
    openai.api_key = openai_api_key

setup()

def compose_system(system):
    return [{
        "role": "system",
        "content": system
    }]

def compose_examples(examples):
    # TODO experiment with 'name' field (https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb)
    out = [] # TODO use list comprehension
    for example in examples:
        out.append({"role": "user", "content": example[0]})
        out.append({"role": "assistant", "content": example[1]})
    return out

def compose_user(user):
    return [{
        "role": "user",
        "content": user
    }]

def compose_messages(system, examples, user):
    return [
        *compose_system(system),
        *compose_examples(examples),
        *compose_user(user),
    ]

def count_chat_completion_prompt_tokens(system, examples, user, model: ModelType):
    return {
        "system": count_tokens(compose_system(system), model, count_priming_tokens=False),
        "examples": count_tokens(compose_examples(examples), model, count_priming_tokens=False),
        "user": count_tokens(compose_user(user), model, count_priming_tokens=False),
        "total": count_tokens(compose_messages(system, examples, user), model),
        "model_max": get_model_spec(model)["max_tokens"]
    }

def check_chat_completion_prompt(system, examples, user, model: ModelType, completion_size=0):
    counts = count_chat_completion_prompt_tokens(system, examples, user, model)

    return counts["total"] <= counts["model_max"] - completion_size, counts

def chat_completion(system, examples, user, model: ModelType):
    try:
        model_spec = get_model_spec(model)

        messages = compose_messages(system, examples, user)

        local_prompt_token_count = count_tokens(messages, model)

        completion = openai.ChatCompletion.create(
            model=model_spec["id"],
            messages=messages,
            temperature=0, # based on HuggingGPT
            # TODO max_tokens = model_spec["max_tokens"] - local_prompt_tokens
        )

        token_log_lines = [
            f"Prompt (Actual): {completion.usage.prompt_tokens}",
            f"Prompt (Expected): {local_prompt_token_count}",
            f"Prompt (Δ): {completion.usage.prompt_tokens - local_prompt_token_count}",
            f"Completion: {completion.usage.completion_tokens}",
            f"Total: {completion.usage.total_tokens}"
        ]

        console.log(f"[purple bold](llm) Token Count:[/]\n{' | '.join(token_log_lines)}")

        return completion.choices[0].message.content
    except openai.error.APIError as e:
        console.error(f"(llm) OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        console.error(f"(llm) Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        console.error(f"(llm) OpenAI API request exceeded rate limit: {e}")
        pass
    except Exception as e:
        console.error(f"(llm) {e.__class__.__name__}: {e}")
        pass
