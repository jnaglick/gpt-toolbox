from enum import Enum

# model info: https://platform.openai.com/docs/models
# pricing: https://openai.com/pricing
# token counting: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

class ModelType(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"

    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_3_5_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"

    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"
    GPT_4_32K_0613 = "gpt-4-32k-0613"

    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

def create_completion_model_spec(name, openai_id, usd_per_prompt_token, usd_per_completion_token, max_tokens, tokens_per_message, tokens_per_name, deprecation_date):
    return {
        "name": name,
        "id": openai_id,
        "usd_per_prompt_token": usd_per_prompt_token,
        "usd_per_completion_token": usd_per_completion_token,
        "max_tokens": max_tokens,
        "tokens_per_message": tokens_per_message,
        "tokens_per_name": tokens_per_name,
        "deprecation_date": deprecation_date,
    }

gpt_3_5_turbo_0301_model_spec = create_completion_model_spec(
    name="GPT-3.5 Turbo (0301)",
    openai_id="gpt-3.5-turbo-0301",
    usd_per_prompt_token=0.0015 / 1000,
    usd_per_completion_token=0.002 / 1000,
    max_tokens=4096,
    tokens_per_message=4,
    tokens_per_name=-1,
    deprecation_date=None, # TBD
)

gpt_3_5_turbo_0613_model_spec = create_completion_model_spec(
    name="GPT-3.5 Turbo (0613)",
    openai_id="gpt-3.5-turbo-0613",
    usd_per_prompt_token=0.0015 / 1000,
    usd_per_completion_token=0.002 / 1000,
    max_tokens=4096,
    tokens_per_message=3,
    tokens_per_name=1,
    deprecation_date=None, # TBD
)

gpt_3_5_turbo_16k_0613_model_spec = create_completion_model_spec(
    name="GPT-3.5 Turbo 16k (0613)",
    openai_id="gpt-3.5-turbo-16k-0613",
    usd_per_prompt_token=0.003 / 1000, # TODO check this
    usd_per_completion_token=0.004 / 1000, # TODO check this
    max_tokens=16384,
    tokens_per_message=3,
    tokens_per_name=1,
    deprecation_date=None, # TBD
)

gpt_4_0314_model_spec = create_completion_model_spec(
    name="GPT-4 (0314)",
    openai_id="gpt-4-0314",
    usd_per_prompt_token=0.03 / 1000,
    usd_per_completion_token=0.06 / 1000,
    max_tokens=8192,
    tokens_per_message=3,
    tokens_per_name=1,
    deprecation_date=None, # TBD
)

gpt_4_0613_model_spec = create_completion_model_spec(
    name="GPT-4 (0613)",
    openai_id="gpt-4-0613",
    usd_per_prompt_token=0.03 / 1000, # TODO check this
    usd_per_completion_token=0.06 / 1000, # TODO check this
    max_tokens=8192,
    tokens_per_message=3,
    tokens_per_name=1,
    deprecation_date=None, # TBD
)

gpt_4_32k_0314_model_spec = create_completion_model_spec(
    name="GPT-4 32k (0314)",
    openai_id="gpt-4-32k-0314",
    usd_per_prompt_token=0.06 / 1000,
    usd_per_completion_token=0.12 / 1000,
    max_tokens=32768,
    tokens_per_message=3,  # not sure
    tokens_per_name=1,  # not sure
    deprecation_date=None, # TBD
)

gpt_4_32k_0613_model_spec = create_completion_model_spec(
    name="GPT-4 32k (0613)",
    openai_id="gpt-4-32k-0613",
    usd_per_prompt_token=0.06 / 1000,
    usd_per_completion_token=0.12 / 1000,
    max_tokens=32768,
    tokens_per_message=3,  # not sure
    tokens_per_name=1,  # not sure
    deprecation_date=None, # TBD
)

text_embedding_ada_002_model_spec = { # <- NOTE THIS ISNT A COMPLETION MODEL (will clean this file up later)
    "name": "Text Embedding Ada (002)",
    "id": "text-embedding-ada-002",
    "usd_per_input_token": 0.0004 / 1000,
    "max_tokens": 8191,
}

# Using the fixed model versions for general reproducibility, and because the continuously updated models dont have guaranteed token counts
model_specs = {
    ModelType.GPT_3_5_TURBO:      gpt_3_5_turbo_0613_model_spec,
    ModelType.GPT_3_5_TURBO_0301: gpt_3_5_turbo_0301_model_spec,
    ModelType.GPT_3_5_TURBO_0613: gpt_3_5_turbo_0613_model_spec,

    ModelType.GPT_3_5_TURBO_16K:      gpt_3_5_turbo_16k_0613_model_spec,
    ModelType.GPT_3_5_TURBO_16K_0613: gpt_3_5_turbo_16k_0613_model_spec,

    ModelType.GPT_4:      gpt_4_0613_model_spec,
    ModelType.GPT_4_0314: gpt_4_0314_model_spec,
    ModelType.GPT_4_0613: gpt_4_0613_model_spec,

    ModelType.GPT_4_32K:      gpt_4_32k_0613_model_spec,
    ModelType.GPT_4_32K_0314: gpt_4_32k_0314_model_spec,
    ModelType.GPT_4_32K_0613: gpt_4_32k_0613_model_spec,

    ModelType.TEXT_EMBEDDING_ADA_002: text_embedding_ada_002_model_spec,
}

def get_model_spec(model_type: ModelType):
    return model_specs[model_type]
