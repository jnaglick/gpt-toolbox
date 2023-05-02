# count tokens of chat completion api calls
# From https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

import tiktoken

from .model_specs import get_model_spec

def count_tokens(messages, model):
    model_spec = get_model_spec(model)

    tokens_per_message = model_spec["tokens_per_message"]
    tokens_per_name = model_spec["tokens_per_name"]

    encoding = tiktoken.encoding_for_model(model_spec["id"])

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>

    return num_tokens