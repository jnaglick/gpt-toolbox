from dotenv import load_dotenv
import json
import openai
import os

def setup():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
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

def chat_completion(system, examples, user):
    try:
        # TODO temp=0 and other params
        # TODO count tokens (complete rewrite with direct requests?)
        messages = compose(system, examples, user)

        # print(json.dumps(user, indent=4)) # if verbose

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return completion.choices[0].message.content
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except Exception as e:
        print(f"Unknown error: {e}")
        pass
