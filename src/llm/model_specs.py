from enum import Enum

# model info: https://platform.openai.com/docs/models
# pricing: https://openai.com/pricing
# token counting: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

class ModelType(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"

    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"

def create_model_spec(name, openai_id, usd_per_prompt_token, usd_per_completion_token, max_tokens, tokens_per_message, tokens_per_name, deprecation_date):
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

gpt_3_5_turbo_0301_model_spec = create_model_spec(
    name="GPT-3.5 Turbo (0301)",
    openai_id="gpt-3.5-turbo-0301",
    usd_per_prompt_token=0.002,
    usd_per_completion_token=0.002,
    max_tokens=4096,
    tokens_per_message=4,
    tokens_per_name=-1,
    deprecation_date=None, # TBD
)

gpt_4_0314_model_spec = create_model_spec(
    name="GPT-4 (0314)",
    openai_id="gpt-4-0314",
    usd_per_prompt_token=0.03,
    usd_per_completion_token=0.06,
    max_tokens=8192,
    tokens_per_message=3,
    tokens_per_name=1,
    deprecation_date=None, # TBD
)

gpt_4_32k_0314_model_spec = create_model_spec(
    name="GPT-4 32k (0314)",
    openai_id="gpt-4-32k-0314",
    usd_per_prompt_token=0.06,
    usd_per_completion_token=0.12,
    max_tokens=32768,
    tokens_per_message=3,  # not sure
    tokens_per_name=1,  # not sure
    deprecation_date=None, # TBD
)

# Using the fixed model versions for general reproducibility, and because the continuously updated models dont have guaranteed token counts
model_specs = {
    ModelType.GPT_3_5_TURBO:      gpt_3_5_turbo_0301_model_spec,
    ModelType.GPT_3_5_TURBO_0301: gpt_3_5_turbo_0301_model_spec,

    ModelType.GPT_4:      gpt_4_0314_model_spec,
    ModelType.GPT_4_0314: gpt_4_0314_model_spec,

    ModelType.GPT_4_32K:      gpt_4_32k_0314_model_spec,
    ModelType.GPT_4_32K_0314: gpt_4_32k_0314_model_spec,
}

def get_model_spec(model_type: ModelType):
    return model_specs[model_type]
