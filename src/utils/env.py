from dotenv import load_dotenv
import os

AWS_REGION = "AWS_REGION"
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
LOG_LEVEL = "LOG_LEVEL"
OPENAI_API_KEY = "OPENAI_API_KEY"
WANDB_ENABLED = "WANDB_ENABLED"

def load_env():
    load_dotenv()

    return {
        AWS_REGION: os.getenv(AWS_REGION),
        AWS_ACCESS_KEY_ID: os.getenv(AWS_ACCESS_KEY_ID),
        AWS_SECRET_ACCESS_KEY: os.getenv(AWS_SECRET_ACCESS_KEY),
        OPENAI_API_KEY: os.getenv(OPENAI_API_KEY),
        LOG_LEVEL: os.getenv(LOG_LEVEL),
        WANDB_ENABLED: os.getenv(WANDB_ENABLED) == "TRUE"
    }

env = load_env()
