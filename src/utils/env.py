from dotenv import load_dotenv
import os

OPENAI_API_KEY = "OPENAI_API_KEY"
LOG_LEVEL = "LOG_LEVEL"
WANDB_ENABLED = "WANDB_ENABLED"

def load_env():
    load_dotenv()

    return {
        OPENAI_API_KEY: os.getenv(OPENAI_API_KEY),
        LOG_LEVEL: os.getenv(LOG_LEVEL),
        WANDB_ENABLED: os.getenv(WANDB_ENABLED) == "TRUE"
    }

env = load_env()
