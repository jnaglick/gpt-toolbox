import openai

from console import console
from utils import env

from .count_tokens import count_tokens

def setup():
    openai_api_key = env["OPENAI_API_KEY"]
    if not openai_api_key:
        raise ValueError("Put your OpenAI API key in the OPENAI_API_KEY environment variable.")
    openai.api_key = openai_api_key

setup()

def compose_examples(examples):
    # TODO experiment with 'name' field (https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb)
    out = []
    for example in examples:
        out.append({"role": "user", "content": example[0]})
        out.append({"role": "assistant", "content": example[1]})
    return out

def compose(system, examples, user):
    return [
        {"role": "system", "content": system},
        *compose_examples(examples),
        {"role": "user", "content": user},
    ]

def chat_completion(system, examples, user, model="gpt-3.5-turbo"):
    try:
        messages = compose(system, examples, user)

        expected_num_tokens = count_tokens(messages, model)

        # TODO heuristic downsize prompt if too large

        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # based on HuggingGPT
            # TODO max_tokens = max_for_model(model) - expected_num_tokens
        )

        token_log_lines = [
            f"Prompt (Actual): {completion.usage.prompt_tokens}",
            f"Prompt (Expected): {expected_num_tokens}",
            f"Prompt (Δ): {completion.usage.prompt_tokens - expected_num_tokens}",
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
