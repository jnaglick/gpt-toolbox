import openai

from console import console
from utils import env

def setup():
    openai_api_key = env["OPENAI_API_KEY"]
    if not openai_api_key:
        raise ValueError("Put your OpenAI API key in the OPENAI_API_KEY environment variable.")
    openai.api_key = openai_api_key

setup()

def compose_examples(examples):
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

        # TODO count tokens (complete rewrite with direct requests?) and use max_tokens=

        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # based on HuggingGPT
            # best_of
            # n
        )
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
